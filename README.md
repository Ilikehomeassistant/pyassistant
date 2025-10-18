# Python Voice Assistant

A fully offline, pip-only voice assistant that narrates responses, opens apps and websites, controls media playback, checks battery and brightness, and responds to conversational commands — all without admin privileges or external installers.

## Features

- Voice recognition via microphone
- Narrates every response using `pyttsx3`
- Opens apps and websites by name or domain
- Controls media playback (play/pause, next, volume)
- Announces battery level and charging status
- Adjusts screen brightness to any level
- Responds to basic conversational prompts
- Narrator mute/unmute toggle
- Works with only `pip install` dependencies
- No admin rights or external tools required

## Installation

Install Python 3.8+ and run:

```bash
pip install speechrecognition pyttsx3 pyautogui psutil screen_brightness_control
```

## Usage

Run the assistant:

```bash
python assistant.py
```

Then speak commands like:

- `open calculator`
- `open youtube.com`
- `pause music`
- `volume up`
- `check battery`
- `set brightness to 40`
- `what time is it`
- `tell me a joke`
- `mute narrator` / `unmute narrator`
- `stop` (to exit)

## How It Works

- Uses `speech_recognition` to capture voice input
- Uses `pyttsx3` for offline text-to-speech
- Uses `pyautogui` to simulate key presses and app launches
- Uses `psutil` to check battery status
- Uses `screen_brightness_control` to adjust brightness

## Dependencies

All dependencies are pip-installable:

- `speechrecognition`
- `pyttsx3`
- `pyautogui`
- `psutil`
- `screen_brightness_control`
