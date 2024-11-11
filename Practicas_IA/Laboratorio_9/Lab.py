import numpy as np
from sklearn.model_selection import train_test_split, KFold, LeaveOneOut
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.datasets import load_iris, load_wine, load_digits

# Función para calcular la distancia Euclidiana
def distancia_euclidiana(X_entrenamiento, X_prueba):
    return np.linalg.norm(X_entrenamiento - X_prueba, axis=1)

# Función para implementar el clasificador Euclidiano
def clasificador_euclidiano(X_entrenamiento, y_entrenamiento, X_prueba):
    y_predicho = []
    for x_prueba in X_prueba:
        distancias = distancia_euclidiana(X_entrenamiento, x_prueba)
        indice_mas_cercano = np.argmin(distancias)
        y_predicho.append(y_entrenamiento[indice_mas_cercano])
    return np.array(y_predicho)

# Función para implementar el clasificador 1NN
def clasificador_1nn(X_entrenamiento, y_entrenamiento, X_prueba):
    clasificador = KNeighborsClassifier(n_neighbors=1)
    clasificador.fit(X_entrenamiento, y_entrenamiento)
    return clasificador.predict(X_prueba)

# Función para evaluar el desempeño del modelo
def evaluar_modelo(X, y, clasificador, metodo_validacion):
    n_clases = len(np.unique(y))
    exactitud = 0
    matriz_confusion = np.zeros((n_clases, n_clases), dtype=int)
    
    if metodo_validacion == 'hold_out':
        X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(X, y, test_size=0.3, random_state=42)
        y_predicho = clasificador(X_entrenamiento, y_entrenamiento, X_prueba)
        exactitud = accuracy_score(y_prueba, y_predicho)
        matriz_confusion = confusion_matrix(y_prueba, y_predicho, labels=np.arange(n_clases))
        
    elif metodo_validacion == '10_fold':
        validacion_kf = KFold(n_splits=10, shuffle=True, random_state=42)
        exactitudes = []
        for indice_entrenamiento, indice_prueba in validacion_kf.split(X):
            X_entrenamiento, X_prueba = X[indice_entrenamiento], X[indice_prueba]
            y_entrenamiento, y_prueba = y[indice_entrenamiento], y[indice_prueba]
            y_predicho = clasificador(X_entrenamiento, y_entrenamiento, X_prueba)
            exactitudes.append(accuracy_score(y_prueba, y_predicho))
            matriz_confusion += confusion_matrix(y_prueba, y_predicho, labels=np.arange(n_clases))
        exactitud = np.mean(exactitudes)
        
    elif metodo_validacion == 'leave_one_out':
        validacion_loo = LeaveOneOut()
        exactitudes = []
        for indice_entrenamiento, indice_prueba in validacion_loo.split(X):
            X_entrenamiento, X_prueba = X[indice_entrenamiento], X[indice_prueba]
            y_entrenamiento, y_prueba = y[indice_entrenamiento], y[indice_prueba]
            y_predicho = clasificador(X_entrenamiento, y_entrenamiento, X_prueba)
            exactitudes.append(accuracy_score(y_prueba, y_predicho))
            matriz_confusion += confusion_matrix(y_prueba, y_predicho, labels=np.arange(n_clases))
        exactitud = np.mean(exactitudes)

    return exactitud, matriz_confusion

# Lista de conjuntos de datos para evaluar
conjuntos_datos = {
    "Iris": load_iris(),
    "Wine": load_wine(),
    "Digits": load_digits()
}

# Evaluar clasificadores en cada conjunto de datos y método de validación
for nombre, conjunto in conjuntos_datos.items():
    X = conjunto.data
    y = conjunto.target
    print(f"\nEvaluación para el conjunto de datos: {nombre}")
    
    # Clasificador Euclidiano
    print("\nClasificador Euclidiano")
    for metodo in ['hold_out', '10_fold', 'leave_one_out']:
        exactitud, matriz_confusion = evaluar_modelo(X, y, clasificador_euclidiano, metodo)
        print(f"{metodo} -> Exactitud: {exactitud:.2f}, Matriz de confusión:\n{matriz_confusion}")
    
    # Clasificador 1-NN
    print("\nClasificador 1-NN")
    for metodo in ['hold_out', '10_fold', 'leave_one_out']:
        exactitud, matriz_confusion = evaluar_modelo(X, y, clasificador_1nn, metodo)
        print(f"{metodo} -> Exactitud: {exactitud:.2f}, Matriz de confusión:\n{matriz_confusion}")
