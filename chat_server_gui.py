import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12349

win = tk.Tk()
win.title("Server - Chat App")
win.geometry("400x500")
win.configure(bg="#111")

chat_log = ScrolledText(win, bg="black", fg="white", font=("Consolas", 12))
chat_log.pack(padx=10, pady=10, fill="both", expand=True)
chat_log.config(state="disabled")

entry = tk.Entry(win, bg="#222", fg="white", font=("Consolas", 12))
entry.pack(padx=10, pady=(0, 10), fill="x")

client_socket = None

def log_message(msg):
    chat_log.config(state="normal")
    chat_log.insert("end", msg + "\n")
    chat_log.yview("end")
    chat_log.config(state="disabled")

def receive():
    global client_socket
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            log_message(f"👤 Client: {message}")
        except:
            break

def send_message(event=None):
    global client_socket
    msg = entry.get()
    if msg and client_socket:
        client_socket.send(msg.encode())
        log_message(f"🧑‍💻 You: {msg}")
        entry.delete(0, tk.END)

entry.bind("<Return>", send_message)

def start_server():
    global client_socket
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(1)
    log_message(f"🟢 Server listening on {SERVER_HOST}:{SERVER_PORT}")
    client_socket, addr = s.accept()
    log_message(f"✅ Client connected: {addr}")
    threading.Thread(target=receive, daemon=True).start()

threading.Thread(target=start_server, daemon=True).start()
win.mainloop()
