# nodo.py
# Unidad básica de la lista enlazada.
# 'dato' puede ser cualquier objeto: Post, Usuario, string, etc.

class Nodo:
    def __init__(self, dato):
        self.dato = dato        # contenido del nodo
        self.siguiente = None   # puntero al siguiente nodo
