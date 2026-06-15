import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# Theme Settings
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue") 

# --- COMPONENT: THE NEW ENTRY MODAL POPUP ---
class NewEntryModal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("New Administrative Entry")
        self.geometry("850x750")
        self.configure(fg_color="white")
        
        # Ensure it stays on top and focuses
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        # Main Padding Container
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # 1. HEADER
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 25))
        ctk.CTkLabel(header_frame, text="New Administrative Entry", font=("Arial", 24, "bold"), text_color="#0f172a").pack(side="left")
        ctk.CTkButton(header_frame, text="✕", width=30, height=30, fg_color="#f1f5f9", text_color="#64748b", hover_color="#e2e8f0", command=self.destroy).pack(side="right")

        # Scrollable container for the form
        form_scroll = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent", label_text="")
        form_scroll.pack(fill="both", expand=True)

        def create_label(text):
            return ctk.CTkLabel(form_scroll, text=text, font=("Arial", 11, "bold"), text_color="#64748b")

        # --- ROW 1: 3 COLUMNS ---
        row1 = ctk.CTkFrame(form_scroll, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 15))
        row1.columnconfigure((0, 1, 2), weight=1)

        # Date Received
        c1 = ctk.CTkFrame(row1, fg_color="transparent")
        c1.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        create_label("DATE RECEIVED").pack(anchor="w")
        ctk.CTkEntry(c1, placeholder_text="mm/dd/yyyy", height=45).pack(fill="x", pady=5)

        # Time Received
        c2 = ctk.CTkFrame(row1, fg_color="transparent")
        c2.grid(row=0, column=1, padx=10, sticky="ew")
        create_label("TIME RECEIVED").pack(anchor="w")
        ctk.CTkEntry(c2, placeholder_text="--:-- --", height=45).pack(fill="x", pady=5)

        # Ref No
        c3 = ctk.CTkFrame(row1, fg_color="transparent")
        c3.grid(row=0, column=2, padx=(10, 0), sticky="ew")
        create_label("REF NO").pack(anchor="w")
        ctk.CTkEntry(c3, height=45).pack(fill="x", pady=5)

        # --- SINGLE COLUMN FIELDS ---
        create_label("TYPE").pack(anchor="w", pady=(10, 0))
        ctk.CTkEntry(form_scroll, height=45).pack(fill="x", pady=(5, 15))

        create_label("PROPONENT").pack(anchor="w", pady=(10, 0))
        ctk.CTkEntry(form_scroll, height=45).pack(fill="x", pady=(5, 15))

        create_label("SUBJECT").pack(anchor="w", pady=(10, 0))
        ctk.CTkTextbox(form_scroll, height=80, border_width=2, border_color="#e2e8f0").pack(fill="x", pady=(5, 15))

        create_label("DESCRIPTION").pack(anchor="w", pady=(10, 0))
        ctk.CTkTextbox(form_scroll, height=80, border_width=2, border_color="#e2e8f0").pack(fill="x", pady=(5, 15))

        create_label("NOTATION").pack(anchor="w", pady=(10, 0))
        ctk.CTkTextbox(form_scroll, height=60, border_width=2, border_color="#e2e8f0").pack(fill="x", pady=(5, 15))

        # --- FOOTER BUTTONS ---
        footer = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        footer.pack(fill="x", side="bottom", pady=(20, 0))
        
        ctk.CTkButton(footer, text="Save New Record", fg_color="#10b981", hover_color="#059669", 
                      height=45, font=("Arial", 14, "bold"), command=self.save_and_close).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(footer, text="Discard", fg_color="#f1f5f9", text_color="#475569", 
                      hover_color="#e2e8f0", height=45, width=100, command=self.destroy).pack(side="right")

    def save_and_close(self):
        messagebox.showinfo("Success", "New Administrative Entry saved successfully!")
        self.destroy()


