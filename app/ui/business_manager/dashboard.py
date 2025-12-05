#app/ui/business_manager/dashboard.py

from tkinter import *
from tkinter import ttk
from app.ui.general.components.personal_info import PersonalInfo
from app.logic.user_linking import UserLinking
from app.logic.user_manager import UserManager

class DashboardScreen(Tk):
    def __init__(self, gebruikers_id, role):
        super().__init__()
        self.gebruikers_id = gebruikers_id
        self.role = role
        self.title("People Manager Dashboard")
        self.geometry("800x500")

        # Display welcome label
        user_info = UserManager.get_user_info_by_id(gebruikers_id)
        username = user_info.get("voornaam", "") if user_info else ""
        ttk.Label(self, text=f"Welcome People Manager {username}!", font=("Segoe UI", 14)).pack(padx=20, pady=10)

        # Shared personal info component
        info = PersonalInfo(self, gebruikers_id)
        info.pack(padx=20, pady=10)

        # Manager features: link trainees
        self.manager_features()

        # Logout button
        ttk.Button(self, text="Logout", command=self.destroy).pack(pady=10)

        self.mainloop()

    def manager_features(self):
        frame = ttk.LabelFrame(self, text="Trainees")
        frame.pack(padx=10, pady=10, fill="x")

        # List available trainees (not yet linked to this manager)
        self.available_trainees = UserLinking.get_available_trainees_for_manager(self.role, self.gebruikers_id)
        self.listbox = Listbox(frame, selectmode=MULTIPLE, height=8)
        for t_id in self.available_trainees:
            trainee_info = UserManager.get_user_info_by_id(t_id)
            display_name = f"{trainee_info.get('voornaam','')} {trainee_info.get('achternaam','')}"
            self.listbox.insert(END, f"{display_name} ({t_id})")
        self.listbox.grid(row=0, column=0, padx=5, pady=5)

        # Link selected button
        ttk.Button(frame, text="Link selected", command=self.link_selected).grid(row=0, column=1, padx=5, pady=5)

        # Treeview for already linked trainees
        self.tree = ttk.Treeview(frame, columns=("trainee",), show="headings", height=8)
        self.tree.heading("trainee", text="Linked Trainees")
        self.tree.grid(row=0, column=2, padx=5, pady=5)
        self.update_linked_view()

    def link_selected(self):
        selected_indices = self.listbox.curselection()
        selected_ids = [self.available_trainees[i] for i in selected_indices]

        # Link trainees to this people manager
        for t_id in selected_ids:
            UserLinking.link_trainee(t_id, people_manager_id=self.gebruikers_id)

        # Remove linked trainees from available list
        self.available_trainees = [t for t in self.available_trainees if t not in selected_ids]
        self.listbox.delete(0, END)
        for t_id in self.available_trainees:
            trainee_info = UserManager.get_user_info_by_id(t_id)
            display_name = f"{trainee_info.get('voornaam','')} {trainee_info.get('achternaam','')}"
            self.listbox.insert(END, f"{display_name} ({t_id})")

        self.update_linked_view()

    def update_linked_view(self):
        # Clear existing tree items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load linked trainees
        linked_ids = UserLinking.get_linked_trainees(self.gebruikers_id)
        for t_id in linked_ids:
            trainee_info = UserManager.get_user_info_by_id(t_id)
            display_name = f"{trainee_info.get('voornaam','')} {trainee_info.get('achternaam','')}"
            self.tree.insert("", END, values=(f"{display_name} ({t_id})",))
