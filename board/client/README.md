

# **Automatic Chess with Voice Commands**

This project enables users to play chess through voice commands, using a Vosk voice recognition model and serial communication to interact with a physical device (such as an ESP32). Below, you’ll find instructions for setting up, running, and understanding the components of the system.

## **Dependencies**

The required dependencies for running this project are listed in `requirements.txt`. You can install them using:

`pip install -r requirements.txt`

To generate `requirements.txt`, use:

`pip freeze > requirements.txt`

### **Key Dependencies:**

* **vosk**: For speech-to-text recognition.  
* **numpy**: For audio data processing.  
* **pyttsx3**: For text-to-speech synthesis.  
* **pyserial**: For serial communication with the physical device (if used).  
* **pyaudio**: For handling microphone input in real-time.

## **Initial Setup**

1. **Download the Vosk Model**:  
   * Download an appropriate Vosk model for your language from https://alphacephei.com/vosk/models.  
   * Extract the downloaded ZIP file and place the model folder in an accessible directory.  
2. **Update `config.json`**:  
   * Edit the `config.json` file with the path to the extracted Vosk model and other configuration settings. The file should look like this:

json  
`{`  
    `"MODEL_PATH": "path/to/your/model",  // Replace with the actual path to your Vosk model folder`  
    `"SAMPLE_RATE": 16000,`  
    `"SERIAL_PORT": "COM3",               // Adjust to your device's serial port`  
    `"BAUD_RATE": 9600`  
`}`

3. 

## **Project Structure**

Here’s a brief overview of each file in the project:

* **`main.py`**: The entry point for the program. Initializes the voice detector and, optionally, the serial connection, then starts the main game loop in `game_loop`.  
* **`game_controller.py`**: Contains the main `game_loop` function, which manages the core logic. It listens for the "chess" command, then waits for additional commands to execute actions. It also sends and receives commands over a serial connection.  
* **`voice_detector.py`**: Defines the `VoiceDetector` class, which initializes the Vosk model, manages the audio stream, and handles voice command recognition. It also includes `user_cmd_listener` to listen for specific user commands.  
* **`serial_communication.py`**: Provides functions for initializing, sending, and receiving data through a serial connection with a physical device (e.g., ESP32).  
* **`tts.py`**: Contains the `speak_message` function, which uses `pyttsx3` to provide spoken feedback to the user.  
* **`move_translation.py`**: Contains a function to translate and correct recognized commands into a format understood by the chess game (e.g., mapping "two" to "2" or "three" to "3"). This module also helps handle misrecognized words, such as converting "for" to "four."  
* **`config.py`**: Centralizes configuration and logging. It includes:  
  * `load_config`: Loads settings from `config.json`.  
  * `setup_logging`: Configures the logging system with a specified format and log level, allowing consistent logging across all modules.  
* **`config.json`**: A configuration file specifying the Vosk model path, audio sample rate, serial port, and baud rate.

## **How to Run the Project**

1. **Create and Activate a Virtual Environment**:  
   * In the project directory, create a virtual environment (optional but recommended).

`python -m venv .venv`

2.   
   * Activate the virtual environment:

On Windows:

`.venv\Scripts\activate`

* 

On macOS/Linux:

`source .venv/bin/activate`

*   
3. **Install Dependencies**:  
   * Install all required dependencies with:

`pip install -r requirements.txt`

4. **Configure the Vosk Model**:  
   * Make sure you have downloaded and extracted the Vosk model, and update the `MODEL_PATH` in `config.json`.  
5. **Run the Project**:  
   * Start the program by running:

`python main.py`

6. **Interacting with the Program**:  
   * **Say "chess"**: This activates the program, allowing it to listen for the next command.  
   * **Give a chess move command** (e.g., "d5"): The program will process this command and send it to the physical device through serial communication. The device is expected to execute the command by moving the chess piece.  
7. **Exiting the Program**:  
   * The program is designed to close the serial connection automatically upon exit to free up the port.

## **Additional Information**

* **Microphone/Audio Errors**: If you see "Speech-to-text system is unavailable," check that your microphone is connected and configured correctly.  
* **Serial Communication**: Serial communication is essential for this project as it sends commands to a physical device (like an ESP32) to perform the actual chess moves. Ensure `SERIAL_PORT` and `BAUD_RATE` in `config.json` are set correctly based on your device’s configuration. If the device is not connected, commands won’t execute physically, but the program will still run.  
* **`move_translation.py` Customization**: This module helps correct misinterpreted voice commands (e.g., converting "for" to "four") to ensure accuracy. You may need to customize it further to handle specific voice recognition errors based on your language or dialect.

## **Recent Changes**

* **Created `config.py` Module**: Centralized configuration and logging setup in `config.py` to avoid redundant setup code across modules.  
* **Added `move_translation.py`**: A module to correct recognized commands, ensuring that phrases like "two" are interpreted as "2" in chess moves.  
* **Separated Logic in `main.py` and `game_controller.py`**: Moved the main loop logic to `game_controller.py`, making `main.py` a simpler entry point.  
* **Serial Communication Module**: Created `serial_communication.py` to handle serial communication with a physical device, allowing for cleaner and more modular code.  
* **Complete Modularization**: Organized the code into multiple modules (`tts.py`, `voice_detector.py`, etc.) for better readability and maintainability.

