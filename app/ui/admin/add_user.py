# app/ui/admin/add_user.py

import csv
import tkinter as tk
from tkinter import ttk, messagebox
import re
from app.config import TEST_CSV  # TEST_CSV komt uit config.json als Path-object

CSV_FILE = TEST_CSV  # gebruik het pad uit config

# Zorg dat de data-map bestaat
CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

# Maak CSV aan als deze nog niet bestaat, met admin-account
if not CSV_FILE.exists():
    with CSV_FILE.open(mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "gebruikers_id","voornaam","achternaam",
            "gebruikersnaam","wachtwoord","rol",
            "email","telefoon","adres"
        ])
        writer.writerow(["001","Systeem","Admin","admin","pass001","admin","","",""])

class AddUserApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nieuwe gebruiker toevoegen")
        self.geometry("450x400")

        # GUI-velden
        self.fields = {}
        labels = ["Voornaam", "Achternaam", "Email", "Telefoon", "Adres"]
        for i, label in enumerate(labels):
            ttk.Label(self, text=label).grid(row=i, column=0, pady=5, padx=5, sticky="w")
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.fields[label.lower()] = entry

        # Rol dropdown
        ttk.Label(self, text="Rol").grid(row=len(labels), column=0, pady=5, padx=5, sticky="w")
        self.role_var = tk.StringVar()
        self.role_dropdown = ttk.Combobox(self, textvariable=self.role_var, state="readonly")
        self.role_dropdown['values'] = ["trainee", "people_manager", "business_manager"]
        self.role_dropdown.grid(row=len(labels), column=1, pady=5, padx=5)
        self.role_dropdown.current(0)

        # Toevoegen knop
        ttk.Button(self, text="Toevoegen", command=self.add_user).grid(
            row=len(labels)+1, column=0, columnspan=2, pady=20
        )

        self.mainloop()

    def add_user(self):
        first_name = self.fields['voornaam'].get().strip()
        last_name = self.fields['achternaam'].get().strip()
        email = self.fields['email'].get().strip()
        phone = self.fields['telefoon'].get().strip()
        address = self.fields['adres'].get().strip()
        role = self.role_var.get().strip()

        if not all([first_name, last_name, role]):
            messagebox.showerror("Fout", "Voornaam, achternaam en rol zijn verplicht.")
            return

        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Fout", "Ongeldig email-formaat.")
            return
        if phone and not re.match(r"^\+?\d+$", phone):
            messagebox.showerror("Fout", "Telefoonnummer mag alleen cijfers bevatten (eventueel +).")
            return

        # Lees bestaande gebruikers
        with CSV_FILE.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            users = list(reader)

        # Autogenerate gebruikers_id
        ids = [int(u["gebruikers_id"]) for u in users] if users else []
        next_id = max(ids) + 1 if ids else 1
        gebruikers_id = f"{next_id:03}"

        # Autogenerate gebruikersnaam en wachtwoord
        gebruikersnaam = (first_name + last_name).lower()
        if any(u["gebruikersnaam"] == gebruikersnaam for u in users):
            messagebox.showerror("Fout", "Gebruikersnaam bestaat al.")
            return
        wachtwoord = f"pass{gebruikers_id}"

        # Schrijf naar CSV
        with CSV_FILE.open(mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([gebruikers_id, first_name, last_name, gebruikersnaam, wachtwoord, role, email, phone, address])

        messagebox.showinfo("Succes", f"Gebruiker toegevoegd!\nUsername: {gebruikersnaam}\nWachtwoord: {wachtwoord}")

        for entry in self.fields.values():
            entry.delete(0, tk.END)
        self.role_dropdown.current(0)
