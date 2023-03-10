# Librerias
import requests
from bs4 import BeautifulSoup

# Headers para poder acceder a la pagina
header = {
    'User-Agent': 'Chrome 108.0.5359.125',
    'Accept-Language': 'es'
}



# Link original de la pagina web, ya que los links de las recetas no se guardan la ruta completa
url_hogarmania_principal = "https://www.hogarmania.com"
# Link de la pagina web para su categoria de recetas
url_hogarmania = "https://www.hogarmania.com/cocina/recetas/"
pagina_hogarmania = requests.get(url_hogarmania, headers=header)
soup_hogarmania = BeautifulSoup(pagina_hogarmania.content, 'html.parser')


def obtenerListaCategorias_Hogarmania():

    lista_links_titulos_categoria_hogarmania = []

    # Obtener los diferentes links pertenecientes a cada categoria
    # Se han quitado los 2 titulos utlimos porque son consejos
    titulos_categorias_hogarmania = soup_hogarmania.find_all('h2', class_="m-titulo")
    for titulo in range(len(titulos_categorias_hogarmania[:-3])):
        lista_titulos_hogarmania = list(titulos_categorias_hogarmania)[titulo]
        link_titulo_categoria_hogarmania = lista_titulos_hogarmania.find('a').get('href')
        # Se une el link horiginal junto al link obtenido de cada categoria, para que a la hora de navegar se tenga la
        # url completa
        link_titulo_final = url_hogarmania_principal+link_titulo_categoria_hogarmania
        lista_links_titulos_categoria_hogarmania.append(link_titulo_final)

    return lista_links_titulos_categoria_hogarmania



def obtenerNumPaginasPorCategoria(lista_links_titulos_categoria_hogarmania):
    paginas_totales_todasCategorias_hogarmania = []
    # Variable que comprueba que el paginador sea un numero o un signo, ya que en este sitio el boton para pasar de hoja
    # no tiene un identificador por lo que solo tienen un icono "»", el cual es el que va comparando con otros
    # para saber si existe una pagina siguiente para una cierta categoria
    paginador_numero = False
    contador_hogarmania = 0

    # Se recorren las diferentes categorias
    for categoria in lista_links_titulos_categoria_hogarmania:
        url_prueba = categoria

        # Se comprueba si se ha acabado de recorrer todas las categorias
        if contador_hogarmania == (len(lista_links_titulos_categoria_hogarmania) - 1):
            paginador_numero = True
        else:
            paginador_numero = False

        paginas_totales_todasCategorias_hogarmania.append(url_prueba)
        # Bucle que comprueba si existen mas paginas para cierta categoria, obteniendo su respectivo link
        while (paginador_numero == False):

            pagina_categoria_hogarmania = requests.get(url_prueba, headers=header)
            soup_categoria_hogarmania = BeautifulSoup(pagina_categoria_hogarmania.content, 'html.parser')

            # Se obtienen el contenedor que guarda la paginacion para la categoria deseada
            paginador_siguiente_hogarmania = soup_categoria_hogarmania.find('ul', class_="pagination")
            link_paginador_hogarmania = paginador_siguiente_hogarmania.find_all('a')

            for i in range(len(link_paginador_hogarmania)):
                # Se comprueba que el texto que aperece en el paginador sea igual al signo que representa la siguiente pagina
                if (link_paginador_hogarmania[i].get_text()) == "»":
                    # Si existe se obtiene el link
                    link_semicompleto = link_paginador_hogarmania[i].get('href')
                    # Se une el link original y el nuevo link obtenido
                    link_completo = url_hogarmania_principal + link_semicompleto
                    url_prueba = link_completo
                    paginas_totales_todasCategorias_hogarmania.append(url_prueba)
                    paginador_numero = False

                else:
                    # Si el paginador no es el signo de "siguiente"
                    paginador_numero = True
            if paginador_numero == True:
                print("")
            contador_hogarmania += 1


    # Lista que guarda todas las recetas de cada categoria
    link_todasRecetasPorCategoria = []

    # Recorre todas las hojas de una categoria para obtener todas las recetas bajo esa categoria
    for hoja in paginas_totales_todasCategorias_hogarmania:
        link_hojaDeRecetas_categoria_hogarmania = hoja
        pag_linkHojaRecetas_categoria_ = requests.get(link_hojaDeRecetas_categoria_hogarmania, headers=header)
        soup_pagHojaRecetas_categoria = BeautifulSoup(pag_linkHojaRecetas_categoria_.content, 'html.parser')
        # Se obtiene el contenedor que guarda el link de la receta
        contenedor_titulos_recetas_hogarmania = soup_pagHojaRecetas_categoria.find('div', class_="especial listado")
        articulo_recetas = contenedor_titulos_recetas_hogarmania.find_all('article', class_="modulo")

        # Se recorre el contenedor que guarda la informacion de la receta
        for articulo in range(len(articulo_recetas)):
            lista_articulo_recetas = list(articulo_recetas)[articulo]
            link_receta = lista_articulo_recetas.find_all('h2', class_="m-titulo")

            # Se obtiene el link de la recetas
            for contenido in range(len(link_receta)):
                lista_contenido = list(link_receta)[contenido]
                links_titulo_receta_hogarmaniaCategoria = lista_contenido.find_all('a')
                urls_titulos_receta_hogarmaniaCategoria = list(links_titulo_receta_hogarmaniaCategoria)[contenido]
                url_todasRecetasPorCategoria = url_hogarmania_principal + urls_titulos_receta_hogarmaniaCategoria.get(
                    'href')

                link_todasRecetasPorCategoria.append(url_todasRecetasPorCategoria)

    return link_todasRecetasPorCategoria




