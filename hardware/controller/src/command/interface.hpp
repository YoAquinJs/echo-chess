#include "WString.h"

#ifndef CONTROLLER_COMMAND_INTERFACE_H
#define CONTROLLER_COMMAND_INTERFACE_H

#define COMMAND_ID_SIZE 1
#define COORD_BIT_SIZE 4

typedef uint8_t EncPos;
typedef int16_t EncMov;

// |left bits|X Coord : COORD_BIT_SIZE|Y Coord : COORD_BIT_SIZE|
// ||X Coord : 4|
constexpr EncPos COORD_Y_BIT_MASK = (1 << COORD_BIT_SIZE) - 1;
constexpr EncPos COORD_X_BIT_MASK =
    ((1 << (COORD_BIT_SIZE * 2)) - 1) ^ COORD_Y_BIT_MASK;

// represents command codes recieved from client
enum CommandCode {
    // returns AVL when command is enabled, UNVAL otherwise
    // command <cmd>
    AVAILABLE = 0x00,
    // clears movement queue
    CLEAR = 0x01,
    // enqueues movement
    // origin <enc_pos> dest <enc_pos>
    MOVEMENT = 0x02,
    // prints content to display
    // content <str>
    PRINT = 0x03,
};

// represents response codes
enum ResponseStatus {
    OK = 0,
    ERROR = 1,
    AVL = 2,
    UNAVL = 3,
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

struct Command {
    virtual void Execute() = 0;
    virtual ResponseStatus Parse(String args) = 0;

    // allocates a new command into decoded_command
    static ResponseStatus DecodeCommand(String raw_input,
                                        Command** decoded_command);
};

class AvailableCommand : public Command {
    CommandCode command;

   public:
    void Execute();
    ResponseStatus Parse(String args);
};

class MovementCommand : public Command {
    EncodedPosition origin;
    EncodedPosition dest;

   public:
    void Execute();
    ResponseStatus Parse(String args);
};

class ClearCommand : public Command {
   public:
    void Execute();
    ResponseStatus Parse(String args);
};

class PrintCommand : public Command {
    String content;

   public:
    void Execute();
    ResponseStatus Parse(String args);
};

#endif  // CONTROLLER_COMMAND_INTERFACE_H
