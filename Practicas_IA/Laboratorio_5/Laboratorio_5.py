import heapq
import numpy as np

# Función de Himmelblau
def himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

# Vecinos posibles (pequeños cambios en x y y)
def obtener_vecinos(actual, paso=0.1):
    x, y = actual
    vecinos = [
        (x + paso, y), (x - paso, y),
        (x, y + paso), (x, y - paso),
        (x + paso, y + paso), (x - paso, y - paso),
        (x + paso, y - paso), (x - paso, y + paso)
    ]
    return [v for v in vecinos if -5 <= v[0] <= 5 and -5 <= v[1] <= 5]  # limitar al rango [-5, 5]

# Implementación del algoritmo A*
def algoritmo_a_estrella_himmelblau(inicio, tolerancia=1e-6, paso=0.1):
    lista_abierta = []
    heapq.heappush(lista_abierta, (himmelblau(*inicio), inicio))  # (coste actual, nodo)
    visitados = set()

    while lista_abierta:
        costo_actual, actual = heapq.heappop(lista_abierta)

        if actual in visitados:
            continue
        visitados.add(actual)

        # Si el valor de la función es menor que la tolerancia, hemos encontrado un mínimo
        if costo_actual < tolerancia:
            return actual, costo_actual

        # Explorar vecinos
        for vecino in obtener_vecinos(actual, paso):
            if vecino not in visitados:
                costo_vecino = himmelblau(*vecino)
                heapq.heappush(lista_abierta, (costo_vecino, vecino))

    return None  # No se encontró un mínimo dentro de la tolerancia

# Definir el punto de inicio y el paso
inicio = (0, 0)  # Comenzamos en el origen
tolerancia = 1e-6
paso = 0.1

# Ejecutar el algoritmo A*
minimo, valor_minimo = algoritmo_a_estrella_himmelblau(inicio, tolerancia, paso)

# Mostrar el resultado
print(f"Valor mínimo encontrado: {valor_minimo} en el punto {minimo}")