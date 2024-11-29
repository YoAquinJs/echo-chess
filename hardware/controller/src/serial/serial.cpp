#include "HardwareSerial.h"
#include "esp32-hal.h"

#include "serial.hpp"
#include "src/command/handler.hpp"
#include "src/command/interface.hpp"

void SerialSetup() {
    Serial2.begin(115200, SERIAL_8N1, SERIAL_RX, SERIAL_TX);
    while (!Serial2) {
        delay(10);
    }

    Serial.println("hardware-side serial comunication with client ready");
}

String input_buffer;

void SerialTask(void* pvParameters) {
    while (true) {
        if (!Serial2.available()) {
            continue;
        }

        input_buffer = Serial2.readStringUntil(MESSAGE_TERMINATOR);
        if (input_buffer.length() == 0) {
            continue;
        }

        CommandHandler handler;
        handler.Decode(input_buffer);
        if (!EnqueueCommandHandler(handler)) {
            Serial.println(
                "overflow in the command queue, ignoring the overflown "
                "command");
        }
    }
}

void SerialResponse(CommandResponse response) {
    Serial2.write(response);
    Serial2.write(MESSAGE_TERMINATOR);
}
