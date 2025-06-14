import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import requests
import pyautogui
import threading
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import pywhatkit
from googletrans import Translator

# -------------------- TEXT-TO-SPEECH --------------------
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()

# -------------------- VOICE LISTEN --------------------
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except:
            return ""

# -------------------- AI INFERENCE --------------------
def ask_huggingface(question):
    API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-3B"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Replace with your actual key
    payload = {"inputs": question}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json().get("generated_text", "I'm not sure about that.")
    except:
        return "Sorry, the AI service is unavailable."

# -------------------- WEATHER --------------------
def get_weather(city="Hyderabad"):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url).json()
        if response["cod"] != 200:
            return "Weather not found."
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"It is currently {temp}°C with {desc} in {city}."
    except:
        return "Weather service is unavailable."

# -------------------- COMMAND EXECUTION --------------------
def execute_command(command):
    if "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "play" in command and "on youtube" in command:
        song = command.replace("play", "").replace("on youtube", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
    elif "weather" in command:
        speak("Fetching the weather")
        weather_report = get_weather()
        speak(weather_report)
    elif "shutdown" in command:
        speak("System will shut down in 5 seconds")
        os.system("shutdown /s /t 5")
    elif "increase volume" in command:
        pyautogui.press("volumeup")
        speak("Volume increased")
    elif "decrease volume" in command:
        pyautogui.press("volumedown")
        speak("Volume decreased")
    elif "open task manager" in command:
        os.system("taskmgr")
        speak("Task Manager opened")
    elif "open file explorer" in command:
        os.system("explorer")
        speak("File Explorer opened")
    elif "lock screen" in command:
        speak("Locking your computer")
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif "take screenshot" in command:
        file_name = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(file_name)
        speak("Screenshot saved")
    elif "type hello world" in command:
        pyautogui.write("Hello, World!", interval=0.1)
        speak("Typed Hello World")
    elif "move cursor" in command:
        pyautogui.moveTo(500, 500)
        speak("Cursor moved")
    elif "say in hindi" in command:
        translator = Translator()
        original = command.replace("say in hindi", "").strip()
        translated = translator.translate(original, dest="hi").text
        speak(translated)
    elif "ask ai" in command:
        speak("What would you like to ask?")
        question = listen_command()
        answer = ask_huggingface(question)
        speak(answer)
    else:
        speak("Command not recognized. Learning mode activated.")

# -------------------- SYSTEM MONITOR --------------------
def update_system_status(status_label):
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        battery = psutil.sensors_battery().percent
        status = f"CPU: {cpu}% | RAM: {memory}% | Battery: {battery}%"
        status_label.config(text=status)
        status_label.after(2000, update_system_status, status_label)
        break

# -------------------- MAIN JARVIS LOOP --------------------
def run_jarvis(log_widget):
    speak("Hello, I am Jarvis. Ready to help.")
    while True:
        user_command = listen_command()
        if user_command:
            log_widget.insert(tk.END, f"You said: {user_command}\n")
            log_widget.yview(tk.END)
            if "exit" in user_command or "stop" in user_command:
                speak("Shutting down. Goodbye.")
                break
            else:
                execute_command(user_command)

# -------------------- GUI INTERFACE --------------------
def start_gui():
    root = tk.Tk()
    root.title("JARVIS - Voice Assistant")
    root.geometry("600x450")
    root.configure(bg="#101820")

    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#FEE715", font=('Helvetica', 12))

    title = tk.Label(root, text="JARVIS Voice Assistant", bg="#101820", fg="#FEE715", font=("Helvetica", 20, "bold"))
    title.pack(pady=10)

    status_label = tk.Label(root, text="", fg="#FEE715", bg="#101820", font=("Consolas", 10))
    status_label.pack(pady=2)
    update_system_status(status_label)

    log_frame = tk.Frame(root, bg="#101820")
    log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    log_widget = tk.Text(log_frame, bg="#1A1A1A", fg="#39FF14", font=("Consolas", 12), wrap=tk.WORD)
    log_widget.pack(fill=tk.BOTH, expand=True)

    start_button = ttk.Button(root, text="🎙️ Start Listening", command=lambda: threading.Thread(target=run_jarvis, args=(log_widget,)).start())
    start_button.pack(pady=5)

    exit_button = ttk.Button(root, text="❌ Exit", command=root.destroy)
    exit_button.pack(pady=5)

    root.mainloop()

# -------------------- ENTRY POINT --------------------
if __name__ == "__main__":
    start_gui()
