import heapq
import time

# Representación del laberinto
# 0 = camino, 1 = pared
laberinto = [
    [1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1]
]

# Posición de inicio y salida
inicio = (0, 1)  # Coordenadas (fila, columna) de inicio
salida = (3, 4)  # Coordenadas (fila, columna) de salida

# Función heurística (distancia Manhattan)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Implementación del algoritmo A*
def algoritmo_a_estrella(laberinto, inicio, salida):
    filas, columnas = len(laberinto), len(laberinto[0])
    lista_abierta = []
    heapq.heappush(lista_abierta, (0, inicio))  # (coste total estimado, nodo)
    de_donde_viene = {}
    costo_g = {inicio: 0}  # Coste desde el inicio
    costo_f = {inicio: heuristica(inicio, salida)}  # Coste total estimado
    
    while lista_abierta:
        actual = heapq.heappop(lista_abierta)[1]
        
        if actual == salida:
            camino = []
            while actual in de_donde_viene:
                camino.append(actual)
                actual = de_donde_viene[actual]
            camino.append(inicio)
            return camino[::-1]  # Devolver el camino en el orden correcto
        
        # Vecinos posibles (arriba, abajo, izquierda, derecha)
        vecinos = [(actual[0]+1, actual[1]), (actual[0]-1, actual[1]),
                   (actual[0], actual[1]+1), (actual[0], actual[1]-1)]
        
        for vecino in vecinos:
            fila, columna = vecino
            if 0 <= fila < filas and 0 <= columna < columnas and laberinto[fila][columna] == 0:  # Vecino válido
                costo_g_tentativo = costo_g[actual] + 1
                
                if vecino not in costo_g or costo_g_tentativo < costo_g[vecino]:
                    de_donde_viene[vecino] = actual
                    costo_g[vecino] = costo_g_tentativo
                    costo_f[vecino] = costo_g_tentativo + heuristica(vecino, salida)
                    heapq.heappush(lista_abierta, (costo_f[vecino], vecino))
    
    return None  # No hay solución

# Medir el tiempo de ejecución
tiempo_inicio = time.time()
camino = algoritmo_a_estrella(laberinto, inicio, salida)
tiempo_fin = time.time()

# Mostrar resultados
if camino:
    print(f"Camino encontrado: {camino}")
else:
    print("No se encontró un camino.")
print(f"Tiempo de ejecución: {tiempo_fin - tiempo_inicio:.6f} segundos\n")

# Escenario adicional con laberinto más grande
laberinto_grande = [
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
]

# Nueva posición de inicio y salida
inicio_grande = (0, 1)
salida_grande = (8, 8)

# Ejecutar A* con el nuevo laberinto
tiempo_inicio_grande = time.time()
camino_grande = algoritmo_a_estrella(laberinto_grande, inicio_grande, salida_grande)
tiempo_fin_grande = time.time()

print("LABERINTO MÁS GRANDE")
# Mostrar resultados del laberinto más grande
if camino_grande:
    print(f"Camino encontrado en el laberinto más grande: {camino_grande}")
else:
    print("No se encontró un camino en el laberinto más grande.")
print(f"Tiempo de ejecución para el laberinto más grande: {tiempo_fin_grande - tiempo_inicio_grande:.6f} segundos")
