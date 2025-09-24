def suma(a, b):
    return a + b


def producto(a, b):
    return a * b


while True:
    num1 = float(input("Ingrese el primer numero (0 para terminar): "))
    if num1 == 0:
        print("El programa ha terminado correctamente")
        break
    num2 = float(input("Ingrese el segundo numero: "))

    if num1 > num2:
        print(producto(num1, num2))
    else:
        print(suma(num1, num2))
