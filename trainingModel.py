
import os

import joblib
import numpy as np
from pathlib import Path
from nltk import word_tokenize, RegexpTokenizer
import natsort
from nltk.stem import SnowballStemmer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline


import procesamientoTexto

pd.options.mode.chained_assignment = None

df_recetas = pd.DataFrame(columns=["Receta", "Categoria"])

carpetaCategorias = "categorias"
rutasCategorias = dict()

def leerTodasCateogrias():

    contadorCategorias = 1

    for categoria in os.listdir(carpetaCategorias):
        rutaCategoria = carpetaCategorias+"/"+categoria

        rutasCategorias[contadorCategorias] = rutaCategoria

        contadorCategorias += 1







def leerRecetasCategorias():

    listaRecetas = []
    listaCategorias = []

    for num_categoria, categoria in rutasCategorias.items():

        sorted_files = natsort.natsorted(os.listdir(categoria), reverse=False)

        for receta in sorted_files:
            receta = categoria+"/"+receta
            #f = open(receta, "r", encoding="ISO 8859-1")
            f = open(receta, "r", encoding="utf-8", errors="ignore")
            f = f.read().replace("\n", " ")

            listaRecetas.append(f)
            listaCategorias.append(num_categoria)

    return listaRecetas, listaCategorias








def calculate_weightKnn(df_entrenamiento):
    listaUnidos = []
    for i in range(len(df_entrenamiento["Receta"])):
        unidos = " ".join(df_entrenamiento["Receta"][i])

        df_entrenamiento["Receta"][i] = str(unidos)

    X = df_entrenamiento['Receta']
    y = df_entrenamiento['Categoria']

    model_knn = Pipeline([('vect', CountVectorizer(lowercase=False, preprocessor=None, tokenizer=None, stop_words=None,
                                                   min_df=1)),
                          ('tfidf', TfidfTransformer()),
                          ('knn', KNeighborsClassifier())])


    model_knn.fit(X, y)


    precisionKnn = round(model_knn.score(X, y) * 100, 2)

    y_train_pred = model_knn.predict(X)

    cm_train = confusion_matrix(y, y_train_pred)

    df_matrix_confusion_entrenamiento = pd.DataFrame(cm_train)

    sumaPositivos = 0
    sumaFalsosPositivos = 0

    # Obtener los resultados de la matriz de confusion
    for i in range(len(df_matrix_confusion_entrenamiento)):
        for j in range(len(df_matrix_confusion_entrenamiento[i])):
            if i == j:
                sumaPositivos += df_matrix_confusion_entrenamiento[i][j]
            else:
                sumaFalsosPositivos += df_matrix_confusion_entrenamiento[i][j]

    df_matrix_confusion_precision_recall = df_matrix_confusion_entrenamiento.copy()

    listaPrecision = []
    listaRecall = []

    # suma de diagonal
    true_pos = np.diag(df_matrix_confusion_precision_recall)
    # suma de columnas
    false_pos = np.sum(df_matrix_confusion_precision_recall, axis=0) - true_pos
    # suma de filas
    false_neg = np.sum(df_matrix_confusion_precision_recall, axis=1) - true_pos

    for i in range(len(df_matrix_confusion_precision_recall)):
        recallCategoria = round((true_pos[i] / (true_pos[i] + false_pos[i])) * 100, 2)
        listaRecall.append(recallCategoria)
        precisionlCategoria = round((true_pos[i] / (true_pos[i] + false_neg[i])) * 100, 2)
        listaPrecision.append(precisionlCategoria)

    df_matrix_confusion_precision_recall["Precision"] = listaPrecision
    ultimoIndice = df_matrix_confusion_precision_recall.index[-1]
    df_matrix_confusion_precision_recall["Recall"] = listaRecall

    return df_matrix_confusion_precision_recall, precisionKnn, sumaPositivos, sumaFalsosPositivos, model_knn



# Funcion que cuenta el numero de apariciones de cada palabra en cada receta y calcula su peso con Random Forest

