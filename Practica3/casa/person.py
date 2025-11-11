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
    def create_patient(name: str, first_surname: str, second_surname: str, id: int) -> "Patient":
        return Patient(name, first_surname, second_surname, id)

    @staticmethod
    def generate_patient() -> "Patient":
        name = input("Enter patient's name: ")
        first_surname = input("Enter patient's first surname: ")
        second_surname = input("Enter patient's second surname: ")
        id = int(input("Enter patient's ID: "))
        patient = Patient.create_patient(
            name, first_surname, second_surname, id)
        return patient


class Doctor(Person):
    def __init__(self, name: str, first_surname: str, second_surname: str, id: int, hospital_name: str):
        super().__init__(name, first_surname, second_surname, id)
        self.hospital = hospital_name

    def __str__(self) -> str:
        return f"Dr. {self.first_surname} {self.second_surname}, {self.name} (ID: {self.id}) at {self.hospital}"

    @staticmethod
    def create_doctor(name: str, first_surname: str, second_surname: str, id: int, hospital_name: str) -> "Doctor":
        return Doctor(name, first_surname, second_surname, id, hospital_name)

    @staticmethod
    def generate_doctor(hospital_name: str) -> "Doctor":
        name = input("Enter doctor's name: ")
        first_surname = input("Enter doctor's first surname: ")
        second_surname = input("Enter doctor's second surname: ")
        id = int(input("Enter doctor's ID: "))
        doctor = Doctor.create_doctor(
            name, first_surname, second_surname, id, hospital_name)
        return doctor
