# Librerias
import math

import joblib
import pymysql
import requests
from bs4 import BeautifulSoup
import pandas as pd

import PruebaAPIYoutube
import procesamientoTexto

# Headers para poder acceder a la pagina
header = {
    'User-Agent': 'Chrome 108.0.5359.125',
    'Accept-Language': 'es'
}

# Link de la pagina de Recetas Gratis
url_recetas_gratis = "https://www.recetasgratis.net"
pagina_recetas_gratis = requests.get(url_recetas_gratis, headers=header)
soup_recetas_gratis = BeautifulSoup(pagina_recetas_gratis.content, 'html.parser')


# Funcion para obtener los links de las diferentes categorias que tiene la pagina
def obtener_links_categorias():
    # Obtener los tags <a> de las diferentes categorias
    titulos_categorias_recetas_gratis = []
    contenedores_categorias_recetas_gratis = soup_recetas_gratis.find_all('div', class_="categoria ga")
    for categoria in range(len(contenedores_categorias_recetas_gratis)):
        titulos_categorias_recetas_gratis.append(
            contenedores_categorias_recetas_gratis[categoria].find('a', class_="titulo"))

    # Obtener el link de cada categoría
    links_categorias = []
    for categoria in range(len(titulos_categorias_recetas_gratis)):
        lista_links = list(titulos_categorias_recetas_gratis)[categoria]
        link_categoria_recetasGratis = lista_links.get('href')
        if link_categoria_recetasGratis != "https://www.recetasgratis.net/Recetas-de-Consejos-de-cocina-listado_receta-6146_1.html":
            links_categorias.append(link_categoria_recetasGratis)

    return links_categorias


def obtener_numPaginasPorCategoria(links_categorias):
    final = False
    num_categoria = 0
    links = []

    # Por cada categoria se recogen las diferentes paginas que existen para esa categoria
    for i in links_categorias:

        url_prueba = i

        # Comrpobar si ha llegado al final de la lista de links de las categorias
        if num_categoria == len(links_categorias) - 1:
            final = True
        else:
            final = False

        links.append(url_prueba)
        # Bucle que recorre todas las paginas en una categoria, obteniendo los diferentes links de cada hoja
        while (final == False):

            pags_mirar2 = requests.get(url_prueba)
            soup = BeautifulSoup(pags_mirar2.content, 'html.parser')

            # Obtener el marcador de siguiente hoja
            icon_next = soup.find('a', {"class": "next ga"})
            # Si el icono resulta nulo significa que nos encontramos al final de las hojas para esa categoria
            if icon_next is None:
                final = True
                links.append(url_prueba)
            else:
                # Si existe, se obtiene el link de la siguiente hoja
                icon_next = soup.find('a', {"class": "next ga"}).get("href")
                links.append(icon_next)
                url_prueba = icon_next

        num_categoria += 1

    # Navega entre las diferentes hojas de cada categoria y obtiene los links de las diferentes
    nombres_recetas_pag = []
    for i in links:
        url_bs4 = i
        pag_receta = requests.get(url_bs4)
        soup = BeautifulSoup(pag_receta.content, 'html.parser')
        # Guarda los tags <a> pertenecientes al titulo de cada receta por hoja
        informacion = soup.find_all('a', class_='titulo titulo--resultado')

        # Se obtiene el link guardado bajo el titulo de la receta
        for i in range(len(informacion)):
            receta = list(informacion)[i]
            link = receta.get("href")
            # Se aniade a la lista
            nombres_recetas_pag.append(link)

    return nombres_recetas_pag


