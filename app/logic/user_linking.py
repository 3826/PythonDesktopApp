import csv
from app.config import USER_LINKS_CSV
from app.logic.user_manager import UserManager

class UserLinking:

    @staticmethod
    def get_linked_trainees(manager_id):
        """Return list of trainee IDs linked to the given manager (people or business)."""
        trainees = []
        if not USER_LINKS_CSV.exists():
            return trainees

        with USER_LINKS_CSV.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("people_manager_id") == str(manager_id) or row.get("business_manager_id") == str(manager_id):
                    trainees.append(row["trainee_id"])
        return trainees

    @staticmethod
    def link_trainee(trainee_id, people_manager_id=None, business_manager_id=None):
        """Add or update links for a trainee."""
        rows = []
        found = False
        if USER_LINKS_CSV.exists():
            with USER_LINKS_CSV.open(newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                for row in rows:
                    if row["trainee_id"] == trainee_id:
                        if people_manager_id:
                            row["people_manager_id"] = str(people_manager_id)
                        if business_manager_id:
                            row["business_manager_id"] = str(business_manager_id)
                        found = True
                        break

        if not found:
            rows.append({
                "trainee_id": trainee_id,
                "people_manager_id": str(people_manager_id) if people_manager_id else "",
                "business_manager_id": str(business_manager_id) if business_manager_id else ""
            })

        with USER_LINKS_CSV.open(mode="w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["trainee_id","people_manager_id","business_manager_id"])
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def get_available_trainees_for_manager(manager_role, manager_id):
        """Return trainee IDs not yet linked to this manager."""
        all_trainees = [
            u["gebruikers_id"]
            for u in UserManager.get_all_users()
            if u.get("rol") == "trainee"
        ]

        if not USER_LINKS_CSV.exists():
            return all_trainees

        linked = []
        with USER_LINKS_CSV.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if manager_role == "people_manager" and row.get("people_manager_id") == str(manager_id):
                    linked.append(row["trainee_id"])
                if manager_role == "business_manager" and row.get("business_manager_id") == str(manager_id):
                    linked.append(row["trainee_id"])
        return [t for t in all_trainees if t not in linked]

    @staticmethod
    def get_trainee_info(trainee_id):
        """Fetch personal info for a trainee via UserManager."""
        return UserManager.get_user_info_by_id(trainee_id)
