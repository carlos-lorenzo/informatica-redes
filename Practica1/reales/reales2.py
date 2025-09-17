velocidad = float(input("Indica la velocidad del vehículo (m/s): "))
distancia = float(input("Indica la distancia recorrida (m): "))
tiempo_total = float(input("Indica el tiempo total del recorrido (s): "))

distancia_total = velocidad * tiempo_total
distancia_restante = distancia_total - distancia

print(f"La distancia restante por recorrer es: {round(distancia_restante, 2)} metros")