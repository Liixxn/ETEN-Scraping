import csv
from googleapiclient.discovery import build
import os
import json
from googleapiclient.errors import HttpError
import pandas as pd
import AnalisisSentimiento


# NO FUNCIONALES
# API_KEY = 'AIzaSyDpszMMMOUF5-UAKFgol_PkNL-yynGrm_o' NO USAR ESTA NO FUNCIONA #ETEN 1 V7
# API_KEY = 'AIzaSyAm6dYaJRkBCnNWRu3wlaKAiPH0R7sQYj8' NO USAR ESTA NO FUNCIONA #ETEN 2 V7
# API_KEY = 'AIzaSyBoMHUrv3fV8SxPkD7glL1Bg-ChLySgeec' NO USAR ESTA NO FUNCIONA #ETEN 3 V7
# API_KEY = 'AIzaSyCOslOfaXKgSKizk0kl4EjUiAY8XW-bNYc' NO USAR ESTA NO FUNCIONA #ETEN 4 V7
# API_KEY = 'AIzaSyBr92n46pRMd5YPKoMibZ9cxrlDx_yQgns' NO USAR ESTA NO FUNCIONA #ETEN 5 V7
# API_KEY = 'AIzaSyAwna4o263V8AXg9E_aHD4Xl3mlP2Vto0s' NO USAR ESTA NO FUNCIONA #ETEN 6 V7
# API_KEY = 'AIzaSyAUhCwefUaYwI0UUnjsaYCS7SIMDovuY2Y' NO USAR ESTA NO FUNCIONA #ETEN 7 V7
# API_KEY = 'AIzaSyCdRCf0j6rdvsgJeisstLfHpUX_Ek80Hcg' NO USAR ESTA NO FUNCIONA #ETEN 8 V7
# API_KEY = 'AIzaSyC7fjU_tyZF9ooIpYLqpTf_r5LbtaGT0CU' NO USAR ESTA NO FUNCIONA #ETEN 9 V7
# API_KEY = 'AIzaSyDbopTGy2oaK742rQqlzF0mQb3zNRQ8f5g' NO USAR ESTA NO FUNCIONA #ETEN 10 V7
# API_KEY = 'AIzaSyDUK1ZWGHhDXLDTUYiC5HlyHs4hhH85e4o' NO USAR ESTA NO FUNCIONA #ETEN 11 V7
# API_KEY = 'AIzaSyAIyxRxl-PmFs1h_xZXg4-vi-M3qvAF-7E' NO USAR ESTA NO FUNCIONA #ETEN 12 V7


# FUNCIONALES
# API_KEY = 'AIzaSyCp9wr43CLpp02FnZPYF4aTi8SuIZ3sE_E'
# API_KEY = 'AIzaSyDSYGd1W9HHIofRBr-DjZLG_GUlbDqLNxQ' # Rober
# API_KEY = 'AIzaSyCs6FGPDPU_EwzwZ-t9rLimZMUcW4BNj80'
# API_KEY = 'AIzaSyBSamf7FvHUAkOkWMKsZmy0uaXXgEEJ7xI'
# API_KEY = 'AIzaSyDfGzMMQi5Kk2c-5fmVlOJHu8HWW2iZO6Y' #ETEN 9 V3
# API_KEY = 'AIzaSyBnruy1PukSyB5r_aAoZmQ7UtmtvuZgRSw' #ETEN 10 V3
# API_KEY = 'AIzaSyCGGupT8tR4QNhDzEuBwWUmoggd8E2W3KM' #ETEN 11 V3
# API_KEY = 'AIzaSyA8uGQQEUvLfenpgyi20GKUAOYlgOfCT6U' #ETEN 12 V3
# API_KEY = 'AIzaSyC5JqynwqM5BMPAtGuPfGyesWes12Jaa4k' #ETEN 9 V1
# API_KEY = 'AIzaSyAD2A40-I3bC8IYpcOsEtNEYjs_EpNhyc0' #ETEN 10 V1
# API_KEY = 'AIzaSyBsyBZDG0BF6F9BAi95G_bW_wVP3xt7_sc' #ETEN 11 V1
# API_KEY = 'AIzaSyDqB2JlDslftu_18ebkAE_5XG30Mivu9Bs' #ETEN 12 V1

# API_KEY = 'AIzaSyBoTD-PhKmAGCtJsVPqVzX7UhyaLSvFElI' #ETEN 4 V1
# API_KEY = 'AIzaSyBiEAoDNOj_8EZYl3CqqzlMNmdBdBz4myE' #ETEN 5 V1
# API_KEY = 'AIzaSyBFVOV4GeyX41mnPrGKul_4oh0im4utIOk' #ETEN 6 V1
# API_KEY = 'AIzaSyBENfn34CTKfv8-_5ksys5gttv6KjiQmJw' #ETEN 7 V1
# API_KEY = 'AIzaSyDU_TvRPkDLkCs8N-fY8Bv3i0CbHMI6u4o' #ETEN 8 V1



