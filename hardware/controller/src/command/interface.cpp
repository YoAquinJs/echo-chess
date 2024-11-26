#include "interface.hpp"

EncodedPosition::EncodedPosition(EncPos pos)
    : coordX(pos >> COORD_BIT_SIZE), coordY(pos & COORD_Y_BIT_MASK) {
}

EncodedPosition::EncodedPosition() : coordX(0), coordY(0) {
}

EncodedMovement::EncodedMovement(EncodedPosition origin, EncodedPosition dest)
    : distX(dest.coordX - origin.coordX), distY(dest.coordY - origin.coordY) {
}
