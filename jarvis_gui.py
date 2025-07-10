print("Jarvis GUI Starting...")

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import requests
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
import queue

# OFFLINE AI RESPONSE FUNCTION
def offline_chatbot_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"
    elif "how are you" in user_input:
        return "I'm doing great! Thanks for asking."
    elif "your name" in user_input:
        return "I am Jarvis, your personal assistant."
    elif "bye" in user_input:
        return "Goodbye! Have a nice day."
    elif "what can you do" in user_input:
        return "I can tell time, date, jokes, search Wikipedia, open websites, and more."
    else:
        return "I'm not sure how to respond to that. Try asking something else!"

# GUI Setup FIRST
root = tk.Tk()
root.title("Jarvis AI")
root.geometry("600x600")
root.configure(bg="#1e1e1e")

query_var = tk.StringVar()
response_var = tk.StringVar()

# 🗾️ Add Iron Man Image
try:
    img = Image.open("ironman.png")
    img = img.resize((150, 150))
    photo = ImageTk.PhotoImage(img)
    tk.Label(root, image=photo, bg="#1e1e1e").pack(pady=10)
except Exception as e:
    print("Image loading failed:", e)

# 🗘️ Chat Log Area
chat_log = tk.Text(root, bg="#121212", fg="white", font=("Arial", 12), wrap="word", height=20, state="disabled")
chat_log.pack(padx=10, pady=10, fill="both", expand=True)

# TTS Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# 🔊 Speech Queue
speech_queue = queue.Queue()

def speech_loop():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        log_chat("Jarvis", text)
        engine.say(text)
        engine.runAndWait()

Thread(target=speech_loop, daemon=True).start()

def speak(text):
    speech_queue.put(text)

def log_chat(speaker, text):
    chat_log.config(state="normal")
    if speaker == "You":
        chat_log.insert(tk.END, f"👤 {speaker}: {text}\n")
    else:
        chat_log.insert(tk.END, f"🤖 {speaker}: {text}\n")
    chat_log.config(state="disabled")
    chat_log.see(tk.END)

def time():
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak(f"The current time is {current_time}")

def date():
    now = datetime.datetime.now()
    speak(f"The current date is {now.day} {now.strftime('%B')} {now.year}")

def load_name():
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"

def screenshot():
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~/Pictures/screenshot.png")
    img.save(img_path)
    speak(f"Screenshot saved as {img_path}")

def play_music(song_name=None):
    song_dir = os.path.expanduser("~/Music")
    if not os.path.exists(song_dir):
        speak("Your Music folder doesn't exist.")
        return
    songs = os.listdir(song_dir)
    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]
    if songs:
        song = random.choice(songs)
        os.system(f'open "{os.path.join(song_dir, song)}"')
        speak(f"Playing {song}")
    else:
        speak("No song found.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def search_wikipedia(query):
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("Sorry, I couldn't find anything on Wikipedia.")

def duckduckgo_answer(query):
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
    try:
        res = requests.get(url, params=params)
        data = res.json()
        answer = data.get("AbstractText", "")
        if answer:
            speak(answer)
        else:
            speak("No relevant answer found.")
    except:
        speak("Error reaching DuckDuckGo.")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        try:
            audio = r.listen(source, timeout=5)
        except:
            speak("Timeout occurred. Try again.")
            return None
    try:
        query = r.recognize_google(audio, language="en-in")
        log_chat("You", query)
        return query.lower()
    except:
        speak("I did not understand that.")
        return None

def handle_query():
    query = takecommand()
    if not query:
        return
    if "time" in query:
        time()
    elif "date" in query:
        date()
    elif "wikipedia" in query:
        search_wikipedia(query.replace("wikipedia", "").strip())
    elif "play music" in query:
        play_music(query.replace("play music", "").strip())
    elif "youtube" in query:
        wb.open("https://youtube.com")
        speak("Opening YouTube")
    elif "google" in query:
        wb.open("https://google.com")
        speak("Opening Google")
    elif "screenshot" in query:
        screenshot()
    elif "joke" in query:
        tell_joke()
    elif "who is" in query or "what is" in query or "define" in query:
        duckduckgo_answer(query)
    elif "exit" in query or "offline" in query:
        speak("Going offline. Have a good day!")
        speech_queue.put(None)
        root.quit()
    else:
        ai_reply = offline_chatbot_response(query)
        speak(ai_reply)

def start_assistant():
    Thread(target=handle_query).start()

def style_button(btn, normal_bg, hover_bg):
    btn.configure(
        font=("Arial", 14, "bold"),
        width=12,
        relief="flat",
        bd=0,
        bg=normal_bg,
        fg="white",
        activebackground=hover_bg,
        cursor="hand2"
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg))

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

speak_btn = tk.Button(btn_frame, text="🎤", command=start_assistant)
style_button(speak_btn, "#28a745", "#218838")
speak_btn.grid(row=0, column=0, padx=15)

exit_btn = tk.Button(btn_frame, text="❌", command=lambda: [speech_queue.put(None), root.quit()])
style_button(exit_btn, "#dc3545", "#c82333")
exit_btn.grid(row=0, column=1, padx=15)

def init_jarvis():
    speak("Initializing Jarvis")
    name = load_name()
    speak(f"{name} at your service. Press Speak and start talking.")

init_jarvis()
root.mainloop()
