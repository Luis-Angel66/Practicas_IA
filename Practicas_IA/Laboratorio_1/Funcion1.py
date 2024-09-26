import numpy as np
from scipy.optimize import minimize

# Definimos la función objetivo
def f(vars):
    x, y = vars
    return (1.5 - x + x * y)**2 + (2.25 - x + x * y**2)**2 + (2.625 - x + x * y**3)**2

# Definimos las restricciones para x e y
bounds = [(-4.5, 4.5), (-4.5, 4.5)]

# Valor inicial
initial_guess = [0, 0]

# Utilizamos la función minimize con el método L-BFGS-B que permite incluir restricciones
result = minimize(f, initial_guess, bounds=bounds, method='L-BFGS-B')

# Mostramos el resultado
print("Punto mínimo encontrado:", result.x)
print("Valor mínimo de la función:", result.fun)

# Si se desea verificar el éxito del proceso de optimización:
if result.success:
    print("Optimización exitosa.")
else:
    print("La optimización falló.")
    print("Mensaje de error:", result.message)
