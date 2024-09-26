import tkinter as tk
import random

class JuegoGato:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Gato 4x4")
        self.tablero = [[' ' for _ in range(4)] for _ in range(4)]
        self.turno_usuario = True

        self.boton = [[tk.Button(root, text=' ', font=('Arial', 24), width=5, height=2, command=lambda i=i, j=j: self.jugar(i, j)) for j in range(4)] for i in range(4)]
        for i in range(4):
            for j in range(4):
                self.boton[i][j].grid(row=i, column=j)

        self.estado_label = tk.Label(root, text="Tu turno", font=('Arial', 16))
        self.estado_label.grid(row=4, column=0, columnspan=4)

    def jugar(self, i, j):
        if self.tablero[i][j] == ' ' and self.turno_usuario:
            self.tablero[i][j] = 'X'
            self.boton[i][j].config(text='X')
            if self.verificar_ganador('X'):
                self.estado_label.config(text="¡Ganaste!")
                return
            if self.tablero_lleno():
                self.estado_label.config(text="Empate.")
                return
            self.turno_usuario = False
            self.movimiento_computadora()
            if self.verificar_ganador('O'):
                self.estado_label.config(text="La computadora ganó.")
                return
            if self.tablero_lleno():
                self.estado_label.config(text="Empate.")
                return
            self.turno_usuario = True
            self.estado_label.config(text="Tu turno")

    def verificar_ganador(self, jugador):
        for i in range(4):
            if all(self.tablero[i][j] == jugador for j in range(4)):
                return True
            if all(self.tablero[j][i] == jugador for j in range(4)):
                return True
        if all(self.tablero[i][i] == jugador for i in range(4)):
            return True
        if all(self.tablero[i][3-i] == jugador for i in range(4)):
            return True
        return False

    def tablero_lleno(self):
        return all(self.tablero[i][j] != ' ' for i in range(4) for j in range(4))

    def movimiento_computadora(self):
        if self.hacer_movimiento_optimizado('O'):
            return
        if self.hacer_movimiento_optimizado('X'):
            return
        movimientos = [(i, j) for i in range(4) for j in range(4) if self.tablero[i][j] == ' ']
        if movimientos:
            fila, col = random.choice(movimientos)
            self.tablero[fila][col] = 'O'
            self.boton[fila][col].config(text='O')

    def hacer_movimiento_optimizado(self, jugador):
        for i in range(4):
            for j in range(4):
                if self.tablero[i][j] == ' ':
                    self.tablero[i][j] = jugador
                    if self.verificar_ganador(jugador):
                        self.boton[i][j].config(text='O' if jugador == 'O' else 'X')
                        return True
                    self.tablero[i][j] = ' '
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoGato(root)
    root.mainloop()
 