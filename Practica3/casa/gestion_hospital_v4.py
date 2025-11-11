from utils import validate_input

from person import Patient, Doctor
from room import BedRoom, OperatingRoom, Floors


class Hospital:
    def __init__(self, hospital_name: str, bed_rooms: int, operating_rooms: int):
        self.hospital_name = hospital_name
        self._patients: dict[str, Patient] = {}
        self._doctors: dict[str, Doctor] = {}
        self._bedrooms: dict[int, BedRoom] = {int(f"{floor.value}{str(num):02}"): BedRoom(f"{floor.value}{str(num):02}")
                                              for floor in Floors for num in range(1, (bed_rooms // len(Floors)) + 1)}

        self._operating_rooms: dict[int, OperatingRoom] = {int(f"{floor.value}{str(num):02}"): OperatingRoom(f"{floor.value}{str(num):02}")
                                                           for floor in Floors for num in range(1, (operating_rooms // len(Floors)) + 1)}

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
        if not self._doctors:
            print("No doctors available.")
        else:
            print("-"*50)
            print("Available doctors".center(50))
            for doctor in self._doctors.values():
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

    def get_patient(self, i: int) -> Patient | None:
        if 0 <= i < len(self._patients):
            return list(self._patients.values())[i]
        return None

    def edit_patient(self, i: int, new_patient: Patient) -> None:
        if 0 <= i < len(self._patients):
            key = list(self._patients.keys())[i]
            self._patients[key] = new_patient

    def toggle_bedroom_occupancy(self, room_number: int) -> None:
        room = self._bedrooms.get(
            room_number) or self._operating_rooms.get(room_number)
        if room:
            room.is_occupied = not room.is_occupied
            status = "Occupied" if room.is_occupied else "Available"
            print(f"Room {room_number} is now {status}.")
        else:
            print(f"No room found with number {room_number}.")

    def toggle_operating_room_occupancy(self, room_number: int) -> None:
        room = self._operating_rooms.get(room_number)
        if room:
            room.is_occupied = not room.is_occupied
            status = "Occupied" if room.is_occupied else "Available"
            print(f"Operating Room {room_number} is now {status}.")
        else:
            print(f"No operating room found with number {room_number}.")

    def view_bedroom_occupancy(self) -> None:
        print("-"*50)
        print("Bedroom Occupancy".center(50))
        for room in self._bedrooms.values():
            print(room)
        print("-"*50)

    def view_operating_room_occupancy(self) -> None:
        print("-"*50)
        print("Operating Room Occupancy".center(50))
        for room in self._operating_rooms.values():
            print(room)
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
            "7": {
                "description": "Toggle Bedroom Occupancy",
                "action": lambda: self.toggle_bedroom_occupancy(validate_input(int, "Enter bedroom number to toggle occupancy: "))
            },
            "8": {
                "description": "Toggle Operating Room Occupancy",
                "action": lambda: self.toggle_operating_room_occupancy(validate_input(int, "Enter operating room number to toggle occupancy: "))
            },
            "9": {
                "description": "View Bedroom Occupancy",
                "action": self.view_bedroom_occupancy
            },
            "10": {
                "description": "View Operating Room Occupancy",
                "action": self.view_operating_room_occupancy
            }

        }

        while True:
            print("-"*50)
            print("Management Terminal".center(50))
            print("0. Exit")
            for key, option in options.items():
                print(f"{key}. {option['description']}")
            print("-"*50)

            choice = input("Select an option: ")
            if choice in options:
                options[choice]["action"]()
            elif choice == "0":
                print("Exiting management terminal.")
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    hospital = Hospital("City Hospital", 20, 9)
    hospital.management_terminal()
