#programa que lea el archivo bezdekIris.data y lo almacene en una matriz
archivo = 'bezdekIris.data'

# Leer el archivo y almacenar en una lista
datos = []

try:
    with open(archivo, 'r') as f:
        for linea in f:
            #Separación de los datos
            fila = linea.strip().split(',')  #El separador usado es ","
            datos.append(fila)

    # Mostrar los datos
    for fila in datos:
        print(fila)
except FileNotFoundError:
    print(f"El archivo {archivo} no fue encontrado.")
except Exception as e:
    print(f"Ocurrió un error: {e}")

#En este código, cada línea del archivo se convierte en una lista 
#y se añade a la lista datos. Al final, datos será una lista de listas, 
# donde cada sublista representa una fila del archivo.
