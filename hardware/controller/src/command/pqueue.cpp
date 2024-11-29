#include "handler.hpp"
#include <cstring>

// Priority Queue implementation for command processing

#define PQUEUE_PARENT(node_i) (((node_i) - 1) / 2)
#define PQUEUE_LEFT_CHILD(node_i) (2 * (node_i) + 1)
#define PQUEUE_RIGHT_CHILD(node_i) (2 * (node_i) + 2)
#define COMMAND_HANDLER_SWAP(a, b) \
    do {                           \
        CommandHandler temp = (a); \
        (a) = (b);                 \
        (b) = temp;                \
    } while (0);

portMUX_TYPE COMMAND_QUEUE_LOCK = portMUX_INITIALIZER_UNLOCKED;
CommandHandler COMMAND_QUEUE[MAX_COMMAND_QUEUE];
static size_t command_queue_size;

void PQueueEnqueue(CommandHandler& handler);
CommandHandler PQueueDequeue();

bool EnqueueCommandHandler(CommandHandler handler) {
    if (command_queue_size == MAX_COMMAND_QUEUE) {
        return false;
    }

    portENTER_CRITICAL(&COMMAND_QUEUE_LOCK);
    PQueueEnqueue(handler);
    portEXIT_CRITICAL(&COMMAND_QUEUE_LOCK);
}

bool DequeueCommandHandler(CommandHandler* handler) {
    if (command_queue_size == 0) {
        return false;
    }

    portENTER_CRITICAL(&COMMAND_QUEUE_LOCK);
    *handler = PQueueDequeue();
    portEXIT_CRITICAL(&COMMAND_QUEUE_LOCK);

    return true;
}

size_t CommandQueueSize() {
    return command_queue_size;
}

void PQueueShiftUp(size_t i) {
    while (i > 0 && COMMAND_QUEUE[PQUEUE_PARENT(i)].priority >
                        COMMAND_QUEUE[i].priority) {
        COMMAND_HANDLER_SWAP(COMMAND_QUEUE[PQUEUE_PARENT(i)], COMMAND_QUEUE[i])
        i = PQUEUE_PARENT(i);
    }
}

void PQueueShiftDown(size_t i) {
    size_t min_index = i;

    size_t l = PQUEUE_LEFT_CHILD(i);
    if (l <= command_queue_size &&
        COMMAND_QUEUE[l].priority < COMMAND_QUEUE[min_index].priority) {
        min_index = l;
    }

    size_t r = PQUEUE_RIGHT_CHILD(i);
    if (r <= command_queue_size &&
        COMMAND_QUEUE[r].priority < COMMAND_QUEUE[min_index].priority) {
        min_index = r;
    }

    if (i != min_index) {
        COMMAND_HANDLER_SWAP(COMMAND_QUEUE[min_index], COMMAND_QUEUE[i])
        PQueueShiftDown(min_index);
    }
}

void PQueueEnqueue(CommandHandler& handler) {
    command_queue_size++;

    COMMAND_QUEUE[command_queue_size] = handler;

    PQueueShiftUp(command_queue_size);
}

CommandHandler PQueueDequeue() {
    CommandHandler deq = COMMAND_QUEUE[command_queue_size];

    COMMAND_HANDLER_SWAP(COMMAND_QUEUE[0], COMMAND_QUEUE[command_queue_size])
    command_queue_size--;

    PQueueShiftDown(0);
    return deq;
}
