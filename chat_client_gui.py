import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12349

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))

win = tk.Tk()
win.title("Client - Chat App")
win.geometry("400x500")
win.configure(bg="#111")

chat_log = ScrolledText(win, bg="black", fg="white", font=("Consolas", 12))
chat_log.pack(padx=10, pady=10, fill="both", expand=True)
chat_log.config(state="disabled")

entry = tk.Entry(win, bg="#222", fg="white", font=("Consolas", 12))
entry.pack(padx=10, pady=(0, 10), fill="x")

def log_message(msg):
    chat_log.config(state="normal")
    chat_log.insert("end", msg + "\n")
    chat_log.yview("end")
    chat_log.config(state="disabled")

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            log_message(f"👤 Server: {message}")
        except:
            break

def send_message(event=None):
    message = entry.get()
    if message:
        log_message(f"🧑‍💻 You: {message}")
        client.send(message.encode("utf-8"))
        entry.delete(0, tk.END)

entry.bind("<Return>", send_message)
threading.Thread(target=receive, daemon=True).start()
log_message("✅ Connected to Server.")
win.mainloop()
