dias_semana = (
    "Lunes",
    "Martes",
    "Miercoles",
    "Jueves",
    "Viernes",
    "Sabado",
    "Domingo"
)

numero_dia = int(input("Ingrese un numero del 1 al 7: "))
if numero_dia < 1 or numero_dia > 7:
    print("El numero ingresado no es valido")
else:
    print(dias_semana[numero_dia - 1])
