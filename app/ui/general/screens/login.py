from tkinter import *
from tkinter import ttk, messagebox
from app.logic.user_manager import UserManager

class LoginScreen(Tk):
    def __init__(self):
        super().__init__()
        print("LoginScreen(Tk)")
        self.title("Login")
        self.geometry("300x180")

        frame = ttk.Frame(self, padding=10)
        frame.grid()

        ttk.Label(frame, text="Username:").grid(column=0, row=0, sticky=W)
        ttk.Label(frame, text="Password:").grid(column=0, row=1, sticky=W)

        self.username = StringVar()
        self.password = StringVar()

        ttk.Entry(frame, textvariable=self.username).grid(column=1, row=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.password, show="*").grid(column=1, row=1, padx=5, pady=5)

        ttk.Button(frame, text="Login", command=self.check_login).grid(column=1, row=2, pady=10)
        self.message = ttk.Label(frame, text="", foreground="red")
        self.message.grid(column=0, row=3, columnspan=2)

    def check_login(self):
        print("check_login()")
        username_input = self.username.get().strip()
        password = self.password.get().strip()

        user_info = UserManager.validate_user(username_input, password)

        if user_info:
            gebruikers_id = user_info.get("gebruikers_id")
            role = user_info.get("rol", "").lower()
            self.destroy()
            self.open_dashboard(gebruikers_id, role)
        else:
            self.message.config(text="Invalid username or password", foreground="red")

    def open_dashboard(self, gebruikers_id, role):
        try:
            if role == "admin":
                from app.ui.admin.add_user import AddUserApp
                AddUserApp()
            else:
                import importlib
                module = importlib.import_module(f"ui.{role}.dashboard")
                module.DashboardScreen(gebruikers_id, role)
        except ModuleNotFoundError:
            messagebox.showerror("Missing", f"No dashboard for role '{role}'")
