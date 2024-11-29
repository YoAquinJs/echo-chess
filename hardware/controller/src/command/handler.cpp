#include "HardwareSerial.h"

#include "handler.hpp"
#include "src/serial/serial.hpp"
#include <cstring>

void CommandHandlerSetup() {
}

// Command Handler execution task

void CommandHandlerTask(void* pvParameters) {
    while (true) {
        CommandHandler handler;
        if (!DequeueCommandHandler(&handler)) {
            continue;
        }

        CommandResponse response = handler.CommandInterface()->Execute();
        SerialResponse(response);
    }
}

// CommandHandler implementation

CommandHandler::CommandHandler() {
}

CommandHandler::~CommandHandler() {
}

void CommandHandler::Decode(String command) {
    if (command.length() == 0) {
        Serial.print("invalid command string is being decoded");
        return;
    }

    id = static_cast<CommandId>(command[0]);
    priority = static_cast<CommandPriority>(CommandPriorityMap(id));
    CommandInterface()->Parse(command.substring(1));
}

Command* CommandHandler::CommandInterface() {
    switch (id) {
        case CommandId::AVAILABLE_ID:
            return &available;
        case CommandId::MOVEMENT_ID:
            return &movement;
        case CommandId::CLEAR_MOVS_ID:
            return &clear;
        case CommandId::PRINT_ID:
            return &print;
    }
    return nullptr;
}
