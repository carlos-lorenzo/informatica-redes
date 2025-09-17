def print_header(date: str) -> None:
    import os
    file_name = os.path.basename(__file__)
    print("="*40)
    attributes = {
        "Archivo": file_name,
        "Grupo": "1AB1",
        "Autor": "Carlos Lorenzo",
        "Fecha": date,
        "Nota": "N/A"
    }

    for key, value in attributes.items():
        print(f"{key.center(15)}: {value}")
    print("="*40)


def method_header(func: callable):
    def wrapper(*args, **kwargs):
        print(f"{'-'*10} {func.__name__.replace('_', ' ').title()} {'-'*10}")
        output = func(*args, **kwargs)
        print("\n")
        return output

    return wrapper
