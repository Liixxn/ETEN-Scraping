import os

import joblib
import numpy as np
from pathlib import Path
from nltk import word_tokenize, RegexpTokenizer
import natsort
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd





# Funcion que pasa a minusculas y elimina los signos de puntuacion
def tratamientoBasico(df_sinTratar):
    listatokens = []

    for indiceDF, fila in df_sinTratar.iterrows():
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(fila["Receta"])
        listatokens.append(tokens)

    for i in range(len(listatokens)):
        listatokens[i] = [w.lower() for w in listatokens[i]]
        df_sinTratar["Receta"][i] = listatokens[i]

    return df_sinTratar



# Funcion que aplica las stopwords al datafram que se le pasa
def quit_stopwords(df_conStopwords):
    listaStopwords = []
    try:
        # Se carga en fichero de las stopwords
        ruta = os.getcwd()
        data_folder = Path(ruta + "/StopWords/")
        archivoAbir = data_folder / "stop_words_spanish.txt"

        txt_stopwords = open(archivoAbir, "r")
        stop_words = txt_stopwords.read()

        filtered_sentence = []

        for indiceDF, fila in df_conStopwords.iterrows():
            filtered_sentence = [w for w in fila["Receta"] if not w in stop_words]
            listaStopwords.append(filtered_sentence)

        for i in range(len(listaStopwords)):
            df_conStopwords["Receta"][i] = listaStopwords[i]

    except Exception as e:
        print(e)

    return df_conStopwords


# Funcion que aplica el stemming al dataframe que se le pasa
def stemming(df_sinStemming):
    listaStemming = []
    lista_stem = []

    # Se establece el idioma
    stemmer = SnowballStemmer('spanish')

    for indiceDF, fila in df_sinStemming.iterrows():
        if indiceDF != 0:
            lista_stem.append(listaStemming)
            listaStemming = []

        for word in range(len(fila["Receta"])):
            w = stemmer.stem(fila["Receta"][word])
            listaStemming.append(w)

    for i in range(len(lista_stem)):
        df_sinStemming["Receta"][i] = lista_stem[i]

    return df_sinStemming