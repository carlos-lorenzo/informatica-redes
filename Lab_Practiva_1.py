def correo():
    name = input("Ingrese su nombre: ")
    surname = input("Ingrese su apellido: ")
    email = f"{name[0].lower()}.{surname.lower()[:3]}@hotmail.com"
    print(f"Su correo electrónico es: {email}")


correo()
