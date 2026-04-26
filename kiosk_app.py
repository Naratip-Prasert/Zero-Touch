import tkinter as tk
import time


class ZeroTouchFoodKiosk:
    def __init__(self, root):
        self.root = root
        self.root.title("Zero Touch Food Kiosk")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#f5f5f5")

        self.cart = []
        self.last_action_time = time.time()

        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.create_home()
        self.check_idle()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_home(self):
        self.clear_screen()
        self.last_action_time = time.time()

        self.root.configure(bg="#b91c1c")

        title = tk.Label(
            self.root,
            text="ZERO TOUCH\nSELF SERVICE KIOSK",
            font=("Arial", 48, "bold"),
            fg="white",
            bg="#b91c1c",
            justify="center"
        )
        title.pack(pady=120)

        start = tk.Button(
            self.root,
            text="PINCH TO START",
            command=self.page_burgers,
            font=("Arial", 30, "bold"),
            width=20,
            height=2,
            bg="white",
            fg="#b91c1c",
            activebackground="#facc15",
            activeforeground="#111827",
            relief="flat"
        )
        start.pack(pady=30)

        hint = tk.Label(
            self.root,
            text="Move cursor • Pinch to select • Swipe to scroll",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#b91c1c"
        )
        hint.pack(pady=20)

    def layout(self, title_text):
        self.clear_screen()
        self.last_action_time = time.time()
        self.root.configure(bg="#f5f5f5")

        header = tk.Frame(self.root, bg="#b91c1c", height=90)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text=title_text,
            font=("Arial", 34, "bold"),
            fg="white",
            bg="#b91c1c"
        )
        title.pack(side="left", padx=35, pady=20)

        cart_btn = tk.Button(
            header,
            text=f"🛒 Cart ({len(self.cart)})",
            command=self.page_cart,
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#b91c1c",
            relief="flat",
            width=14
        )
        cart_btn.pack(side="right", padx=80, pady=20)

        body = tk.Frame(self.root, bg="#f5f5f5")
        body.pack(fill="both", expand=True, padx=60, pady=30)

        sidebar = tk.Frame(body, bg="#111827", width=280)
        sidebar.pack(side="left", fill="y")

        content = tk.Frame(body, bg="#f5f5f5")
        content.pack(side="right", fill="both", expand=True)

        self.sidebar_button(sidebar, "🍔 Burgers", self.page_burgers)
        self.sidebar_button(sidebar, "🥤 Drinks", self.page_drinks)
        self.sidebar_button(sidebar, "🍟 Combo", self.page_sets)
        self.sidebar_button(sidebar, "🛒 Cart", self.page_cart)
        self.sidebar_button(sidebar, "🏠 Home", self.create_home)

        return content

    def sidebar_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 20, "bold"),
            bg="#111827",
            fg="white",
            activebackground="#facc15",
            activeforeground="#111827",
            relief="flat",
            anchor="w",
            padx=20,
            height=3
        )
        btn.pack(fill="x", pady=5)

    def make_scroll_area(self, parent):
        canvas = tk.Canvas(parent, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        scroll_frame = tk.Frame(canvas, bg="#f5f5f5")
        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def update_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        scroll_frame.bind("<Configure>", update_scroll)
        canvas.bind("<Configure>", update_scroll)

        def mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", mouse_wheel)

        return scroll_frame

    def food_card(self, parent, name, price, emoji):
        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#e5e7eb",
            highlightthickness=2
        )
        card.pack(padx=25, pady=18, fill="x")

        icon = tk.Label(
            card,
            text=emoji,
            font=("Arial", 48),
            bg="white"
        )
        icon.pack(side="left", padx=30, pady=25)

        info = tk.Frame(card, bg="white")
        info.pack(side="left", fill="both", expand=True)

        name_label = tk.Label(
            info,
            text=name,
            font=("Arial", 26, "bold"),
            fg="#111827",
            bg="white"
        )
        name_label.pack(anchor="w", pady=(25, 5))

        price_label = tk.Label(
            info,
            text=f"{price} THB",
            font=("Arial", 22, "bold"),
            fg="#b91c1c",
            bg="white"
        )
        price_label.pack(anchor="w")

        add_btn = tk.Button(
            card,
            text="ADD",
            command=lambda: self.add_to_cart(name, price),
            font=("Arial", 22, "bold"),
            bg="#b91c1c",
            fg="white",
            activebackground="#facc15",
            activeforeground="#111827",
            relief="flat",
            width=8,
            height=2
        )
        add_btn.pack(side="right", padx=30)

    def add_to_cart(self, name, price):
        self.cart.append((name, price))
        self.last_action_time = time.time()
        self.show_added(name)

    def page_burgers(self):
        content = self.layout("BURGERS")
        frame = self.make_scroll_area(content)

        self.food_card(frame, "Cheese Burger", 89, "🍔")
        self.food_card(frame, "Chicken Burger", 79, "🍔")
        self.food_card(frame, "Double Beef Burger", 129, "🍔")
        self.food_card(frame, "Fish Burger", 99, "🍔")
        self.food_card(frame, "Spicy Burger", 109, "🍔")

    def page_drinks(self):
        content = self.layout("DRINKS")
        frame = self.make_scroll_area(content)

        self.food_card(frame, "Coke", 35, "🥤")
        self.food_card(frame, "Sprite", 35, "🥤")
        self.food_card(frame, "Orange Juice", 45, "🧃")
        self.food_card(frame, "Water", 20, "💧")

    def page_sets(self):
        content = self.layout("COMBO SETS")
        frame = self.make_scroll_area(content)

        self.food_card(frame, "Burger Set", 139, "🍔")
        self.food_card(frame, "Chicken Set", 149, "🍗")
        self.food_card(frame, "Family Set", 299, "👨‍👩‍👧")
        self.food_card(frame, "Snack Set", 99, "🍟")
        self.food_card(frame, "Party Set", 399, "🎉")

    def page_cart(self):
        self.clear_screen()
        self.root.configure(bg="#f5f5f5")
        self.last_action_time = time.time()

        header = tk.Frame(self.root, bg="#b91c1c", height=90)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="YOUR ORDER",
            font=("Arial", 34, "bold"),
            fg="white",
            bg="#b91c1c"
        )
        title.pack(side="left", padx=35, pady=20)

        back = tk.Button(
            header,
            text="Back",
            command=self.page_burgers,
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#b91c1c",
            relief="flat",
            width=10
        )
        back.pack(side="right", padx=150, pady=20)

        body = tk.Frame(self.root, bg="#f5f5f5")
        body.pack(fill="both", expand=True, padx=60, pady=40)

        if not self.cart:
            empty = tk.Label(
                body,
                text="Your cart is empty",
                font=("Arial", 30, "bold"),
                fg="#6b7280",
                bg="#f5f5f5"
            )
            empty.pack(pady=80)
            return

        total = 0

        for name, price in self.cart:
            row = tk.Frame(body, bg="white", highlightbackground="#e5e7eb", highlightthickness=2)
            row.pack(fill="x", pady=10)

            item = tk.Label(
                row,
                text=name,
                font=("Arial", 24, "bold"),
                fg="#111827",
                bg="white"
            )
            item.pack(side="left", padx=25, pady=20)

            price_label = tk.Label(
                row,
                text=f"{price} THB",
                font=("Arial", 22, "bold"),
                fg="#b91c1c",
                bg="white"
            )
            price_label.pack(side="right", padx=25)

            total += price

        total_label = tk.Label(
            body,
            text=f"TOTAL: {total} THB",
            font=("Arial", 34, "bold"),
            fg="#b91c1c",
            bg="#f5f5f5"
        )
        total_label.pack(pady=25)

        confirm = tk.Button(
            body,
            text="CONFIRM ORDER",
            command=self.confirm_order,
            font=("Arial", 26, "bold"),
            bg="#16a34a",
            fg="white",
            relief="flat",
            width=18,
            height=2
        )
        confirm.pack(pady=10)

        clear = tk.Button(
            body,
            text="CLEAR CART",
            command=self.clear_cart,
            font=("Arial", 22, "bold"),
            bg="#dc2626",
            fg="white",
            relief="flat",
            width=16,
            height=2
        )
        clear.pack(pady=10)

    def show_added(self, name):
        popup = tk.Toplevel(self.root)
        popup.geometry("440x170+450+260")
        popup.configure(bg="#16a34a")
        popup.overrideredirect(True)

        label = tk.Label(
            popup,
            text=f"ADDED\n{name}",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#16a34a"
        )
        label.pack(expand=True)

        popup.after(700, popup.destroy)

    def confirm_order(self):
        self.clear_screen()
        self.root.configure(bg="#b91c1c")

        title = tk.Label(
            self.root,
            text="ORDER CONFIRMED",
            font=("Arial", 46, "bold"),
            fg="white",
            bg="#b91c1c"
        )
        title.pack(pady=120)

        queue = tk.Label(
            self.root,
            text="Queue No: A001",
            font=("Arial", 40, "bold"),
            fg="#facc15",
            bg="#b91c1c"
        )
        queue.pack(pady=20)

        msg = tk.Label(
            self.root,
            text="Thank you for using Zero Touch Kiosk",
            font=("Arial", 24),
            fg="white",
            bg="#b91c1c"
        )
        msg.pack(pady=20)

        self.cart = []

        home = tk.Button(
            self.root,
            text="BACK TO HOME",
            command=self.create_home,
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#b91c1c",
            relief="flat",
            width=18,
            height=2
        )
        home.pack(pady=40)

    def clear_cart(self):
        self.cart = []
        self.page_cart()

    def check_idle(self):
        if time.time() - self.last_action_time > 30:
            self.create_home()
            self.last_action_time = time.time()

        self.root.after(1000, self.check_idle)


root = tk.Tk()
app = ZeroTouchFoodKiosk(root)
root.mainloop()