def calculate_weightRF(df_entrenamiento):
    listaUnidos = []
    for i in range(len(df_entrenamiento["Receta"])):
        unidos = " ".join(df_entrenamiento["Receta"][i])

        df_entrenamiento["Receta"][i] = str(unidos)

    X = df_entrenamiento['Receta']
    y = df_entrenamiento['Categoria']
    print(X)
    model_rf = Pipeline([('vect', CountVectorizer(lowercase=False, preprocessor=None, tokenizer=None, stop_words=None,
                                                  min_df=1)),
                         ('tfidf', TfidfTransformer()),
                         ('rf', RandomForestClassifier())])
    try:
        model_rf.fit(X, y)
    except Exception as e:
        print(e)
    precisionRF = round(model_rf.score(X, y) * 100, 2)

    y_train_pred = model_rf.predict(X)
    cm_train = confusion_matrix(y, y_train_pred)

    df_matrix_confusion_entrenamiento = pd.DataFrame(cm_train)

    sumaPositivos = 0
    sumaFalsosPositivos = 0



    # Obtener los resultados de la matriz de confusion
    for i in range(len(df_matrix_confusion_entrenamiento)):
        for j in range(len(df_matrix_confusion_entrenamiento[i])):
            if i == j:
                sumaPositivos += df_matrix_confusion_entrenamiento[i][j]
            else:
                sumaFalsosPositivos += df_matrix_confusion_entrenamiento[i][j]

    df_matrix_confusion_precision_recall = df_matrix_confusion_entrenamiento.copy()

    listaPrecision = []
    listaRecall = []

    # suma de diagonal
    true_pos = np.diag(df_matrix_confusion_precision_recall)
    # suma de columnas
    false_pos = np.sum(df_matrix_confusion_precision_recall, axis=0) - true_pos
    # suma de filas
    false_neg = np.sum(df_matrix_confusion_precision_recall, axis=1) - true_pos



    for i in range(len(df_matrix_confusion_precision_recall)):
        recallCategoria = round((true_pos[i] / (true_pos[i] + false_pos[i]))*100, 2)
        listaRecall.append(recallCategoria)
        precisionlCategoria = round((true_pos[i] / (true_pos[i] + false_neg[i]))*100, 2)
        listaPrecision.append(precisionlCategoria)

    df_matrix_confusion_precision_recall["Precision"] = listaPrecision
    ultimoIndice = df_matrix_confusion_precision_recall.index[-1]
    df_matrix_confusion_precision_recall["Recall"] = listaRecall

    return df_matrix_confusion_precision_recall, precisionRF, sumaPositivos, sumaFalsosPositivos, model_rf




# Funcion que cuenta el numero de apariciones de cada palabra en cada receta y calcula su peso con Naive Bayes

def calculate_weightNB(df_entrenamiento):
    listaUnidos = []
    for i in range(len(df_entrenamiento["Receta"])):
        unidos = " ".join(df_entrenamiento["Receta"][i])

        df_entrenamiento["Receta"][i] = str(unidos)

    X = df_entrenamiento['Receta']
    y = df_entrenamiento['Categoria']

    model_nb = Pipeline([('vect', CountVectorizer(lowercase=False, preprocessor=None, tokenizer=None, stop_words=None,
                                                  min_df=1)),
                         ('tfidf', TfidfTransformer()),
                         ('nb', MultinomialNB())])

    model_nb.fit(X, y)

    precisionNB = round(model_nb.score(X, y) * 100, 2)

    y_train_pred = model_nb.predict(X)
    cm_train = confusion_matrix(y, y_train_pred)

    df_matrix_confusion_entrenamiento = pd.DataFrame(cm_train)

    sumaPositivos = 0
    sumaFalsosPositivos = 0

    # Obtener los resultados de la matriz de confusion
    for i in range(len(df_matrix_confusion_entrenamiento)):
        for j in range(len(df_matrix_confusion_entrenamiento[i])):
            if i == j:
                sumaPositivos += df_matrix_confusion_entrenamiento[i][j]
            else:
                sumaFalsosPositivos += df_matrix_confusion_entrenamiento[i][j]

    df_matrix_confusion_precision_recall = df_matrix_confusion_entrenamiento.copy()

    listaPrecision = []
    listaRecall = []

    # suma de diagonal
    true_pos = np.diag(df_matrix_confusion_precision_recall)
    # suma de columnas
    false_pos = np.sum(df_matrix_confusion_precision_recall, axis=0) - true_pos
    # suma de filas
    false_neg = np.sum(df_matrix_confusion_precision_recall, axis=1) - true_pos

    for i in range(len(df_matrix_confusion_precision_recall)):
        recallCategoria = round((true_pos[i] / (true_pos[i] + false_pos[i])) * 100, 2)
        listaRecall.append(recallCategoria)
        precisionlCategoria = round((true_pos[i] / (true_pos[i] + false_neg[i])) * 100, 2)
        listaPrecision.append(precisionlCategoria)

    df_matrix_confusion_precision_recall["Precision"] = listaPrecision
    ultimoIndice = df_matrix_confusion_precision_recall.index[-1]
    df_matrix_confusion_precision_recall["Recall"] = listaRecall


    return df_matrix_confusion_precision_recall, precisionNB, sumaPositivos, sumaFalsosPositivos, model_nb


