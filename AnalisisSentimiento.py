
import regex as re
import os
from cleantext import clean
import json
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


def leer_stopwords(self, path):
    with open(path) as f:
        # Lee las stopwords del archivo y las guarda en una lista
        mis_stopwords = [line.strip() for line in f]
    return mis_stopwords

def tratamientoTextos(self, info):
    #Le pasa un stopword de palabras en español a la lista de palabras que le llega
    stop_words_sp = self.leer_stopwords("./StopWords/stop_words_spanish.txt")
    pasarStopWords = [i for i in texto if i not in stop_words_sp]
