# Chess Board Hardware

Robotic chessboard for playing chess via commands received from the client. The
board works by displacing an electromagnet in a cartesian frame, which moves
the ferromagnetic material attached to the bottom of the pieces. The movements
are received via UART serial communication from the board client, then queued
and handled for activating the electronics.

We chose the raspberry pi for running the board client, because we needed to
run stt and tts models, and easily communicate via serial to the
microcontroller.

for the microcontroller we chose the esp32, as it's cheap, small, easy to
quickstart and provides all the hardware interfaces we require.

We decided that building the mechanic frame from zero would be inviable due to
deadlines, so we modified a personal laser cutter, swapping the laser with the
electromagnet and removing it's motherboard, so we could focus on the
electronics and programming.

If you intend to build the mechanic system, we include a materials section
which lists the general pieces you need to make it work, be aware you will need
more than what's listed, as we only specified the general pieces.


### Materials

In parenthesis we specify what specific component we used

- **Mechanic:*
    - Linear rails and carriages
    - Transmission, timing belt, dented pulleys, more...
    - Mounting of the stepper motors
    - Cable distribution
    - Casing and chessboard
- **Electronics:*
    - DC Power Supply (12V 5A), and voltage regulation module (12V to 5V)
    - Raspberry PI (Model 4B with 4Gb)
    - Microcontroller compatible with the arduino framework (ESP32)
    - Stepper Motors (Nema 17 17HS4401), and their corresponding drivers
    (a4988), at least 2 of each
    - Electromagnet (keyStudio KS0320)
    - Display (OLED display 0.96 inc)

The motors we used work with 12V and consume less than 1A, the electromagnet
works with 5V and consumes 300mA at max,

### Usage

The program can be loaded to the microcontroller via the arduino-cli. If you
are not using the ESP32, modify the pinout in the code to match your board's
pinout, additionally if `./board/new-sketch.sh` does not correctly recognizes
your board, try the [official arduino-cli tutorial](https://arduino.github.io/arduino-cli/1.0/getting-started/).

```bash
cd board

# replace esp32 with your corresponding board name
./new-sketch.sh controller esp32
```

once the sketch configuration is in place, you can compile, upload to your
board and listen to serial output with:

```bash
cd controller

arduino-cli compile
arduino upload
arduino monitor
```
