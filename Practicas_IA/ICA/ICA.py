import numpy as np

# Configuración del problema
def cost_function(x):
    return np.sum(x**2)  # Función de costo simple (minimizar la suma de cuadrados)

n_variables = 5
n_countries = 20
n_imperialists = 3
max_iterations = 100

# Inicialización de países (soluciones)
countries = np.random.uniform(-10, 10, (n_countries, n_variables))
costs = np.array([cost_function(country) for country in countries])

# Identificar imperialistas y colonias
sorted_indices = np.argsort(costs)
imperialists = countries[sorted_indices[:n_imperialists]]
colonies = countries[sorted_indices[n_imperialists:]]

# Asignar colonias a imperialistas
n_colonies = len(colonies)
colonies_per_imperialist = n_colonies // n_imperialists
assignments = [colonies[i * colonies_per_imperialist:(i + 1) * colonies_per_imperialist] for i in range(n_imperialists)]

# Iteraciones del algoritmo
for iteration in range(max_iterations):
    # Asimilación: mover colonias hacia su imperialista
    for i, imperialist in enumerate(imperialists):
        for j, colony in enumerate(assignments[i]):
            direction = imperialist - colony
            step = np.random.uniform(0, 1) * direction
            assignments[i][j] += step

    # Revolución: cambios aleatorios
    for i, imperialist in enumerate(imperialists):
        if np.random.rand() < 0.1:  # Probabilidad de revolución
            assignments[i] += np.random.uniform(-1, 1, assignments[i].shape)

    # Intercambio de posiciones si una colonia mejora al imperialista
    for i, imperialist in enumerate(imperialists):
        for colony in assignments[i]:
            if cost_function(colony) < cost_function(imperialist):
                imperialist, colony = colony, imperialist

    # Recalcular costos y redistribuir colonias si es necesario
    total_costs = [cost_function(imperialist) + np.mean([cost_function(colony) for colony in group]) for imperialist, group in zip(imperialists, assignments)]
    weakest_index = np.argmax(total_costs)
    strongest_index = np.argmin(total_costs)
    
    # Transferir colonia más débil al imperio más fuerte
    weakest_colony = assignments[weakest_index][-1]
    assignments[weakest_index] = assignments[weakest_index][:-1]
    assignments[strongest_index] = np.vstack((assignments[strongest_index], weakest_colony))

    # Eliminar imperios sin colonias
    assignments = [group for group in assignments if len(group) > 0]
    imperialists = imperialists[:len(assignments)]

# Resultado final
best_solution = imperialists[np.argmin([cost_function(imp) for imp in imperialists])]
print("Mejor solución encontrada:", best_solution)
print("Costo de la mejor solución:", cost_function(best_solution))