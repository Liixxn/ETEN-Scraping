from googleapiclient.discovery import build
import os
import json
from googleapiclient.errors import HttpError

API_KEY = 'AIzaSyD8vdwq8_SmkGaTSSVJGc4Fzs2w7OGfc7U'
youtube = build('youtube', 'v3', developerKey=API_KEY)
#order='viewCount'
todosVideos = youtube.search().list(q='gato', part='id,snippet', type='video', order='relevance', maxResults=3).execute()


rutaJson='comentarios.json'
if os.path.exists(rutaJson):
    if not rutaJson:
        with open(rutaJson, 'r', encoding="utf8") as f:
            data = json.load(f)
    else:
        data = {}
else:
    data = {}

for video in todosVideos.get('items', []):
    video_id = video['id']['videoId']
    video_url = 'https://www.youtube.com/watch?v=' + video_id
    todosComentarios = []
    sumaComentarios = []
    try:
        comentariosVideo = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText", maxResults = 100).execute()
        banderaHayMasComentarios=True
        while banderaHayMasComentarios:
            sumaComentarios += comentariosVideo["items"]
            # Revisa si hay mas paginas de comentarios
            if "nextPageToken" in comentariosVideo:
                comentariosVideo = youtube.commentThreads().list(part="snippet",videoId=video_id,textFormat="plainText",maxResults=100,pageToken=comentariosVideo["nextPageToken"]).execute()
            else:
                banderaHayMasComentarios=False
        #print(sumaComentarios)
        #Para organizar los comentarios:
        for sumaCom in sumaComentarios:
            comentariosIndividuales = sumaCom["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            todosComentarios.append(comentariosIndividuales)
        data[video_url] = todosComentarios
        #print(todosComentarios)
    except HttpError as error:
        if error.resp.status == 403 and b"commentsDisabled" in error.content:
            print("Los comentarios estan deshabilitados para el video: {}".format(video_url))
        else:
            print("Ocurrio un error al obtener los comentarios para el video: {}".format(video_url))

with open(rutaJson, 'w') as f:
    json.dump(data, f)

print('Comentarios almacenados en el archivo: ' + rutaJson)