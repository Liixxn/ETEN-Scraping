# Librerias
import math

import joblib
import pymysql
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

import PruebaAPIYoutube
import procesamientoTexto

# Headers para poder acceder a la pagina
header = {
    'User-Agent': 'Chrome 108.0.5359.125',
    'Accept-Language': 'es'
}

# Se realiza una peticion a la pagina web de recetas online
url_hola = "https://www.hola.com/cocina/"
pag_hola = requests.get(url_hola, headers=header)
soup_hola = BeautifulSoup(pag_hola.content, 'html.parser')
nombres_categorias = []


def sacarCategoriasHola():

    todasCategorias = soup_hola.find_all(
        'span', class_="categories-component__item-title")
    for cat in todasCategorias:
        nombres_categorias.append(cat.get_text())

    # Se obtienen las diferentes categorias que se encuentran en el sub menu del navegador principal
    sub_menu_categorias = soup_hola.find_all(
        'div', class_="categories-component_button")

    links_categorias_hola = []
    # Sacamos todas las url a las diferentes categorias
    for i in range(len(sub_menu_categorias)):
        link = sub_menu_categorias[i].find('a').get("href")
        links_categorias_hola.append(link)
    return links_categorias_hola


def scrapingPorCategoria(todas_categorias_hola):
    titulo_recetas = []
    imagen_cadaReceta = []
    recetas_duracion = []
    recetas_dificultad = []

    recetas_n_comensales = []
    recetas_ingredientes = []
    pasos_receta = []
    nombre_categoria_receta = []

    iteradorCategoria = 0
    # for categoria_actual in todas_categorias_hola:
    lista_url_paginacion = []
    url_categoria_hola = todas_categorias_hola[17]  # categoria_actual
    nombre_categoria_seleccionada = nombres_categorias[17]  # iteradorCategoria
    nombre_categoria_seleccionada = nombre_categoria_seleccionada.upper() + '/'

    # Guardamos el primer enlace de las primeras recetas
    lista_url_paginacion.append(url_categoria_hola)

    pag_hola_categoria = requests.get(url_categoria_hola, headers=header)
    soup_categoria_hola = BeautifulSoup(
        pag_hola_categoria.content, 'html.parser')

    # Se obtienen los enlaces de todas las ventanas de la categoria (paginacion por categoria)
    bandera = True
    while bandera:
        # Hay variosbotones de hacia delante y hacia atras, solo nos interesa el ultimo que es hacia delante
        siguiente_enlace = soup_categoria_hola.find_all(
            'li', class_='pagination__item')[-1]
        try:
            paginacion_siguiente = siguiente_enlace.find('a').get('href')
            print(paginacion_siguiente)
        except:
            paginacion_siguiente = None

        if paginacion_siguiente is None:
            bandera = False
        else:
            lista_url_paginacion.append(paginacion_siguiente)
            pag_hola_categoria = requests.get(
                paginacion_siguiente, headers=header)
            soup_categoria_hola = BeautifulSoup(
                pag_hola_categoria.content, 'html.parser')

    for lista_paginas in lista_url_paginacion:
        print('Inicio extraccion')
        print(lista_paginas)
        paginacion_cat = requests.get(lista_paginas, headers=header)
        soup_hola = BeautifulSoup(paginacion_cat.content, 'html.parser')
        cards = soup_hola.find_all('div', class_='full-width-card')
        # print(cards)
        for c in cards:
            if c.find('div', class_='o-card-caption_parameters') and nombre_categoria_seleccionada == c.find('span', class_='o-card-caption_section').get_text().strip():
                titulo_recetas.append(
                    c.find('a', class_='o-card_title stretched-link').get_text().strip())
                if c.find('img', class_='o-card-figure_image').get('src') is None:
                    imagen_cadaReceta.append(
                        '/assets/imgs/recetaSinImagen.jpg')
                else:
                    imagen_cadaReceta.append(
                        c.find('img', class_='o-card-figure_image').get('src'))
                print(c.find('img', class_='o-card-figure_image').get('src'))
                recetas_duracion.append(
                    c.find('p', class_='o-card-parameter o-card-parameter_time').get_text().strip())
                recetas_dificultad.append(
                    c.find('p', class_='o-card-parameter o-card-parameter_dificulty').get_text().strip())
                url_receta_final = c.find(
                    'a', class_='o-card_title stretched-link').get('href')

                recetaFinal = requests.get(
                    url_receta_final, headers=header)
                soup_receta_final = BeautifulSoup(
                    recetaFinal.content, 'html.parser')

                try:
                    recetas_n_comensales.append(soup_receta_final.find(
                        'span', class_='rations').get_text().strip())
                except:
                    recetas_n_comensales.append('')

                try:
                    ingredientes = soup_receta_final.find_all(
                        'li', class_='recipe_ingredients-item')
                except:
                    ingredientes = soup_receta_final.find_all(
                        'li', class_='ingredient-item')

                new_list_ingredientes_li = []
                for i in ingredientes:
                    texto = i.text.strip()
                    texto = texto.replace('\n', '').replace('\t', '')
                    texto = re.sub('\s+', ' ', texto).strip()
                    new_list_ingredientes_li.append(texto)
                recetas_ingredientes.append(new_list_ingredientes_li)

                try:
                    pasos = soup_receta_final.find_all(
                        'div', class_='recipe-instructions_step')
                except:
                    pasos = soup_receta_final.find_all(
                        'li', class_='instruction-item')

                new_list_pasos = []
                for p in pasos:
                    new_list_pasos.append(
                        p.find('span').get_text().strip())
                pasos_receta.append(new_list_pasos)

                name_categoria = nombre_categoria_seleccionada.replace(
                    '/', '').lower()
                nombre_categoria_receta.append(name_categoria)

    print('---------------------------------------------------------------------------------------------------------------')
    iteradorCategoria += 1
    return titulo_recetas, imagen_cadaReceta, recetas_n_comensales, recetas_duracion, recetas_dificultad, recetas_ingredientes, pasos_receta, nombre_categoria_receta


