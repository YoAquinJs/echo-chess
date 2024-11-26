#include "esp32-hal-gpio.h"

#include "stepper.hpp"

void SetupMotorPins() {
    pinMode(STEPPER_DIR_X, OUTPUT);
    pinMode(STEPPER_STEP_X, INPUT_PULLUP);
    pinMode(LIMIT_SWITCH_X, INPUT);

    pinMode(STEPPER_DIR_Y, OUTPUT);
    pinMode(STEPPER_STEP_Y, INPUT);
    pinMode(LIMIT_SWITCH_Y, INPUT_PULLUP);
}
