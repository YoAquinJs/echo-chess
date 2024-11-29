#ifndef CONTROLLER_SERIAL_H
#define CONTROLLER_SERIAL_H

#include "src/command/interface.hpp"

#define BAUDRATE 9600
#define SERIAL_RX 16
#define SERIAL_TX 17

void SerialSetup();
void SerialTask(void* pvParameters);

void SerialResponse(CommandResponse response);

#endif  // CONTROLLER_SERIAL_H
