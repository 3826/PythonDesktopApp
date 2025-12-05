# app/ui/people_manager/dashboard.py

from tkinter import *
from tkinter import ttk
from app.ui.general.components.personal_info import PersonalInfo
from app.logic.user_manager import UserManager
from app.logic.user_linking import UserLinking

class DashboardScreen(Tk):
    def __init__(self, gebruikers_id, role):
        super().__init__() #initialize screen
        self.gebruikers_id = gebruikers_id
        self.role = role

        # Fetch user info once
        self.user_info = UserManager.get_user_info_by_id(gebruikers_id)
        voornaam = self.user_info.get("voornaam", "") if self.user_info else ""

        self.title(f"{role.replace('_',' ').title()} Dashboard")
        self.geometry("800x500")

        # Initialize attributes for fun
        self.trainees: list[str] = []
        self.listbox = None
        self.tree = None

        # Welcome label, using pack() for stacking layout components
        ttk.Label(self, text=f"Welcome People Manager {voornaam}!", font=("Segoe UI", 14)).pack(padx=20, pady=10)

        # Shared personal info component
        info = PersonalInfo(self, self.user_info)
        info.pack(padx=20, pady=10)

        # Manager-specific features
        self.manager_features()

        ttk.Button(self, text="Exit", command=self.destroy).pack(pady=10)

        self.mainloop()

    def manager_features(self):
        frame = ttk.LabelFrame(self, text="Trainees")
        frame.pack(padx=10, pady=10, fill="x")

        # List of available trainees not yet linked to this manager
        self.trainees = UserLinking.get_available_trainees_for_manager(self.role, self.user_info.get("gebruikersnaam", ""))
        self.listbox = Listbox(frame, selectmode=MULTIPLE)
        for t in self.trainees:
            self.listbox.insert(END, t)
        self.listbox.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(frame, text="Link selected", command=self.link_selected).grid(row=0, column=1, padx=5, pady=5)

        # Treeview of linked trainees
        self.tree = ttk.Treeview(frame, columns=("trainee",), show="headings")
        self.tree.heading("trainee", text="Linked Trainees")
        self.tree.grid(row=0, column=2, padx=5, pady=5)
        self.update_linked_view()

    def link_selected(self):
        selected_indices = self.listbox.curselection()
        selected_trainees = [self.trainees[i] for i in selected_indices]

        UserLinking.link_trainee(selected_trainees, self.role, self.user_info.get("gebruikersnaam", ""))

        # Refresh list of available trainees
        self.trainees = [t for t in self.trainees if t not in selected_trainees]
        self.listbox.delete(0, END)
        for t in self.trainees:
            self.listbox.insert(END, t)

        self.update_linked_view()

    def update_linked_view(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        linked_usernames = UserLinking.get_linked_trainees(self.user_info.get("gebruikersnaam", ""))
        for t in linked_usernames:
            self.tree.insert("", END, values=(t,))
