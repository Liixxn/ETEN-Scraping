from nltk.sentiment import SentimentIntensityAnalyzer
import regex as re
import statistics
from cleantext import clean
import json
import nltk


# Las siguientes 3 lineas solo se ejecutan una vez para descargar algunos elementos:
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('vader_lexicon')


# Metodo que aplica el fichero stopWords
def leer_stopwords(path):
    with open(path) as f:
        # Lee las stopwords del archivo y las guarda en una lista
        mis_stopwords = [line.strip() for line in f]
    return mis_stopwords


# Metodo que porcentualiza los resultados del analisis de sentimiento


def sacarPorcentajeAnalisis(resultados):
    resultadosFinales = {}
    for key, resultados_valores in resultados.items():
        porcentajes = []
        # Sacamos el total de sumar los comentarios Positivos (resultados_valores[0]) y los negativos (resultados_valores[1])
        totalPosNeg = resultados_valores[0] + resultados_valores[1]
        # Sacamos los porcentajes
        # Si no hay comentarios positivos ni negativos igualamos el porcentaje poniendo 50% a cada uno
        if totalPosNeg != 0:
            porcenPos = round(((resultados_valores[0] * 100) / totalPosNeg), 2)
            porcenNeg = round(((resultados_valores[1] * 100) / totalPosNeg), 2)
        else:
            porcenPos = 50
            porcenNeg = 50

        # Metemos los porcentajes en una lista
        porcentajes.append(porcenPos)
        porcentajes.append(porcenNeg)
        # Metemos la lista con los porcentajes dentro del diccionario con la key correspondiente
        resultadosFinales[key] = porcentajes
    return resultadosFinales

# Para comprobar si los valores del array son todos 0


def es_entero_de_cero(arr):
    for num in arr:
        if not isinstance(num, int) or num != 0:
            return False
    return True


def analisisSentimiento():
    # Leemos los datos
    global resultados_valores
    with open('comentarios.json', 'r', encoding='utf-8') as f:
        comments = json.load(f)

    # Tratamos los datos
    for key, value in comments.items():
        listaComentariosTratados = []
        for coment in value:
            # Quitamos emojis
            coment = clean(coment, no_emoji=True)
            # Quitamos simbolos
            textoSinSimbolos = re.sub("[^0-9A-Za-z_]", " ", coment)
            # Tokenizamos cada texto
            textoTokenizado = nltk.tokenize.word_tokenize(textoSinSimbolos)
            # Pasamos todo a minusculas
            textoMinusculas = (map(lambda x: x.lower(), textoTokenizado))
            # Seleccionamos nuestro fichero de stopwords y lo aplicamos
            stop_words_sp = leer_stopwords(
                "./StopWords/stop_words_spanish.txt")
            pasarStopWords = [
                i for i in textoMinusculas if i not in stop_words_sp]
            # Metemos el resultado final en una lista llamada listaComentariosTratados
            listaComentariosTratados.append(pasarStopWords)
        # metemos la listaComentariosTratados en el diccionario con su respectiva clave la cual es la url del video
        comments[key] = listaComentariosTratados

    # inicializar el analizador de sentimientos de NLTK
    analyzer = SentimentIntensityAnalyzer()

    # Diccionario para guardar los resultados de cada análisis
    resultados = {}

    for key, valores in comments.items():
        # Crear listas para guardar los valores de cada comentario
        resultados_valores = []
        positivos = []
        negativos = []

        # Recorremos los valores de cada key
        for valor in valores:
            # Unimos en una cadena cada token sacado al hacer el tratamiento del texto
            text = ' '.join(valor)
            # Analizamos el sentimiento con SentimentIntensityAnalyzez
            sentimiento = analyzer.polarity_scores(text)

            # Metemos en arrays diferentes los comentarios positivos y los negativos
            positivos.append(sentimiento['pos'])
            negativos.append(sentimiento['neg'])

        # Para cada Key hacemos la media de los comentarios
        if len(positivos) == 0 or len(negativos) == 0:
            media_positivos = 0
            media_negativos = 0
        else:
            media_positivos = statistics.mean(positivos)
            media_negativos = statistics.mean(negativos)

        # Metemos las medias en una lista
        resultados_valores.append(media_positivos)
        resultados_valores.append(media_negativos)

        # Guardamos los resultados de cada key en el diccionario de resultados
        resultados[key] = resultados_valores

    # LLamamos al metodo que nos saca el porcentaje de los comentarios y nos lo redondea a 2 decimales
    resultadosFinales = sacarPorcentajeAnalisis(resultados)

    datoFinalPositivo = []
    datoFinalNegativo = []
    # Pintamos resultados
    for key, resultados_valores in resultadosFinales.items():
        datoFinalPositivo.append(resultados_valores[0])
        datoFinalNegativo.append(resultados_valores[1])
        print(key + ' -> Positivo: ' +
              str(resultados_valores[0]) + ', Negativo: ' + str(resultados_valores[1]))

    if es_entero_de_cero(datoFinalPositivo):
        resultado_Pos = 0
        resultado_Neg = 100
    elif es_entero_de_cero(datoFinalNegativo):
        resultado_Pos = 100
        resultado_Neg = 0
    else:
        # Con esto el return devuelve la media final de los sentimientos pos y neg para poder guardarse en la BBDD
        resultado_Pos = round(statistics.mean(datoFinalPositivo), 2)
        resultado_Neg = round(statistics.mean(datoFinalNegativo), 2)
    return resultado_Pos, resultado_Neg
