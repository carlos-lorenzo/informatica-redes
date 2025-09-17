pacientes_nuevos = int(input("Indica el número de pacientes nuevos hoy: "))
altas_mismo_dia = int(input("Indica el número de altas de los pacientes que entraron hoy: "))
hospitalizados = pacientes_nuevos - altas_mismo_dia

print(f"El número de pacientes hospitalizados hoy es: {hospitalizados}")