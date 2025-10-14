from tkinter import *
from tkinter import ttk
from dashboard_screen import DashboardScreen
import csv


class LoginScreen(Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x180")

        frame = ttk.Frame(self, padding=10)
        frame.grid()

        # Labels
        ttk.Label(frame, text="Username:").grid(column=0, row=0, sticky=W)
        ttk.Label(frame, text="Password:").grid(column=0, row=1, sticky=W)

        # Input fields
        self.username = StringVar()
        self.password = StringVar()

        ttk.Entry(frame, textvariable=self.username).grid(column=1, row=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.password, show="*").grid(column=1, row=1, padx=5, pady=5)

        # Login button
        ttk.Button(frame, text="Login", command=self.check_login).grid(column=1, row=2, pady=10)

        # Message label for invalid credentials
        self.message = ttk.Label(frame, text="", foreground="red")
        self.message.grid(column=0, row=3, columnspan=2)

    def check_login(self):
        user = self.username.get().strip()
        pw = self.password.get().strip()

        # Check credentials in users.csv
        if self.validate_user(user, pw):
            self.destroy()
            DashboardScreen(user)
        else:
            self.message.config(text="Invalid username or password", foreground="red")

    def validate_user(self, username, password):
        """Check if username and password exist in users.csv"""
        try:
            with open("users.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["username"] == username and row["password"] == password:
                        return True
            return False
        except FileNotFoundError:
            self.message.config(text="users.csv not found!", foreground="red")
            return False
