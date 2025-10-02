def validate_input(type: object, prompt: str) -> object:
    while True:
        try:
            return type(input(prompt))
        except ValueError:
            print(f"Please enter a valid value for {type.__name__}.")
