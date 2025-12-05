#app/ui/trainee/personal_info.py

from tkinter import *
from tkinter import ttk

class DashboardScreen(Tk):
    def __init__(self, username):
        super().__init__()
        self.title("Trainee Dashboard")
        self.geometry("400x250")

        ttk.Label(self, text=f"Welcome trainee {username}!", font=("Segoe UI", 14)).pack(pady=20)
        ttk.Label(self, text="Here you can see your training schedule.").pack(pady=5)

        ttk.Button(self, text="Logout", command=self.logout).pack(pady=20)
        self.mainloop()

    def logout(self):
        self.destroy()
