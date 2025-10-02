class Person:
    def __init__(self, name, first_surname: str, second_surname: str, id: int):
        self.name = name
        self.first_surname = first_surname
        self.second_surname = second_surname
        self.id = id

    def __str__(self) -> str:
        return f"{self.name} {self.first_surname} {self.second_surname} (ID: {self.id})"


class Patient(Person):
    def __init__(self, name: str, first_surname: str, second_surname: str, id: int):
        super().__init__(name, first_surname, second_surname, id)
        self._room_number: str = ""

    def __str__(self) -> str:
        return f"{self.name} {self.first_surname} {self.second_surname} (ID: {self.id}) at room {self._room_number}"

    def set_room_number(self, room_number: str) -> None:
        self._room_number = room_number

    def get_room_number(self) -> str:
        return self._room_number

    @staticmethod
    def generate_patient() -> "Patient":
        name = input("Enter patient's name: ")
        first_surname = input("Enter patient's first surname: ")
        second_surname = input("Enter patient's second surname: ")
        id = int(input("Enter patient's ID: "))
        patient = Patient(name, first_surname, second_surname, id)
        return patient


class Doctor(Person):
    def __init__(self, name: str, first_surname: str, second_surname: str, id: int, hospital_name: str):
        super().__init__(name, first_surname, second_surname, id)
        self.hospital = hospital_name

    def __str__(self) -> str:
        return f"Dr. {self.first_surname} {self.second_surname}, {self.name} (ID: {self.id}) at {self.hospital}"

    @staticmethod
    def generate_doctor(hospital_name: str) -> "Doctor":
        name = input("Enter doctor's name: ")
        first_surname = input("Enter doctor's first surname: ")
        second_surname = input("Enter doctor's second surname: ")
        id = int(input("Enter doctor's ID: "))
        doctor = Doctor(name, first_surname, second_surname, id, hospital_name)
        return doctor


class Hospital:
    def __init__(self, hospital_name: str):
        self.hospital_name = hospital_name
        self._patients: dict[str, Patient] = {}
        self._doctors: dict[str, Doctor] = {}

    def add_patient(self) -> None:
        patient = Patient.generate_patient()
        self._patients[patient.id] = patient
        print(f"{patient} added successfully.")

    def remove_patient(self, id: str) -> None:
        for key, patient in list(self._patients.items()):
            if patient.id == id:
                del self._patients[key]
                print(f"Patient with ID {id} removed successfully.")
                return
        print(f"No patient found with ID {id}.")

    def add_doctor(self) -> None:
        doctor = Doctor.generate_doctor(self.hospital_name)
        self._doctors[doctor.id] = doctor
        print(f"{doctor} added successfully.")

    def remove_doctor(self, id: str) -> None:
        for key, doctor in list(self._doctors.items()):
            if doctor.id == id:
                del self._doctors[key]
                print(f"Doctor with ID {id} removed successfully.")
                return
        print(f"No doctor found with ID {id}.")

    def view_doctors(self) -> None:
        if not self.doctors:
            print("No doctors available.")
        else:
            print("-"*50)
            print("Available doctors".center(50))
            for doctor in self.doctors.values():
                print(f"- {doctor}")

            print("-"*50)

    def view_patients(self) -> None:
        if not self._patients:
            print("No patients available.")
        else:
            print("-"*50)
            print("Active patients".center(50))
            for patient in self._patients.values():
                print(f"- {patient}")

            print("-"*50)

    def management_terminal(self) -> None:
        options: dict[str, dict[str, callable]] = {
            "1": {
                "description": "Add Patient",
                "action": self.add_patient
            },
            "2": {
                "description": "Remove Patient",
                "action": lambda: self.remove_patient(input("Enter patient ID to remove: "))
            },
            "3": {
                "description": "Add Doctor",
                "action": self.add_doctor
            },
            "4": {
                "description": "Remove Doctor",
                "action": lambda: self.remove_doctor(input("Enter doctor ID to remove: "))
            },
            "5": {
                "description": "View Doctors",
                "action": self.view_doctors
            },
            "6": {
                "description": "View Patients",
                "action": self.view_patients
            },

        }

        while True:
            print("-"*50)
            print("Management Terminal".center(50))
            for key, option in options.items():
                print(f"{key}. {option['description']}")
            print("0. Exit")
            print("-"*50)

            choice = input("Select an option: ")
            if choice in options:
                options[choice]["action"]()
            elif choice == "0":
                print("Exiting management terminal.")
                break
            else:
                print("Invalid option. Please try again.")


hospital = Hospital("City Hospital")
hospital.management_terminal()
