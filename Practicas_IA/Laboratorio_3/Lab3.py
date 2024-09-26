from collections import deque

# Función para verificar si una posición es válida (dentro de los límites del laberinto y no es una pared)
def is_valid_move(maze, visited, row, col):
    return (
        0 <= row < len(maze) and       # Dentro de los límites del laberinto (filas)
        0 <= col < len(maze[0]) and    # Dentro de los límites del laberinto (columnas)
        maze[row][col] == 0 and        # Es un camino, no una pared
        not visited[row][col]          # No ha sido visitado previamente
    )

# Función para resolver el laberinto usando BFS
def bfs_maze(maze, start, end):
    # Movimientos posibles: arriba, abajo, izquierda, derecha
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Inicializamos la cola para BFS y el conjunto de posiciones visitadas
    queue = deque([(start, [start])])  # Cada elemento de la cola es una tupla (posición actual, camino recorrido)
    visited = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    
    # Marcamos la posición inicial como visitada
    visited[start[0]][start[1]] = True
    
    while queue:
        (current_pos, path) = queue.popleft()  # Extraemos la primera posición en la cola
        row, col = current_pos
        
        # Si hemos llegado a la posición final
        if current_pos == end:
            return path  # Retornamos el camino que lleva a la salida
        
        # Exploramos las 4 direcciones posibles
        for move in moves:
            new_row, new_col = row + move[0], col + move[1]
            
            if is_valid_move(maze, visited, new_row, new_col):
                visited[new_row][new_col] = True
                queue.append(((new_row, new_col), path + [(new_row, new_col)]))
    
    return None  # No se encontró un camino

# Resolver el 4-puzzle usando BFS
def bfs_puzzle_4x4(start, goal):
    # Movimientos posibles para el espacio vacío: arriba, abajo, izquierda, derecha
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Convertimos la configuración inicial y final a tuplas (las listas no son hashables)
    start = tuple(map(tuple, start))
    goal = tuple(map(tuple, goal))
    
    # Inicializamos la cola para BFS y el conjunto de configuraciones visitadas
    queue = deque([(start, [])])  # Cada elemento es una tupla (estado actual, movimientos realizados)
    visited = set()
    visited.add(start)
    
    while queue:
        current, path = queue.popleft()  # Extraemos el primer estado en la cola
        
        # Si llegamos al estado objetivo
        if current == goal:
            return path  # Retornamos la secuencia de movimientos
        
        # Buscamos la posición del espacio vacío (0)
        zero_pos = [(r, c) for r in range(4) for c in range(4) if current[r][c] == 0][0]
        zero_r, zero_c = zero_pos
        
        # Exploramos las posibles posiciones hacia donde podemos mover el espacio vacío
        for move in moves:
            new_r, new_c = zero_r + move[0], zero_c + move[1]
            
            if 0 <= new_r < 4 and 0 <= new_c < 4:  # Verificamos que el movimiento sea válido
                # Generamos un nuevo estado al intercambiar el espacio vacío con la nueva posición
                new_state = [list(row) for row in current]
                new_state[zero_r][zero_c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[zero_r][zero_c]
                new_state = tuple(map(tuple, new_state))  # Convertimos a tuplas para poder hacer hashing
                
                if new_state not in visited:  # Si no hemos visitado este estado
                    visited.add(new_state)
                    queue.append((new_state, path + [(new_r, new_c)]))  # Añadimos el nuevo estado y el camino
    
    return None  # Si no encontramos una solución

# Representación del laberinto
maze = [
    [1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1]
]

# Posición de inicio y salida para el laberinto
start = (0, 1)  # Coordenadas (fila, columna) de inicio
end = (3, 4)    # Coordenadas (fila, columna) de salida

# Ejecutamos la función para el laberinto
maze_path = bfs_maze(maze, start, end)

# Mostramos el resultado para el laberinto
if maze_path:
    print("Camino encontrado en el laberinto:", maze_path)
else:
    print("No se encontró un camino en el laberinto.")

# Configuración inicial del puzzle 4x4
initial_puzzle = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 0, 12],
    [13, 14, 11, 15]
]

# Configuración objetivo del puzzle 4x4
goal_puzzle = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]

# Ejecutamos la función para el 4-puzzle
puzzle_solution = bfs_puzzle_4x4(initial_puzzle, goal_puzzle)

# Mostramos el resultado para el 4-puzzle
if puzzle_solution:
    print("Movimientos para resolver el puzzle 4x4:", puzzle_solution)
else:
    print("No se encontró solución para el puzzle 4x4.")