def obtener_datos_receta(nombres_recetas_pag):
    titulo_recetas = []
    imagen_cadaReceta = []
    recetas_n_comensales = []
    recetas_duracion = []
    recetas_dificultad = []
    recetas_ingredientes = []
    pasos_receta = []
    lista_sentimientoPositivos = []
    lista_sentimientoNegativos = []

    # Recorre cada link de cada receta guardada en la lista
    for j in nombres_recetas_pag:
        link_receta = j
        lista_nueva = []
        pag_receta_info = requests.get(link_receta)
        soup_receta_info = BeautifulSoup(pag_receta_info.content, 'html.parser')

        # Obtener los ingredientes de la receta

        # Algunas recetas resultan ser un top de recetas, por lo que si existe un indice se trata de un top, que en este caso
        # no se tomaran como recetas
        indice = soup_receta_info.find('div', class_="indice")
        if indice is None:

            # Obtener el titulo de la receta
            titulo = soup_receta_info.find('h1', class_="titulo titulo--articulo")
            if titulo is None:
                titulo = "Sin Informacion"
            else:
                titulo = soup_receta_info.find('h1', class_="titulo titulo--articulo").get_text()

            titulo_recetas.append(titulo)

            # Obtener la imagen de la receta
            try:
                imagen_plato_recetasGratis = soup_receta_info.find('div', class_="imagen")

                if imagen_plato_recetasGratis is None:
                    imagen_plato_recetasGratis = "Sin Informacion"
                    imagen_cadaReceta.append(imagen_plato_recetasGratis)
                else:
                    # Se obtiene la etiqueta <img> y de ella la url de la imagen
                    link_imagen_plato = imagen_plato_recetasGratis.find('img').get('src')

                    imagen_cadaReceta.append(link_imagen_plato)
            except Exception as e:
                imagen_plato_recetasGratis = "Sin Informacion"
                imagen_cadaReceta.append(imagen_plato_recetasGratis)

            # Obtener el numero de comensales
            n_comensales = soup_receta_info.find('span', {"class": "property comensales"})
            if n_comensales is None:
                n_comensales = "Sin Informacion"
            else:
                n_comensales = soup_receta_info.find('span', {"class": "property comensales"}).get_text()

            recetas_n_comensales.append(n_comensales)

            # Obtener el tiempo de preparacion de la receta
            tiempo_duracion = soup_receta_info.find('span', {"class": "property duracion"})
            if tiempo_duracion is None:
                tiempo_duracion = "Sin Informacion"
            else:
                tiempo_duracion = soup_receta_info.find('span', {"class": "property duracion"}).get_text()

            recetas_duracion.append(tiempo_duracion)

            # Obtener el nivel de dificultad de la receta
            dificultad_coccion = soup_receta_info.find('span', {"class": "property dificultad"})
            if dificultad_coccion is None:
                dificultad_coccion = "Sin Informacion"
            else:
                dificultad_coccion = soup_receta_info.find('span', {"class": "property dificultad"}).get_text()
            recetas_dificultad.append(dificultad_coccion)

            # Obtener la lista de ingredientes de la receta
            lista_ingredientes = soup_receta_info.find_all('li', class_="ingrediente")

            # De la lista de ingredientes obtener la etiqueta <label> que contiene el texto
            for i in range(len(lista_ingredientes)):
                lista_ingredient = list(lista_ingredientes)[i]
                nombres_ingredientes = lista_ingredient.find_all('label')

                # Se obtiene el texto crudo de todas las etiquetas <label>
                for j in range(len(nombres_ingredientes)):
                    lista_nueva.append(nombres_ingredientes[j].get_text())

            # quitar los saltos de linea
            new_list = []
            for i in lista_nueva:
                new_list.append(i.strip())
            recetas_ingredientes.append(new_list)

            # Obtener los pasos de cada receta
            # En los pasos se debe eliminar el ultimo parrafo ya que no se trata de un paso
            list_temp_pasos = []
            contenedor_pasos = soup_receta_info.find_all('div', class_="apartado")
            for i in range(len(contenedor_pasos)):
                pasos = contenedor_pasos[i].find_all('p')
                for j in pasos:
                    list_temp_pasos.append(j.get_text())
            pasos_receta.append(list_temp_pasos)

            if (titulo=="Sin Informacion" or titulo==""):
                lista_sentimientoPositivos.append(0)
                lista_sentimientoNegativos.append(0)
            else:
                senPos, senNeg = PruebaAPIYoutube.sentimientosPosNeg(titulo)
                lista_sentimientoPositivos.append(senPos)
                lista_sentimientoNegativos.append(senNeg)

    return titulo_recetas, imagen_cadaReceta, recetas_n_comensales, recetas_duracion, recetas_dificultad, recetas_ingredientes, pasos_receta, lista_sentimientoPositivos, lista_sentimientoNegativos


lista_linksCadaCategoria = obtener_links_categorias()
lista_paginasCadaCategoria = obtener_numPaginasPorCategoria(lista_linksCadaCategoria)

titulos, imagen, comensales, duracion, dificultad, ingredientes, pasos, senPos, senNeg = obtener_datos_receta(
    lista_paginasCadaCategoria)
df = pd.DataFrame(columns=["titulo", "imagen", "comensales", "duracion", "dificultad", "ingredientes", "pasos", "sentimientoPos", "sentimientoNeg"])
df["titulo"] = titulos
df["imagen"] = imagen
df["comensales"] = comensales
df["duracion"] = duracion
df["dificultad"] = dificultad
df["ingredientes"] = ingredientes
df["pasos"] = pasos
df["sentimientoPos"] = senPos
df["sentimientoNeg"] = senNeg


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