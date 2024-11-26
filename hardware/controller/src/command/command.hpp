#ifndef CONTROLLER_COMMAND_H
#define CONTROLLER_COMMAND_H 

#include "interface.hpp"

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

#endif // CONTROLLER_COMMAND_H