# --- MAIN APPLICATION ---
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
        navbar = ctk.CTkFrame(self.container, fg_color="white", height=70, corner_radius=0, border_width=1, border_color="#f1f5f9")
        navbar.pack(fill="x", side="top")
        
        ctk.CTkLabel(navbar, text="🏛️", font=("Arial", 24)).pack(side="left", padx=(30, 10))
        title_box = ctk.CTkFrame(navbar, fg_color="transparent")
        title_box.pack(side="left", pady=10)
        ctk.CTkLabel(title_box, text="Sangguniang Panlungsod", font=("Arial", 15, "bold"), text_color="#0f172a").pack(anchor="w")
        ctk.CTkLabel(title_box, text="CITY COUNCIL (BAGUIO CITY)", font=("Arial", 10), text_color="#64748b").pack(anchor="w")

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

        ctk.CTkLabel(self.frame, text="CITY COUNCIL OF BAGUIO", font=("Arial", 18, "bold"), text_color="#1e293b").pack(pady=(30, 5))
        ctk.CTkLabel(self.frame, text="Authorized Personnel Only", font=("Arial", 12), text_color="#64748b").pack(pady=(0, 30))

        self.passkey_entry = ctk.CTkEntry(self.frame, width=220, height=45, placeholder_text="Enter Passkey", show="*", justify="center")
        self.passkey_entry.pack(pady=10)
        self.passkey_entry.bind('<Return>', lambda event: self.verify_passkey())

        ctk.CTkButton(self.frame, text="AUTHENTICATE", command=self.verify_passkey, fg_color="#2563eb", height=40, font=("Arial", 13, "bold")).pack(pady=30)

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
            ("📁", "Registry", "Central Database", 0, 1, self.show_record_registry),
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

    def show_record_registry(self):
        self.clear_screen()
        self.create_navbar()

        body = ctk.CTkFrame(self.container, fg_color="white", corner_radius=20, border_width=1, border_color="#e2e8f0")
        body.pack(fill="both", expand=True, padx=30, pady=30)

        # 1. HEADER ROW
        header_row = ctk.CTkFrame(body, fg_color="transparent")
        header_row.pack(fill="x", padx=30, pady=(30, 20))

        title_box = ctk.CTkFrame(header_row, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(title_box, text="Record Registry", font=("Arial", 32, "bold"), text_color="#0f172a").pack(side="left")
        
        ctk.CTkLabel(title_box, text="Total: 41,785", font=("Arial", 11), fg_color="#f1f5f9", text_color="#64748b", corner_radius=15, width=90, height=26).pack(side="left", padx=(20, 5))
        ctk.CTkLabel(title_box, text="Filtered: 41,785", font=("Arial", 11), fg_color="#eff6ff", text_color="#2563eb", corner_radius=15, width=100, height=26).pack(side="left", padx=5)

        btn_frame = ctk.CTkFrame(header_row, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="Template", fg_color="white", text_color="#334155", border_width=1, border_color="#e2e8f0", width=100, height=45).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Export Selected (0)", fg_color="white", text_color="#334155", border_width=1, border_color="#e2e8f0", width=150, height=45).pack(side="left", padx=5)
        
        # LINKED POPUP HERE
        ctk.CTkButton(btn_frame, text="+ New Record", fg_color="#10b981", hover_color="#059669", font=("Arial", 13, "bold"), width=150, height=45, command=lambda: NewEntryModal(self)).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="📁 Import CSV", fg_color="#2563eb", hover_color="#1d4ed8", font=("Arial", 13, "bold"), width=140, height=45).pack(side="left", padx=5)

        # 2. FILTER BAR
        filter_bar = ctk.CTkFrame(body, fg_color="transparent")
        filter_bar.pack(fill="x", padx=30, pady=10)

        search_entry = ctk.CTkEntry(filter_bar, placeholder_text="🔍 Search records...", height=45, width=400, border_color="#e2e8f0")
        search_entry.pack(side="left")

        right_filters = ctk.CTkFrame(filter_bar, fg_color="transparent")
        right_filters.pack(side="right")

        ctk.CTkOptionMenu(right_filters, values=["All Years", "2024", "2023"], fg_color="white", text_color="#334155", border_width=1, border_color="#e2e8f0", button_color="#f8fafc", width=120, height=45).pack(side="left", padx=5)
        
        date_frame = ctk.CTkFrame(right_filters, fg_color="#f8fafc", border_width=1, border_color="#e2e8f0", corner_radius=8)
        date_frame.pack(side="left", padx=5)
        ctk.CTkLabel(date_frame, text="FROM", font=("Arial", 10, "bold"), text_color="#94a3b8").pack(side="left", padx=10)
        ctk.CTkEntry(date_frame, placeholder_text="mm/dd/yyyy", width=110, height=35, border_width=0, fg_color="transparent").pack(side="left")
        ctk.CTkLabel(date_frame, text="TO", font=("Arial", 10, "bold"), text_color="#94a3b8").pack(side="left", padx=10)
        ctk.CTkEntry(date_frame, placeholder_text="mm/dd/yyyy", width=110, height=35, border_width=0, fg_color="transparent").pack(side="left")

        ctk.CTkOptionMenu(right_filters, values=["Newest First", "Oldest First"], fg_color="white", text_color="#334155", border_width=1, border_color="#e2e8f0", button_color="#f8fafc", width=140, height=45).pack(side="left", padx=5)
        ctk.CTkButton(right_filters, text="Apply", fg_color="#1e293b", hover_color="#0f172a", width=80, height=45, font=("Arial", 13, "bold")).pack(side="left", padx=5)

        # 3. TABLE HEADER
        table_header = ctk.CTkFrame(body, fg_color="transparent", height=40)
        table_header.pack(fill="x", padx=30, pady=(20, 0))
        table_header.pack_propagate(False)

        ctk.CTkCheckBox(table_header, text="", width=20).pack(side="left", padx=(5, 20))
        headers = ["DATE REC.", "TYPE", "PROPONENT", "SUBJECT", "LATEST ACTION"]
        for h in headers:
            ctk.CTkLabel(table_header, text=h, font=("Arial", 11, "bold"), text_color="#64748b").pack(side="left", expand=True)

        ctk.CTkFrame(body, height=1, fg_color="#f1f5f9").pack(fill="x", padx=30)

    def show_event_categories(self):
        self.clear_screen()
        self.create_navbar()

        ctk.CTkLabel(self.container, text="Event Categories", font=("Arial", 42, "bold"), text_color="#0f172a").pack(pady=(60, 5))
        ctk.CTkLabel(self.container, text="Select a category to manage specific schedules and records.", font=("Arial", 16), text_color="#64748b").pack(pady=(0, 50))

        grid = ctk.CTkFrame(self.container, fg_color="transparent")
        grid.pack(expand=True, fill="both", padx=100)
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        cats = [
            ("👥", "Seminars", "Description", 0, 0),
            ("👨‍🏫", "Public Consultation", "Description", 0, 1),
            ("🏛️", "Committee Level Hearing", "Description", 0, 2),
            ("📁", "Others", "General events and special occasions", 1, 0)
        ]

        for icon, title, desc, r, c in cats:
            card = ctk.CTkFrame(grid, fg_color="white", corner_radius=30, border_width=1, border_color="#f1f5f9", width=340, height=380)
            card.grid(row=r, column=c, padx=20, pady=20)
            card.grid_propagate(False)
            ctk.CTkLabel(card, text=icon, font=("Arial", 60)).pack(pady=(50, 10))
            ctk.CTkLabel(card, text=title, font=("Arial", 22, "bold"), text_color="#0f172a").pack(pady=5)
            ctk.CTkLabel(card, text=desc, font=("Arial", 14), text_color="#64748b", wraplength=280).pack(pady=(0, 20))
            ctk.CTkButton(card, text="Open Manager →", fg_color="transparent", text_color="#2563eb", hover_color="#f0f7ff", font=("Arial", 15, "bold")).pack(side="bottom", pady=40)

if __name__ == "__main__":
    app = BaguioCouncilApp()
    app.mainloop()
