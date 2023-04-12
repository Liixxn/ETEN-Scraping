import os

import joblib
import numpy as np
import pandas as pd

import procesamientoTexto

df_clasificacion = pd.DataFrame(columns=["Receta", "Categoria"])

def leerRecetasUnlabeled():
    df_recetas_online = pd.read_csv("recetas_csv/df_recetas_online.csv", sep=";")


    listaRecetasContenido = []

    for indiceDF, fila in df_recetas_online.iterrows():

        listaRecetasContenido.append(fila["titulo"]+fila["pasos"])

    df_clasificacion["Receta"] = listaRecetasContenido
    df_clasificacion["Categoria"] = "Sin Clasificar"

leerRecetasUnlabeled()

df_tratado = procesamientoTexto.tratamientoBasico(df_clasificacion)
df_stopwords = procesamientoTexto.quit_stopwords(df_tratado)
df_stem = procesamientoTexto.stemming(df_stopwords)

cargaModelo = joblib.load("modeloRandomForest.pkl")
for i in range(len(df_stem["Receta"])):
    unidos = " ".join(df_stem["Receta"][i])

    df_stem["Receta"][i] = str(unidos)

Y_pred = cargaModelo.predict(df_stem['Receta'])
listaPredicciones = Y_pred.tolist()
df_recetas = pd.read_csv("recetas_csv/df_recetas_online.csv", sep=";")
df_recetas["Categoria"] = listaPredicciones
df_recetas.to_csv("recetas_csv/df_recetas_online.csv", sep=";", index=False)



