import customtkinter as ctk
from tkinter import messagebox

# Theme Settings
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green") 

class BaguioCouncilApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Baguio City Council - Secure Access")
        self.geometry("400x450")
        self.resizable(False, False)

        # Container to hold the current view
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_login_screen()

    def show_login_screen(self):
        # Clear container
        for widget in self.container.winfo_children():
            widget.destroy()

        # YOUR EXACT DESIGN STARTS HERE
        self.frame = ctk.CTkFrame(self.container, corner_radius=15)
        self.frame.pack(pady=40, padx=40, fill="both", expand=True)

        self.header = ctk.CTkLabel(self.frame, text="CITY COUNCIL OF BAGUIO", 
                                   font=("Helvetica", 18, "bold"), text_color="#1B4D3E")
        self.header.pack(pady=(30, 5))

        self.sub_header = ctk.CTkLabel(self.frame, text="Authorized Personnel Only", 
                                       font=("Helvetica", 12))
        self.sub_header.pack(pady=(0, 30))

        self.instruction = ctk.CTkLabel(self.frame, text="Enter Passkey", 
                                        font=("Helvetica", 13, "bold"))
        self.instruction.pack(pady=5)

        self.passkey_entry = ctk.CTkEntry(self.frame, width=220, height=45, 
                                          placeholder_text="••••••••", 
                                          show="*", justify="center",
                                          font=("Arial", 20))
        self.passkey_entry.pack(pady=10)
        self.passkey_entry.bind('<Return>', lambda event: self.verify_passkey())

        self.unlock_button = ctk.CTkButton(self.frame, text="AUTHENTICATE", 
                                           command=self.verify_passkey,
                                           fg_color="#1B4D3E", 
                                           hover_color="#14362B",
                                           height=40,
                                           font=("Helvetica", 13, "bold"))
        self.unlock_button.pack(pady=30)

        self.notice = ctk.CTkLabel(self.frame, text="Unauthorized access is recorded.", 
                                   font=("Helvetica", 10), text_color="red")
        self.notice.pack(side="bottom", pady=10)
        # YOUR EXACT DESIGN ENDS HERE

    def verify_passkey(self):
        SECRET_PASSKEY = "Baguio2024"
        if self.passkey_entry.get() == SECRET_PASSKEY:
            self.show_dashboard()
        else:
            messagebox.showerror("Access Denied", "Invalid Passkey.")
            self.passkey_entry.delete(0, 'end')

    def show_dashboard(self):
        # Resize window for the dashboard
        self.geometry("1100x600")
        self.resizable(True, True)
        
        # Clear login screen
        for widget in self.container.winfo_children():
            widget.destroy()

        # --- NAVIGATION BAR (SIDEBAR) ---
        self.sidebar = ctk.CTkFrame(self.container, width=220, corner_radius=0, fg_color="#1B4D3E")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="COUNCIL MENU", font=("Helvetica", 16, "bold"), text_color="white").pack(pady=30, padx=20)
        
        nav_buttons = ["🏠 Dashboard", "📅 Events", "📂 Registry", "📚 Resources"]
        for btn in nav_buttons:
            ctk.CTkButton(self.sidebar, text=btn, fg_color="transparent", anchor="w", hover_color="#2D5A27").pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(self.sidebar, text="Logout", fg_color="#A63D40", command=self.logout).pack(side="bottom", pady=20, padx=20, fill="x")

        # --- MAIN CONTENT AREA ---
        self.main_content = ctk.CTkFrame(self.container, fg_color="#F2F2F2")
        self.main_content.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(self.main_content, text="Legislative Dashboard", font=("Helvetica", 24, "bold"), text_color="#333").pack(anchor="w", padx=30, pady=(30, 20))

        # --- CARDS CONTAINER ---
        self.card_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.card_frame.pack(fill="both", expand=True, padx=20)

        # Data for Cards
        cards_data = [
            ("📅", "EVENTS", "Schedule of Sessions\nand Public Hearings"),
            ("📂", "REGISTRY DATABASE", "Official Ordinances\nand Records Archive"),
            ("📚", "RESOURCES", "Legal Forms, Manuals\nand Guidelines")
        ]

        for i, (icon, title, desc) in enumerate(cards_data):
            self.create_card(icon, title, desc, i)

    def create_card(self, icon, title, desc, col):
        card = ctk.CTkFrame(self.card_frame, width=280, height=320, corner_radius=15, fg_color="white", border_width=1, border_color="#DDD")
        card.grid(row=0, column=col, padx=15, pady=10)
        card.grid_propagate(False)

        ctk.CTkLabel(card, text=icon, font=("Helvetica", 50)).pack(pady=(40, 10))
        ctk.CTkLabel(card, text=title, font=("Helvetica", 16, "bold"), text_color="#1B4D3E").pack(pady=5)
        ctk.CTkLabel(card, text=desc, font=("Helvetica", 12), text_color="gray", justify="center").pack(pady=10, padx=20)
        ctk.CTkButton(card, text="View Records", fg_color="#1B4D3E", width=140).pack(side="bottom", pady=30)

    def logout(self):
        self.geometry("400x450")
        self.resizable(False, False)
        self.show_login_screen()

if __name__ == "__main__":
    app = BaguioCouncilApp()
    app.mainloop()