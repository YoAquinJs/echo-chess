# Chess Board

Mecatronic chessboard for playing chess via voice commands.

The board listens to the user, uses an STT model and parse the commands, communicate with
the Voice-Chess API, then sends the corresponding movement coordinates via Serial UART
to the Hardware Controller, which programs an XY CNC to move an electromagnet beneath the
pieces.

# Program Division

This branch is divided into two programs, the Board Client (running in a Raspberry PI),
and the Hardware Controller (running in a microcontroller).

We split the Board Client and Hardware Controller, for decoupling the overall project,
and realtime OS (FreeRTOS) for the XY CNC control.
this allow us to easily mock the hardware on the board, providing a Board Client
to the API with no hardware required to function.
Plus the CNC program is more reliable and manteinable in an RTOS and microcontroller
frameworks like Arduino.

We chose the Raspberry PI for running the Board Client, because we needed to run
STT and TTS models, and easily communicate to the microcontroller.

For the microcontroller we chose the Esp32, as it's cheap, small, easy to quickstart
and provides all the hardware interfaces we require.

We decided that building the mechanic frame from zero would be inviable duo to deadlines,
so we modified a personal laser cutter, swapping the laser with the electromagnet
and removing it's motherboard, so we could focus on the electronic and programming.

If you intend to build the mechanic frame, we included a materials section which
lists the general pieces you need to make it work, be aware you will need more than
what's listed, as we only specified the general pieces.

## Board Client

Client to the Voice-Chess API, listening and parsing user commands, and when present,
sending movement commands via serial to the Hardware Controller.

### Configuration

Configured with an env file in `./client/src/.env`, with this format

```env
# true or false
HARDWARE_ENABLED=true
```

### Usage

Check the [commands](board/client/commands.md) available for the board client.

Portaudio is required by pyaudio which is used for the audio stream,
it can be installed in the Raspberry Pi via (or debian based systems):

```bash
sudo apt install portaudio19-dev
```

The dependency management is handled by [poetry](https://python-poetry.org/)

```bash
cd board/client

poetry install --no-dev --user
poetry run -- python3 src/main.py
```

## Hardware Controller

XY CNC controller for the chess-piece movement, works by displacing an electromagnet,
which on activation, moves the ferromagnetic material attached to the chess pieces.
Receives movement commands from the Board Client via serial, queues the commands received
and handles the electronic components for executing them.

### Materials

In parenthesis we specify what specific component we used

- **Mechanic:*
	- Linear rails and carriages
	- Transmission, timing belt, dented pulleys, more...
	- Mounting of the stepper motors
	- Cable distribution
	- Casing and chessboard
- **Electronics:*
	- DC Power Supply (12V 5A), and voltage regulation module
	- Raspberry PI (Model 4B with 4Gb)
	- Microcontroller compatible with the code (Esp32)
	- Stepper Motors (Nema 17 17HS4401), and their drivers (a4988), at least 2 of each
	- Electromagnet (keyStudio KS0320)
	- Display (OLED display 0.96 inc)

The motors we used work with 12V and consume less than 1A, the electromagnet works with
5V and consumes 0.3A max,

### Usage

TODO
