import customtkinter as ctk
from datetime import datetime

class LegislativeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Legislative Management System - Baguio City")
        self.geometry("1280x800")
        self.configure(fg_color="#f8fafc")

        # The main container where pages are swapped
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both")

        # Start at the new Admin Dashboard (Homepage)
        self.show_dashboard()

    def clear_screen(self):
        """Clears the container before loading a new page view."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- SHARED COMPONENTS ---
    def create_navbar(self):
        navbar = ctk.CTkFrame(self.main_container, fg_color="white", height=70, corner_radius=0)
        navbar.pack(fill="x", side="top")
        
        # Logo and Title
        ctk.CTkLabel(navbar, text="🏛️", font=("Arial", 24)).pack(side="left", padx=(30, 10))
        title_box = ctk.CTkFrame(navbar, fg_color="transparent")
        title_box.pack(side="left", pady=10)
        ctk.CTkLabel(title_box, text="Sangguniang Panlungsod", font=("Arial", 16, "bold"), text_color="#0f172a").pack(anchor="w")
        ctk.CTkLabel(title_box, text="CITY COUNCIL (BAGUIO CITY)", font=("Arial", 11), text_color="#64748b").pack(anchor="w")

        # Buttons
        ctk.CTkButton(navbar, text="Logout", fg_color="#fff1f2", text_color="#e11d48", hover_color="#ffe4e6", width=90).pack(side="right", padx=30)
        ctk.CTkButton(navbar, text="Home", fg_color="white", text_color="#333", border_width=1, border_color="#ddd", width=80, command=self.show_dashboard).pack(side="right")
        return navbar

    # --- PAGE 1: ADMIN DASHBOARD (HOMEPAGE) ---
    def show_dashboard(self):
        self.clear_screen()
        self.create_navbar()

        # Welcome Section
        welcome_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=60, pady=(40, 20))

        welcome_lbl = ctk.CTkLabel(welcome_frame, text="Welcome back, ", font=("Arial", 36, "bold"), text_color="#0f172a")
        welcome_lbl.pack(side="left")
        ctk.CTkLabel(welcome_frame, text="Admin!", font=("Arial", 36, "bold"), text_color="#2563eb").pack(side="left")
        
        date_str = datetime.now().strftime("%B %d, %Y")
        ctk.CTkLabel(welcome_frame, text=date_str, font=("Arial", 14, "bold"), fg_color="white", width=150, height=40, corner_radius=10).pack(side="right")
        
        ctk.CTkLabel(self.main_container, text="System Overview & Control Panel", font=("Arial", 18), text_color="#64748b").pack(anchor="w", padx=60)
        ctk.CTkLabel(self.main_container, text="MANAGEMENT TOOLS", font=("Arial", 12, "bold"), text_color="#94a3b8").pack(anchor="w", padx=60, pady=(30, 10))

        # 3x2 Grid
        grid = ctk.CTkFrame(self.main_container, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=50)

        tools = [
            ("📅", "Events", "Seminars & Trainings", 0, 0, self.show_event_categories),
            ("📁", "Registry", "Central Database", 0, 1, self.show_record_registry),
            ("☁️", "Cloud Files", "Storage & Transfer", 0, 2, None),
            ("👥", "Accounts", "User Management", 1, 0, None),
            ("🛡️", "Security", "Login & IP Logs", 1, 1, None),
            ("📚", "Resources", "Shared Docs, Photos & Videos", 1, 2, None)
        ]

        for icon, title, sub, r, c, cmd in tools:
            card = ctk.CTkFrame(grid, fg_color="white", corner_radius=20, border_width=1, border_color="#f1f5f9")
            card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
            grid.grid_columnconfigure(c, weight=1)
            grid.grid_rowconfigure(r, weight=1)

            ctk.CTkLabel(card, text=icon, font=("Arial", 30), fg_color="#eff6ff", width=60, height=60, corner_radius=12).pack(side="left", padx=20, pady=20)
            txt_box = ctk.CTkFrame(card, fg_color="transparent")
            txt_box.pack(side="left", anchor="center")
            ctk.CTkLabel(txt_box, text=title, font=("Arial", 16, "bold")).pack(anchor="w")
            ctk.CTkLabel(txt_box, text=sub, font=("Arial", 12), text_color="#64748b").pack(anchor="w")
            
            if cmd: card.bind("<Button-1>", lambda e, func=cmd: func())

    # --- PAGE 2: EVENT CATEGORIES ---
    def show_event_categories(self):
        self.clear_screen()
        self.create_navbar()

        ctk.CTkLabel(self.main_container, text="Event Categories", font=("Arial", 30, "bold")).pack(pady=(40, 5))
        ctk.CTkLabel(self.main_container, text="Select a category to manage specific schedules and records.", text_color="#64748b").pack(pady=(0, 40))

        grid = ctk.CTkFrame(self.main_container, fg_color="transparent")
        grid.pack(expand=True, fill="both", padx=60)

        cats = [
            ("👥", "Seminars", 0, 0), ("🧑‍🏫", "Public Consultation", 0, 1),
            ("🏛️", "Committee Level Hearing", 0, 2), ("📂", "Others", 1, 0)
        ]

        for icon, title, r, c in cats:
            card = ctk.CTkFrame(grid, fg_color="white", corner_radius=20, border_width=1, border_color="#eee")
            card.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")
            grid.grid_columnconfigure(c, weight=1)

            ctk.CTkLabel(card, text=icon, font=("Arial", 50)).pack(pady=(30, 10))
            ctk.CTkLabel(card, text=title, font=("Arial", 18, "bold")).pack()
            ctk.CTkLabel(card, text="Description", text_color="#94a3b8").pack(pady=5)
            ctk.CTkButton(card, text="Open Manager →", fg_color="transparent", text_color="#2563eb", hover_color="#f0f7ff", font=("Arial", 13, "bold")).pack(pady=(10, 30))

    # --- PAGE 3: RECORD REGISTRY ---
    def show_record_registry(self):
        self.clear_screen()
        self.create_navbar()

        body = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=20, border_width=1, border_color="#eee")
        body.pack(expand=True, fill="both", padx=20, pady=20)

        # Header Row
        header = ctk.CTkFrame(body, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=20)
        ctk.CTkLabel(header, text="Record Registry", font=("Arial", 28, "bold")).pack(side="left")
        
        # Action Buttons
        ctk.CTkButton(header, text="Import CSV", fg_color="#2563eb", width=110).pack(side="right", padx=5)
        ctk.CTkButton(header, text="+ New Record", fg_color="#10b981", width=110).pack(side="right", padx=5)
        ctk.CTkButton(header, text="Export Selected (0)", fg_color="white", text_color="#333", border_width=1, width=140).pack(side="right", padx=5)

        # Filter Bar
        fbar = ctk.CTkFrame(body, fg_color="transparent")
        fbar.pack(fill="x", padx=25, pady=(0, 20))
        ctk.CTkEntry(fbar, placeholder_text="🔍 Search records...", width=350, height=40).pack(side="left")
        ctk.CTkButton(fbar, text="Apply", fg_color="#1e293b", width=80, height=40).pack(side="right", padx=5)
        ctk.CTkOptionMenu(fbar, values=["Newest First", "Oldest First"], height=40, fg_color="white", text_color="black").pack(side="right", padx=10)

        # Table Headers
        table_h = ctk.CTkFrame(body, fg_color="transparent")
        table_h.pack(fill="x", padx=25)
        ctk.CTkCheckBox(table_h, text="", width=20).pack(side="left")
        for h in ["DATE REC.", "TYPE", "PROPONENT", "SUBJECT", "LATEST ACTION"]:
            ctk.CTkLabel(table_h, text=h, font=("Arial", 11, "bold"), text_color="#64748b").pack(side="left", expand=True, fill="x")

if __name__ == "__main__":
    app = LegislativeApp()
    app.mainloop()