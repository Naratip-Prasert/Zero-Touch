import tkinter as tk
import time
import platform
import csv
import os
import uuid
from datetime import datetime

# --- Modern Color Palette ---
BG_COLOR = "#f3f4f6"        # พื้นหลังสีเทาอ่อน สบายตา
PRIMARY_RED = "#E31837"     # สีแดงสดแบบร้าน Fast Food
PRIMARY_HOVER = "#C8102E"   # สีแดงเข้มเมื่อชี้
ACCENT_YELLOW = "#FFC72C"   # สีเหลืองทอง
TEXT_DARK = "#111827"       # สีดำเทาสำหรับตัวหนังสือ
CARD_BG = "#ffffff"         # สีพื้นหลังการ์ดอาหาร
ADD_BTN = "#059669"         # สีเขียวมรกต สำหรับปุ่ม ADD ให้เด่นชัด
ADD_BTN_HOVER = "#047857"   # สีเขียวเข้มเมื่อชี้

class ZeroTouchFoodKiosk:
    def __init__(self, root):
        self.root = root
        self.root.title("Zero Touch Premium Kiosk")
        self.root.attributes("-fullscreen", True)
        # ซ่อน cursor ปกติ
        self.root.config(cursor="none")
        
        self.root.attributes("-fullscreen", True)
        # --- Kiosk cursor ---
        self.kiosk_cursor = self.get_supported_cursor(
            ["target", "tcross", "crosshair"]
        )

        self.root.config(cursor=self.kiosk_cursor)
        
        self.cart = []
        self.last_action_time = time.time()

        # --- Experiment / CSV state ---
        self.csv_file = "kiosk_experiment_log.csv"
        self.session_id = None
        self.participant_name = ""
        self.control_mode = tk.StringVar(value="Zero Touch")
        self.order_start_time = None
        self.order_start_world_time = ""
        self.order_started = False
        self.add_click_count = 0

        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.create_setup_page()
        self.check_idle()

    def get_supported_cursor(self, candidates):
        """เลือก cursor ที่เครื่องรองรับจริง เพื่อกัน TclError บน Windows"""
        for cursor_name in candidates:
            try:
                self.root.config(cursor=cursor_name)
                return cursor_name
            except tk.TclError:
                continue
        return "arrow"

    # --- Utility Functions ---
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.config(cursor=self.kiosk_cursor)

    def update_activity(self):
        self.last_action_time = time.time()

    def add_hover(self, widget, normal_bg, hover_bg, normal_fg="white", hover_fg="white"):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg, fg=hover_fg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg, fg=normal_fg))

    def now_text(self):
        # เวลาจริงของโลก ตอนเก็บข้อมูล
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_elapsed(self):
        if self.order_start_time is None:
            return ""
        return round(time.time() - self.order_start_time, 3)

    def cart_total(self):
        return sum(price for _, price in self.cart)

    def ensure_csv_header(self):
        file_exists = os.path.exists(self.csv_file)
        if not file_exists:
            with open(self.csv_file, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "session_id",
                    "participant_name",
                    "control_mode",
                    "start_world_time",
                    "finish_world_time",
                    "elapsed_seconds",
                    "add_click_count",
                    "final_cart_count",
                    "cart_total",
                ])

    def save_summary_row(self):
        # บันทึกแค่ 1 บรรทัดต่อผู้ทดลอง ตอนกด CONFIRM & PAY
        self.ensure_csv_header()
        with open(self.csv_file, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                self.session_id,
                self.participant_name,
                self.control_mode.get(),
                self.order_start_world_time,
                self.now_text(),
                self.get_elapsed(),
                self.add_click_count,
                len(self.cart),
                self.cart_total(),
            ])

    def create_setup_page(self):
        self.clear_screen()
        self.root.configure(bg=BG_COLOR)
        self.cart = []
        self.order_start_time = None
        self.order_start_world_time = ""
        self.order_started = False
        self.add_click_count = 0
        self.session_id = str(uuid.uuid4())[:8]

        box = tk.Frame(self.root, bg="white", highlightbackground="#e5e7eb", highlightthickness=2)
        box.place(relx=0.5, rely=0.5, anchor="center", width=820, height=620)

        tk.Label(box, text="🧪 KIOSK TEST SETUP", font=("Arial", 44, "bold"),
                 fg=PRIMARY_RED, bg="white").pack(pady=(45, 20))

        tk.Label(box, text="Select control mode", font=("Arial", 24, "bold"),
                 fg=TEXT_DARK, bg="white").pack(pady=(10, 10))

        mode_frame = tk.Frame(box, bg="white")
        mode_frame.pack(pady=5)

        for mode in ["Normal Mouse", "Zero Touch"]:
            rb = tk.Radiobutton(
                mode_frame, text=mode, value=mode, variable=self.control_mode,
                font=("Arial", 22, "bold"), bg="white", fg=TEXT_DARK,
                selectcolor=ACCENT_YELLOW, indicatoron=False, width=16, height=2,
                relief="flat", bd=2
            )
            rb.pack(side="left", padx=15)

        tk.Label(box, text="Participant name", font=("Arial", 24, "bold"),
                 fg=TEXT_DARK, bg="white").pack(pady=(35, 10))

        self.name_entry = tk.Entry(box, font=("Arial", 28), justify="center", relief="solid", bd=2)
        self.name_entry.pack(ipady=10, ipadx=10, fill="x", padx=120)
        self.name_entry.focus_set()

        warning = tk.Label(box, text="", font=("Arial", 18, "bold"), fg="#ef4444", bg="white")
        warning.pack(pady=10)

        def continue_to_home():
            name = self.name_entry.get().strip()
            if not name:
                warning.config(text="Please enter participant name first")
                return
            self.participant_name = name
            self.create_home()

        start_setup_btn = tk.Button(
            box, text="CONTINUE TO START PAGE", command=continue_to_home,
            font=("Arial", 28, "bold"), bg=PRIMARY_RED, fg="white",
            relief="flat", pady=18, cursor=self.kiosk_cursor
        )
        start_setup_btn.pack(fill="x", padx=120, pady=(20, 10))
        self.add_hover(start_setup_btn, PRIMARY_RED, PRIMARY_HOVER)

    def start_order_timer(self):
        self.cart = []
        self.add_click_count = 0
        self.order_start_time = time.time()
        self.order_start_world_time = self.now_text()
        self.order_started = True
        self.page_burgers()

    # --- Pages ---
    def create_home(self):
        self.clear_screen()
        self.update_activity()
        self.root.configure(bg=PRIMARY_RED)

        logo_label = tk.Label(self.root, text="🍔", font=("Arial", 140), bg=PRIMARY_RED, fg=ACCENT_YELLOW)
        logo_label.pack(pady=(120, 10))

        title = tk.Label(
            self.root,
            text="ZERO-TOUCH KIOSK",
            font=("Arial", 64, "bold"),
            fg="white", bg=PRIMARY_RED, justify="center"
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            self.root,
            text="The Future of Safe Dining",
            font=("Arial", 28),
            fg=ACCENT_YELLOW, bg=PRIMARY_RED
        )
        subtitle.pack(pady=(0, 50))

        start_btn = tk.Button(
            self.root, text="PINCH HERE TO START", command=self.start_order_timer,
            font=("Arial", 36, "bold"), bg=ACCENT_YELLOW, fg=TEXT_DARK,
            activebackground="white", activeforeground=TEXT_DARK,
            relief="flat", width=22, height=2, cursor=self.kiosk_cursor
        )
        start_btn.pack(pady=30)
        self.add_hover(start_btn, ACCENT_YELLOW, "white", TEXT_DARK, TEXT_DARK)

        hint = tk.Label(
            self.root, text="🖐 Move hand to guide cursor   •   🤏 Pinch to click   •   ↕️ Swipe to scroll",
            font=("Arial", 22, "bold"), fg="white", bg=PRIMARY_RED
        )
        hint.pack(side="bottom", pady=60)

    def layout(self, title_text):
        self.clear_screen()
        self.update_activity()
        self.root.configure(bg=BG_COLOR)

        # Header
        header = tk.Frame(self.root, bg=PRIMARY_RED, height=110)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(header, text=title_text, font=("Arial", 42, "bold"), fg="white", bg=PRIMARY_RED)
        title.pack(side="left", padx=60, pady=20)

        # Body
        body = tk.Frame(self.root, bg=BG_COLOR)
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(body, bg="white", width=320)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Shadow
        shadow = tk.Frame(body, bg="#d1d5db", width=3)
        shadow.pack(side="left", fill="y")

        content = tk.Frame(body, bg=BG_COLOR)
        content.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        # Sidebar Buttons
        self.sidebar_button(sidebar, "🍔 Burgers", self.page_burgers, title_text == "PREMIUM BURGERS")
        self.sidebar_button(sidebar, "🍗 Combos", self.page_sets, title_text == "COMBO SETS")
        self.sidebar_button(sidebar, "🥤 Drinks", self.page_drinks, title_text == "DRINKS & SHAKES")
        
        # Spacer
        tk.Label(sidebar, bg="white").pack(fill="y", expand=True)

        self.sidebar_button(sidebar, "🛒 View Cart", self.page_cart, title_text == "YOUR ORDER", is_cart=True)
        self.sidebar_button(sidebar, "🏠 End / New Tester", self.create_setup_page, is_cancel=True)

        return content

    def sidebar_button(self, parent, text, command, is_active=False, is_cart=False, is_cancel=False):
        bg_color = "white"
        fg_color = TEXT_DARK
        
        if is_active:
            bg_color = ACCENT_YELLOW
            fg_color = TEXT_DARK
        if is_cancel:
            fg_color = PRIMARY_RED
        if is_cart and not is_active:
            bg_color = TEXT_DARK
            fg_color = "white"

        btn = tk.Button(
            parent, text=text, command=command,
            font=("Arial", 24, "bold"), bg=bg_color, fg=fg_color,
            relief="flat", anchor="w", padx=50, height=3
        )
        btn.pack(fill="x", pady=2)
        
        if not is_active:
            hover_bg = "#f3f4f6" if not is_cart else "#374151"
            hover_fg = fg_color
            if is_cancel: hover_bg = "#fee2e2"
            self.add_hover(btn, bg_color, hover_bg, fg_color, hover_fg)

    def make_scroll_area(self, parent):
        canvas = tk.Canvas(parent, bg=BG_COLOR, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scroll_frame = tk.Frame(canvas, bg=BG_COLOR)
        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def update_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        scroll_frame.bind("<Configure>", update_scroll)
        canvas.bind("<Configure>", update_scroll)

        # --- แก้ไขส่วนนี้ให้รองรับ Mac ---
        def mouse_wheel(event):
            if platform.system() == 'Darwin':  # สำหรับ macOS
                canvas.yview_scroll(int(-1 * event.delta), "units")
            else:  # สำหรับ Windows
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", mouse_wheel)

        return scroll_frame

    def populate_grid(self, frame, items):
        row, col = 0, 0
        for name, price, emoji in items:
            self.food_card(frame, name, price, emoji, row, col)
            col += 1
            if col > 1: # 2 Columns layout for big hitboxes
                col = 0
                row += 1

    def food_card(self, parent, name, price, emoji, row, col):
        card = tk.Frame(parent, bg=CARD_BG, highlightbackground="#e5e7eb", highlightthickness=2)
        card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        icon = tk.Label(card, text=emoji, font=("Arial", 70), bg=CARD_BG)
        icon.pack(pady=(40, 15))

        name_label = tk.Label(card, text=name, font=("Arial", 26, "bold"), fg=TEXT_DARK, bg=CARD_BG, wraplength=350)
        name_label.pack(pady=(0, 5))

        price_label = tk.Label(card, text=f"{price} ฿", font=("Arial", 28, "bold"), fg=PRIMARY_RED, bg=CARD_BG)
        price_label.pack(pady=(5, 30))

        add_btn = tk.Button(
            card, text="➕ ADD TO ORDER", command=lambda: self.add_to_cart(name, price),
            font=("Arial", 22, "bold"), bg=ADD_BTN, fg="white",
            relief="flat", pady=20
        )
        add_btn.pack(fill="x", side="bottom")
        self.add_hover(add_btn, ADD_BTN, ADD_BTN_HOVER)

    def add_to_cart(self, name, price):
        self.cart.append((name, price))
        self.add_click_count += 1
        self.update_activity()
        self.show_added(name)

    # --- Extended Menu Data (For Swiping Demonstration) ---
    def page_burgers(self):
        content = self.layout("PREMIUM BURGERS")
        frame = self.make_scroll_area(content)
        items = [
            ("Signature Beef Burger", 159, "🍔"), ("Classic Cheese Burger", 89, "🍔"),
            ("Spicy Chicken Crispy", 109, "🍗"), ("Ocean Fish Deluxe", 119, "🐟"),
            ("Double Patty Smash", 199, "🍔"), ("Bacon & Egg Burger", 149, "🥓"),
            ("Truffle Mushroom Beef", 189, "🍄"), ("Hawaiian Chicken", 139, "🍍"),
            ("Veggie Plant-Based", 129, "🥗"), ("Kurobuta Pork Burger", 149, "🐷"),
            ("Spicy Jalapeno Beef", 169, "🌶️"), ("Mac & Cheese Burger", 159, "🧀"),
            ("Giant Tower Burger", 259, "🗼"), ("Teriyaki Chicken", 129, "🎌"),
            ("Grilled Salmon Burger", 219, "🎣"), ("Super Crispy Chicken", 119, "🍗")
        ]
        self.populate_grid(frame, items)

    def page_drinks(self):
        content = self.layout("DRINKS & SHAKES")
        frame = self.make_scroll_area(content)
        items = [
            ("Cola Regular", 45, "🥤"), ("Cola Zero Sugar", 45, "🥤"),
            ("Iced Lemon Tea", 55, "🍋"), ("Fresh Orange Juice", 65, "🍊"),
            ("Vanilla Milkshake", 85, "🍦"), ("Chocolate Shake", 85, "🍫"),
            ("Strawberry Shake", 85, "🍓"), ("Iced Americano", 55, "☕"),
            ("Iced Latte", 65, "☕"), ("Matcha Green Tea", 75, "🍵"),
            ("Mineral Water", 25, "💧"), ("Sparkling Water", 35, "🫧"),
            ("Root Beer", 45, "🍺"), ("Pink Lemonade", 55, "🍹"),
            ("Mango Smoothie", 85, "🥭"), ("Mixed Berry Frappe", 95, "🫐")
        ]
        self.populate_grid(frame, items)

    def page_sets(self):
        content = self.layout("COMBO SETS")
        frame = self.make_scroll_area(content)
        items = [
            ("Value Beef Combo", 199, "🍔🍟"), ("Spicy Chicken Set", 189, "🍗🥤"),
            ("Fish & Chips Set", 179, "🐟🍟"), ("Pork Burger Meal", 189, "🐷🍟"),
            ("Family Feast Box", 499, "👨‍👩‍👧‍👦"), ("Couple Sharing Set", 299, "🍔🍔"),
            ("Snack Party Box", 159, "🍟🥟"), ("Kids Happy Meal", 129, "🎁"),
            ("Mega Tower Combo", 359, "🗼🥤"), ("Healthy Veggie Set", 179, "🥗🧃"),
            ("Truffle Lover Set", 249, "🍄🍟"), ("Breakfast Set", 119, "☕🥐"),
            ("Midnight Craving", 229, "🍔🍗"), ("Nuggets Combo (10pcs)", 149, "🍗🍟"),
            ("Double Trouble Set", 279, "🍔🍔"), ("Ultimate Party Bucket", 599, "🍗🎉")
        ]
        self.populate_grid(frame, items)

    def page_cart(self):
        self.clear_screen()
        self.update_activity()
        self.root.configure(bg=BG_COLOR)

        header = tk.Frame(self.root, bg=TEXT_DARK, height=110)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(header, text="🛒 YOUR ORDER", font=("Arial", 42, "bold"), fg="white", bg=TEXT_DARK)
        title.pack(side="left", padx=60, pady=20)

        back_btn = tk.Button(
            header, text="BACK TO MENU", command=self.page_burgers,
            font=("Arial", 22, "bold"), bg="#4b5563", fg="white", relief="flat", padx=30, pady=10
        )
        back_btn.pack(side="right", padx=60, pady=15)
        self.add_hover(back_btn, "#4b5563", "#374151")

        content = tk.Frame(self.root, bg=BG_COLOR)
        content.pack(fill="both", expand=True, padx=80, pady=40)
        
        if not self.cart:
            empty = tk.Label(content, text="Your cart is currently empty.", font=("Arial", 36, "bold"), fg="#9ca3af", bg=BG_COLOR)
            empty.pack(expand=True)
            return

        list_frame = tk.Frame(content, bg=BG_COLOR)
        list_frame.pack(fill="both", expand=True)
        scroll_area = self.make_scroll_area(list_frame)

        total = 0
        for name, price in self.cart:
            row = tk.Frame(scroll_area, bg=CARD_BG, highlightbackground="#e5e7eb", highlightthickness=1)
            row.pack(fill="x", pady=8)

            item = tk.Label(row, text=name, font=("Arial", 28, "bold"), fg=TEXT_DARK, bg=CARD_BG)
            item.pack(side="left", padx=40, pady=30)

            price_label = tk.Label(row, text=f"{price} ฿", font=("Arial", 28, "bold"), fg=PRIMARY_RED, bg=CARD_BG)
            price_label.pack(side="right", padx=40)
            total += price

        # Modern Checkout Footer
        bottom = tk.Frame(content, bg=CARD_BG, highlightbackground="#e5e7eb", highlightthickness=2)
        bottom.pack(fill="x", side="bottom", pady=20)

        total_frame = tk.Frame(bottom, bg=CARD_BG)
        total_frame.pack(fill="x", padx=40, pady=30)

        total_text = tk.Label(total_frame, text="GRAND TOTAL", font=("Arial", 32, "bold"), fg=TEXT_DARK, bg=CARD_BG)
        total_text.pack(side="left")

        total_val = tk.Label(total_frame, text=f"{total} ฿", font=("Arial", 48, "bold"), fg=PRIMARY_RED, bg=CARD_BG)
        total_val.pack(side="right")

        btn_frame = tk.Frame(bottom, bg=CARD_BG)
        btn_frame.pack(fill="x", padx=40, pady=(0, 40))

        clear_btn = tk.Button(
            btn_frame, text="🗑 CLEAR CART", command=self.clear_cart,
            font=("Arial", 26, "bold"), bg="#ef4444", fg="white", relief="flat", width=15, pady=20
        )
        clear_btn.pack(side="left")
        self.add_hover(clear_btn, "#ef4444", "#dc2626")

        confirm_btn = tk.Button(
            btn_frame, text="💳 CONFIRM & PAY", command=self.confirm_order,
            font=("Arial", 26, "bold"), bg=ADD_BTN, fg="white", relief="flat", pady=20
        )
        confirm_btn.pack(side="right", fill="x", expand=True, padx=(20, 0))
        self.add_hover(confirm_btn, ADD_BTN, ADD_BTN_HOVER)

    def show_added(self, name):
        popup = tk.Toplevel(self.root)
        popup.geometry("600x120+660+800") 
        popup.configure(bg=ADD_BTN)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)

        label = tk.Label(popup, text=f"✅ ADDED: {name}", font=("Arial", 26, "bold"), fg="white", bg=ADD_BTN)
        label.pack(expand=True)
        popup.after(1200, popup.destroy)

    def confirm_order(self):
        final_time = self.get_elapsed()
        final_total = self.cart_total()
        final_add_click_count = self.add_click_count
        self.save_summary_row()

        self.clear_screen()
        self.root.configure(bg=ADD_BTN)

        title = tk.Label(self.root, text="🎉 ORDER RECEIVED!", font=("Arial", 64, "bold"), fg="white", bg=ADD_BTN)
        title.pack(pady=(80, 20))

        queue = tk.Label(self.root, text="Your Queue No: 089", font=("Arial", 70, "bold"), fg=ACCENT_YELLOW, bg=ADD_BTN)
        queue.pack(pady=20)

        msg = tk.Label(self.root, text=f"Please proceed to the counter for payment.\nTime used: {final_time} seconds | Add clicks: {final_add_click_count} | Total: {final_total} ฿", font=("Arial", 32), fg="white", bg=ADD_BTN)
        msg.pack(pady=20)

        self.cart = []

        home_btn = tk.Button(
            self.root, text="START NEW TESTER", command=self.create_setup_page,
            font=("Arial", 32, "bold"), bg="white", fg=ADD_BTN, relief="flat", width=20, pady=20
        )
        home_btn.pack(pady=80)
        self.add_hover(home_btn, "white", "#f3f4f6", ADD_BTN, ADD_BTN)

    def clear_cart(self):
        self.cart = []
        self.page_cart()

    def check_idle(self):
        if time.time() - self.last_action_time > 60:
            self.cart = []
            self.create_setup_page()
            self.last_action_time = time.time()
        self.root.after(1000, self.check_idle)

if __name__ == "__main__":
    root = tk.Tk()
    app = ZeroTouchFoodKiosk(root)
    root.mainloop()