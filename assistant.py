import speech_recognition as sr
import pyttsx3
import pyautogui
import webbrowser
import time
import getpass
import re
import psutil
import screen_brightness_control as sbc
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import os

narrator_muted = False
audio_q = queue.Queue()

def speak(text):
    global narrator_muted
    print(f"Assist: {text}")
    if not narrator_muted:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

# Vosk model setup
model_path = "model"
if not os.path.exists(model_path):
    speak("Vosk model not found. Please download and unzip it as 'model'.")
    exit()

model = Model(model_path)
rec = KaldiRecognizer(model, 16000)

def hotword_listener():
    def callback(indata, frames, time, status):
        audio_q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Waiting for hotword...")
        while True:
            data = audio_q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "text" in result and "hey assist" in result["text"]:
                    speak("Yes?")
                    break

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            return None
        except sr.RequestError:
            if not narrator_muted:
                speak("Speech service is unavailable.")
            return None

def is_domain(text):
    return re.search(r"\.(com|org|net|io|gov|edu|co\.uk|ie|ai|dev|app|tv|info|biz)$", text)

def launch_with_search_bar(appname):
    speak(f"Opening {appname}")
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.typewrite(appname)
    time.sleep(0.5)
    pyautogui.press('enter')

def control_media(action):
    key_map = {
        "pause music": "playpause",
        "play music": "playpause",
        "next track": "nexttrack",
        "previous track": "prevtrack",
        "volume up": "volumeup",
        "volume down": "volumedown"
    }
    if action in key_map:
        pyautogui.press(key_map[action])
        speak(f"{action.capitalize()} command sent.")

def check_battery():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = battery.power_plugged
        status = "charging" if plugged else "not charging"
        speak(f"Battery is at {percent}% and {status}.")
    else:
        speak("Battery information is not available.")

def set_brightness(level):
    try:
        level = int(level)
        if 0 <= level <= 100:
            sbc.set_brightness(level)
            speak(f"Brightness set to {level} percent.")
        else:
            speak("Please choose a brightness between 0 and 100.")
    except:
        speak("Couldn't adjust brightness. Make sure you're on a supported device.")

def execute_command(command):
    global narrator_muted

    if command.startswith("open "):
        target = command.replace("open ", "").strip()
        if is_domain(target):
            url = target if target.startswith("http") else f"https://{target}"
            speak(f"Opening {target}")
            webbrowser.open(url)
        else:
            launch_with_search_bar(target)

    elif command in ["pause music", "play music", "next track", "previous track", "volume up", "volume down"]:
        control_media(command)

    elif command in ["what time is it", "tell me the time"]:
        current_time = time.strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif command in ["what day is it", "what's the date"]:
        today = time.strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")

    elif command in ["what's your name", "what is your name"]:
        speak("My name is Assist. I'm your voice assistant.")

    elif command in ["hello", "hi"]:
        username = getpass.getuser()
        speak(f"Hello {username}, how can I help you today?")

    elif command == "stop":
        speak("Goodbye!")
        exit()

    elif command == "mute narrator":
        narrator_muted = True
        print("Narrator muted.")

    elif command == "unmute narrator":
        narrator_muted = False
        speak("Narrator unmuted.")

    elif command == "how are you":
        speak("I'm ready.")

    elif command == "thank you":
        speak("You're welcome.")

    elif command == "tell me a joke":
        speak("Why did the computer go to therapy? Because it had too many bytes of trauma.")

    elif command == "check battery":
        check_battery()

    elif command.startswith("set brightness to "):
        level = command.replace("set brightness to ", "").strip()
        set_brightness(level)

    else:
        speak("I didn't recognise that command. Try saying 'open', 'check battery', or 'stop'.")

# Initialize recognizer
recognizer = sr.Recognizer()

# Main loop
while True:
    hotword_listener()
    while True:
        user_command = listen()
        if user_command is None or user_command == "nevermind":
            speak("Okay, I'm standing by.")
            break
        execute_command(user_command)
