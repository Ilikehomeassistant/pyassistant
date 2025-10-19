# Assist — Python Voice Assistant

A single-file, offline-friendly voice assistant built with Python and Vosk.  
Designed for simplicity, speed, and full control. No cloud dependencies, no background processes.

## Features

- Hotword detection (via continuous listening)
- Read clipboard contents aloud
- Save spoken notes to timestamped text files
- Report system status (CPU, RAM, battery)
- Set offline countdown timers
- Open local files by name
- List available commands
- Exit with "nevermind"

## Requirements

- Python 3.8+
- Vosk model folder named "model" in the same directory

## Dependencies

Install with:

```bash
pip install vosk pyttsx3 sounddevice psutil pyperclip
