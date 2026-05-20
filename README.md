COMANDO EN TERMINAL abierta en el proyecto: 
python src\dataset_preprocessor.py
python src\main.py

# Sistema de Red Social - Índice Invertido
**Estructuras de Datos – CIN311/INF313/ICI313 (5/2026)**  
Escuela de Ingeniería Informática, Facultad de Ingeniería

---

## Integrantes


---

## Descripción del Proyecto

Sistema que modela una red social mediante índices invertidos, permitiendo búsquedas eficientes de publicaciones por términos y consulta de contactos entre usuarios. Los datos provienen del dataset **Social Media Sentiments Analysis** (Kaggle).

---

## Estructura del Proyecto

```
Estructura/
├── data/
│   ├── sentimentdataset.csv            ← dataset original de Kaggle
│   ├── sentimentdataset_procesado.csv  ← generado por el preprocesador
│   └── Stopword_English.txt            ← lista de stopwords
└── src/
    ├── dataset_preprocessor.py         ← limpieza y preprocesamiento del CSV
    ├── loader.py                        ← carga del CSV procesado a memoria
    ├── nodo.py                          ← clase Nodo genérico
    ├── lista_enlazada.py                ← lista enlazada implementada desde cero
    ├── usuario.py                       ← clase Usuario
    ├── post.py                          ← clase Post
    ├── indice_invertido.py              ← índice invertido de posts y usuarios
    └── main.py                          ← punto de entrada y menú principal
```

---

## Instrucciones de Ejecución

### Requisitos previos

- Python 3.12 o superior
- Librerías: `pandas`, `nltk` (solo para omw, no para stopwords)

Instalar dependencias:
```bash
pip install pandas nltk
```

### Paso 1 - Preprocesar el dataset

Debe ejecutarse una sola vez, o cada vez que se quiera regenerar el CSV procesado:

```bash
python src/dataset_preprocessor.py
```

Esto genera el archivo `data/sentimentdataset_procesado.csv`.

### Paso 2 - Ejecutar el programa

```bash
python src/main.py
```

Al iniciarse, el programa pedirá la ruta del dataset. Presionar **Enter** para usar la ruta por defecto.

---

## Descripción de las Estructuras de Datos

### Nodo (`nodo.py`)

Unidad básica de la lista enlazada. Contiene un `dato` de cualquier tipo y un puntero `siguiente` al próximo nodo. Si `siguiente` es `None`, es el último nodo de la lista.

```
┌─────────────┬──────────┐
│    dato     │ siguiente│ ──→ siguiente Nodo (o None)
└─────────────┴──────────┘
```

### ListaEnlazada (`lista_enlazada.py`)

Lista enlazada simple implementada con Nodos propios. No utiliza listas ni estructuras internas de Python. Métodos principales:

- `insertar(dato)` — inserta al final de la lista
- `insertar_sin_duplicado(dato, clave_fn)` — inserta solo si no existe ya un elemento con esa clave
- `buscar(clave, clave_fn)` — recorre la lista buscando por clave
- `contiene(clave, clave_fn)` — retorna True si existe el elemento
- `a_lista_python()` — convierte la lista enlazada a lista Python para recorrer
- `largo()` — cuenta los nodos de la lista

### Usuario (`usuario.py`)

Representa un perfil de la red social. Atributos:

- `nombre` — identificador del usuario
- `amigos` — `ListaEnlazada` de objetos `Usuario` con sus contactos

### Post (`post.py`)

Representa una publicación. Atributos:

- `id_post` — identificador único
- `autor` — nombre del usuario que publicó
- `texto` — texto original del post
- `hashtags` — lista de hashtags del post
- `likes` — cantidad de likes recibidos
- `liked_by` — `ListaEnlazada` de `Usuario` que dieron like (estructura disponible; dataset no provee esta información)

### IndiceInvertido (`indice_invertido.py`)

Implementado sobre un diccionario de Python (permitido por el enunciado) donde cada valor es una `ListaEnlazada` propia. Se crean dos instancias:

