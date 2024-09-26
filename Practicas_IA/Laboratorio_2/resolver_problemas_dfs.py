# Importa la biblioteca de estructuras de datos
from biblioteca_estructuras import crear_pila, esta_vacia_pila, push, pop

# =======================
# Resolver problemas con DFS
# =======================

# Resolver el 4-puzzle usando DFS
def resolver_puzzle_dfs(estado_inicial, estado_meta):
    pila = crear_pila()
    push(pila, (estado_inicial, []))
    visitados = set()

    while not esta_vacia_pila(pila):
        estado_actual, camino = pop(pila)
        
        if estado_actual in visitados:
            continue
        
        visitados.add(estado_actual)
        
        if estado_actual == estado_meta:
            return camino
        
        for sucesor in generar_sucesores(estado_actual):
            if sucesor not in visitados:
                push(pila, (sucesor, camino + [sucesor]))

    return None

# Función auxiliar para generar sucesores del puzzle
def generar_sucesores(estado):
    sucesores = []
    indice_vacio = estado.index(0)
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    filas, columnas = 2, 2

    fila_vacia, col_vacia = divmod(indice_vacio, columnas)
    for mov in movimientos:
        nueva_fila = fila_vacia + mov[0]
        nueva_columna = col_vacia + mov[1]
        if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
            nuevo_indice = nueva_fila * columnas + nueva_columna
            nuevo_estado = list(estado)
            nuevo_estado[indice_vacio], nuevo_estado[nuevo_indice] = nuevo_estado[nuevo_indice], nuevo_estado[indice_vacio]
            sucesores.append(tuple(nuevo_estado))
    return sucesores

# Ejemplo de uso del 4-puzzle
estado_inicial = (1, 2, 3, 0)
estado_meta = (0, 1, 2, 3)

solucion_puzzle = resolver_puzzle_dfs(estado_inicial, estado_meta)
print(f"Solución del 4-puzzle: {solucion_puzzle}")


# Resolver el laberinto usando DFS
def resolver_laberinto_dfs(maze, start, end):
    pila = crear_pila()
    push(pila, (start, [start]))
    visitados = set()

    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while not esta_vacia_pila(pila):
        (fila_actual, col_actual), camino = pop(pila)

        if (fila_actual, col_actual) == end:
            return camino

        if (fila_actual, col_actual) in visitados:
            continue

        visitados.add((fila_actual, col_actual))

        for mov in movimientos:
            nueva_fila = fila_actual + mov[0]
            nueva_columna = col_actual + mov[1]

            if 0 <= nueva_fila < len(maze) and 0 <= nueva_columna < len(maze[0]) and maze[nueva_fila][nueva_columna] == 0:
                nueva_posicion = (nueva_fila, nueva_columna)
                push(pila, (nueva_posicion, camino + [nueva_posicion]))

    return None

# Ejemplo de uso del laberinto
maze = [
    [1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1]
]

start = (0, 1)
end = (3, 4)

camino_laberinto = resolver_laberinto_dfs(maze, start, end)
print(f"Camino del laberinto: {camino_laberinto}")