def obtenerDatosRecetasHogarmania(link_todasRecetasPorCategoria):

    titulos_recetasHogarmania = []
    imagenes_recetasHogarmania = []
    tiempo_total_RecetasHogarmania = []
    ingredientes_total_RecetasHogarmania = []
    pasos_RecetaHogarmania = []
    # Lista de prueba para no tener que ejecutar todo
    # lin_ = []
    # lin_.append('https://www.hogarmania.com/cocina/recetas/postres/orejas-carnaval-sin-gluten.html')
    # lin_.append('https://www.hogarmania.com/cocina/recetas/postres/tarta-de-naranja-y-queso.html')

    # Se recorre todas las recetas de todas las categorias
    for receta in link_todasRecetasPorCategoria:
        url_receta = receta
        pagina_receta_hogarmania = requests.get(url_receta, headers=header)
        soup_receta_hogarmania = BeautifulSoup(pagina_receta_hogarmania.content, 'html.parser')

        # Obtener el tiempo de preparacion
        contenedor_tiempo_total_receta_hogarmania = soup_receta_hogarmania.find_all('b')
        if contenedor_tiempo_total_receta_hogarmania is None:
            tiempo_total_RecetasHogarmania.append('Sin Informacion')
        else:
            # El tiempo se guarda junto a otro tiempo, por lo tanto se deben separar para obtener el tiempo final de preparacion
            for tiempos in range(len(contenedor_tiempo_total_receta_hogarmania)):
                tiempo_totalPreparacion_recetaHogarmania = contenedor_tiempo_total_receta_hogarmania[tiempos].get_text()

            tiempo_total_RecetasHogarmania.append(tiempo_totalPreparacion_recetaHogarmania)

        # Obtener el titulo de la receta
        titulo_receta_hogarmania = soup_receta_hogarmania.find('h1', class_="m-titulo")
        if titulo_receta_hogarmania is None:
            titulo_receta_hogarmania = "Sin Informacion"
        else:
            titulo_receta_hogarmania = soup_receta_hogarmania.find('h1', class_="m-titulo").get_text()
        titulos_recetasHogarmania.append(titulo_receta_hogarmania)

        # Obtener la imagen del plato
        imagen_plato = soup_receta_hogarmania.find('div', class_="print_video")
        if imagen_plato is None:
            imagen_plato = "Sin Informacion"
            imagenes_recetasHogarmania.append(imagen_plato)
        else:
            url_imagenPlato_completa = url_hogarmania_principal + imagen_plato.find('img').get('src')
            imagenes_recetasHogarmania.append(url_imagenPlato_completa)

        # Obtener los diferentes ingredientes
        contenedor_ingredientes_recetaHogarmania = soup_receta_hogarmania.find('ul', class_="ingredientes")
        lista_ingredientes_tmp = []
        # Se recorre la lista de los ingredientes para obtener el texto
        for ingrediente_hogarmania in contenedor_ingredientes_recetaHogarmania:
            ingrediente_deLaLista = ingrediente_hogarmania.get_text()
            lista_ingredientes_tmp.append(ingrediente_deLaLista)
        ingredientes_total_RecetasHogarmania.append(lista_ingredientes_tmp)

        # Obtener los pasos a seguir
        lista_identificadores_h2 = []
        # Obtener el id del titulo, ya que la parte de elaboracion no tiene identificador
        for titulos_h2_hogarmania in soup_receta_hogarmania.find_all('h2'):
            lista_identificadores_h2.append(titulos_h2_hogarmania.get('id'))

        # Como el contenido de los pasos no tiene un identificador, para obtener tal informacion, se obtiene el identificador
        # del titulo que da comienzo a la elaboracion del plato y el siguiente titulo que da comienza a otra fase

        # Titulo de comienzo de la elaboracion
        start_h2_recetaElaboracion_hogarmania = soup_receta_hogarmania.find('h2', {'id': lista_identificadores_h2[1]})
        # Titulo del siguiente parrafo de contenido
        end_h2_recetaElaboracion_hogarmania = soup_receta_hogarmania.find('h2', {'id': lista_identificadores_h2[2]})
        content = ""
        # Se obtiene las siguientes partes de la web que siguen tras el titulo de comienzo de la elaboracion
        item = start_h2_recetaElaboracion_hogarmania.nextSibling

        # Se une el contenido y se aniade a una lista
        lista_contenido_tmp = list()
        # Se compara que las siguientes partes del titulo de comienzo no sean igual al titulo del final
        while item != end_h2_recetaElaboracion_hogarmania:
            content = item
            item = item.nextSibling
            lista_contenido_tmp.append(content)

        # Se van a eliminar todas aquellas etiquetas que no sean de texto
        lista_pasos_tmp = []
        for tag in range(len(lista_contenido_tmp)):

            tags = list(lista_contenido_tmp)[tag]

            # Se comprueba que el tipo sea un bs4 tag element
            if (type(tags)) == (type(start_h2_recetaElaboracion_hogarmania)):

                # Se obtiene el texto, se reliza un try ya que la web tiene elementos que no son del tipo tag, y puede dar error
                # a la hora de intentar rescatar el texto que se encuentra en el
                try:
                    contenido_pasos = tags.get_text()
                    lista_pasos_tmp.append(contenido_pasos)

                except Exception as e:
                    print("no se puede obtener el texto")

            else:
                print("")
        pasos_RecetaHogarmania.append(lista_pasos_tmp)

    return titulos_recetasHogarmania, imagenes_recetasHogarmania, tiempo_total_RecetasHogarmania, ingredientes_total_RecetasHogarmania, pasos_RecetaHogarmania






lista_categoriasHogarmania = obtenerListaCategorias_Hogarmania()
lista_RecetasHogarmania = obtenerNumPaginasPorCategoria(lista_categoriasHogarmania)
obtenerDatosRecetasHogarmania(lista_RecetasHogarmania)