**Índice de Posts:**
```
"sunday"  → ListaEnlazada → [Post(11), Post(45), Post(203)]
"beach"   → ListaEnlazada → [Post(11), Post(78)]
"workout" → ListaEnlazada → [Post(2),  Post(99)]
```

**Índice de Usuarios:**
```
"User123"     → Usuario(amigos → ListaEnlazada → [Usuario, Usuario, ...])
"FitnessFan"  → Usuario(amigos → ListaEnlazada → [Usuario, Usuario, ...])
```

---

## Descripción de Funciones Principales

### `dataset_preprocessor.py`

| Función | Descripción |
|---------|-------------|
| `cargar_stopwords(ruta_txt)` | Lee el archivo de stopwords separadas por coma y retorna un conjunto |
| `limpiar_texto(texto)` | Convierte a minúsculas, elimina URLs, menciones, hashtags, caracteres especiales y stopwords |
| `generar_amigos(usuario, todos, n)` | Asigna aleatoriamente n amigos a cada usuario |
| `procesar_dataset()` | Orquesta la limpieza, eliminación de columnas y generación de la columna amigos |

### `loader.py`

| Función | Descripción |
|---------|-------------|
| `cargar_dataset(ruta_csv)` | Lee el CSV procesado y retorna una lista de diccionarios con los campos normalizados |

### `lista_enlazada.py`

| Función | Descripción |
|---------|-------------|
| `insertar(dato)` | Recorre hasta el final e inserta un nuevo Nodo |
| `insertar_sin_duplicado(dato, clave_fn)` | Verifica existencia antes de insertar para evitar duplicados |
| `buscar(clave, clave_fn)` | Recorre la lista comparando claves hasta encontrar o retornar None |
| `a_lista_python()` | Recorre la lista enlazada y retorna sus datos como lista Python |

### `indice_invertido.py`

| Función | Descripción |
|---------|-------------|
| `insertar_post(termino, post)` | Crea la lista del término si no existe e inserta el Post sin duplicar |
| `buscar_por_termino(termino)` | Retorna todos los Posts asociados al término como lista Python |
| `insertar_usuario(nombre, usuario)` | Registra un Usuario en el índice bajo su nombre como clave |
| `buscar_usuario(nombre)` | Retorna el objeto Usuario correspondiente al nombre, o None |

### `main.py`

| Función | Descripción |
|---------|-------------|
| `construir_indices(registros)` | Crea objetos Post y Usuario y los indexa en ambos índices invertidos |
| `buscar_posts(indice_posts)` | Filtra stopwords de la consulta y busca posts que contengan todos los términos (AND) |
| `buscar_amigos(indice_usuarios)` | Busca un usuario y lista todos sus contactos |
| `menu_principal()` | Carga el dataset, construye los índices y presenta el menú de opciones |

---

## Algoritmo de Construcción del Índice

1. El preprocesador limpia cada texto y elimina stopwords, generando `clean_text`
2. El loader lee el CSV y normaliza los campos en diccionarios
3. `construir_indices` recorre cada registro y:
   - Crea un objeto `Post` con los datos del registro
   - Indexa el post por cada término de `clean_text` y por cada hashtag
   - Crea o recupera el objeto `Usuario` del índice
   - Agrega sus amigos como objetos `Usuario` a su `ListaEnlazada`

## Algoritmo de Búsqueda de Posts

1. Se recibe la consulta del usuario y se filtra por stopwords
2. Se obtienen los posts del primer término desde el índice
3. Por cada término adicional, se eliminan los posts que no lo contengan
4. Se muestran solo los posts que contienen **todos** los términos buscados (AND)

---

## Dataset

**Nombre:** Social Media Sentiments Analysis Dataset  
**Fuente:** [Kaggle - kashishparmar02](https://www.kaggle.com/datasets/kashishparmar02/social-media-sentiments-analysis-dataset)  
**Columnas originales:** Text, User, Hashtags, Likes, Platform, Sentiment, Retweets, Timestamp, Country, Year, Month, Day, Hour  
**Columnas tras preprocesamiento:** Text, User, Hashtags, Likes, clean_text, amigos  
**Filas:** 732