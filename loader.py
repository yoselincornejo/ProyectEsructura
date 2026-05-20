
import csv
import ast
import os
import sys

def cargar_dataset(ruta_csv: str) -> list[dict]:
    """
    Carga el dataset ya preprocesado por dataset_preprocessor.py.
    Columnas esperadas: User, Text, Hashtags, Likes, clean_text, amigos
    """
    if not os.path.exists(ruta_csv):
        print(f"[ERROR] Archivo no encontrado: {ruta_csv}")
        sys.exit(1)

    columnas_requeridas = {"User", "Text", "Hashtags", "Likes", "clean_text", "amigos"}
    registros = []

    with open(ruta_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)

        encabezados = set(lector.fieldnames or [])
        faltantes = columnas_requeridas - encabezados
        if faltantes:
            print(f"[ADVERTENCIA] Columnas faltantes en el CSV: {faltantes}")
            print(f"  Columnas encontradas: {encabezados}")

        for numero_fila, fila in enumerate(lector, start=2):  # start=2 porque fila 1 es el header
            usuario   = fila.get("User", "").strip()
            texto_raw = fila.get("Text", "").strip()

            # Saltar filas sin datos esenciales
            if not usuario or not texto_raw:
                continue

            # amigos viene como string representando una lista Python: "['user1', 'user2', ...]"
            amigos_raw = fila.get("amigos", "[]").strip()
            try:
                amigos = ast.literal_eval(amigos_raw)
                if not isinstance(amigos, list):
                    amigos = []
            except (ValueError, SyntaxError):
                print(f"[ADVERTENCIA] Fila {numero_fila}: no se pudo parsear 'amigos': {amigos_raw[:50]}")
                amigos = []

            # Likes puede venir vacío o con valor no numérico
            try:
                likes = int(float(fila.get("Likes", 0) or 0))
            except ValueError:
                likes = 0

            # Hashtags: separados por espacio, limpiar '#' y espacios extra
            hashtags_raw = fila.get("Hashtags", "").strip()
            hashtags = [h.strip().lstrip("#") for h in hashtags_raw.split() if h.strip()]

            # Términos del texto limpio: ya vienen sin stopwords ni puntuación
            clean_text = fila.get("clean_text", "").strip()
            terminos = clean_text.split() if clean_text else []

            registro = {
                "usuario":   usuario,
                "texto":     texto_raw,
                "terminos":  terminos,   # palabras limpias para el índice invertido de posts
                "hashtags":  hashtags,   # lista de hashtags sin '#'
                "likes":     likes,
                "amigos":    amigos,     # lista de strings con nombres de usuarios amigos
            }
            registros.append(registro)

    print(f"[OK] Dataset cargado: {len(registros)} registros desde '{ruta_csv}'")
    return registros


if __name__ == "__main__":
    # Uso: python src/loader.py data/sentimentdataset_procesado.csv
    if len(sys.argv) < 2:
        print("Uso: python loader.py <ruta_al_csv>")
        sys.exit(1)

    datos = cargar_dataset(sys.argv[1])

    print("\n--- Muestra de los primeros 3 registros ---")
    for i, d in enumerate(datos[:3]):
        print(f"\nRegistro {i + 1}:")
        for clave, valor in d.items():
            # Truncar listas largas para no saturar la consola
            if isinstance(valor, list) and len(valor) > 5:
                print(f"  {clave}: {valor[:5]} ... ({len(valor)} elementos)")
            else:
                print(f"  {clave}: {valor}")