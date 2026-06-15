import customtkinter as ctk
from datetime import datetime

# --- NEW COMPONENT: THE MODAL WINDOW ---
class NewRecordModal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("New Administrative Entry")
        self.geometry("800x700")
        self.configure(fg_color="white")
        
        # Make the window modal (stays on top, blocks interaction with main window)
        self.transient(parent)
        self.grab_set()
        
        # Main Padding Container
        self.container = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.container.pack(fill="both", expand=True, padx=40, pady=20)

        # 1. Header
        header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header_frame, text="New Administrative Entry", font=("Arial", 24, "bold"), text_color="#0f172a").pack(side="left")
        ctk.CTkButton(header_frame, text="✕", width=30, fg_color="#f1f5f9", text_color="#64748b", hover_color="#e2e8f0", command=self.destroy).pack(side="right")

        # Scrollable area for the form fields
        form_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent", label_text="")
        form_frame.pack(fill="both", expand=True)

        # Helper function to create labeled fields
        def create_label(parent, text):
            lbl = ctk.CTkLabel(parent, text=text, font=("Arial", 11, "bold"), text_color="#64748b")
            return lbl

        # --- Row 1: Date, Time, Ref No (3 Columns) ---
        row1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1.pack(fill="x", pady=10)
        row1.columnconfigure((0, 1, 2), weight=1)

        # Date
        c1 = ctk.CTkFrame(row1, fg_color="transparent")
        c1.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        create_label(c1, "DATE RECEIVED").pack(anchor="w")
        ctk.CTkEntry(c1, placeholder_text="mm/dd/yyyy", height=40).pack(fill="x", pady=5)

        # Time
        c2 = ctk.CTkFrame(row1, fg_color="transparent")
        c2.grid(row=0, column=1, padx=10, sticky="ew")
        create_label(c2, "TIME RECEIVED").pack(anchor="w")
        ctk.CTkEntry(c2, placeholder_text="--:-- --", height=40).pack(fill="x", pady=5)

        # Ref No
        c3 = ctk.CTkFrame(row1, fg_color="transparent")
        c3.grid(row=0, column=2, padx=(10, 0), sticky="ew")
        create_label(c3, "REF NO").pack(anchor="w")
        ctk.CTkEntry(c3, height=40).pack(fill="x", pady=5)

        # --- Single Column Fields ---
        fields = [
            ("TYPE", 40), 
            ("PROPONENT", 40), 
            ("SUBJECT", 80), 
            ("DESCRIPTION", 80), 
            ("NOTATION", 60)
        ]

        for label_text, h in fields:
            f = ctk.CTkFrame(form_frame, fg_color="transparent")
            f.pack(fill="x", pady=10)
            create_label(f, label_text).pack(anchor="w")
            
            if h > 40: # Use Textbox for larger areas
                ctk.CTkTextbox(f, height=h, border_width=2, border_color="#e2e8f0").pack(fill="x", pady=5)
            else:
                ctk.CTkEntry(f, height=h).pack(fill="x", pady=5)

        # --- Footer Buttons ---
        footer = ctk.CTkFrame(self.container, fg_color="transparent")
        footer.pack(fill="x", side="bottom", pady=(20, 0))
        
        ctk.CTkButton(footer, text="Save New Record", fg_color="#10b981", hover_color="#059669", 
                      height=45, font=("Arial", 14, "bold"), command=self.save_data).pack(side="right", padx=(10, 0))
        ctk.CTkButton(footer, text="Discard", fg_color="#f1f5f9", text_color="#475569", 
                      hover_color="#e2e8f0", height=45, width=100, command=self.destroy).pack(side="right")

    def save_data(self):
        # Add your saving logic here
        print("Data Saved!")
        self.destroy()

