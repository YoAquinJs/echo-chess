#include "interface.hpp"

CommandPriority CommandPriorityMap(CommandId id) {
    CommandPriority IdPriorityMap[CommandId::PRINT_ID];

    IdPriorityMap[CommandId::AVAILABLE_ID] =
        CommandPriority::AVAILABLE_PRIORITY;
    IdPriorityMap[CommandId::MOVEMENT_ID] = CommandPriority::MOVEMENT_PRIORITY;
    IdPriorityMap[CommandId::CLEAR_MOVS_ID] =
        CommandPriority::CLEAR_MOVS_PRIORITY;
    IdPriorityMap[CommandId::PRINT_ID] = CommandPriority::PRINT_PRIORITY;

    return IdPriorityMap[id];
}

EncodedPosition::EncodedPosition(EncPos pos)
    : coordX(pos >> COORD_BIT_SIZE), coordY(pos & COORD_Y_BIT_MASK) {
}

EncodedPosition::EncodedPosition() : coordX(0), coordY(0) {
}

EncodedMovement::EncodedMovement(EncodedPosition origin, EncodedPosition dest)
    : distX(dest.coordX - origin.coordX), distY(dest.coordY - origin.coordY) {
}
