# Chess Board Client

A client for the Echo-Chess API, providing an interface for a playable
chessboard, whether virtual or hardware-based. It also integrates voice commands
through an STT (Speech-to-Text) model and delivers corresponding responses via
TTS (Text-to-Speech). The client can be  configurable to mock hardware behavior
when needed.


### Configuration

Configured with an env file in `./client/src/.env`, with this format

```env
# true or false
MOCK_HARDWARE=true
```

### Usage

Check the [commands](client/commands.md) available for the board client.

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
