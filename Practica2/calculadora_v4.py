class Calculator:
    def __init__(self) -> None:
        # Ordered according to BIDMAS
        self.operators: dict[str, callable] = {
            "^": lambda x, y: x ** y,
            "/": lambda x, y: x / y,
            "//": lambda x, y: x // y,
            "%": lambda x, y: x % y,
            "*": lambda x, y: x * y,
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
        }

    def split(self, expression: str) -> list:
        return

    def evaluate(self, expression: str) -> float:
        if expression[0].lower() == "f":
            return
