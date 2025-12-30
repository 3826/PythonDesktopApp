# app/ui/people_manager/dashboard.py

from tkinter import *
from tkinter import ttk, Toplevel
from app.ui.general.components.personal_info import PersonalInfo
from app.logic.user_manager import UserManager
from app.logic.user_linking import UserLinking


class DashboardScreen(Tk):
    def __init__(self, gebruikers_id, role):
        super().__init__()
        self.gebruikers_id = gebruikers_id
        self.role = role

        # Fetch user info once
        self.user_info = UserManager.get_user_info_by_id(gebruikers_id)
        voornaam = self.user_info.get("voornaam", "") if self.user_info else ""

        self.title(f"{role.replace('_',' ').title()} Dashboard")
        self.geometry("800x500")

        # Welcome label
        ttk.Label(
            self,
            text=f"Welcome People Manager {voornaam}!",
            font=("Segoe UI", 14)
        ).pack(padx=20, pady=10)

        # Personal info component
        info = PersonalInfo(self, self.user_info)
        info.pack(padx=20, pady=10)

        # Manager-specific features
        self.manager_features()

        ttk.Button(self, text="Exit", command=self.destroy).pack(pady=10)

        self.mainloop()

    # -----------------------------
    # Manager Features
    # -----------------------------
    def manager_features(self):
        frame = ttk.LabelFrame(self, text="Linked Trainees")
        frame.pack(padx=10, pady=10, fill="x")

        # Treeview showing linked trainees
        self.tree = ttk.Treeview(frame, columns=("trainee",), show="headings", height=6)
        self.tree.heading("trainee", text="Trainee Username")
        self.tree.pack(side=LEFT, padx=10, pady=10, fill="x")
        self.update_linked_view()

        # Bind click event to show trainee personal info
        self.tree.bind("<Double-1>", self.show_trainee_info)

        # Button opens popup to link new trainees
        ttk.Button(
            frame, text="Show Available Trainees", command=self.open_trainee_popup
        ).pack(side=LEFT, padx=20)

    # -----------------------------
    # Popup Window: Link Trainees
    # -----------------------------
    def open_trainee_popup(self):
        popup = Toplevel(self)
        popup.title("Available Trainees")
        popup.geometry("350x300")

        ttk.Label(popup, text="Available Trainees", font=("Segoe UI", 12)).pack(pady=10)

        # Fetch (id, username) tuples of unlinked trainees
        trainees = UserLinking.get_available_trainees_for_manager(self.role) #self.gebruikers_id

        # Convert to list of tuples (id, username)
        trainee_list = [(tid, UserManager.get_user_info_by_id(tid).get("gebruikersnaam", tid)) for tid in trainees]

        listbox = Listbox(popup, selectmode=MULTIPLE, width=40, height=10)
        listbox.pack(padx=10, pady=10)

        for _, tname in trainee_list:
            listbox.insert(END, tname)

        def link_selected():
            selected_indices = listbox.curselection()
            for i in selected_indices:
                trainee_id = trainee_list[i][0]
                if self.role == "people_manager":
                    UserLinking.link_trainee(trainee_id, people_manager_id=self.gebruikers_id)
                elif self.role == "business_manager":
                    UserLinking.link_trainee(trainee_id, business_manager_id=self.gebruikers_id)
            popup.destroy()
            self.update_linked_view()

        ttk.Button(popup, text="Link selected", command=link_selected).pack(pady=10)

    # -----------------------------
    # Update Treeview with linked trainees
    # -----------------------------
    def update_linked_view(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # use manager ID to get linked trainees
        linked_ids = UserLinking.get_linked_trainees(self.gebruikers_id)
        for tid in linked_ids:
            user_info = UserManager.get_user_info_by_id(tid)
            username = user_info.get("gebruikersnaam", tid) if user_info else tid
            self.tree.insert("", END, values=(username,))

    # -----------------------------
    # Show clicked trainee personal info
    # -----------------------------
    def show_trainee_info(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_index = selected_item[0]
        username = self.tree.item(item_index, "values")[0]

        # Find trainee ID from username
        linked_ids = UserLinking.get_linked_trainees(self.gebruikers_id)
        trainee_id = None
        for tid in linked_ids:
            info = UserManager.get_user_info_by_id(tid)
            if info and info.get("gebruikersnaam") == username:
                trainee_id = tid
                break
        if not trainee_id:
            return

        # Open popup with PersonalInfo component
        popup = Toplevel(self)
        popup.title(f"{username} - Personal Info")
        info = PersonalInfo(popup, UserManager.get_user_info_by_id(trainee_id))
        info.pack(padx=20, pady=20)
