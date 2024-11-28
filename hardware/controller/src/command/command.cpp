#include "command.hpp"
#include "interface.hpp"

CommandResponse AvailableCommand::Execute() {
}
CommandResponse AvailableCommand::Parse(String args) {
    command = static_cast<CommandId>(args[0]);
}

CommandResponse MovementCommand::Execute() {
}
CommandResponse MovementCommand::Parse(String args) {
    origin = EncodedPosition(args[0]);
    dest = EncodedPosition(args[1]);
    return CommandResponse::EXECUTE;
}

CommandResponse ClearMovementsCommand::Execute() {
}
CommandResponse ClearMovementsCommand::Parse(String args) {
    return CommandResponse::EXECUTE;
}

CommandResponse PrintCommand::Execute() {
}
CommandResponse PrintCommand::Parse(String args) {
    content = args;
    return CommandResponse::EXECUTE;
}
