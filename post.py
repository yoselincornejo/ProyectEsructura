# post.py
# Representa una publicación de la red social.
# Los usuarios que dieron like se almacenan en una lista enlazada propia.

from lista_enlazada import ListaEnlazada

class Post:
    def __init__(self, id_post, autor, texto, hashtags, likes):
        self.id_post   = id_post    # identificador único (número de fila)
        self.autor     = autor      # string con el nombre del usuario
        self.texto     = texto      # texto original del post
        self.hashtags  = hashtags   # lista Python de strings (viene del loader)
        self.likes     = likes      # cantidad de likes (entero)
        self.liked_by  = ListaEnlazada()  # lista enlazada de Usuarios que dieron like

    def agregar_like(self, usuario):
        """Registra que un usuario dio like, sin duplicados."""
        self.liked_by.insertar_sin_duplicado(
            usuario,
            clave_fn=lambda u: u.nombre
        )

    def __repr__(self):
        return f"Post(id={self.id_post}, autor={self.autor})"
