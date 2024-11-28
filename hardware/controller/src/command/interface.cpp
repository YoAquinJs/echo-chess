#include "interface.hpp"

CommandPriority IdPriorityMap[] = {
    [CommandId::AVAILABLE_ID] = CommandPriority::AVAILABLE_PRIORITY,
    [CommandId::MOVEMENT_ID] = CommandPriority::MOVEMENT_PRIORITY,
    [CommandId::CLEAR_MOVS_ID] = CommandPriority::CLEAR_MOVS_PRIORITY,
    [CommandId::PRINT_ID] = CommandPriority::PRINT_PRIORITY,
};

CommandPriority CommandPriorityMap(CommandId id) {
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
