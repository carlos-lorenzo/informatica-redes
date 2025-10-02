from person import Engineer, SHIFTS
from header_template import method_header


class CompanyManagement:
    def __init__(self):
        self.name = "BioTech Solutions"
        self.engineers: dict[str, Engineer] = {}

    def add_engineer(self, engineer: Engineer) -> None:
        self.engineers[engineer.get_id()] = engineer

    def list_engineers(self) -> None:
        if not self.engineers:
            print("No engineers in the system.")
            return
        for engineer in self.engineers.values():
            print(engineer)

    def add_engineer_interactive(self) -> None:
        engineer = Engineer.generate_engineer()
        self.add_engineer(engineer)
        print(f"Engineer {engineer.get_full_name()} added successfully.")

    def remove_engineer(self) -> None:
        id = input("Enter the ID of the engineer to remove: ")
        if id in self.engineers:
            del self.engineers[id]
            print(f"Engineer with ID {id} removed successfully.")
        else:
            print(f"No engineer found with ID {id}.")

    def edit_engineer_shift(self) -> None:
        if not self.engineers:
            print("No engineers in the system.")
            return
        self.list_engineers()
        print("\n")
        id = input("Enter the ID of the engineer to edit: ")
        if id in self.engineers:
            engineer = self.engineers[id]
            print(f"Current shift: {engineer.get_shift().name}\n")
            print("Available shifts:")
            for shift in SHIFTS:
                print(f"{shift.value}. {shift.name}")
            print("\n")
            shift_value = int(input("Enter new shift value: "))
            if shift_value in [shift.value for shift in SHIFTS]:
                engineer.set_shift(SHIFTS(shift_value))
                print(f"Shift updated to {engineer.get_shift().name}.")
            else:
                print("Invalid shift value.")
        else:
            print(f"No engineer found with ID {id}.")

    def exit_management_terminal(self) -> None:
        print("Exiting management terminal.")
        exit(0)

    @method_header
    def management_terminal(self) -> None:
        options: dict[str, dict[str, callable]] = {
            "0": {"description": "Exit", "action": self.exit_management_terminal},
            "1": {"description": "List Engineers", "action": self.list_engineers},
            "2": {"description": "Add Engineer", "action": self.add_engineer_interactive},
            "3": {"description": "Remove Engineer", "action": self.remove_engineer},
            "4": {"description": "Edit Engineer Shift", "action": self.edit_engineer_shift},
        }

        while True:
            print("-"*50)
            print("Management Terminal".center(50))
            for key, option in options.items():
                print(f"{key}. {option['description']}")
            print("-"*50)

            choice = input("Select an option: ")
            if choice in options:
                options[choice]["action"]()
            else:
                print("Invalid option. Please enter a valid option.")


company = CompanyManagement()
company.management_terminal()
