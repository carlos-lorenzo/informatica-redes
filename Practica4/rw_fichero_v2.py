written_data = [
    "Esto es una cadena de caracteres\n",
    "2023\n",
    "3.14\n",
    "True",
]
with open("datos_escritos.txt", "r") as file:
    read_data = file.readlines()
    if read_data == written_data:
        print("PERFECTO: los datos leidos son iguales a los escritos")
    else:
        print("ERROR: los datos leidos son distintos a los escritos")
