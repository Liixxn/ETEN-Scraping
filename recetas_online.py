# Librerias
import joblib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
import math

import PruebaAPIYoutube
import procesamientoTexto

# Headers para poder acceder a la pagina
header = {
    'User-Agent': 'Chrome 108.0.5359.125',
    'Accept-Language': 'es'
}

# Se realiza una peticion a la pagina web de recetas online
url_recetas_online = "https://www.recetasonline.net/recetas-de-cocina/"
pag_recetas_online = requests.get(url_recetas_online, headers=header)
soup_recetas_online = BeautifulSoup(pag_recetas_online.content, 'html.parser')


def obtenerCategorias_RecetasOnline():
    # Se obtienen las diferentes categorias que se encuentran en el sub menu del navegador principal
    sub_menu_categorias = soup_recetas_online.find('ul', class_="sub-menu")
    # Se obtienen las etiquetas <a> de las diferentes categorias
    link_sub_menu = sub_menu_categorias.find_all('a')

    # Se obtienen los diferentes links de las categorias
    links_categorias_recetas_online = []
    for i in range(len(link_sub_menu)):
        link = link_sub_menu[i].get("href")
        links_categorias_recetas_online.append(link)
    return links_categorias_recetas_online


def obtenerNumPaginasPorCategoria(links_categorias_recetas_online):
    # Variable que almacena el numero de paginas que tiene cada categoria
    paginas_totales_por_categoria = []
    # Variable que comprueba si se ha llegado al final de las hojas para x categoria
    final_recetas_online = False
    contador = 0

    # Recorre la lista de los links de las diferentes categorias, para obtener el numero total de paginas pertenecientes a esa
    # categoria
    for categoria in links_categorias_recetas_online:
        url_categoria_recetas_online = categoria

        # Comprueba que se ha llegado al final de las categorias existentes
        if contador == len(links_categorias_recetas_online) - 1:
            final_recetas_online = True
        else:
            final_recetas_online = False

        # Por cada categoria revisa si existe una siguiente hoja
        paginas_totales_por_categoria.append(url_categoria_recetas_online)
        while (final_recetas_online == False):
            pag_categoria_recetas_online = requests.get(url_categoria_recetas_online)
            soup_pag_categoria_recetas_online = BeautifulSoup(pag_categoria_recetas_online.content, 'html.parser')

            # comprobar si exiten mas hojas para la x categoria
            mark_next_page = soup_pag_categoria_recetas_online.find('a', class_="next page-numbers")

            num_paginas_categoria = 1
            # Si no existe significa que se ha llegado al final de las hojas de x categoria
            if mark_next_page is None:
                final_recetas_online = True
            else:
                # Si existe se obtiene el link de la siguienta hoja de recetas para x categoria
                mark_next_page = soup_pag_categoria_recetas_online.find('a', class_="next page-numbers").get('href')
                url_categoria_recetas_online = mark_next_page
                paginas_totales_por_categoria.append(url_categoria_recetas_online)

        contador += 1

    # Lista que guardara las recetas que se encuentran bajo una categoria
    recetas_x_categoria = []
    # Lista que guardara las imagenes de cada plato
    imagen_recetas_recetas_online = []

    # Se recorre cada pagina guardada en la lista de "paginas_totales_por_categoria"
    for pagina in paginas_totales_por_categoria:
        url_link_categoria_pagina = pagina
        pag_link_categoria_ = requests.get(url_link_categoria_pagina, headers=header)
        soup_pag_link_categoria_ = BeautifulSoup(pag_link_categoria_.content, 'html.parser')
        # Se obtienen los titulos de las recetas
        titulo_receta_recetas_online = soup_pag_link_categoria_.find_all('h2', class_="entry-title")

        # Obtener la imagen de cada plato
        imagen_plato = soup_pag_link_categoria_.find_all('div', class_="post-thumb single-img-box")
        if imagen_plato is None:
            imagen_plato = "Sin Informacion"
            imagen_recetas_recetas_online.append(imagen_plato)
        else:

            # Se obtiene la url de la imagen, guardada en la etiqueta <meta>
            for etiqueta in range(len(imagen_plato)):
                meta_imagen = list(imagen_plato)[etiqueta].find('meta').get('content')
                imagen_recetas_recetas_online.append(meta_imagen)

        # Se obtienen los links que se encuentran en los titulos de cada receta
        for i in range(len(titulo_receta_recetas_online)):
            link_titulo_receta_recetas_online = list(titulo_receta_recetas_online)[i].find('a').get('href')
            recetas_x_categoria.append(link_titulo_receta_recetas_online)

    return recetas_x_categoria, imagen_recetas_recetas_online


