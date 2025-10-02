def print_header() -> None:
    print("="*40)
    attributes = {
        "Grupo": "1AB1",
        "Autor": "Carlos Lorenzo",
        "Nota": "10/10"
    }

    for key, value in attributes.items():
        print(f"{key.center(15)}: {value}")
    print("="*40)


def method_header(func: callable):
    """
    Decorator function that prints a header before calling the function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.
    """
    def wrapper(*args, **kwargs):
        print_header()
        output = func(*args, **kwargs)
        print("\n")
        return output

    return wrapper
