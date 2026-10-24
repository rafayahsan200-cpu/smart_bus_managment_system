"""
SMARTBUS — Smart Bus Ticket Booking & Reservation System
Professional Tkinter desktop application.

Features retained and improved from the original console project:
- View and search routes
- Book tickets with passenger details and seat count
- View and cancel bookings
- Seat availability
- Route schedule
- Booking report and revenue summary
- Exit confirmation

Note: This version stores bookings in memory. Records reset when the app closes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

ROUTES = [
    {"id": "R101", "from": "Karachi", "to": "Hyderabad", "time": "08:00 AM", "fare": 1200, "capacity": 40, "available": 40},
    {"id": "R102", "from": "Karachi", "to": "Sukkur", "time": "09:30 AM", "fare": 2000, "capacity": 36, "available": 36},
    {"id": "R103", "from": "Hyderabad", "to": "Mirpur Khas", "time": "11:00 AM", "fare": 800, "capacity": 32, "available": 32},
    {"id": "R104", "from": "Karachi", "to": "Lahore", "time": "07:00 PM", "fare": 5000, "capacity": 45, "available": 45},
    {"id": "R105", "from": "Sukkur", "to": "Hyderabad", "time": "02:00 PM", "fare": 1500, "capacity": 30, "available": 30},
]
BOOKINGS = []
NEXT_BOOKING_ID = 1001

# Theme
BG = "#F4F7FB"
NAVY = "#13233F"
NAVY_LIGHT = "#1C3357"
BLUE = "#2F6FED"
BLUE_HOVER = "#2458C7"
WHITE = "#FFFFFF"
TEXT = "#18263D"
MUTED = "#708099"
BORDER = "#E0E7F0"
GREEN = "#138A61"
TEAL = "#0F766E"
RED = "#C23B4A"
AMBER = "#B7791F"
PURPLE = "#7453C8"


class SmartBusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartBus | Booking & Reservation System")
        self.root.geometry("1280x800")
        self.root.minsize(1060, 680)
        self.root.configure(bg=BG)
        self.search_var = tk.StringVar()
        self.booking_search_var = tk.StringVar()
        self.passenger_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.seat_count_var = tk.StringVar(value="1")
        self.route_choice_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Welcome to SmartBus")
        self.active_page = "Dashboard"
        self._styles()
        self._layout()
        self._show_page("Dashboard")
        self.refresh_all()
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def _styles(self):
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure("Treeview", background=WHITE, foreground=TEXT,
                    fieldbackground=WHITE, rowheight=34, borderwidth=0,
                    font=("Segoe UI", 10))
        s.configure("Treeview.Heading", background="#EAF0F8", foreground=NAVY,
                    font=("Segoe UI", 9, "bold"), padding=(10, 11), relief="flat")
        s.map("Treeview", background=[("selected", "#DCE9FF")],
              foreground=[("selected", NAVY)])
        s.configure("TEntry", padding=9, font=("Segoe UI", 10))
        s.configure("TCombobox", padding=8, font=("Segoe UI", 10))
        s.configure("TSpinbox", padding=8, font=("Segoe UI", 10))

    def _layout(self):
        # Fixed left navigation
        self.sidebar = tk.Frame(self.root, bg=NAVY, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = tk.Frame(self.sidebar, bg=NAVY)
        logo.pack(fill="x", padx=22, pady=(25, 30))
        tk.Label(logo, text="✦  SMARTBUS", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(logo, text="BOOKING & RESERVATION", bg=NAVY, fg="#9EB3D4",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=(29, 0), pady=(4, 0))

        tk.Label(self.sidebar, text="WORKSPACE", bg=NAVY, fg="#8298B8",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=22, pady=(0, 10))
        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "▦"),
            ("Routes & Search", "⇄"),
            ("Book a Ticket", "＋"),
            ("Bookings", "▤"),
            ("Seat Availability", "◷"),
            ("Route Schedule", "☷"),
            ("Reports", "▥"),
        ]
        for name, icon in nav_items:
            btn = tk.Button(
                self.sidebar, text=f"   {icon}    {name}", anchor="w",
                command=lambda n=name: self._show_page(n),
                bg=NAVY, fg="#D5E0F1", activebackground=NAVY_LIGHT,
                activeforeground=WHITE, relief="flat", bd=0, cursor="hand2",
                font=("Segoe UI", 10, "bold"), padx=13, pady=13
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[name] = btn

        spacer = tk.Frame(self.sidebar, bg=NAVY)
        spacer.pack(fill="both", expand=True)
        tk.Frame(self.sidebar, bg="#304361", height=1).pack(fill="x", padx=18, pady=(0, 12))
        tk.Label(self.sidebar, text="●  System ready", bg=NAVY, fg="#76D6B0",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=24, pady=(0, 4))
        tk.Label(self.sidebar, text="Desktop edition  •  v2.0", bg=NAVY, fg="#8298B8",
                 font=("Segoe UI", 8)).pack(anchor="w", padx=24, pady=(0, 20))
        exit_btn = tk.Button(self.sidebar, text="   ↪    Exit application", anchor="w",
                             command=self.exit_app, bg=NAVY, fg="#F5A5AE",
                             activebackground=NAVY_LIGHT, activeforeground=WHITE,
                             relief="flat", bd=0, cursor="hand2",
                             font=("Segoe UI", 10, "bold"), padx=13, pady=12)
        exit_btn.pack(fill="x", padx=12, pady=(0, 14))

        # Right workspace
        self.workspace = tk.Frame(self.root, bg=BG)
        self.workspace.pack(side="left", fill="both", expand=True)

        topbar = tk.Frame(self.workspace, bg=WHITE, height=62,
                          highlightbackground=BORDER, highlightthickness=1)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Label(topbar, text="SMARTBUS  /  TRANSPORT MANAGEMENT", bg=WHITE,
                 fg=MUTED, font=("Segoe UI", 9, "bold")).pack(side="left", padx=26)
        self.top_time = tk.Label(topbar, text="", bg=WHITE, fg=TEXT,
                                 font=("Segoe UI", 9, "bold"))
        self.top_time.pack(side="right", padx=25)
        self._update_clock()

        self.content = tk.Frame(self.workspace, bg=BG)
        self.content.pack(fill="both", expand=True, padx=26, pady=23)

        footer = tk.Frame(self.workspace, bg=WHITE, height=31)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)
        tk.Label(footer, textvariable=self.status_var, bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9)).pack(side="left", padx=24, pady=6)
        tk.Label(footer, text="SMARTBUS  •  PYTHON DESKTOP APP", bg=WHITE,
                 fg=MUTED, font=("Segoe UI", 8, "bold")).pack(side="right", padx=24, pady=6)

    def _update_clock(self):
        self.top_time.config(text=datetime.now().strftime("%a, %d %b %Y  |  %I:%M %p"))
        self.root.after(30000, self._update_clock)

    def _button(self, parent, text, command, color=BLUE, width=None):
        return tk.Button(parent, text=text, command=command, width=width,
                         bg=color, fg=WHITE, activebackground=BLUE_HOVER,
                         activeforeground=WHITE, relief="flat", bd=0,
                         cursor="hand2", font=("Segoe UI", 9, "bold"),
                         padx=14, pady=10)

    def _entry(self, parent, variable, width=28):
        return ttk.Entry(parent, textvariable=variable, width=width)

    def _page_heading(self, title, subtitle):
        head = tk.Frame(self.content, bg=BG)
        head.pack(fill="x", pady=(0, 20))
        tk.Label(head, text=title, bg=BG, fg=TEXT,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(head, text=subtitle, bg=BG, fg=MUTED,
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

    def _clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def _show_page(self, page):
        self.active_page = page
        for name, button in self.nav_buttons.items():
            button.configure(bg=BLUE if name == page else NAVY,
                             fg=WHITE if name == page else "#D5E0F1")
        self._clear_content()
        if page == "Dashboard":
            self._dashboard_page()
        elif page == "Routes & Search":
            self._routes_page()
        elif page == "Book a Ticket":
            self._booking_page()
        elif page == "Bookings":
            self._bookings_page()
        elif page == "Seat Availability":
            self._seats_page()
        elif page == "Route Schedule":
            self._schedule_page()
        elif page == "Reports":
            self._reports_page()
        self.status_var.set(f"{page} opened")

    def _card(self, parent, title, value, accent, note):
        card = tk.Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        card.pack(side="left", fill="x", expand=True, padx=(0, 13))
        tk.Frame(card, bg=accent, height=4).pack(fill="x")
        inner = tk.Frame(card, bg=WHITE)
        inner.pack(fill="x", padx=17, pady=15)
        tk.Label(inner, text=title.upper(), bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(inner, text=value, bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 21, "bold")).pack(anchor="w", pady=(8, 2))
        tk.Label(inner, text=note, bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 8)).pack(anchor="w")
        return card

    def _dashboard_page(self):
        self._page_heading("Dashboard", "Your quick overview of routes, reservations and seat capacity.")
        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x", pady=(0, 22))
        self._card(stats, "Active routes", str(len(ROUTES)), BLUE, "Routes currently listed")
        self._card(stats, "Total bookings", str(len(BOOKINGS)), GREEN, "Reservations this session")
        self._card(stats, "Available seats", str(sum(r["available"] for r in ROUTES)),
                   PURPLE, "Across all routes")
        self._card(stats, "Booking revenue", f'Rs {sum(b["fare"] for b in BOOKINGS):,}',
                   AMBER, "From current bookings")

        lower = tk.Frame(self.content, bg=BG)
        lower.pack(fill="both", expand=True)
        panel = self._panel(lower)
        panel.pack(side="left", fill="both", expand=True, padx=(0, 14))
        tk.Label(panel, text="Popular routes", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(17, 4))
        tk.Label(panel, text="A snapshot of all available services.", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=18, pady=(0, 12))
        for r in ROUTES[:4]:
            row = tk.Frame(panel, bg="#F8FAFD")
            row.pack(fill="x", padx=16, pady=4)
            tk.Label(row, text=f'{r["from"]}  →  {r["to"]}', bg="#F8FAFD", fg=TEXT,
                     font=("Segoe UI", 10, "bold")).pack(side="left", padx=12, pady=11)
            tk.Label(row, text=f'Rs {r["fare"]:,}', bg="#F8FAFD", fg=BLUE,
                     font=("Segoe UI", 10, "bold")).pack(side="right", padx=12)
        quick = self._panel(lower)
        quick.configure(width=255)
        quick.pack(side="right", fill="y")
        quick.pack_propagate(False)
        tk.Label(quick, text="Quick actions", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=17, pady=(17, 13))
        self._button(quick, "＋  Book a ticket", lambda: self._show_page("Book a Ticket")).pack(fill="x", padx=15, pady=5)
        self._button(quick, "⇄  Search routes", lambda: self._show_page("Routes & Search"), NAVY_LIGHT).pack(fill="x", padx=15, pady=5)
        self._button(quick, "▤  View bookings", lambda: self._show_page("Bookings"), TEAL).pack(fill="x", padx=15, pady=5)
        self._button(quick, "▥  View reports", lambda: self._show_page("Reports"), PURPLE).pack(fill="x", padx=15, pady=5)
        tk.Label(quick, text="Tip: double-click a route\nin the route list to book it.",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 9), justify="left").pack(anchor="w", padx=17, pady=(17, 0))

    def _panel(self, parent):
        return tk.Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)

    def _route_table(self, parent, search_var=None, height=11):
        wrapper = tk.Frame(parent, bg=WHITE)
        cols = ("id", "from", "to", "time", "fare", "available", "capacity")
        tree = ttk.Treeview(wrapper, columns=cols, show="headings", height=height, selectmode="browse")
        headers = [
            ("id", "ROUTE ID", 90), ("from", "DEPARTURE", 140), ("to", "DESTINATION", 150),
            ("time", "DEPARTURE TIME", 135), ("fare", "FARE (PKR)", 110),
            ("available", "SEATS LEFT", 100), ("capacity", "CAPACITY", 90)
        ]
        for col, title, width in headers:
            tree.heading(col, text=title)
            tree.column(col, width=width, anchor="w" if col in ("from", "to") else "center")
        scroll = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        if search_var is not None:
            search_var.trace_add("write", lambda *_: self._populate_routes(tree, search_var.get()))
        self._populate_routes(tree, search_var.get() if search_var else "")
        tree.bind("<Double-1>", lambda _e: self._route_double_click(tree))
        return wrapper, tree

    def _populate_routes(self, tree, query=""):
        query = query.strip().lower()
        for item in tree.get_children():
            tree.delete(item)
        for r in ROUTES:
            text = " ".join(str(r[k]) for k in ("id", "from", "to", "time", "fare", "available")).lower()
            if query and query not in text:
                continue
            tree.insert("", "end", iid=r["id"], values=(
                r["id"], r["from"], r["to"], r["time"], f'{r["fare"]:,}', r["available"], r["capacity"]
            ))

    def _route_double_click(self, tree):
        selected = tree.selection()
        if selected:
            self.route_choice_var.set(selected[0])
            self._show_page("Book a Ticket")

    def _routes_page(self):
        self._page_heading("Routes & Search", "Find a bus by route ID, city, departure time or fare.")
        panel = self._panel(self.content)
        panel.pack(fill="both", expand=True)
        bar = tk.Frame(panel, bg=WHITE)
        bar.pack(fill="x", padx=18, pady=16)
        tk.Label(bar, text="All bus routes", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        search = tk.StringVar()
        tk.Label(bar, text="Search routes", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(side="right", padx=(10, 7))
        self._entry(bar, search, 27).pack(side="right")
        wrapper, tree = self._route_table(panel, search, 13)
        wrapper.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        foot = tk.Frame(panel, bg="#F8FAFD")
        foot.pack(fill="x", padx=1, pady=(0, 1))
        tk.Label(foot, text="Select a route and book it, or double-click a route row.",
                 bg="#F8FAFD", fg=MUTED, font=("Segoe UI", 9)).pack(side="left", padx=18, pady=13)
        self._button(foot, "Book selected route", lambda: self._book_selected(tree)).pack(side="right", padx=15, pady=7)

    def _book_selected(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select a route", "Please select a route first.")
            return
        self.route_choice_var.set(selected[0])
        self._show_page("Book a Ticket")

    def _booking_page(self):
        self._page_heading("Book a Ticket", "Enter passenger information, choose a route and confirm the reservation.")
        body = tk.Frame(self.content, bg=BG)
        body.pack(fill="both", expand=True)
        form = self._panel(body)
        form.pack(side="left", fill="both", expand=True, padx=(0, 15))
        tk.Label(form, text="Passenger information", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=22, pady=(22, 4))
        tk.Label(form, text="Fields marked with * are required.", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=22, pady=(0, 17))
        self._form_label(form, "Passenger full name *")
        self._entry(form, self.passenger_var, 38).pack(anchor="w", padx=22, pady=(0, 15), ipady=2)
        self._form_label(form, "Contact number *")
        self._entry(form, self.phone_var, 38).pack(anchor="w", padx=22, pady=(0, 15), ipady=2)
        self._form_label(form, "Select route *")
        route_values = [f'{r["id"]} | {r["from"]} → {r["to"]} | Rs {r["fare"]:,}' for r in ROUTES]
        self.route_combo = ttk.Combobox(form, state="readonly", values=route_values, width=48)
        self.route_combo.pack(anchor="w", padx=22, pady=(0, 15))
        current = next((i for i, r in enumerate(ROUTES) if r["id"] == self.route_choice_var.get()), 0)
        self.route_combo.current(current)
        self.route_combo.bind("<<ComboboxSelected>>", lambda _e: self._update_booking_summary())
        self._form_label(form, "Number of seats *")
        self.seat_spin = ttk.Spinbox(form, from_=1, to=45, textvariable=self.seat_count_var, width=10,
                                     command=self._update_booking_summary)
        self.seat_spin.pack(anchor="w", padx=22, pady=(0, 18))
        self.seat_count_var.trace_add("write", lambda *_: self._update_booking_summary())
        actions = tk.Frame(form, bg=WHITE)
        actions.pack(anchor="w", padx=22, pady=(0, 22))
        self._button(actions, "Confirm booking", self._confirm_booking).pack(side="left", padx=(0, 9))
        self._button(actions, "Clear form", self._clear_booking_form, "#63738B").pack(side="left")

        summary = self._panel(body)
        summary.configure(width=270)
        summary.pack(side="right", fill="y")
        summary.pack_propagate(False)
        tk.Label(summary, text="Booking summary", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(22, 18))
        self.summary_route = tk.Label(summary, text="", bg=WHITE, fg=TEXT,
                                      font=("Segoe UI", 11, "bold"), wraplength=220, justify="left")
        self.summary_route.pack(anchor="w", padx=18, pady=(0, 8))
        self.summary_time = tk.Label(summary, text="", bg=WHITE, fg=MUTED,
                                     font=("Segoe UI", 9))
        self.summary_time.pack(anchor="w", padx=18, pady=(0, 20))
        tk.Frame(summary, bg=BORDER, height=1).pack(fill="x", padx=18)
        tk.Label(summary, text="FARE PER SEAT", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=18, pady=(18, 4))
        self.summary_fare = tk.Label(summary, text="", bg=WHITE, fg=TEXT,
                                     font=("Segoe UI", 16, "bold"))
        self.summary_fare.pack(anchor="w", padx=18)
        tk.Label(summary, text="TOTAL ESTIMATE", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=18, pady=(20, 4))
        self.summary_total = tk.Label(summary, text="", bg=WHITE, fg=BLUE,
                                      font=("Segoe UI", 23, "bold"))
        self.summary_total.pack(anchor="w", padx=18)
        self.summary_seats = tk.Label(summary, text="", bg=WHITE, fg=GREEN,
                                      font=("Segoe UI", 9, "bold"))
        self.summary_seats.pack(anchor="w", padx=18, pady=(13, 0))
        tk.Label(summary, text="Please check route and passenger details before confirming.",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 9), wraplength=225,
                 justify="left").pack(anchor="w", padx=18, pady=(25, 0))
        self._update_booking_summary()

    def _form_label(self, parent, text):
        tk.Label(parent, text=text, bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=22, pady=(0, 6))

    def _chosen_route(self):
        try:
            route_id = self.route_combo.get().split("|")[0].strip()
        except (AttributeError, tk.TclError):
            route_id = self.route_choice_var.get()
        return next((r for r in ROUTES if r["id"] == route_id), ROUTES[0])

    def _update_booking_summary(self):
        if not hasattr(self, "route_combo") or not self.route_combo.winfo_exists():
            return
        r = self._chosen_route()
        try:
            count = max(1, int(self.seat_count_var.get()))
        except (ValueError, tk.TclError):
            count = 1
        self.summary_route.config(text=f'{r["from"]}  →  {r["to"]}')
        self.summary_time.config(text=f'{r["id"]}   •   Departs {r["time"]}')
        self.summary_fare.config(text=f'Rs {r["fare"]:,}')
        self.summary_total.config(text=f'Rs {r["fare"] * count:,}')
        self.seat_spin.configure(to=max(1, r["available"]))
        if r["available"] < 1:
            self.summary_seats.config(text="Fully booked", fg=RED)
        else:
            self.summary_seats.config(text=f'{r["available"]} seats currently available', fg=GREEN)

    def _clear_booking_form(self):
        self.passenger_var.set("")
        self.phone_var.set("")
        self.seat_count_var.set("1")
        if hasattr(self, "route_combo") and self.route_combo.winfo_exists():
            self.route_combo.current(0)
        self.route_choice_var.set(ROUTES[0]["id"])
        self._update_booking_summary()

    def _confirm_booking(self):
        global NEXT_BOOKING_ID
        name = self.passenger_var.get().strip()
        phone = self.phone_var.get().strip()
        if not name or not phone:
            messagebox.showwarning("Required information", "Please enter passenger name and contact number.")
            return
        r = self._chosen_route()
        try:
            count = int(self.seat_count_var.get())
        except ValueError:
            messagebox.showwarning("Invalid seats", "Enter a valid whole number of seats.")
            return
        if count < 1:
            messagebox.showwarning("Invalid seats", "At least one seat must be booked.")
            return
        if count > r["available"]:
            messagebox.showerror("Not enough seats", f'Only {r["available"]} seat(s) remain on this route.')
            return
        total = r["fare"] * count
        if not messagebox.askyesno("Confirm reservation",
            f"Passenger: {name}\nRoute: {r['from']} → {r['to']}\n"
            f"Seats: {count}\nTotal fare: Rs {total:,}\n\nConfirm this booking?"):
            return
        b = {"id": NEXT_BOOKING_ID, "name": name, "phone": phone, "route_id": r["id"],
             "from": r["from"], "to": r["to"], "time": r["time"], "seats": count,
             "fare": total, "created": datetime.now().strftime("%d %b %Y %I:%M %p")}
        BOOKINGS.append(b)
        r["available"] -= count
        NEXT_BOOKING_ID += 1
        self.refresh_all()
        self._update_booking_summary()
        self.status_var.set(f"Booking SB{b['id']} confirmed")
        messagebox.showinfo("Booking successful",
            f"Your booking has been confirmed!\n\nBooking ID: SB{b['id']}\n"
            f"Passenger: {name}\nRoute: {r['from']} → {r['to']}\n"
            f"Departure: {r['time']}\nSeats: {count}\nTotal fare: Rs {total:,}")
        self._clear_booking_form()

    def _bookings_page(self):
        self._page_heading("Bookings", "Review passenger reservations or cancel a booking by selecting its record.")
        panel = self._panel(self.content)
        panel.pack(fill="both", expand=True)
        bar = tk.Frame(panel, bg=WHITE); bar.pack(fill="x", padx=18, pady=15)
        tk.Label(bar, text="Reservation records", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        search = tk.StringVar()
        tk.Label(bar, text="Search bookings", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(side="right", padx=(10, 7))
        self._entry(bar, search, 24).pack(side="right")
        cols = ("id", "name", "phone", "route", "time", "seats", "fare", "created")
        tree = ttk.Treeview(panel, columns=cols, show="headings", height=12, selectmode="browse")
        for c, label, width in [
            ("id","BOOKING ID",90),("name","PASSENGER",130),("phone","CONTACT",115),
            ("route","ROUTE",165),("time","DEPARTURE",105),("seats","SEATS",60),
            ("fare","TOTAL FARE",100),("created","BOOKED AT",145)]:
            tree.heading(c, text=label); tree.column(c, width=width, anchor="center")
        tree.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        def populate(*_):
            for item in tree.get_children(): tree.delete(item)
            q = search.get().lower().strip()
            for b in BOOKINGS:
                values = (f'SB{b["id"]}', b["name"], b["phone"],
                          f'{b["from"]} → {b["to"]}', b["time"], b["seats"],
                          f'Rs {b["fare"]:,}', b["created"])
                if not q or q in " ".join(map(str, values)).lower():
                    tree.insert("", "end", iid=str(b["id"]), values=values)
        search.trace_add("write", populate)
        populate()
        bottom = tk.Frame(panel, bg="#F8FAFD"); bottom.pack(fill="x")
        tk.Label(bottom, text=f"{len(BOOKINGS)} reservation(s) in this session",
                 bg="#F8FAFD", fg=MUTED, font=("Segoe UI", 9)).pack(side="left", padx=18, pady=12)
        self._button(bottom, "Cancel selected booking", lambda: self._cancel_selected(tree), RED).pack(side="right", padx=15, pady=7)
        self._button(bottom, "Refresh records", lambda: self._show_page("Bookings"), NAVY_LIGHT).pack(side="right", padx=5, pady=7)
        if not BOOKINGS:
            tk.Label(panel, text="No bookings yet. Create a reservation from “Book a Ticket”.",
                     bg=WHITE, fg=MUTED, font=("Segoe UI", 10)).pack(pady=(0, 14))

    def _cancel_selected(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select booking", "Select a booking record to cancel.")
            return
        bid = int(selected[0])
        b = next((x for x in BOOKINGS if x["id"] == bid), None)
        if not b:
            messagebox.showerror("Not found", "This booking record could not be found.")
            return
        if not messagebox.askyesno("Confirm cancellation",
                f'Cancel booking SB{bid} for {b["name"]}?\n{b["seats"]} seat(s) will be released.'):
            return
        route = next(r for r in ROUTES if r["id"] == b["route_id"])
        route["available"] += b["seats"]
        BOOKINGS.remove(b)
        self.refresh_all()
        self._show_page("Bookings")
        self.status_var.set(f"Booking SB{bid} cancelled")
        messagebox.showinfo("Booking cancelled", f"Booking SB{bid} has been cancelled.")

    def _seats_page(self):
        self._page_heading("Seat Availability", "Monitor remaining capacity across all bus routes.")
        cards = tk.Frame(self.content, bg=BG); cards.pack(fill="x", pady=(0, 18))
        for r in ROUTES:
            card = self._panel(cards)
            card.pack(fill="x", pady=5)
            row = tk.Frame(card, bg=WHITE); row.pack(fill="x", padx=18, pady=14)
            left = tk.Frame(row, bg=WHITE); left.pack(side="left", fill="x", expand=True)
            tk.Label(left, text=f'{r["from"]}  →  {r["to"]}', bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(left, text=f'{r["id"]}  •  Departure {r["time"]}  •  Rs {r["fare"]:,} per seat',
                     bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 0))
            tk.Label(row, text=f'{r["available"]} / {r["capacity"]}', bg=WHITE,
                     fg=GREEN if r["available"] > 0 else RED,
                     font=("Segoe UI", 13, "bold")).pack(side="right", padx=(12, 0))
            bar_bg = tk.Frame(card, bg="#E8EDF5", height=5); bar_bg.pack(fill="x", padx=18, pady=(0, 14))
            fill = tk.Frame(bar_bg, bg=GREEN if r["available"] > 0 else RED,
                            height=5, width=max(0, int(300 * r["available"] / r["capacity"])))
            fill.place(relx=0, rely=0, relheight=1, relwidth=r["available"] / r["capacity"])

    def _schedule_page(self):
        self._page_heading("Route Schedule", "Review departure times and planned connections for every listed route.")
        panel = self._panel(self.content); panel.pack(fill="both", expand=True)
        tk.Label(panel, text="Daily departure schedule", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(18, 12))
        cols = ("time", "id", "from", "to", "fare", "status")
        tree = ttk.Treeview(panel, columns=cols, show="headings", height=12)
        for c, title, width in [
            ("time","DEPARTURE TIME",160),("id","ROUTE ID",110),("from","ORIGIN",180),
            ("to","DESTINATION",190),("fare","FARE (PKR)",140),("status","SEAT STATUS",150)]:
            tree.heading(c, text=title); tree.column(c, width=width, anchor="center")
        tree.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        sorted_routes = sorted(ROUTES, key=lambda r: datetime.strptime(r["time"], "%I:%M %p"))
        for r in sorted_routes:
            state = "Available" if r["available"] else "Fully booked"
            tree.insert("", "end", values=(r["time"], r["id"], r["from"], r["to"],
                                           f'{r["fare"]:,}', f'{state} ({r["available"]})'))

    def _reports_page(self):
        self._page_heading("Reports & Summary", "A live summary calculated from current session bookings.")
        revenue = sum(b["fare"] for b in BOOKINGS)
        seats_booked = sum(b["seats"] for b in BOOKINGS)
        cards = tk.Frame(self.content, bg=BG); cards.pack(fill="x", pady=(0, 20))
        self._card(cards, "Bookings", str(len(BOOKINGS)), BLUE, "Confirmed reservations")
        self._card(cards, "Seats sold", str(seats_booked), GREEN, "Passenger seats reserved")
        self._card(cards, "Revenue", f"Rs {revenue:,}", PURPLE, "Total booking value")
        self._card(cards, "Routes", str(len(ROUTES)), AMBER, "Routes in the system")
        panel = self._panel(self.content); panel.pack(fill="both", expand=True)
        tk.Label(panel, text="Route performance", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(18, 12))
        cols = ("route", "journey", "bookings", "seats", "available", "revenue")
        tree = ttk.Treeview(panel, columns=cols, show="headings", height=8)
        for c, title, width in [
            ("route","ROUTE ID",100),("journey","JOURNEY",210),("bookings","BOOKINGS",100),
            ("seats","SEATS SOLD",100),("available","SEATS LEFT",110),("revenue","REVENUE",140)]:
            tree.heading(c, text=title); tree.column(c, width=width, anchor="center")
        tree.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        for r in ROUTES:
            bs = [b for b in BOOKINGS if b["route_id"] == r["id"]]
            tree.insert("", "end", values=(r["id"], f'{r["from"]} → {r["to"]}', len(bs),
                sum(b["seats"] for b in bs), r["available"], f'Rs {sum(b["fare"] for b in bs):,}'))

    def refresh_all(self):
        self.status_var.set("Data refreshed successfully")
        if self.active_page:
            self._show_page(self.active_page)

    def exit_app(self):
        if messagebox.askyesno("Exit SmartBus", "Are you sure you want to close SmartBus?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartBusApp(root)
    root.mainloop()
