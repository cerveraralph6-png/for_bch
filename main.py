import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# Theme Settings
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue") 

class BaguioCouncilApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Baguio City Council - Secure Access")
        self.geometry("1280x800")
        self.resizable(True, True)
        self.configure(fg_color="#f8fafc") 

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def create_navbar(self):
        """Standard Navbar for all internal pages"""
        navbar = ctk.CTkFrame(self.container, fg_color="white", height=70, corner_radius=0, border_width=1, border_color="#f1f5f9")
        navbar.pack(fill="x", side="top")
        
        # Logo and Title Left
        ctk.CTkLabel(navbar, text="🏛️", font=("Arial", 24)).pack(side="left", padx=(30, 10))
        title_box = ctk.CTkFrame(navbar, fg_color="transparent")
        title_box.pack(side="left", pady=10)
        ctk.CTkLabel(title_box, text="Sangguniang Panlungsod", font=("Arial", 15, "bold"), text_color="#0f172a").pack(anchor="w")
        ctk.CTkLabel(title_box, text="CITY COUNCIL (BAGUIO CITY)", font=("Arial", 10), text_color="#64748b").pack(anchor="w")

        # Buttons Right
        ctk.CTkButton(navbar, text="Logout", fg_color="#fff1f2", text_color="#e11d48", hover_color="#ffe4e6", 
                      width=90, font=("Arial", 12, "bold"), command=self.show_login_screen).pack(side="right", padx=30)
        
        ctk.CTkButton(navbar, text="Home", fg_color="#10b981", text_color="white", hover_color="#059669", 
                      width=80, font=("Arial", 12, "bold"), command=self.show_dashboard).pack(side="right")

    def show_login_screen(self):
        self.clear_screen()
        self.geometry("400x450")
        self.resizable(False, False)
        
        self.frame = ctk.CTkFrame(self.container, corner_radius=15, fg_color="white", border_width=1, border_color="#e2e8f0")
        self.frame.pack(pady=40, padx=40, fill="both", expand=True)

        self.header = ctk.CTkLabel(self.frame, text="CITY COUNCIL OF BAGUIO", font=("Arial", 18, "bold"), text_color="#1e293b")
        self.header.pack(pady=(30, 5))

        self.sub_header = ctk.CTkLabel(self.frame, text="Authorized Personnel Only", font=("Arial", 12), text_color="#64748b")
        self.sub_header.pack(pady=(0, 30))

        self.passkey_entry = ctk.CTkEntry(self.frame, width=220, height=45, placeholder_text="Enter Passkey", show="*", justify="center")
        self.passkey_entry.pack(pady=10)
        self.passkey_entry.bind('<Return>', lambda event: self.verify_passkey())

        self.unlock_button = ctk.CTkButton(self.frame, text="AUTHENTICATE", command=self.verify_passkey, fg_color="#2563eb", height=40, font=("Arial", 13, "bold"))
        self.unlock_button.pack(pady=30)

    def verify_passkey(self):
        if self.passkey_entry.get() == "Baguio2024":
            self.show_dashboard()
        else:
            messagebox.showerror("Access Denied", "Invalid Passkey.")

    def show_dashboard(self):
        self.clear_screen()
        self.geometry("1280x800")
        self.resizable(True, True)
        self.create_navbar()

        header_section = ctk.CTkFrame(self.container, fg_color="transparent")
        header_section.pack(fill="x", padx=80, pady=(50, 0))

        ctk.CTkLabel(header_section, text="Welcome back, Admin!", font=("Arial", 42, "bold"), text_color="#0f172a").pack(side="left")
        
        date_str = datetime.now().strftime("%B %d, %Y")
        ctk.CTkLabel(header_section, text=date_str, font=("Arial", 14), fg_color="white", width=160, height=45, corner_radius=12).pack(side="right")
        
        ctk.CTkLabel(self.container, text="System Overview & Control Panel", font=("Arial", 18), text_color="#64748b").pack(anchor="w", padx=80, pady=(5, 40))
        ctk.CTkLabel(self.container, text="MANAGEMENT TOOLS", font=("Arial", 11, "bold"), text_color="#94a3b8").pack(anchor="w", padx=80, pady=(0, 20))

        grid_container = ctk.CTkFrame(self.container, fg_color="transparent")
        grid_container.pack(fill="both", expand=True, padx=70)

        tools = [
            ("📅", "Events", "Seminars & Trainings", 0, 0, self.show_event_categories),
            ("📁", "Registry", "Central Database", 0, 1, None),
            ("☁️", "Cloud Files", "Storage & Transfer", 0, 2, None),
            ("👥", "Accounts", "User Management", 1, 0, None),
            ("🛡️", "Security", "Login & IP Logs", 1, 1, None),
            ("📚", "Resources", "Shared Docs, Photos & Videos", 1, 2, None)
        ]

        for icon, title, sub, r, c, command in tools:
            card = ctk.CTkFrame(grid_container, fg_color="white", corner_radius=20, border_width=1, border_color="#f1f5f9", height=140, cursor="hand2")
            card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
            grid_container.grid_columnconfigure(c, weight=1)
            card.grid_propagate(False)

            ctk.CTkLabel(card, text=icon, font=("Arial", 24), fg_color="#eff6ff", width=55, height=55, corner_radius=12).pack(side="left", padx=(25, 15))
            txt_box = ctk.CTkFrame(card, fg_color="transparent")
            txt_box.pack(side="left", anchor="center")
            ctk.CTkLabel(txt_box, text=title, font=("Arial", 16, "bold"), text_color="#1e293b").pack(anchor="w")
            ctk.CTkLabel(txt_box, text=sub, font=("Arial", 12), text_color="#64748b").pack(anchor="w")

            if command: card.bind("<Button-1>", lambda e, cmd=command: cmd())

    # --- FIXED EVENT CATEGORIES PAGE ---
    def show_event_categories(self):
        self.clear_screen()
        self.create_navbar()

        # Page Titles
        ctk.CTkLabel(self.container, text="Event Categories", font=("Arial", 42, "bold"), text_color="#0f172a").pack(pady=(60, 5))
        ctk.CTkLabel(self.container, text="Select a category to manage specific schedules and records.", font=("Arial", 16), text_color="#64748b").pack(pady=(0, 50))

        # Main Grid Container
        grid = ctk.CTkFrame(self.container, fg_color="transparent")
        grid.pack(expand=True, fill="both", padx=100)
        
        # Configure the 3 columns to be exactly equal
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        categories = [
            ("👥", "Seminars", "Description", 0, 0),
            ("👨‍🏫", "Public Consultation", "Description", 0, 1),
            ("🏛️", "Committee Level Hearing", "Description", 0, 2),
            ("📁", "Others", "General events and special occasions", 1, 0) # Placed in col 0 of row 1
        ]

        for icon, title, desc, r, c in categories:
            # FIX: corner_radius=25 (not 75) to prevent pill-shape. Fixed width and height.
            card = ctk.CTkFrame(grid, fg_color="white", corner_radius=30, border_width=1, border_color="#f1f5f9", width=340, height=380)
            card.grid(row=r, column=c, padx=20, pady=20)
            card.grid_propagate(False) # Prevents content from stretching the card

            # Icon
            ctk.CTkLabel(card, text=icon, font=("Arial", 60)).pack(pady=(50, 10))
            
            # Title
            ctk.CTkLabel(card, text=title, font=("Arial", 22, "bold"), text_color="#0f172a").pack(pady=5)
            
            # Description (Wraplength ensures text doesn't break alignment)
            ctk.CTkLabel(card, text=desc, font=("Arial", 14), text_color="#64748b", wraplength=280).pack(pady=(0, 20))
            
            # Action Button (Sticks to bottom)
            btn = ctk.CTkButton(card, text="Open Manager →", fg_color="transparent", text_color="#2563eb", 
                                hover_color="#f0f7ff", font=("Arial", 15, "bold"), 
                                command=lambda t=title: print(f"Opening manager for {t}"))
            btn.pack(side="bottom", pady=40)

if __name__ == "__main__":
    app = BaguioCouncilApp()
    app.mainloop()