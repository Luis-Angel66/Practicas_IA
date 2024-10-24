import math

#Laboratorio 7 Minimax, Poda Alfa Beta
# Juego de gato en una matriz 4x4 con Minimax y Poda Alfa Beta

def crear_tablero():
    return [[' ' for _ in range(4)] for _ in range(4)]

def imprimir_tablero(tablero):
    print("   0   1   2   3 ")
    print("  ---------------")
    for i in range(4):
        print(i, "|", " | ".join(tablero[i]), "|")
        print("  ---------------")

def verificar_ganador(tablero, jugador):
    # Verificar filas
    for fila in tablero:
        if fila.count(jugador) == 4:
            return True

    # Verificar columnas
    for col in range(4):
        if all(tablero[fila][col] == jugador for fila in range(4)):
            return True

    # Verificar diagonales
    if all(tablero[i][i] == jugador for i in range(4)) or all(tablero[i][3 - i] == jugador for i in range(4)):
        return True

    return False

def tablero_lleno(tablero):
    for fila in tablero:
        if ' ' in fila:
            return False
    return True

def movimientos_disponibles(tablero):
    return [(i, j) for i in range(4) for j in range(4) if tablero[i][j] == ' ']

def evaluar_tablero(tablero):
    if verificar_ganador(tablero, 'O'):
        return 10
    elif verificar_ganador(tablero, 'X'):
        return -10
    else:
        return 0

def minimax(tablero, profundidad, es_maximizador, alpha, beta, profundidad_maxima):
    puntaje = evaluar_tablero(tablero)

    # Si hay un ganador o se ha llegado al final del juego
    if puntaje == 10 or puntaje == -10:
        return puntaje

    if tablero_lleno(tablero):
        return 0

    # Freno en profundidad máxima
    if profundidad == profundidad_maxima:
        return puntaje

    if es_maximizador:
        mejor = -math.inf
        for (i, j) in movimientos_disponibles(tablero):
            tablero[i][j] = 'O'  # La IA es 'O'
            mejor = max(mejor, minimax(tablero, profundidad + 1, False, alpha, beta, profundidad_maxima))
            tablero[i][j] = ' '
            alpha = max(alpha, mejor)
            if beta <= alpha:
                break
        return mejor
    else:
        mejor = math.inf
        for (i, j) in movimientos_disponibles(tablero):
            tablero[i][j] = 'X'  # El jugador es 'X'
            mejor = min(mejor, minimax(tablero, profundidad + 1, True, alpha, beta, profundidad_maxima))
            tablero[i][j] = ' '
            beta = min(beta, mejor)
            if beta <= alpha:
                break
        return mejor

def mejor_movimiento(tablero, profundidad_maxima):
    mejor_valor = -math.inf
    mejor_movimiento = (-1, -1)

    for (i, j) in movimientos_disponibles(tablero):
        tablero[i][j] = 'O'  # La IA juega como 'O'
        movimiento_valor = minimax(tablero, 0, False, -math.inf, math.inf, profundidad_maxima)
        tablero[i][j] = ' '

        if movimiento_valor > mejor_valor:
            mejor_movimiento = (i, j)
            mejor_valor = movimiento_valor

    return mejor_movimiento

def jugar_humano(tablero, jugador):
    while True:
        try:
            fila = int(input(f"Jugador {jugador}, ingresa el número de fila (0-3): "))
            columna = int(input(f"Jugador {jugador}, ingresa el número de columna (0-3): "))

            if tablero[fila][columna] == ' ':
                tablero[fila][columna] = jugador
                break
            else:
                print("Posición ya ocupada, elige otra.")
        except ValueError:
            print("Entrada no válida, intenta de nuevo.")

def iniciar_juego():
    while True:
        juego_gato()
        respuesta = input("¿Quieres volver a jugar? (s/n): ").lower()
        if respuesta != 's':
            print("Gracias por jugar. ¡Hasta la próxima!")
            break

def juego_gato():
    tablero = crear_tablero()
    profundidad_maxima = 6  # Limitar la profundidad del árbol

    print("Selecciona la modalidad:")
    print("1. Humano vs Humano")
    print("2. Humano vs IA")
    print("3. IA vs IA")
    opcion = input("Ingresa el número de la modalidad: ")

    if opcion == '1':
        jugador_actual = 'X'
        while True:
            imprimir_tablero(tablero)
            jugar_humano(tablero, jugador_actual)

            if verificar_ganador(tablero, jugador_actual):
                imprimir_tablero(tablero)
                print(f"¡El jugador {jugador_actual} ha ganado!")
                break

            if tablero_lleno(tablero):
                imprimir_tablero(tablero)
                print("El juego ha terminado en empate.")
                break

            jugador_actual = 'O' if jugador_actual == 'X' else 'X'

    elif opcion == '2':
        jugador_actual = 'X'
        while True:
            imprimir_tablero(tablero)

            if jugador_actual == 'X':
                jugar_humano(tablero, jugador_actual)
            else:
                print("Turno de la IA")
                fila, columna = mejor_movimiento(tablero, profundidad_maxima)
                tablero[fila][columna] = 'O'

            if verificar_ganador(tablero, jugador_actual):
                imprimir_tablero(tablero)
                print(f"¡El jugador {jugador_actual} ha ganado!")
                break

            if tablero_lleno(tablero):
                imprimir_tablero(tablero)
                print("El juego ha terminado en empate.")
                break

            jugador_actual = 'O' if jugador_actual == 'X' else 'X'

    elif opcion == '3':
        jugador_actual = 'X'
        while True:
            imprimir_tablero(tablero)

            if jugador_actual == 'X':
                print("Turno de la IA (X)")
                fila, columna = mejor_movimiento(tablero, profundidad_maxima)
                tablero[fila][columna] = 'X'
            else:
                print("Turno de la IA (O)")
                fila, columna = mejor_movimiento(tablero, profundidad_maxima)
                tablero[fila][columna] = 'O'

            if verificar_ganador(tablero, jugador_actual):
                imprimir_tablero(tablero)
                print(f"¡El jugador {jugador_actual} ha ganado!")
                break

            if tablero_lleno(tablero):
                imprimir_tablero(tablero)
                print("El juego ha terminado en empate.")
                break

            jugador_actual = 'O' if jugador_actual == 'X' else 'X'

    else:
        print("Opción no válida, selecciona 1, 2 o 3.")

# Iniciar el juego con opción de volver a jugar
iniciar_juego()
