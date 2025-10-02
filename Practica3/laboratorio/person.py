from enum import Enum


class SHIFTS(Enum):
    MORNING = 0
    AFTERNOON = 1
    NIGHT = 2


class Person:
    def __init__(self, name, first_surname: str, second_surname: str, id: str):
        self._name = name
        self._first_surname = first_surname
        self._second_surname = second_surname
        self._id = id

    def __str__(self) -> str:
        return f"{self._name} {self._first_surname} {self._second_surname} (ID: {self._id})"


class Engineer(Person):
    def __init__(self, name: str, first_surname: str, second_surname: str, id: int):
        super().__init__(name, first_surname, second_surname, id)
        self._shift: SHIFTS = SHIFTS.MORNING

    def __str__(self) -> str:
        return f"{self._id}: {self._name} {self._first_surname} {self._second_surname} - {self._shift.name} shift"

    def get_shift(self) -> SHIFTS:
        return self._shift

    def set_shift(self, shift: SHIFTS) -> None:
        self._shift = shift

    def get_full_name(self) -> str:
        return f"{self._name} {self._first_surname} {self._second_surname}"

    def get_id(self) -> int:
        return self._id

    @staticmethod
    def generate_engineer() -> "Engineer":
        name = input("Enter engineer's name: ")
        first_surname = input("Enter engineer's first surname: ")
        second_surname = input("Enter engineer's second surname: ")
        id = input("Enter engineer's ID: ")
        engineer = Engineer(name, first_surname, second_surname, id)
        return engineer
