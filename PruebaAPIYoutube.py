import csv
from googleapiclient.discovery import build
import os
import json
from googleapiclient.errors import HttpError
import pandas as pd
import AnalisisSentimiento


# NO FUNCIONALES
# API_KEY = 'AIzaSyD8vdwq8_SmkGaTSSVJGc4Fzs2w7OGfc7U' PERMISO DENEGADO # Loffel
# API_KEY = 'AIzaSyBDkbGwmJ7siXkT9l6q7CMaz_IYB2jPJZ4' NO USAR ESTA NO FUNCIONA
# API_KEY = 'AIzaSyDu24NEirW1WDcMk564p8o8XALiLDU6jEM' NO USAR ESTA NO FUNCIONA  #ETEN 2
# API_KEY = 'AIzaSyD4Dx59fJ4SkuYo4cdmNFLiqa4aRgVDThg' NO USAR ESTA NO FUNCIONA  #ETEN 3
# API_KEY = 'AIzaSyDJnC9nAKtb9PUwXNccit-YtrJXmSxXfLo' NO USAR ESTA NO FUNCIONA  #ETEN 4
# API_KEY = 'AIzaSyBrk6zx8jN9ffdkbyQZv6f0cVqXPizvK-Q' NO USAR ESTA NO FUNCIONA  #ETEN 5
# API_KEY = 'AIzaSyDDcMR8_oddrAIxJjHxL1cVcc66Ni6g5dU' NO USAR ESTA NO FUNCIONA  #ETEN 6
# API_KEY = 'AIzaSyCqFAJMVEkkLXVXq9NzgvCK4cmEC_VhUrs' NO USAR ESTA NO FUNCIONA  #ETEN 7
# API_KEY = 'AIzaSyAD9mv54ByCNWHKxkW4hAVUJCRGGVaizV4' NO USAR ESTA NO FUNCIONA  #ETEN 8
# API_KEY = 'AIzaSyDiUygE5PWK2A_1LkWhZDQo6ORZNgc8D9Y' NO USAR ESTA NO FUNCIONA  #ETEN 9
# API_KEY = 'AIzaSyB93IGtw5_nuRhcImpAGWRhUc7ranbg6LE' NO USAR ESTA NO FUNCIONA   #ETEN 11
# API_KEY = 'AIzaSyDNIAo7tZbaWzv2wPZfsSybzjmEIn8Irbg'  #ETEN 10
# API_KEY = 'AIzaSyDWHjnOU4-mTntPZHd4-C8qYuYnUGHzW9Y' NO USAR ESTA NO FUNCIONA #ETEN 12
# API_KEY = 'AIzaSyD6ekizqDFNazha_sNZd-00-KcaKnp_tNc' NO USAR ESTA NO FUNCIONA #ETEN 1 V2
# API_KEY = 'AIzaSyBHmAby7HWddjhSfJLgio3STSQZ9q4aQOs' NO USAR ESTA NO FUNCIONA #ETEN 2 V2
# API_KEY = 'AIzaSyBiE65QyeOcEB1J3OkbwaKnOaZCWv7IBOc' NO USAR ESTA NO FUNCIONA #ETEN 3 V2
# API_KEY = 'AIzaSyC4asSJjbO32e0uySXNphACZwohx9DYpug' NO USAR ESTA NO FUNCIONA #ETEN 4 V2
# API_KEY = 'AIzaSyBiDR8IBpQJIkh-cDqEDQpQ86TO-qPFs_U' NO USAR ESTA NO FUNCIONA #ETEN 5 V2
# API_KEY = 'AIzaSyAQexx10CmLOAAyqwm1E9lt7XcksWDuB8I' NO USAR ESTA NO FUNCIONA #ETEN 6 V2
# API_KEY = 'AIzaSyA8wfXv49JRIExaqxij2rCCfW27czY7PyI' NO USAR ESTA NO FUNCIONA #ETEN 7 V2
# API_KEY = 'AIzaSyDYIw9k9YvZyd5b0RxQ6-_NSqbFgFuhAkw' NO USAR ESTA NO FUNCIONA #ETEN 8 V2
# API_KEY = 'AIzaSyCopAl4t4oVUjYhQXyiH1tb2tuFYHa1KYo' NO USAR ESTA NO FUNCIONA #ETEN 9 V2
# API_KEY = 'AIzaSyCeSejd5nETIuEQkrahRHxZ46GLL_DK0YQ' NO USAR ESTA NO FUNCIONA #ETEN 10 V2
# API_KEY = 'AIzaSyAHh7-4RzVrRNqab-3iaU2KOlOalpeaSsA' NO USAR ESTA NO FUNCIONA #ETEN 11 V2
# API_KEY = 'AIzaSyAxj5mMSqMDkZS7eXm1zS_0trbQxhqFox8' NO USAR ESTA NO FUNCIONA #ETEN 12 V2
# API_KEY = 'AIzaSyDb-86QdtAwrZCJMkhgcJ7w_tZqzQz-stA' NO USAR ESTA NO FUNCIONA #ETEN 1 V3
# API_KEY = 'AIzaSyB2BeWLY8wcgfsemfNYt1MS7D6TgVe0abw' NO USAR ESTA NO FUNCIONA #ETEN 2 V3
# API_KEY = 'AIzaSyBM_DJJpFbivg_puvK2dvEkRGhm2Bc95X0' NO USAR ESTA NO FUNCIONA #ETEN 3 V3
# API_KEY = 'AIzaSyCVCmvfHJSAFJCyZAh3y1Gm6aWCqQY0kLc' NO USAR ESTA NO FUNCIONA #ETEN 4 V3
# API_KEY = 'AIzaSyACv6RqbK6ZpnO63s_4FTqcX067zk5zqlQ' NO USAR ESTA NO FUNCIONA #ETEN 5 V3
# API_KEY = 'AIzaSyC86hUyS-otknYht8lSvTzMNwr-fj36j6A' NO USAR ESTA NO FUNCIONA #ETEN 6 V3
# API_KEY = 'AIzaSyA961vapEzZja2d12bf6wqHIgm_SmIOa6A' NO USAR ESTA NO FUNCIONA #ETEN 7 V3
# API_KEY = 'AIzaSyCW2CQIn54WiFI5WnYiJZIN2yVpRNsVXs8' NO USAR ESTA NO FUNCIONA #ETEN 8 V3
# API_KEY = 'AIzaSyArVm4ZLq8YdXAIzA3j-qTQ1VEwnrK--fg' NO USAR ESTA NO FUNCIONA #ETEN 1 V4
# API_KEY = 'AIzaSyCpJd-1d941mrg1BAgHf2dMrOJxFv-rtCc' NO USAR ESTA NO FUNCIONA #ETEN 2 V4
# API_KEY = 'AIzaSyDo3cO16DZ5Na9xQ9eA6tZKkqYPYiNpJRM' NO USAR ESTA NO FUNCIONA #ETEN 3 V4
# API_KEY = 'AIzaSyAelcnQ7ingeJj-DVRv1b1SK1Sqy47wX_Y' NO USAR ESTA NO FUNCIONA #ETEN 4 V4
# API_KEY = 'AIzaSyAK99V7N8gNxYKjtYBUApVV8GlZ24uQqtQ' NO USAR ESTA NO FUNCIONA #ETEN 5 V4
# API_KEY = 'AIzaSyDofqndIUq4f9Ghni8WPxTRGDT966bVBJg' NO USAR ESTA NO FUNCIONA #ETEN 6 V4
# API_KEY = 'AIzaSyDaeZe-w0elhvW4LgmKONXcxp2SDzXFbWk' NO USAR ESTA NO FUNCIONA #ETEN 7 V4
# API_KEY = 'AIzaSyBcVu9GY6jSx-fpbf9t_qL1dLR-9Tu9fR8' NO USAR ESTA NO FUNCIONA #ETEN 8 V4
# API_KEY = 'AIzaSyBHP8l4xIiRUURtrx0Vl3DzFYr64kx8XP8' NO USAR ESTA NO FUNCIONA #ETEN 9 V4
# API_KEY = 'AIzaSyBVKSVzEcr7gpPq3LpfmRr4KQUcux_zoDg' NO USAR ESTA NO FUNCIONA #ETEN 10 V4
# API_KEY = 'AIzaSyDG5lJfsV9xAyL8WcKvQ53Cb555wBwUN7k' NO USAR ESTA NO FUNCIONA #ETEN 11 V4
# API_KEY = 'AIzaSyCV-zG7pq_Vn-Q8hYaPs2RePV5wHTXSd6I' NO USAR ESTA NO FUNCIONA #ETEN 12 V4
# API_KEY = 'AIzaSyCMOcxe2amdLpvyY1DGzRHRKo_cBENoOR0' NO USAR ESTA NO FUNCIONA #ETEN 1 V5
# API_KEY = 'AIzaSyCwMhbsrN4G7fjvvIKl7-Z_H16PZ90DuOE' NO USAR ESTA NO FUNCIONA #ETEN 2 V5
# API_KEY = 'AIzaSyC-snXhlTns2ZrnP3vr9upeswmDD9LIBlM' NO USAR ESTA NO FUNCIONA #ETEN 3 V5
# API_KEY = 'AIzaSyCL3FSm18c0UO28BTBUC2NA5DuWyc2vyyY' NO USAR ESTA NO FUNCIONA #ETEN 4 V5
# API_KEY = 'AIzaSyBbk2dw5qt1ETxcvzh_nZRwOEqsL_gwRNw' NO USAR ESTA NO FUNCIONA #ETEN 5 V5
# API_KEY = 'AIzaSyDv9_mo8IdBIklN20wORDgkGzQu6teTU9k' NO USAR ESTA NO FUNCIONA #ETEN 6 V5
# API_KEY = 'AIzaSyB7FTSCTRYf3fQN0decCbbixJYotenACFI' NO USAR ESTA NO FUNCIONA #ETEN 7 V5
# API_KEY = 'AIzaSyAksyuCY6tJsdnTjll4XejtkwWAaJRX2Nw' NO USAR ESTA NO FUNCIONA #ETEN 8 V5
# API_KEY = 'AIzaSyDTiW4sqh0Y-SBi_xK5u7iSTBpW-4HsW4c' NO USAR ESTA NO FUNCIONA #ETEN 9 V5
# API_KEY = 'AIzaSyCYNBMCFaKTXIWuKRX1aNDiDv5Klkh96n4' NO USAR ESTA NO FUNCIONA #ETEN 10 V5
# API_KEY = 'AIzaSyBNEE7B-L0cYWMUOi4M4APy3N58nIDzvxc' NO USAR ESTA NO FUNCIONA #ETEN 11 V5
# API_KEY = 'AIzaSyD4yFrL8rmCKxxv0nRQ8ICYEVLXyEpGnMU' NO USAR ESTA NO FUNCIONA #ETEN 12 V5
# API_KEY = 'AIzaSyD4SxKCeiZnZOuT4SUKpoPHexGdRP1kQY4' NO USAR ESTA NO FUNCIONA #ETEN 1 V6
# API_KEY = 'AIzaSyDJPsUU37faieSXmUEkXqOJhMPNsUwuuX8' NO USAR ESTA NO FUNCIONA #ETEN 2 V6
# API_KEY = 'AIzaSyCH2ONUvVTjX92NCWKEjv875QZBlIquGVw' NO USAR ESTA NO FUNCIONA #ETEN 3 V6
# API_KEY = 'AIzaSyCwE3NsDHa5RJ1M3AGtD4VlFiAaNSUjk0o' NO USAR ESTA NO FUNCIONA #ETEN 4 V6
# API_KEY = 'AIzaSyAVek_49MQ2FYDSpMIGUN1YZgI_H_vb_wA' NO USAR ESTA NO FUNCIONA #ETEN 5 V6
# API_KEY = 'AIzaSyC6uKj5nO4fVmhsjuKyTQswR4knTxTBZrQ' NO USAR ESTA NO FUNCIONA #ETEN 6 V6


