# =======================
# Biblioteca de Estructuras de Datos
# =======================

# Pila (Stack)
def crear_pila():
    return []

def esta_vacia_pila(pila):
    return len(pila) == 0

def push(pila, item):
    pila.append(item)

def pop(pila):
    if not esta_vacia_pila(pila):
        return pila.pop()
    else:
        raise IndexError("La pila está vacía")

def ver_tope_pila(pila):
    if not esta_vacia_pila(pila):
        return pila[-1]
    else:
        raise IndexError("La pila está vacía")

def tamano_pila(pila):
    return len(pila)


# Cola (Queue)
def crear_cola():
    return []

def esta_vacia_cola(cola):
    return len(cola) == 0

def insertar_cola(cola, item):
    cola.insert(0, item)

def quitar_cola(cola):
    if not esta_vacia_cola(cola):
        return cola.pop()
    else:
        raise IndexError("La cola está vacía")

def recorrer_cola(cola):
    return cola[::-1]

def buscar_cola(cola, item):
    return item in cola

def tamano_cola(cola):
    return len(cola)


# Lista Genérica (Generic List)
class Nodo:
    def __init__(self, dato=None):
        self.dato = dato
        self.siguiente = None

def crear_lista():
    return None  # Lista vacía representada como None

def insertar_lista(lista, item):
    nuevo_nodo = Nodo(item)
    nuevo_nodo.siguiente = lista
    return nuevo_nodo  # Devolvemos el nuevo comienzo de la lista

def buscar_lista(lista, item):
    actual = lista
    while actual:
        if actual.dato == item:
            return True
        actual = actual.siguiente
    return False

def tamano_lista(lista):
    actual = lista
    contador = 0
    while actual:
        contador += 1
        actual = actual.siguiente
    return contador
