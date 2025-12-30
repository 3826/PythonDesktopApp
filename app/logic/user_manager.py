#app/logic/user_manager.py

from app.config import TEST_CSV
import csv

CSV_FILE = TEST_CSV  # Path object to users CSV

class UserManager:
    @staticmethod
    def validate_user(username, password):
        print("validate_user(username, password)")
        """Check credentials and return the user row if valid."""
        if not CSV_FILE.exists():
            print("!CSV_FILE.exists()")
            return None

        username_input = username.strip().lower() #strip to be sure

        with CSV_FILE.open(newline='', encoding='utf-8') as f:
            print("CSV_FILE.open()")
            reader = csv.DictReader(f)
            for row in reader:
                row_username = row.get("gebruikersnaam", "").strip().lower()
                row_password = row.get("wachtwoord", "").strip()
                row_role = row.get("rol", "").strip().lower()

                allowed_roles = ["admin", "trainee", "people_manager", "business_manager"]
                if row_username == username_input and row_password == password and row_role in allowed_roles:
                    return row  # includes gebruikers_id, username, role, etc.

        return None

    @staticmethod
    def get_user_info_by_id(gebruikers_id):
        """Return user info dict by gebruikers_id (without password check)."""
        if not CSV_FILE.exists():
            return None

        with CSV_FILE.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("gebruikers_id") == str(gebruikers_id):
                    return row

        return None

    @staticmethod
    def get_all_users():
        """Return a list of all user dicts."""
        if not CSV_FILE.exists():
            return []
        with CSV_FILE.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
