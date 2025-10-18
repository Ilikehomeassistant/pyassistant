import speech_recognition as sr
import pyttsx3
import pyautogui
import webbrowser
import time
import getpass
import re
import speedtest

narrator_muted = False

def speak(text):
    global narrator_muted
    print(f"Assistant: {text}")
    if not narrator_muted:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

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

def check_internet_speed():
    speak("Running internet speed test...")
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000  # Mbps
    upload = st.upload() / 1_000_000      # Mbps
    ping = st.results.ping
    speak(f"Download speed is {download:.2f} megabits per second.")
    speak(f"Upload speed is {upload:.2f} megabits per second.")
    speak(f"Ping is {ping:.0f} milliseconds.")

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
        speak("My name is Copilot. I'm your voice assistant.")

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
        speak("I'm feeling electric!")

    elif command == "thank you":
        speak("You're welcome!")

    elif command == "tell me a joke":
        speak("Why did the computer go to therapy? Because it had too many bytes of trauma.")

    elif command == "check internet speed":
        check_internet_speed()

    else:
        speak("I didn't recognize that command. Try saying 'open', 'check internet speed', or 'stop'.")

# Initialize recognizer
recognizer = sr.Recognizer()

# Main loop
while True:
    user_command = listen()
    if user_command:
        execute_command(user_command)
