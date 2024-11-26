#include "esp32-hal-gpio.h"

#include "electromagnet.hpp"

void SetupElectromagnetPins() {
    pinMode(ELECTROMAGNET_SIG, OUTPUT);
}

void ElectromagnetSet(bool state) {
    digitalWrite(ELECTROMAGNET_SIG, state ? HIGH : LOW);
}