# FUNCIONALES
# API_KEY = 'AIzaSyCp9wr43CLpp02FnZPYF4aTi8SuIZ3sE_E'
# API_KEY = 'AIzaSyDSYGd1W9HHIofRBr-DjZLG_GUlbDqLNxQ' # Rober
# API_KEY = 'AIzaSyCs6FGPDPU_EwzwZ-t9rLimZMUcW4BNj80'
# API_KEY = 'AIzaSyBSamf7FvHUAkOkWMKsZmy0uaXXgEEJ7xI'
# API_KEY = 'AIzaSyDfGzMMQi5Kk2c-5fmVlOJHu8HWW2iZO6Y' #ETEN 9 V3
# API_KEY = 'AIzaSyBnruy1PukSyB5r_aAoZmQ7UtmtvuZgRSw' #ETEN 10 V3
# API_KEY = 'AIzaSyCGGupT8tR4QNhDzEuBwWUmoggd8E2W3KM' #ETEN 11 V3
# API_KEY = 'AIzaSyA8uGQQEUvLfenpgyi20GKUAOYlgOfCT6U' #ETEN 12 V3

# API_KEY = 'AIzaSyBrYlEOY_pC1nWsA_80z1B2s1MspX-4JbI' #ETEN 7 V6
# API_KEY = 'AIzaSyAi_gMMCJ41jZy1opH2IU5duz5XaNvGSpQ' #ETEN 8 V6
# API_KEY = 'AIzaSyBDjdfGQ-JghABzhIiJtTreAf1LeLuBPXU' #ETEN 9 V6
# API_KEY = 'AIzaSyBQBhMRObBFZ92vlcP5X8DXSFqFs6THjds' #ETEN 10 V6
# API_KEY = 'AIzaSyBoMpaKMMtuYVE-8ft4gbwvPOd7FlGsLmI' #ETEN 11 V6
# API_KEY = 'AIzaSyBzjJepx1lzLq-eWUSEixfRxz-YnZjR-VA' #ETEN 12 V6
# API_KEY = 'AIzaSyDpszMMMOUF5-UAKFgol_PkNL-yynGrm_o' #ETEN 1 V7
# API_KEY = 'AIzaSyAm6dYaJRkBCnNWRu3wlaKAiPH0R7sQYj8' #ETEN 2 V7
# API_KEY = 'AIzaSyBoMHUrv3fV8SxPkD7glL1Bg-ChLySgeec' #ETEN 3 V7
# API_KEY = 'AIzaSyCOslOfaXKgSKizk0kl4EjUiAY8XW-bNYc' #ETEN 4 V7
# API_KEY = 'AIzaSyBr92n46pRMd5YPKoMibZ9cxrlDx_yQgns' #ETEN 5 V7
# API_KEY = 'AIzaSyAwna4o263V8AXg9E_aHD4Xl3mlP2Vto0s' #ETEN 6 V7
# API_KEY = 'AIzaSyAUhCwefUaYwI0UUnjsaYCS7SIMDovuY2Y' #ETEN 7 V7
# API_KEY = 'AIzaSyCdRCf0j6rdvsgJeisstLfHpUX_Ek80Hcg' #ETEN 8 V7
# API_KEY = 'AIzaSyC7fjU_tyZF9ooIpYLqpTf_r5LbtaGT0CU' #ETEN 9 V7
# API_KEY = 'AIzaSyDbopTGy2oaK742rQqlzF0mQb3zNRQ8f5g' #ETEN 10 V7
# API_KEY = 'AIzaSyDUK1ZWGHhDXLDTUYiC5HlyHs4hhH85e4o' #ETEN 11 V7
# API_KEY = 'AIzaSyAIyxRxl-PmFs1h_xZXg4-vi-M3qvAF-7E' #ETEN 12 V7