def obtenerComentarios(recetaBuscar):

    # Variable con el texto a buscar en YouTube
    datoBuscar = recetaBuscar

    # Inicializamis nuestr variable youtube con la conexion a youtube, utilizamos la version 3 de la api y nuestra clave o key
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Hacemos la busqueda en youtube la cual nos devuelve una lista con los videos buscados
    # La variable q contiene lo que queremos buscar en youtube
    # La variable part nos devuelve lo que estamos buscando de cada video en nuestro caso el id y el snippet
    # El snippet contiene los metadatos basicos del video, titulo, descripcion, comentarios...
    # La variable type es el tipo de elemento que queremos buscar en nuestro caso video
    # La variable order ordena los videos que estamos buscando en nuestro caso por relevancia,
    # aunque tambien podemos hacerlo por visualizaciones: order='viewCount'
    # La variable maxResults indica la cantidad de videos que queremos buscar
    todosVideos = youtube.search().list(q=datoBuscar, part='id,snippet', type='video', order='relevance',
                                        maxResults=5).execute()

    # Esto se modificara por una BBDD
    rutaJson = 'comentarios.json'
    if os.path.exists(rutaJson):
        if not rutaJson:
            with open(rutaJson, 'r', encoding="utf8") as f:
                data = json.load(f)
        else:
            data = {}
    else:
        data = {}

    # Iteramos por cada uno de los videos obtenidos anteriormente
    for video in todosVideos.get('items', []):
        # Sacamos el id del video (es un string no un int)
        video_id = video['id']['videoId']

        # Guardamos en una variable la url del video al anadirle el id
        video_url = 'https://www.youtube.com/watch?v=' + video_id

        # Variable que contendra todos los comentarios ya tratados
        todosComentarios = []
        # Variable en la que se iran anadiendo cada uno de los comentarios en bruto
        sumaComentarios = []
        try:
            # Guardamos los 100 primeros comentarios en la variable comentariosVideo con formato de texto plano
            # no son realmente los comentarios sino una lista con toda la informacion y metadatos de los comentarios
            comentariosVideo = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText",
                                                             maxResults=100).execute()

            # Variable que comprueba si hay mas comentarios
            banderaHayMasComentarios = True

            # Si hay mas de 100 comentarios entrara en el while para sacar todos los comentarios,
            # esto lo hacemos ya que hay un maximo de comentarios asique hay que ir extrayendolos de 100 en 100 para
            # el buen funcionamiento de la API
            while banderaHayMasComentarios:
                sumaComentarios += comentariosVideo["items"]

                # Revisa si hay mas paginas de comentarios, es decir si hay mas comentarios de los que acabamos
                # de anadir a sumaComentarios. Si es asi se vuelven a coger los 100 siguientes como antes, sino
                # se pone en false la banderaHayMasComentarios, para no volver a entrar al bucle, es decir que
                # ya no hay mas comentarios
                if "nextPageToken" in comentariosVideo:
                    comentariosVideo = youtube.commentThreads().list(part="snippet", videoId=video_id,
                                                                     textFormat="plainText", maxResults=100,
                                                                     pageToken=comentariosVideo["nextPageToken"]).execute()
                else:
                    banderaHayMasComentarios = False

            # Por ultimo recorremos la variable de sumaComentarios con todos los metadatos de los comentarios para
            # seleccionar unicamente el texto de estos
            for sumaCom in sumaComentarios:
                # Con la siguiente linea apuntamos a la informacion del comentario gracias a:["snippet"]["topLevelComment"],
                # y extraemos el contenido del cometario con ["snippet"]["textDisplay"]
                comentariosIndividuales = sumaCom["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                # seguidamente la anadimos a nuestra variable que contiene todos los comentarios del video
                todosComentarios.append(comentariosIndividuales)
            # Al terminar de guardar todos los comentarios los metemos en cada uno de los videos dentro de la variable data,
            # creando una estructura json.
            data[video_url] = todosComentarios
            # print(todosComentarios)
        except HttpError as error:
            # Con este except evitamos que falle la busqueda de los videos con un error de http
            # En este if comprobamos la respuesta 403 para ver si el video tiene o no comentarios habilitados
            if error.resp.status == 403 and b"commentsDisabled" in error.content:
                print("Los comentarios estan deshabilitados para el video: " + video_url)
            else:
                print(
                    "Ocurrio un error al obtener los comentarios para el video: " + video_url)

    # Esto se modificara por una BBDD
    with open(rutaJson, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    print('Comentarios almacenados en el archivo: ' + rutaJson)


# pip install clean-text
# clean(text,no_emoji=True)


datos = pd.read_csv('recetas_csv/df_recetas_gratis_v2.csv',
                    delimiter=';')

# Esto se utiliza para no exceder las peticiones de la api y que no de error
# Se van ejecutando por tramos los csv
# empieza 2 mas que el primero y acaba uno menos que el ultimo
datos_seleccionados = datos.iloc[10900:10980]

for indice, fila in datos_seleccionados.iterrows():

    titulo_recetas = fila['titulo']
    print(titulo_recetas)
    obtenerComentarios(titulo_recetas)

    sentimientoPos, sentimientoNeg = AnalisisSentimiento.analisisSentimiento()
    datos.at[indice, 'sentimientoPos'] = sentimientoPos
    datos.at[indice, 'sentimientoNeg'] = sentimientoNeg


datos.to_csv('recetas_csv/df_recetas_gratis_v2.csv', sep=";", index=False)
