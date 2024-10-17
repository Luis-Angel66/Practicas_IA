import numpy as np
import random
import math

# Definir la función de Himmelblau
def himmelblau_function(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

# Definir el recocido simulado
def simulated_annealing(func, x_range, y_range, temp, cooling_rate, temp_min):
    # Generar una solución inicial aleatoria
    current_x = random.uniform(x_range[0], x_range[1])
    current_y = random.uniform(y_range[0], y_range[1])
    current_solution = func(current_x, current_y)
    
    best_x = current_x
    best_y = current_y
    best_solution = current_solution
    
    while temp > temp_min:
        # Generar un nuevo punto en el vecindario
        new_x = current_x + random.uniform(-1, 1)
        new_y = current_y + random.uniform(-1, 1)
        
        # Asegurarse de que el nuevo punto esté dentro del rango
        new_x = np.clip(new_x, x_range[0], x_range[1])
        new_y = np.clip(new_y, y_range[0], y_range[1])
        
        # Calcular el nuevo valor de la función objetivo
        new_solution = func(new_x, new_y)
        
        # Calcular el cambio de energía
        delta_energy = new_solution - current_solution
        
        # Aceptar o rechazar el nuevo punto basado en la probabilidad de recocido
        if delta_energy < 0 or random.random() < math.exp(-delta_energy / temp):
            current_x = new_x
            current_y = new_y
            current_solution = new_solution
            
            # Actualizar la mejor solución encontrada
            if current_solution < best_solution:
                best_x = current_x
                best_y = current_y
                best_solution = current_solution
        
        # Reducir la temperatura
        temp *= cooling_rate
    
    return best_x, best_y, best_solution

# Parámetros
x_range = (-5, 5)
y_range = (-5, 5)
temp = 1000  # Temperatura inicial
cooling_rate = 0.95  # Tasa de enfriamiento
temp_min = 1e-3  # Temperatura mínima para detener el algoritmo

# Ejecutar el recocido simulado
best_x, best_y, best_value = simulated_annealing(himmelblau_function, x_range, y_range, temp, cooling_rate, temp_min)

# Mostrar los resultados
print(f"Valores óptimos: x = {best_x}, y = {best_y}")
print(f"Valor mínimo de la función: {best_value}")
