import tkinter as tk

def show_page(title, text):
    title_label.config(text=title)
    content_label.config(text=text)

root = tk.Tk()
root.title("Zero Touch Kiosk")
root.geometry("900x600")
root.configure(bg="#111827")

title_label = tk.Label(
    root,
    text="ZERO TOUCH KIOSK",
    font=("Arial", 36, "bold"),
    fg="white",
    bg="#111827"
)
title_label.pack(pady=30)

content_label = tk.Label(
    root,
    text="Use hand gesture to control this kiosk",
    font=("Arial", 20),
    fg="#d1d5db",
    bg="#111827"
)
content_label.pack(pady=20)

button_frame = tk.Frame(root, bg="#111827")
button_frame.pack(pady=30)

buttons = [
    ("Information", "Welcome", "This kiosk provides touchless information service."),
    ("Map", "Map", "Showing building map and directions."),
    ("Queue", "Queue", "Please select service queue."),
    ("Help", "Help", "Raise your hand and pinch to select a button.")
]

for text, title, detail in buttons:
    btn = tk.Button(
        button_frame,
        text=text,
        font=("Arial", 22, "bold"),
        width=18,
        height=2,
        command=lambda t=title, d=detail: show_page(t, d)
    )
    btn.pack(pady=10)

root.mainloop()