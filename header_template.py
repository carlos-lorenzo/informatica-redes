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


if __name__ == "__main__":
    print_header("2024-06-15")
    longitud = len("Lab_Practiva_1.py")
