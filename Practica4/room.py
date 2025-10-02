from enum import Enum


class Floors(Enum):
    GROUND = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3


class Room:
    def __init__(self, number: str) -> None:
        self.number = number
        self.is_occupied = False
        self._floor: Floors | None = None
        self.set_floor()

    def __str__(self) -> str:
        return f"Room {self.number} on floor {self._floor.name if self._floor else 'Unknown'} - {'Occupied' if self.is_occupied else 'Available'}"

    def __repr__(self) -> str:
        return f"Room(room_number={self.number}, _floor={self._floor}, is_occupied={self.is_occupied})"

    def set_floor(self) -> None:
        try:
            self._floor = Floors(int(self.number[0])).name
        except ValueError:
            print("Invalid floor number.")
            self._floor = None

    def get_floor(self) -> Floors | None:
        return self._floor


class BedRoom(Room):
    def __init__(self, number: str) -> None:
        super().__init__(number)

    def __str__(self) -> str:
        return f"Bedroom {self.number} on {self._floor if self._floor else 'Unknown'} floor - {'Occupied' if self.is_occupied else 'Available'}"


class OperatingRoom(Room):
    def __init__(self, number: str) -> None:
        super().__init__(number)

    def __str__(self) -> str:
        return f"Operating Room on floor {self._floor if self._floor else 'Unknown'} - {'Occupied' if self.is_occupied else 'Available'}"