# --- MODIFIED MAIN APP CLASS ---
class LegislativeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Legislative Management System - Baguio City")
        self.geometry("1280x800")
        self.configure(fg_color="#f8fafc")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both")

        self.show_dashboard()

    def clear_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def create_navbar(self):
        navbar = ctk.CTkFrame(self.main_container, fg_color="white", height=70, corner_radius=0)
        navbar.pack(fill="x", side="top")
        
        ctk.CTkLabel(navbar, text="🏛️", font=("Arial", 24)).pack(side="left", padx=(30, 10))
        title_box = ctk.CTkFrame(navbar, fg_color="transparent")
        title_box.pack(side="left", pady=10)
        ctk.CTkLabel(title_box, text="Sangguniang Panlungsod", font=("Arial", 16, "bold"), text_color="#0f172a").pack(anchor="w")
        ctk.CTkLabel(title_box, text="CITY COUNCIL (BAGUIO CITY)", font=("Arial", 11), text_color="#64748b").pack(anchor="w")

        ctk.CTkButton(navbar, text="Logout", fg_color="#fff1f2", text_color="#e11d48", hover_color="#ffe4e6", width=90).pack(side="right", padx=30)
        ctk.CTkButton(navbar, text="Home", fg_color="white", text_color="#333", border_width=1, border_color="#ddd", width=80, command=self.show_dashboard).pack(side="right")
        return navbar

    def show_dashboard(self):
        self.clear_screen()
        self.create_navbar()

        welcome_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=60, pady=(40, 20))

        welcome_lbl = ctk.CTkLabel(welcome_frame, text="Welcome back, ", font=("Arial", 36, "bold"), text_color="#0f172a")
        welcome_lbl.pack(side="left")
        ctk.CTkLabel(welcome_frame, text="Admin!", font=("Arial", 36, "bold"), text_color="#2563eb").pack(side="left")
        
        date_str = datetime.now().strftime("%B %d, %Y")
        ctk.CTkLabel(welcome_frame, text=date_str, font=("Arial", 14, "bold"), fg_color="white", width=150, height=40, corner_radius=10).pack(side="right")
        
        ctk.CTkLabel(self.main_container, text="System Overview & Control Panel", font=("Arial", 18), text_color="#64748b").pack(anchor="w", padx=60)
        ctk.CTkLabel(self.main_container, text="MANAGEMENT TOOLS", font=("Arial", 12, "bold"), text_color="#94a3b8").pack(anchor="w", padx=60, pady=(30, 10))

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
            
            if cmd: 
                # Allow clicking both the card and inner components
                card.bind("<Button-1>", lambda e, func=cmd: func())

    def show_event_categories(self):
        self.clear_screen()
        self.create_navbar()
        # ... (rest of the code same as original)
        ctk.CTkLabel(self.main_container, text="Event Categories", font=("Arial", 30, "bold")).pack(pady=(40, 5))

    def open_new_record_window(self):
        """Helper to launch the modal"""
        NewRecordModal(self)

    def show_record_registry(self):
        self.clear_screen()
        self.create_navbar()

        body = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=20, border_width=1, border_color="#eee")
        body.pack(expand=True, fill="both", padx=20, pady=20)

        header = ctk.CTkFrame(body, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=20)
        ctk.CTkLabel(header, text="Record Registry", font=("Arial", 28, "bold")).pack(side="left")
        
        # --- LINKED BUTTON HERE ---
        ctk.CTkButton(header, text="Import CSV", fg_color="#2563eb", width=110).pack(side="right", padx=5)
        ctk.CTkButton(header, text="+ New Record", fg_color="#10b981", width=110, 
                      command=self.open_new_record_window).pack(side="right", padx=5)
        ctk.CTkButton(header, text="Export Selected (0)", fg_color="white", text_color="#333", border_width=1, width=140).pack(side="right", padx=5)

        # ... (rest of your registry filters and table headers)
        fbar = ctk.CTkFrame(body, fg_color="transparent")
        fbar.pack(fill="x", padx=25, pady=(0, 20))
        ctk.CTkEntry(fbar, placeholder_text="🔍 Search records...", width=350, height=40).pack(side="left")

if __name__ == "__main__":
    app = LegislativeApp()
    app.mainloop()