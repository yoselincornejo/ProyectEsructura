# main.py
# Punto de entrada del sistema.
# Carga el dataset, construye los índices y presenta el menú por consola.

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from loader import cargar_dataset
from indice_invertido import IndiceInvertido
from usuario import Usuario
from post import Post
from dataset_preprocessor import cargar_stopwords


ruta_sw = os.path.join(os.path.dirname(__file__), "..", "data", "Stopword_English.txt")
stop_words = cargar_stopwords(ruta_sw)


def construir_indices(registros):
    indice_posts    = IndiceInvertido()
    indice_usuarios = IndiceInvertido()

    for i, reg in enumerate(registros):

        post = Post(
            id_post  = i,
            autor    = reg["usuario"],
            texto    = reg["texto"],
            hashtags = reg["hashtags"],
            likes    = reg["likes"],
        )

        for termino in reg["terminos"]:
            indice_posts.insertar_post(termino, post)

        for hashtag in reg["hashtags"]:
            indice_posts.insertar_post(hashtag, post)

        nombre = reg["usuario"]
        usuario = indice_usuarios.buscar_usuario(nombre)
        if usuario is None:
            usuario = Usuario(nombre)
            indice_usuarios.insertar_usuario(nombre, usuario)

        for nombre_amigo in reg["amigos"]:
            amigo = indice_usuarios.buscar_usuario(nombre_amigo)
            if amigo is None:
                amigo = Usuario(nombre_amigo)
                indice_usuarios.insertar_usuario(nombre_amigo, amigo)
            usuario.agregar_amigo(amigo)

    return indice_posts, indice_usuarios


def buscar_posts(indice_posts):
    entrada = input("\n  Ingrese término(s) de búsqueda (separados por espacio): ").strip().lower()
    if not entrada:
        print("  [!] No ingresó ningún término.")
        return

    # Filtrar stopwords de la consulta
    terminos = [t for t in entrada.split() if t not in stop_words]

    if not terminos:
        print("  [!] Todos los términos ingresados son stopwords, intente con otras palabras.")
        return

    # AND: cargar posts del primer término y filtrar los que no tengan los demás
    encontrados = {}
    for post in indice_posts.buscar_por_termino(terminos[0]):
        encontrados[post.id_post] = post

    for termino in terminos[1:]:
        ids_termino = {post.id_post for post in indice_posts.buscar_por_termino(termino)}
        for id_post in list(encontrados.keys()):
            if id_post not in ids_termino:
                del encontrados[id_post]

    if not encontrados:
        print(f"\n  No se encontraron posts para: {terminos}")
        return

    resultados = list(encontrados.values())
    print(f"\n  Se encontraron {len(resultados)} post(s):\n")

    for post in resultados:
        print(f"  [{post.id_post}] @{post.autor}")
        texto_corto = post.texto[:80] + ("..." if len(post.texto) > 80 else "")
        print(f"       Texto : {texto_corto}")
        print(f"       Likes : {post.likes}")
        print(f"       Tags  : {post.hashtags}")
        print()


def buscar_amigos(indice_usuarios):
    nombre = input("\n  Ingrese nombre de usuario: ").strip()
    if not nombre:
        print("  [!] No ingresó ningún nombre.")
        return

    usuario = indice_usuarios.buscar_usuario(nombre)
    if usuario is None:
        print(f"\n  Usuario '{nombre}' no encontrado en el índice.")
        return

    amigos = usuario.amigos.a_lista_python()
    if not amigos:
        print(f"\n  El usuario '{nombre}' no tiene amigos registrados.")
        return

    print(f"\n  Amigos de @{nombre} ({len(amigos)}):\n")
    for amigo in amigos:
        print(f"    - @{amigo.nombre}")


def menu_principal():
    print("=" * 50)
    print("   SISTEMA DE RED SOCIAL - ÍNDICE INVERTIDO")
    print("=" * 50)

    ruta_default = os.path.join(os.path.dirname(__file__), "..", "data", "sentimentdataset_procesado.csv")
    ruta = input(f"\nRuta del dataset [{ruta_default}]: ").strip()
    if not ruta:
        ruta = ruta_default

    registros = cargar_dataset(ruta)
    if not registros:
        print("[ERROR] No se cargaron registros. Verifique el archivo CSV.")
        sys.exit(1)

    print("\nConstruyendo índices, espere...")
    indice_posts, indice_usuarios = construir_indices(registros)
    print("[OK] Índices construidos correctamente.\n")

    while True:
        print("-" * 50)
        print("  MENÚ PRINCIPAL")
        print("-" * 50)
        print("  1. Buscar posts por término(s)")
        print("  2. Buscar amigos de un usuario")
        print("  3. Salir")
        print("-" * 50)

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            buscar_posts(indice_posts)
        elif opcion == "2":
            buscar_amigos(indice_usuarios)
        elif opcion == "3":
            print("\n  Hasta luego.\n")
            break
        else:
            print("  [!] Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu_principal()