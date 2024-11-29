#ifndef CONTROLLER_COMMAND_HANDLER_H
#define CONTROLLER_COMMAND_HANDLER_H

#include "esp32-hal.h"

#include "command.hpp"

void CommandHandlerSetup();
void CommandHandlerTask(void* pvParameters);

struct CommandHandler {
    CommandId id;
    CommandPriority priority;
    union {
        AvailableCommand available;
        MovementCommand movement;
        ClearMovementsCommand clear;
        PrintCommand print;
    };

    CommandHandler();
    ~CommandHandler();

    void Decode(String command);
    CommandHandler(const CommandHandler& other) {
        memcpy(this, &other, sizeof(CommandHandler));
    }

    CommandHandler& operator=(const CommandHandler& other) {
        if (this != &other) {
            this->~CommandHandler();  // Destroy the current object
            memcpy(this, &other, sizeof(CommandHandler));
        }
        return *this;
    }
    Command* CommandInterface();
};

// mutually exclusive lock on the COMMAND_QUEUE shared resource
extern portMUX_TYPE COMMAND_QUEUE_LOCK;
// command min priority queue
extern CommandHandler COMMAND_QUEUE[MAX_COMMAND_QUEUE];

// mutex control is managed by this priority queue utilities

// return true when enqueued and false if the operation overflows max capacity
bool EnqueueCommandHandler(CommandHandler handler);

// return true if successfully dequeued, false if not, stores dequeued handler
// in given pointer to Command*
bool DequeueCommandHandler(CommandHandler* handler);

// return the command queue size
size_t CommandQueueSize();

#endif  // CONTROLLER_COMMAND_HANDLER_
