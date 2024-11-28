// shared interface with the client, for command, response and data
// specification

#ifndef CONTROLLER_COMMAND_INTERFACE_H
#define CONTROLLER_COMMAND_INTERFACE_H

#include <cstdint>

// is assumed that client will never send more than this number of commands.
// this is important as if there are more than MAX_COMMAND_QUEUE sent, the
// listener task may start lossing commands.
#define MAX_COMMAND_QUEUE 50

#define MESSAGE_TERMINATOR '\n'

#define COMMAND_ID_SIZE 1
#define COORD_BIT_SIZE 4

typedef uint8_t EncPos;
typedef int16_t EncMov;

// |left bits|X Coord : COORD_BIT_SIZE|Y Coord : COORD_BIT_SIZE|
// ||X Coord : 4|Y Coord : 4|
constexpr EncPos COORD_Y_BIT_MASK = (1 << COORD_BIT_SIZE) - 1;
constexpr EncPos COORD_X_BIT_MASK =
    ((1 << (COORD_BIT_SIZE * 2)) - 1) ^ COORD_Y_BIT_MASK;

// specification for commands received from client
// Available
// returns AVL when command is enabled, UNVAL otherwise
// Movement
// clears movement queue
// Clear Movements
// enqueues movement
// Print
// prints content to display

enum CommandId {
    AVAILABLE_ID = 0x00,
    MOVEMENT_ID = 0x01,
    CLEAR_MOVS_ID = 0x02,
    PRINT_ID = 0x0F,
};

enum CommandPriority {
    AVAILABLE_PRIORITY = 0,
    MOVEMENT_PRIORITY = 2,
    CLEAR_MOVS_PRIORITY = 1,
    PRINT_PRIORITY = 1,
};

enum CommandTimeout {
    AVAILABLE_TIMEOUT = 100,
    MOVEMENT_TIMEOUT = 4000,
    CLEAR_MOVS_TIMEOUT = 100,
    PRINT_TIMEOUT = 100,
};

CommandPriority CommandPriorityMap(CommandId id);

// Command Response Codes
//
//   No errors
// EXECUTED            0x00
// SKIPPED             0x01
//   Availability
// AVAILABLE           0x0A
// UNAVAILABLE         0x0B
//   Error
// CLIENT_ERROR        0x10
// HARDWARE_ERROR      0x11
enum CommandResponse {
    EXECUTED = 0x00,
    SKIPPED = 0x01,

    AVAILABLE = 0xA0,
    UNAVAILABLE = 0xB0,

    CLIENT_ERROR = 0x10,
    HARDWARE_ERROR = 0x11,
};

// encoded position
struct EncodedPosition {
    const EncPos coordX : COORD_BIT_SIZE;
    const EncPos coordY : COORD_BIT_SIZE;

    EncodedPosition();
    explicit EncodedPosition(EncPos pos);
};

// encoded movement, represents signed distances between positions
struct EncodedMovement {
    // signed distances between the two positions
    const EncMov distX : COORD_BIT_SIZE + 1;
    const EncMov distY : COORD_BIT_SIZE + 1;

    EncodedMovement(EncodedPosition origin, EncodedPosition dest);
};

#endif  // CONTROLLER_COMMAND_INTERFACE_H
