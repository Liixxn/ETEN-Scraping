import mysql.connector
import pandas as pd
from numpy import double
import pymysql

df = pd.read_csv("recetas_csv/df_recetas_online.csv", sep=";")


conn = pymysql.connect(host='195.235.211.197', user='pc2_grupo3', password='PComputacion.23', database='pc2_grupo3')
cursor = conn.cursor()

sql_obtenerDatos = "SELECT * FROM recetas"

cursor.execute(sql_obtenerDatos)
resultados = cursor.fetchall()

recetaEncontrada = False

if len(resultados) > 0:
    for receta in range(len(df["titulo"])):
        recetaEncontrada = False
        final = 0
        while(recetaEncontrada==False and final < len(resultados)):
            if df["titulo"][receta] == resultados[final][2]:
                recetaEncontrada = True
            else:
                final += 1

        if recetaEncontrada == False:
            sql = "INSERT INTO recetas (categoria, titulo, descripcion, img, ingredientes, duracion, comensales, dificultad, activo, sentimiento_pos, sentimiento_neg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            categoria = str(df["Categoria"][receta])
            titulo = str(df["titulo"][receta])
            descripcion = str(df["pasos"][receta])
            img = str(df["imagen"][receta])
            ingredientes = str(df["ingredientes"][receta])
            duracion = str(df["duracion"][receta])
            comensales = str(df["comensales"][receta])
            dificultad = str(df["dificultad"][receta])
            activo = 1
            sentimiento_pos = float(df["sentimientoPos"][receta])
            sentimiento_neg = float(df["sentimientoNeg"][receta])

            val = (categoria, titulo, descripcion, img, ingredientes, duracion, comensales, dificultad, activo,
                   sentimiento_pos, sentimiento_neg)
            cursor.execute(sql, val)
            conn.commit()



else:
    for i in range(len(df[:2])):
        sql = "INSERT INTO recetas (categoria, titulo, descripcion, img, ingredientes, duracion, comensales, dificultad, activo, sentimiento_pos, sentimiento_neg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        categoria = str(df["Categoria"][i])
        titulo = str(df["titulo"][i])
        descripcion = str(df["pasos"][i])
        img = str(df["imagen"][i])
        ingredientes = str(df["ingredientes"][i])
        duracion = str(df["duracion"][i])
        comensales = str(df["comensales"][i])
        dificultad = str(df["dificultad"][i])
        activo = 1
        sentimiento_pos = float(df["sentimientoPos"][i])
        sentimiento_neg = float(df["sentimientoNeg"][i])

        val = (categoria, titulo, descripcion, img, ingredientes, duracion, comensales, dificultad, activo, sentimiento_pos, sentimiento_neg)
        cursor.execute(sql, val)
        conn.commit()
