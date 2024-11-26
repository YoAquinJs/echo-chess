#include "command.hpp"

ResponseStatus Command::DecodeCommand(String raw_input,
                                      Command** decoded_command) {
    *decoded_command = nullptr;
    if (raw_input.length() == 0) {
        return ResponseStatus::ERROR;
    }

    Command* command;
    switch (raw_input[0]) {
        case CommandCode::AVAILABLE:
            command = new AvailableCommand();
            break;
        case CommandCode::MOVEMENT:
            command = new MovementCommand();
            break;
        case CommandCode::CLEAR:
            command = new ClearCommand();
            break;
        case CommandCode::PRINT:
            command = new PrintCommand();
            break;
    };

    return command->Parse(raw_input.substring(COMMAND_ID_SIZE));
}

void AvailableCommand::Execute() {
}
ResponseStatus AvailableCommand::Parse(String args) {
}

void MovementCommand::Execute() {
}
ResponseStatus MovementCommand::Parse(String args) {
}

void ClearCommand::Execute() {
}
ResponseStatus ClearCommand::Parse(String args) {
}

void PrintCommand::Execute() {
}
ResponseStatus PrintCommand::Parse(String args) {
}