def calculateweightSVM(df_entrenamiento):
    listaUnidos = []
    for i in range(len(df_entrenamiento["Receta"])):
        unidos = " ".join(df_entrenamiento["Receta"][i])

        df_entrenamiento["Receta"][i] = str(unidos)

    X = df_entrenamiento['Receta']
    y = df_entrenamiento['Categoria']

    model_svc = Pipeline([('vect', CountVectorizer(lowercase=False, preprocessor=None, tokenizer=None, stop_words=None,
                                                  min_df=1)),
                         ('tfidf', TfidfTransformer()),
                         ('nb', SVC())])

    model_svc.fit(X, y)

    precisionNB = round(model_svc.score(X, y) * 100, 2)

    y_train_pred = model_svc.predict(X)
    cm_train = confusion_matrix(y, y_train_pred)

    df_matrix_confusion_entrenamiento = pd.DataFrame(cm_train)

    sumaPositivos = 0
    sumaFalsosPositivos = 0

    # Obtener los resultados de la matriz de confusion
    for i in range(len(df_matrix_confusion_entrenamiento)):
        for j in range(len(df_matrix_confusion_entrenamiento[i])):
            if i == j:
                sumaPositivos += df_matrix_confusion_entrenamiento[i][j]
            else:
                sumaFalsosPositivos += df_matrix_confusion_entrenamiento[i][j]

    df_matrix_confusion_precision_recall = df_matrix_confusion_entrenamiento.copy()

    listaPrecision = []
    listaRecall = []

    # suma de diagonal
    true_pos = np.diag(df_matrix_confusion_precision_recall)
    # suma de columnas
    false_pos = np.sum(df_matrix_confusion_precision_recall, axis=0) - true_pos
    # suma de filas
    false_neg = np.sum(df_matrix_confusion_precision_recall, axis=1) - true_pos

    for i in range(len(df_matrix_confusion_precision_recall)):
        recallCategoria = round((true_pos[i] / (true_pos[i] + false_pos[i])) * 100, 2)
        listaRecall.append(recallCategoria)
        precisionlCategoria = round((true_pos[i] / (true_pos[i] + false_neg[i])) * 100, 2)
        listaPrecision.append(precisionlCategoria)

    df_matrix_confusion_precision_recall["Precision"] = listaPrecision
    ultimoIndice = df_matrix_confusion_precision_recall.index[-1]
    df_matrix_confusion_precision_recall["Recall"] = listaRecall

    return df_matrix_confusion_precision_recall, precisionNB, sumaPositivos, sumaFalsosPositivos, model_svc



leerTodasCateogrias()
print(rutasCategorias)
listaRecetas, listaCategoria = leerRecetasCategorias()

df_recetas["Receta"] = listaRecetas
df_recetas["Categoria"] = listaCategoria

df_tratado = procesamientoTexto.tratamientoBasico(df_recetas)
df_stopwords = procesamientoTexto.quit_stopwords(df_tratado)
df_stem = procesamientoTexto.stemming(df_stopwords)

# Precision de 40.0
#confusionMatrixKnn, precisionKnn, sumaPosKnn, sumaFalsosPosKnn, modelKnn = calculate_weightKnn(df_stem)
#print(confusionMatrixKnn)
#print("Precision " + str(precisionKnn))

# Precision de 98.69
confusionMatrixRf, precisionRF, sumaPosRf, sumaFalsosPosRf, modelRf = calculate_weightRF(df_stem)
print(confusionMatrixRf)
print("Precision " + str(precisionRF))

# Precision de 77.49
#confusionMatrixNB, precisionNB, sumaPosNB, sumaFalsosPosNB, modelNB = calculate_weightNB(df_stem)
#print(confusionMatrixNB)
#print("Precision " + str(precisionNB))

# Precision de 97.98
#confusionMatrixSVC, precisionSVC, sumaPosSVC, sumaFalsosPosSVC, modelSVC = calculateweightSVM(df_stem)
#print(confusionMatrixSVC)
# print("Precision " + str(precisionSVC))

nombreFicheroGuardar = "modeloRandomForest"
joblib.dump(modelRf, nombreFicheroGuardar + ".pkl")
