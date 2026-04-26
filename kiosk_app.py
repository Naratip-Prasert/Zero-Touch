import tkinter as tk
from tkinter import messagebox
import time

class ZeroTouchKiosk:
    def __init__(self, root):
        self.root = root
        self.root.title("Zero Touch Kiosk")
        self.root.geometry("1000x650")
        self.root.configure(bg="#111827")

        self.last_action_time = time.time()

        self.create_home()
        self.check_idle()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_home(self):
        self.clear_screen()

        title = tk.Label(
            self.root,
            text="ZERO TOUCH KIOSK",
            font=("Arial", 38, "bold"),
            fg="white",
            bg="#111827"
        )
        title.pack(pady=35)

        subtitle = tk.Label(
            self.root,
            text="Show palm to activate • Pinch to select • Swipe to navigate",
            font=("Arial", 16),
            fg="#d1d5db",
            bg="#111827"
        )
        subtitle.pack(pady=10)

        frame = tk.Frame(self.root, bg="#111827")
        frame.pack(pady=35)

        self.big_button(frame, "Information", lambda: self.show_page(
            "Information",
            "Welcome to the Zero-Touch Kiosk.\n\nThis system lets users control the screen without touching it."
        ))

        self.big_button(frame, "Map", lambda: self.show_page(
            "Map",
            "Building Map\n\n1st Floor: Lobby and Information\n2nd Floor: Service Center\n3rd Floor: Meeting Rooms"
        ))

        self.big_button(frame, "Queue", lambda: self.show_page(
            "Queue",
            "Queue Service\n\nPlease select your service type.\nA001 - General Service\nB001 - Payment\nC001 - Help Desk"
        ))

        self.big_button(frame, "Help", lambda: self.show_page(
            "Help",
            "How to use:\n\n1. Open palm for 3 seconds to activate\n2. Move index finger to control cursor\n3. Pinch to click\n4. Make a fist for 3 seconds to deactivate"
        ))

    def big_button(self, parent, text, command):
        def wrapped_command():
            self.last_action_time = time.time()
            command()

        btn = tk.Button(
            parent,
            text=text,
            command=wrapped_command,
            font=("Arial", 28, "bold"),
            width=22,
            height=3,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )

        def on_enter(e):
            e.widget.config(bg="#1d4ed8")

        def on_leave(e):
            e.widget.config(bg="#2563eb")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        btn.pack(pady=12)

    def show_page(self, title_text, body_text):
        self.clear_screen()

        title = tk.Label(
            self.root,
            text=title_text,
            font=("Arial", 36, "bold"),
            fg="white",
            bg="#111827"
        )
        title.pack(pady=35)

        body = tk.Label(
            self.root,
            text=body_text,
            font=("Arial", 22),
            fg="#e5e7eb",
            bg="#111827",
            justify="center"
        )
        body.pack(pady=40)

        back_btn = tk.Button(
            self.root,
            text="Back to Home",
            command=self.create_home,
            font=("Arial", 22, "bold"),
            width=18,
            height=2,
            bg="#10b981",
            fg="white",
            relief="flat"
        )
        back_btn.pack(pady=30)

    def check_idle(self):
        if time.time() - self.last_action_time > 20:
            self.create_home()
            self.last_action_time = time.time()

        self.root.after(1000, self.check_idle)    
            


root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())
app = ZeroTouchKiosk(root)
root.mainloop()