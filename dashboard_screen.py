from tkinter import *
from tkinter import ttk


class DashboardScreen(Tk):
    def __init__(self, username):
        super().__init__()
        self.title("Dashboard")
        self.geometry("350x200")

        ttk.Label(self, text=f"Welcome, {username}!", font=("Segoe UI", 14)).pack(padx=20, pady=30)
        ttk.Button(self, text="Logout", command=self.logout).pack(pady=10)

        self.mainloop()

    def logout(self):
        self.destroy()
