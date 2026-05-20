# indice_invertido.py
# Implementa el índice invertido usando un diccionario de Python como mapa
# (permitido por el enunciado) donde cada valor es una ListaEnlazada propia.
#
# Se crean dos instancias de IndiceInvertido en main.py:
#   - indice_posts:    clave = término/hashtag  → lista de Posts
#   - indice_usuarios: clave = nombre de usuario → lista de Usuarios (amigos)

from lista_enlazada import ListaEnlazada

class IndiceInvertido:
    def __init__(self):
        # El diccionario actúa como mapa: clave → ListaEnlazada
        self.indice = {}

    # -------------------------------------------------------
    # Métodos para el índice de POSTS
    # -------------------------------------------------------

    def insertar_post(self, termino, post):
        """
        Asocia un Post a un término.
        Si el término no existe en el índice, crea su lista.
        No inserta el mismo post dos veces para el mismo término.
        """
        termino = termino.lower().strip()
        if not termino:
            return
        if termino not in self.indice:
            self.indice[termino] = ListaEnlazada()
        self.indice[termino].insertar_sin_duplicado(
            post,
            clave_fn=lambda p: p.id_post
        )

    def buscar_por_termino(self, termino):
        """
        Retorna una lista Python con los Posts asociados al término.
        Retorna lista vacía si el término no existe.
        """
        termino = termino.lower().strip()
        if termino not in self.indice:
            return []
        return self.indice[termino].a_lista_python()

    # -------------------------------------------------------
    # Métodos para el índice de USUARIOS
    # -------------------------------------------------------

    def insertar_usuario(self, nombre_clave, usuario):
        """
        Inserta un objeto Usuario en el índice bajo su nombre como clave.
        Si ya existe la clave, no reemplaza (el usuario ya fue insertado).
        """
        nombre_clave = nombre_clave.strip()
        if nombre_clave not in self.indice:
            self.indice[nombre_clave] = usuario  # el valor ES el objeto Usuario
                                                  # (su lista de amigos ya viene adentro)

    def buscar_usuario(self, nombre):
        """
        Retorna el objeto Usuario con ese nombre, o None si no existe.
        """
        return self.indice.get(nombre.strip(), None)

    def todos_los_usuarios(self):
        """Retorna lista Python con todos los objetos Usuario del índice."""
        return list(self.indice.values())
