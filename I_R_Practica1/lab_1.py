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
    print("\n")


def method_header(func: callable):
    def wrapper(*args, **kwargs):
        print(f"{'-'*10} {func.__name__.replace('_', ' ').title()} {'-'*10}")
        output = func(*args, **kwargs)
        print("\n")
        return output

    return wrapper


@method_header
def integer_calc():
    hours = int(input("Ingrese un número de horas: "))
    minutes = int(input("Ingrese un número de minutos: "))
    total_minutes = hours * 60 + minutes
    total_seconds = total_minutes * 60

    print(f"Total de minutos: {total_minutes}")
    print(f"Total de segundos: {total_seconds}")


@method_header
def kinetic_energy():
    mass = float(input("Ingrese la masa en kg: "))
    velocity = float(input("Ingrese la velocidad en m/s: "))
    energy = 0.5 * mass * velocity ** 2
    print(f"La energía cinética es: {round(energy, 2)} J")


@method_header
def correo():
    name = input("Ingrese su nombre: ")
    surname = input("Ingrese su apellido: ")
    email = f"{name[0].lower()}.{surname.lower()[:3]}@hotmail.com"
    print(f"Su correo electrónico es: {email}")


if __name__ == "__main__":
    print_header("2024-06-15")
    correo()
    kinetic_energy()
    integer_calc()
