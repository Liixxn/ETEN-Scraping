import math

import mysql.connector
import pandas as pd
from numpy import double
import re
import pymysql

df = pd.read_csv("recetas_csv/df_hola_todo.csv", sep=";")


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
        print("Receta: " + str(df["titulo"][receta]))
        while(recetaEncontrada==False and final < len(resultados)):
            if (df["titulo"][receta] == resultados[final][2]) and (df["imagen"][receta] == resultados[final][4]):
                recetaEncontrada = True
                print("Receta encontrada: " + str(receta))
            else:
                final += 1
                print("Receta no encontrada: " + str(receta))

        if recetaEncontrada == False:
            print("se inserta")
            sql = "INSERT INTO recetas (categoria, titulo, descripcion, img, duracion, comensales, dificultad, activo, sentimiento_pos, sentimiento_neg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            categoria = str(df["Categoria"][receta])
            titulo = str(df["titulo"][receta])
            descripcion = str(df["pasos"][receta])
            img = str(df["imagen"][receta])
            ingredientes = df["ingredientes"][receta]


            # # PARA EL DE RECETAS ONLINE
            # ingredientes = ingredientes.replace("[", "").replace("]", "")
            # arrayIngredientes = ingredientes.split("', '")
            #
            # arrayIngredientes[0] = arrayIngredientes[0].replace("'", "")
            # arrayIngredientes[len(arrayIngredientes) - 1] = arrayIngredientes[len(arrayIngredientes) - 1].replace("'",
            #                                                                                                       "")



            # PARA EL DE RECETAS HOLA
            ingredientes = ingredientes.replace("[", "").replace("]", "")
            # esto para el de df_hola_todo.csv
            arrayIngredientes = ingredientes.split("', '")

            arrayIngredientes[0] = arrayIngredientes[0].replace("'", "")
            arrayIngredientes[len(arrayIngredientes) - 1] = arrayIngredientes[len(arrayIngredientes) - 1].replace("'",
                                                                                                                  "")






            duracion = str(df["duracion"][receta])
            comensales = str(df["comensales"][receta])
            dificultad = str(df["dificultad"][receta])
            activo = 1
            sentimiento_pos = float(df["sentimientoPos"][receta])
            sentimiento_neg = float(df["sentimientoNeg"][receta])

            if (math.isnan(sentimiento_pos) and math.isnan(sentimiento_neg)):
                sentimiento_pos = 0.0
                sentimiento_neg = 0.0


            val = (categoria, titulo, descripcion, img, duracion, comensales, dificultad, activo,
                   sentimiento_pos, sentimiento_neg)
            cursor.execute(sql, val)
            conn.commit()

            sqlTrasInserccion = "SELECT id FROM recetas ORDER BY id DESC LIMIT 1"
            cursor.execute(sqlTrasInserccion)
            resultadosTrasLaInserccion = cursor.fetchone()

            sqlIngredienes = "INSERT INTO ingredientes (id_receta, nombre_ingrediente) VALUES (%s, %s);"
            id_receta = int(resultadosTrasLaInserccion[0])
            for j in range(len(arrayIngredientes)):
                nombre_ingrediente = str(arrayIngredientes[j])
                val = (id_receta, nombre_ingrediente)
                cursor.execute(sqlIngredienes, val)
                conn.commit()




else:
    for i in range(len(df["titulo"])):
        sql = "INSERT INTO recetas (categoria, titulo, descripcion, img, duracion, comensales, dificultad, activo, sentimiento_pos, sentimiento_neg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        categoria = str(df["Categoria"][i])
        titulo = str(df["titulo"][i])
        descripcion = str(df["pasos"][i])
        img = str(df["imagen"][i])

        ingredientes = df["ingredientes"][i]
        # ingredientes = ingredientes.replace("[", "").replace("]", "")
        # arrayIngredientes = ingredientes.split("', '")
        #
        # arrayIngredientes[0] = arrayIngredientes[0].replace("'", "")
        # arrayIngredientes[len(arrayIngredientes)-1] = arrayIngredientes[len(arrayIngredientes)-1].replace("'", "")




        ## PARA EL DE RECETAS HOLA
        ingredientes = ingredientes.replace("[", "").replace("]", "")
        # esto para el de df_hola_todo.csv
        arrayIngredientes = ingredientes.split("', '")

        arrayIngredientes[0] = arrayIngredientes[0].replace("'", "")
        arrayIngredientes[len(arrayIngredientes) - 1] = arrayIngredientes[len(arrayIngredientes) - 1].replace("'",
                                                                                                              "")


        duracion = str(df["duracion"][i])
        comensales = str(df["comensales"][i])
        dificultad = str(df["dificultad"][i])
        activo = 1
        sentimiento_pos = float(df["sentimientoPos"][i])
        sentimiento_neg = float(df["sentimientoNeg"][i])

        if (math.isnan(sentimiento_pos) and math.isnan(sentimiento_neg)):
            sentimiento_pos = 0.0
            sentimiento_neg = 0.0



        val = (categoria, titulo, descripcion, img, duracion, comensales, dificultad, activo, sentimiento_pos, sentimiento_neg)
        cursor.execute(sql, val)
        conn.commit()

        sqlTrasInserccion = "SELECT id FROM recetas ORDER BY id DESC LIMIT 1"
        cursor.execute(sqlTrasInserccion)
        resultadosTrasLaInserccion = cursor.fetchone()

        sqlIngredienes2 = "INSERT INTO ingredientes (id_receta, nombre_ingrediente) VALUES (%s, %s);"
        id_receta = int(resultadosTrasLaInserccion[0])
        for j in range(len(arrayIngredientes)):
            nombre_ingrediente = str(arrayIngredientes[j])
            val = (id_receta, nombre_ingrediente)
            cursor.execute(sqlIngredienes2, val)
            conn.commit()
