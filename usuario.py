# usuario.py
# Representa un usuario de la red social.
# Sus amigos se almacenan en una lista enlazada propia.

from lista_enlazada import ListaEnlazada

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.amigos = ListaEnlazada()   # lista enlazada de objetos Usuario

    def agregar_amigo(self, usuario_amigo):
        """Agrega un amigo sin duplicados (por nombre)."""
        self.amigos.insertar_sin_duplicado(
            usuario_amigo,
            clave_fn=lambda u: u.nombre
        )

    def __repr__(self):
        return f"Usuario({self.nombre})"
