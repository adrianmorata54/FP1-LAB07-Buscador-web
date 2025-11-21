from collections import Counter

# Conjunto con palabras huecas (se ignoran en las búsquedas, no se indexan)
STOP_WORDS = {'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o'}

# Caracteres de puntuación
PUNTUACION = '!¡"#$%&\'()*+,-./:;<=>?¿@[\\]^_`{|}~'

def normalizar_texto(texto: str) -> list[str]:
    """
    Recibe un texto, lo limpia y devuelve una lista de palabras. En el proceso de limpieza, 
    la función:
    1. Convierte el texto a minúsculas.
    2. Quita los signos de puntuación (los caracteres contenidos en PUNTUACION).
    3.Filtra las palabras huecas (las palabras contenidas en STOP_WORDS).
    
    Ejemplo: normalizar_texto("¡Hola, Mundo!") debería devolver ['hola', 'mundo']

    Parámetros:
    texto (str): El texto a normalizar.
    
    Devuelve:
    list[str]: Una lista de palabras normalizadas.
    """    
    #TODO: Ejercicio 1
    texto_normalizado = texto.lower().split()
    for palabra in texto_normalizado:
        if palabra not in STOP_WORDS:
            palabra_nueva = palabra
            for caracter in palabra:
                if caracter in PUNTUACION:
                    palabra_nueva = palabra_nueva.replace(caracter, '')
                elif str(caracter).isnumeric():
                    palabra_nueva = palabra_nueva.replace(caracter, '')
            texto_normalizado[texto_normalizado.index(palabra)] = palabra_nueva
    texto_copia = texto_normalizado.copy()
    for palabra in texto_copia:
        if palabra in STOP_WORDS:
            texto_normalizado.remove(palabra)
    return texto_normalizado
        

def procesar_url_en_indice(url: str, texto: str, indice: dict[str, set[str]]):
    """
    Recibe la URL, el texto ya extraído de esa URL y un diccionario que indexa
    URLs de páginas web usando las palabras contenidas en la web como clave.
    La función actualiza el diccionario para incluir la URL en los conjuntos asociados
    a las palabras que aparecen en el texto.
    
    Parámetros:
    url (str): La URL de la página web.
    texto (str): El texto extraído de la página web.
    indice (dict[str, set[str]]): El índice de búsqueda a actualizar.
    """
    # TODO: Ejercicio 2
    texto_palabras = normalizar_texto(texto)
    for p in texto_palabras:
        if p not in indice:
            indice[p] = set()
        indice[p].add(url)
    return None


def buscar_palabra_simple(palabra: str, indice: dict[str, set[str]]) -> set[str]:
    """
    Recibe una única palabra de búsqueda y el índice, y devuelve
    un conjunto de URLs donde se encontró esa palabra.
    Si la palabra no está en el índice, debe devolver un conjunto vacío.
    Antes de buscarla, la palabra será normalizada.

    Parámetros:
    palabra (str): La palabra a buscar.
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    set[str]: Un conjunto de URLs donde se encontró la palabra.
    """    
    # TODO: Ejercicio 3
    palabra = normalizar_texto(palabra)
    busqueda = palabra[0]
    if busqueda not in indice:
        return set()
    else:
        return indice[busqueda]


def buscar_palabras_or(frase: str, indice: dict[str, set[str]]) -> set[str]:
    """
    Recibe una frase de búsqueda y el índice, y devuelve
    un conjunto de URLs donde se encuentren alguna de las palabras de la frase.
    Si ninguna de las palabras están en el índice, debe devolver un conjunto vacío.
    La función normalizará el texto de la frase antes de buscar.

    Parámetros:
    frase (str): La frase de búsqueda.
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    set[str]: Un conjunto de URLs donde se encontraron todas las palabras.
    """    
    # TODO: Ejercicio 4
    texto_normalizado = normalizar_texto(frase)
    res = set()
    for palabra in texto_normalizado:
        urls = buscar_palabra_simple(palabra, indice)
        res = res.union(urls)
    return res
        


def buscar_palabras_and(frase: str, indice: dict[str, set[str]]) -> set[str]:
    """
    Recibe una frase de búsqueda y el índice, y devuelve
    un conjunto de URLs donde se encuentren todas las palabras de la frase.
    Si ninguna de las palabras están en el índice, debe devolver un conjunto vacío.
    La función normalizará el texto de la frase antes de buscar.

    Parámetros:
    frase (str): La frase de búsqueda.
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    set[str]: Un conjunto de URLs donde se encontraron todas las palabras.
    """
    # TODO: Ejercicio 5
    texto_normalizado = normalizar_texto(frase)
    urls = buscar_palabra_simple(texto_normalizado[0], indice)
    for i in range(1, len(texto_normalizado)):
        estado = buscar_palabra_simple(texto_normalizado[i], indice)
        urls = urls.intersection(estado)
    return urls

    


def procesar_url_en_indice_top_n(url: str, texto: str, indice: dict[str, set[str]], top_n: int=1000):
    """
    Recibe la URL, el texto ya extraído de esa URL y un diccionario que indexa
    URLs de páginas web usando las palabras contenidas en la web como clave.
    La función actualiza el diccionario para incluir la URL en los conjuntos asociados
    a las 'top_n' palabras más frecuentes de entre las que aparecen en el texto.

    Parámetros:
    url (str): La URL de la página web.
    texto (str): El texto extraído de la página web.
    indice (dict[str, set[str]]): El índice de búsqueda a actualizar.
    top_n (int): Número de palabras más frecuentes a indexar.
    """
    # TODO: Ejercicio 6
    texto_normalizado = normalizar_texto(texto)
    lista = Counter(texto_normalizado).most_common(top_n)
    frase = []
    for conjunto in lista:
        frase.append(conjunto[0])
    for p in frase:
        if p not in indice:
            indice[p] = set()
        indice[p].add(url)
    return None


def calcula_estadisticas_indice(indice: dict[str, set[str]]) -> tuple[int, int, float]:
    """
    Recibe un índice y calcula estadísticas sobre él.

    Parámetros:
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    tuple[int, int, float]: Una tupla con tres valores:
        - Número total de palabras indexadas.
        - Número total de URLs indexadas (sin duplicados).
        - Promedio de URLs por palabra: cuántas URLs hay indexadas para cada palabra, en promedio.
    """
    # TODO: Ejercicio 7
    n_palabras_indexadas = len(indice.keys())
    urls = set()
    total_urls = 0
    for url in indice.values():
        urls = urls.union(url)
        for enlace in url:
            total_urls += 1
    promedio = total_urls/n_palabras_indexadas
    return [n_palabras_indexadas, len(urls), promedio]
    