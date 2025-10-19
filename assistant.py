import pyttsx3
import sounddevice as sd
import queue
import vosk
import json
import pyperclip
import os
import time
import psutil
from datetime import datetime

# Initialize speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize Vosk model
model = vosk.Model("model")
q = queue.Queue()
def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "").lower()

def read_clipboard():
    text = pyperclip.paste()
    if text:
        speak(f"Clipboard says: {text}")
    else:
        speak("Clipboard is empty.")

def take_note():
    speak("What should I write?")
    note = listen()
    if note:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"note_{timestamp}.txt", "w") as f:
            f.write(note)
        speak("Note saved.")

def system_status():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    battery_level = battery.percent if battery else "unknown"
    speak(f"CPU: {cpu} percent. RAM: {ram} percent. Battery: {battery_level} percent.")

def set_timer(command):
    words = command.split()
    try:
        index = words.index("for")
        minutes = int(words[index + 1])
        speak(f"Timer set for {minutes} minutes.")
        time.sleep(minutes * 60)
        speak("Time's up.")
    except:
        speak("Couldn't set timer.")

def open_file(command):
    try:
        filename = command.replace("open file", "").strip()
        if os.path.exists(filename):
            os.startfile(filename) if os.name == "nt" else os.system(f"xdg-open '{filename}'")
            speak(f"Opened {filename}")
        else:
            speak("File not found.")
    except:
        speak("Error opening file.")

def list_commands():
    speak("Available commands are: read clipboard, take a note, system status, set timer for X minutes, open file, what can you do, and nevermind.")

def main():
    speak("Assistant ready.")
    while True:
        command = listen()
        if not command:
            continue
        if "nevermind" in command:
            speak("Exiting.")
            break
        elif "read clipboard" in command:
            read_clipboard()
        elif "take a note" in command:
            take_note()
        elif "system status" in command:
            system_status()
        elif "set timer for" in command:
            set_timer(command)
        elif "open file" in command:
            open_file(command)
        elif "what can you do" in command:
            list_commands()
        else:
            speak("Command not recognized.")

if __name__ == "__main__":
    main()
