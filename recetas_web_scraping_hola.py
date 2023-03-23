# Librerias
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

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
    url_categoria_hola = todas_categorias_hola[10]  # categoria_actual
    nombre_categoria_seleccionada = nombres_categorias[10]  # iteradorCategoria
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
                  "duracion", "dificultad", "ingredientes", "pasos", "nombre_categoria"])
df["titulo"] = titulos
df["imagen"] = imagen
df["comensales"] = comensales
df["duracion"] = duracion
df["dificultad"] = dificultad
df["ingredientes"] = ingredientes
df["pasos"] = pasos
df["nombre_categoria"] = nombre_categoria

df.to_csv('df_hola_final_10.csv', index=False, sep=';')