def obtenerDatosReceta(recetas_x_categoria):
    titulos_recetas_recetas_online = []
    comensales_porReceta_recetas_online = []
    tiempo_porReceta_recetas_online = []
    ingredientes_porReceta_recetas_online = []
    pasos_porReceta_recetas_online = []
    lista_sentimientoPositivos = []
    lista_sentimientoNegativos = []

    # Se recorre la lista de recetas obtenida anteriormente
    for link_receta_ in recetas_x_categoria:
        pag_receta_informacion_recetas_online = requests.get(link_receta_)
        soup_pag_receta_info_recetas_online = BeautifulSoup(pag_receta_informacion_recetas_online.content,
                                                            'html.parser')

        # Titulo de la receta
        titulo_receta = soup_pag_receta_info_recetas_online.find('h1', class_="title fn")
        if titulo_receta is None:
            titulo_receta = "Sin Informacion"
        else:
            titulo_receta = soup_pag_receta_info_recetas_online.find('h1', class_="title fn").get_text()
        titulos_recetas_recetas_online.append(titulo_receta)

        # Numero de comensales
        list_n_comensales_recetas_online = soup_pag_receta_info_recetas_online.find('li', class_="servings")
        if list_n_comensales_recetas_online is None:
            n_comensales_recetas_online = "Sin Informacion"
        else:
            n_comensales_recetas_online = list_n_comensales_recetas_online.find('span').get_text()
        comensales_porReceta_recetas_online.append(n_comensales_recetas_online)

        # Tiempo de preparacion
        list_tiempo_receta_recetas_online = soup_pag_receta_info_recetas_online.find('li', class_="ready-in")
        if list_tiempo_receta_recetas_online is None:
            tiempo_receta_recetas_online = "Sin Informacion"
        else:
            tiempo_receta_recetas_online = list_tiempo_receta_recetas_online.find('span').get_text()
        tiempo_porReceta_recetas_online.append(tiempo_receta_recetas_online)

        # Lista de ingredientes
        list_ingredientes_receta_recetas_online = soup_pag_receta_info_recetas_online.find_all('li',
                                                                                               class_="ingredient")

        lista_temp = []
        for ingredient in range(len(list_ingredientes_receta_recetas_online)):
            lista_temp.append(list_ingredientes_receta_recetas_online[ingredient].get_text())
        ingredientes_porReceta_recetas_online.append(lista_temp)

        # Lista de pasos a seguir
        list_pasos_recetas_online = soup_pag_receta_info_recetas_online.find_all('p', class_="instructions")
        lista_temp_pasos = []
        for paso in range(len(list_pasos_recetas_online)):
            lista_temp_pasos.append(list_pasos_recetas_online[paso].get_text())
        pasos_porReceta_recetas_online.append(lista_temp_pasos)

        # Esta parte es para obtener la informacion de los comentarios de cada receta, no se recomienda hacerlo

        if titulo_receta == "Sin Informacion":
            lista_sentimientoPositivos.append(0)
            lista_sentimientoNegativos.append(0)
        else:
            senPos, senNeg = PruebaAPIYoutube.sentimientosPosNeg(titulo_receta)
            lista_sentimientoPositivos.append(senPos)
            lista_sentimientoNegativos.append(senNeg)

    return titulos_recetas_recetas_online, comensales_porReceta_recetas_online, tiempo_porReceta_recetas_online, ingredientes_porReceta_recetas_online, pasos_porReceta_recetas_online, lista_sentimientoPositivos, lista_sentimientoNegativos


lista_categoriasRecetasOnline = obtenerCategorias_RecetasOnline()
lista_recetasRecetasOnline, lista_imagenesRecetasOnline = obtenerNumPaginasPorCategoria(lista_categoriasRecetasOnline)
obtenerDatosReceta(lista_recetasRecetasOnline)
titulos, comen, tiempo, ingredientes, pasos, senPos, senNeg = obtenerDatosReceta(lista_recetasRecetasOnline)

df = pd.DataFrame(
    columns=["titulo", "imagen", "comensales", "duracion", "dificultad", "ingredientes", "pasos", "sentimientoPos",
             "sentimientoNeg", "Categoria"])
df["titulo"] = titulos
df["imagen"] = lista_imagenesRecetasOnline
df["comensales"] = comen
df["duracion"] = tiempo
df["dificultad"] = ""
df["ingredientes"] = ingredientes
df["pasos"] = pasos
df["sentimientoPos"] = senPos
df["sentimientoNeg"] = senNeg
df["Categoria"] = "Sin Clasificar"



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
        arrayIngredientes[len(arrayIngredientes)-1] = arrayIngredientes[len(arrayIngredientes)-1].replace("'", "")

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




