#include "src/command/handler.hpp"
#include "src/serial/serial.hpp"

void setup() {
    Serial.println("hardware program started execution");

    SerialSetup();
    CommandHandlerSetup();

    // Listens to serial communication for client commands and enqueues them
    // pinned to core 0
    xTaskCreatePinnedToCore(SerialTask, "serial", 10000, NULL, 0, NULL, 0);

    // client commands dispatcher
    // pinned to core 1
    xTaskCreatePinnedToCore(CommandHandlerTask, "command handler", 10000, NULL,
                            0, NULL, 1);
}

void loop() {
}
