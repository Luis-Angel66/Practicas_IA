  import numpy as np
from sklearn.model_selection import train_test_split, KFold, LeaveOneOut
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.datasets import load_iris, load_wine, load_digits

# Función para implementar el clasificador 1NN
def clasificador_1nn(X_entrenamiento, y_entrenamiento, X_prueba):
    clasificador = KNeighborsClassifier(n_neighbors=1)
    clasificador.fit(X_entrenamiento, y_entrenamiento)
    return clasificador.predict(X_prueba)

# Función para implementar el clasificador Naive Bayes
def clasificador_naive_bayes(X_entrenamiento, y_entrenamiento, X_prueba):
    clasificador = GaussianNB()
    clasificador.fit(X_entrenamiento, y_entrenamiento)
    return clasificador.predict(X_prueba)

# Función para implementar el clasificador k-NN con k configurable
def clasificador_knn(X_entrenamiento, y_entrenamiento, X_prueba, k=3):
    clasificador = KNeighborsClassifier(n_neighbors=k)
    clasificador.fit(X_entrenamiento, y_entrenamiento)
    return clasificador.predict(X_prueba)

# Función para evaluar el desempeño del modelo
def evaluar_modelo(X, y, clasificador, metodo_validacion, k=None):
    n_clases = len(np.unique(y))
    exactitud = 0
    matriz_confusion = np.zeros((n_clases, n_clases), dtype=int)

    if metodo_validacion == 'hold_out':
        X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(X, y, test_size=0.3, random_state=42)
        y_predicho = clasificador(X_entrenamiento, y_entrenamiento, X_prueba) if k is None else clasificador(X_entrenamiento, y_entrenamiento, X_prueba, k)
        exactitud = accuracy_score(y_prueba, y_predicho)
        matriz_confusion = confusion_matrix(y_prueba, y_predicho, labels=np.arange(n_clases))

    elif metodo_validacion == '10_fold':
        validacion_kf = KFold(n_splits=10, shuffle=True, random_state=42)
        exactitudes = []
        for indice_entrenamiento, indice_prueba in validacion_kf.split(X):
            X_entrenamiento, X_prueba = X[indice_entrenamiento], X[indice_prueba]
            y_entrenamiento, y_prueba = y[indice_entrenamiento], y[indice_prueba]
            y_predicho = clasificador(X_entrenamiento, y_entrenamiento, X_prueba) if k is None else clasificador(X_entrenamiento, y_entrenamiento, X_prueba, k)
            exactitudes.append(accuracy_score(y_prueba, y_predicho))
            matriz_confusion += confusion_matrix(y_prueba, y_predicho, labels=np.arange(n_clases))
        exactitud = np.mean(exactitudes)

    elif metodo_validacion == 'leave_one_out':
        validacion_loo = LeaveOneOut()
        exactitudes = []
        for indice_entrenamiento, indice_prueba in validacion_loo.split(X):
            X_entrenamiento, X_prueba = X[indice_entrenamiento], X[indice_prueba]
            y_entrenamiento, y_prueba = y[indice_entrenamiento], y[indice_prueba]
            y_predicho = clasificador(X_entrenamiento, y_entrenamiento, X_prueba) if k is None else clasificador(X_entrenamiento, y_entrenamiento, X_prueba, k)
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

    # Clasificador 1-NN
    print("\nClasificador 1-NN")
    for metodo in ['hold_out', '10_fold', 'leave_one_out']:
        exactitud, matriz_confusion = evaluar_modelo(X, y, clasificador_1nn, metodo)
        print(f"{metodo} -> Exactitud: {exactitud:.2f}, Matriz de confusión:\n{matriz_confusion}")

    # Clasificador Naive Bayes
    print("\nClasificador Naive Bayes")
    for metodo in ['hold_out', '10_fold', 'leave_one_out']:
        exactitud, matriz_confusion = evaluar_modelo(X, y, clasificador_naive_bayes, metodo)
        print(f"{metodo} -> Exactitud: {exactitud:.2f}, Matriz de confusión:\n{matriz_confusion}")

    # Clasificador k-NN con k=3 y k=5
    for k in [3, 5]:
        print(f"\nClasificador k-NN (k={k})")
        for metodo in ['hold_out', '10_fold', 'leave_one_out']:
            exactitud, matriz_confusion = evaluar_modelo(X, y, clasificador_knn, metodo, k=k)
            print(f"{metodo} -> Exactitud: {exactitud:.2f}, Matriz de confusión:\n{matriz_confusion}")
