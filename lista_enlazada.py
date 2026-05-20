# lista_enlazada.py
# Lista enlazada simple implementada con Nodos propios.
# No usa listas ni estructuras de Python internamente.

from nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None  # primer nodo de la lista

    def esta_vacia(self):
        return self.cabeza is None

    def insertar(self, dato):
        """Inserta al final de la lista."""
        nuevo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo
            return
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def insertar_sin_duplicado(self, dato, clave_fn):
        """
        Inserta solo si no existe ya un elemento con la misma clave.
        clave_fn: función que recibe un dato y retorna su clave comparable.
        Ejemplo: clave_fn = lambda p: p.id_post
        """
        clave_nueva = clave_fn(dato)
        actual = self.cabeza
        while actual is not None:
            if clave_fn(actual.dato) == clave_nueva:
                return  # ya existe, no insertar
            actual = actual.siguiente
        self.insertar(dato)

    def buscar(self, clave, clave_fn):
        """
        Busca el primer elemento cuya clave coincida.
        clave_fn: función que extrae la clave del dato.
        Retorna el dato o None si no se encuentra.
        """
        actual = self.cabeza
        while actual is not None:
            if clave_fn(actual.dato) == clave:
                return actual.dato
            actual = actual.siguiente
        return None

    def contiene(self, clave, clave_fn):
        """Retorna True si existe un elemento con esa clave."""
        return self.buscar(clave, clave_fn) is not None

    def a_lista_python(self):
        """Retorna los datos en una lista de Python (solo para recorrer/imprimir)."""
        resultado = []
        actual = self.cabeza
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def largo(self):
        """Cuenta cuántos nodos tiene la lista."""
        contador = 0
        actual = self.cabeza
        while actual is not None:
            contador += 1
            actual = actual.siguiente
        return contador