todas_categorias_hola = sacarCategoriasHola()
titulos, imagen, comensales, duracion, dificultad, ingredientes, pasos, nombre_categoria = scrapingPorCategoria(
    todas_categorias_hola)
df = pd.DataFrame(columns=["titulo", "imagen", "comensales",
                  "duracion", "dificultad", "ingredientes", "pasos", "nombre_categoria", "sentimientoPos", "sentimientoNeg"])
df["titulo"] = titulos
df["imagen"] = imagen
df["comensales"] = comensales
df["duracion"] = duracion
df["dificultad"] = dificultad
df["ingredientes"] = ingredientes
df["pasos"] = pasos
df["nombre_categoria"] = nombre_categoria
df["sentimientoPos"] = 0
df["sentimientoNeg"] = 0


lista_sentimientoPositivos = []
lista_sentimientoNegativos = []

for titulo in df["titulo"]:
    if (titulo == '' or titulo == "Sin Informacion"):
        lista_sentimientoPositivos.append(0)
        lista_sentimientoNegativos.append(0)
    else:
        senPos, senNeg = PruebaAPIYoutube.sentimientosPosNeg(titulo)
        lista_sentimientoPositivos.append(senPos)
        lista_sentimientoNegativos.append(senNeg)

df["sentimientoPos"] = lista_sentimientoPositivos
df["sentimientoNeg"] = lista_sentimientoNegativos


df_recetas_online = df.copy()

df_clasificacion = pd.DataFrame(columns=["Receta", "Categoria"])

listaRecetasContenido = []

for indiceDF, fila in df_recetas_online.iterrows():
    listaRecetasContenido.append(fila["titulo"] + fila["pasos"])

df_clasificacion["Receta"] = listaRecetasContenido
df_clasificacion["Categoria"] = "Sin Clasificar"

df_tratado = procesamientoTexto.tratamientoBasico(df_clasificacion)
df_stopwords = procesamientoTexto.quit_stopwords(df_tratado)
df_stem = procesamientoTexto.stemming(df_stopwords)

cargaModelo = joblib.load("modeloRandomForest.pkl")
for i in range(len(df_stem["Receta"])):
    unidos = " ".join(df_stem["Receta"][i])

    df_stem["Receta"][i] = str(unidos)

Y_pred = cargaModelo.predict(df_stem['Receta'])
listaPredicciones = Y_pred.tolist()
df["Categoria"] = listaPredicciones


conn = pymysql.connect(host='195.235.211.197', user='pc2_grupo3',
                       password='PComputacion.23', database='pc2_grupo3')
cursor = conn.cursor()

sql_obtenerDatos = "SELECT * FROM recetas"

cursor.execute(sql_obtenerDatos)
resultados = cursor.fetchall()

recetaEncontrada = False

if len(resultados) > 0:
    for receta in range(len(df["titulo"])):
        recetaEncontrada = False
        final = 0
        while (recetaEncontrada == False and final < len(resultados)):
            if (df["titulo"][receta] == resultados[final][2]) and (df["imagen"][receta] == resultados[final][4]):
                recetaEncontrada = True
            else:
                final += 1

        if recetaEncontrada == False:
            sql = "INSERT INTO recetas (categoria, titulo, descripcion, img, duracion, comensales, dificultad, activo, sentimiento_pos, sentimiento_neg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            categoria = str(df["Categoria"][receta])
            titulo = str(df["titulo"][receta])
            descripcion = str(df["pasos"][receta])
            img = str(df["imagen"][receta])
            ingredientes = df["ingredientes"][receta]

            ingredientes = ingredientes.replace("[", "").replace("]", "")
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

        ingredientes = ingredientes.replace("[", "").replace("]", "")
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

        val = (categoria, titulo, descripcion, img, duracion, comensales,
               dificultad, activo, sentimiento_pos, sentimiento_neg)
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