# API_KEY = 'AIzaSyBoTD-PhKmAGCtJsVPqVzX7UhyaLSvFElI' #ETEN 4 V1
# API_KEY = 'AIzaSyBiEAoDNOj_8EZYl3CqqzlMNmdBdBz4myE' #ETEN 5 V1
# API_KEY = 'AIzaSyBFVOV4GeyX41mnPrGKul_4oh0im4utIOk' #ETEN 6 V1
# API_KEY = 'AIzaSyBENfn34CTKfv8-_5ksys5gttv6KjiQmJw' #ETEN 7 V1
API_KEY = 'AIzaSyDU_TvRPkDLkCs8N-fY8Bv3i0CbHMI6u4o' #ETEN 8 V1
# API_KEY = '' #ETEN 9 V1
# API_KEY = '' #ETEN 10 V1
# API_KEY = '' #ETEN 11 V1
# API_KEY = '' #ETEN 12 V1


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
datos_seleccionados = datos.iloc[9900:9910]

for indice, fila in datos_seleccionados.iterrows():

    titulo_recetas = fila['titulo']
    print(titulo_recetas)
    obtenerComentarios(titulo_recetas)

    sentimientoPos, sentimientoNeg = AnalisisSentimiento.analisisSentimiento()
    datos.at[indice, 'sentimientoPos'] = sentimientoPos
    datos.at[indice, 'sentimientoNeg'] = sentimientoNeg


datos.to_csv('recetas_csv/df_recetas_gratis_v2.csv', sep=";", index=False)
