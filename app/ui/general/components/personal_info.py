from tkinter import ttk
from app.logic.user_manager import UserManager

class PersonalInfo(ttk.Frame):
    def __init__(self, parent, user_info):
        super().__init__(parent, padding=10)

        ttk.Label(self, text="Persoonlijke gegevens", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        if user_info:
            fields = ["voornaam", "achternaam", "email", "telefoon", "adres"]
            for i, field in enumerate(fields, start=1):
                ttk.Label(self, text=f"{field.capitalize()}:").grid(row=i, column=0, sticky="w", padx=5, pady=2)
                ttk.Label(self, text=user_info.get(field, "")).grid(row=i, column=1, sticky="w", padx=5, pady=2)
