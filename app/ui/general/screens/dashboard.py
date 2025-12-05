# app/ui/general/screens/dashboard.py
from tkinter import *
from tkinter import ttk
from app.ui.general.components.personal_info import PersonalInfo

class DashboardScreen(Tk):
    def __init__(self, gebruikers_id, role):
        super().__init__()
        self.gebruikers_id = gebruikers_id
        self.role = role
        self.title(f"{role.replace('_',' ').title()} Dashboard")
        self.geometry("500x300")

        # Personal info component now uses gebruikers_id
        info = PersonalInfo(self, gebruikers_id)
        info.pack(padx=20, pady=20)

        ttk.Button(self, text="Logout", command=self.destroy).pack()
