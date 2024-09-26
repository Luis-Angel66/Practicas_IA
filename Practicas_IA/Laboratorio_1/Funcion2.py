import numpy as np

# Definimos la función objetivo
def f(vars):
    x, y = vars
    return (1.5 - x + x * y)**2 + (2.25 - x + x * y**2)**2 + (2.625 - x + x * y**3)**2

# Configuración de los límites y número máximo de iteraciones
bounds = [-4.5, 4.5]
max_iterations = 10000

# Inicialización de la mejor solución encontrada
best_x = None
best_y = None
best_value = float('inf')

# Búsqueda aleatoria
for _ in range(max_iterations):
    # Generar valores aleatorios para x e y dentro de los límites
    x = np.random.uniform(bounds[0], bounds[1])
    y = np.random.uniform(bounds[0], bounds[1])
    
    # Evaluar la función en estos valores
    value = f([x, y])
    
    # Verificar si esta solución es la mejor encontrada hasta ahora
    if value < best_value:
        best_x = x
        best_y = y
        best_value = value

# Imprimir los resultados
print("Mejor punto encontrado:")
print(f"x = {best_x}")
print(f"y = {best_y}")
print(f"Valor mínimo de la función = {best_value}")
