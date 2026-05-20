#antes de ejecutar este script, abrir una terminal y ejecutar los siguientes comandos: py -3.12 -m pip install nltk pandas , pip install nltk pandas , python -m pip install nltk pandas
import os
import re
import random
import pandas as pd


def cargar_stopwords(ruta_txt):
    with open(ruta_txt, encoding="utf-8") as f:
        contenido = f.read()
    palabras = [p.strip() for p in contenido.split(",") if p.strip()]
    return set(palabras)


# Cargar stopwords desde el archivo
ruta_sw = os.path.join(os.path.dirname(__file__), "..", "data", "Stopword_English.txt")
stop_words = cargar_stopwords(ruta_sw)


def limpiar_texto(texto):
    texto = str(texto).lower()
    texto = re.sub(r"http\S+|www\S+|https\S+", "", texto)
    texto = re.sub(r"@[\w]*", "", texto)
    texto = re.sub(r"#[\w]*", "", texto)
    texto = re.sub(r"[^a-z\s]", "", texto)
    palabras = [p for p in texto.split() if p not in stop_words]
    return " ".join(palabras)


def generar_amigos(usuario, todos_los_usuarios, n=5):
    candidatos = [u for u in todos_los_usuarios if u != usuario]
    return random.sample(candidatos, min(n, len(candidatos)))


def procesar_dataset():
    ruta = os.path.join(os.path.dirname(__file__), "..", "data", "sentimentdataset.csv")
    df = pd.read_csv(ruta)

    # Limpiar texto
    df["clean_text"] = df["Text"].apply(limpiar_texto)

    # Eliminar columnas innecesarias
    columnas_a_eliminar = ["Platform", "Sentiment", "Retweets", "Timestamp", "Country", "Year", "Month", "Day", "Hour", "Unnamed: 0", "Unnamed: 0.1"]
    df.drop(columns=[c for c in columnas_a_eliminar if c in df.columns], inplace=True)

    # Crear columna de amigos
    df["User"] = df["User"].fillna("").astype(str)
    usuarios = df["User"].unique().tolist()
    df["amigos"] = df["User"].apply(lambda u: generar_amigos(u, usuarios))

    return df


if __name__ == "__main__":
    df = procesar_dataset()
    print(df.head())
    print(f"\nColumnas: {df.columns.tolist()}")
    print(f"Filas: {len(df)}")

    # Guardar el CSV procesado
    ruta_salida = os.path.join(os.path.dirname(__file__), "..", "data", "sentimentdataset_procesado.csv")
    df.to_csv(ruta_salida, index=False)
    print(f"\n[OK] CSV guardado en: {ruta_salida}")