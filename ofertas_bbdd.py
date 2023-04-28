import mysql.connector
import pandas as pd
from numpy import double
import re
import pymysql

df = pd.read_csv("ofertas/ofertas_concatenadas.csv", sep=";", encoding='ISO 8859-1')

conn = pymysql.connect(host='195.235.211.197', user='pc2_grupo3', password='PComputacion.23', database='pc2_grupo3')
cursor = conn.cursor()

sql_obtenerDatos = "SELECT * FROM ofertas"

cursor.execute(sql_obtenerDatos)
resultados = cursor.fetchall()

ofertaEncontrada = False

if len(resultados) > 0:
    for oferta in range(len(df["nombreOferta"])):
        ofertaEncontrada = False
        final = 0
        while(ofertaEncontrada==False and final < len(resultados)):
            if (df["nombreOferta"][oferta] == resultados[final][0]) and (df["imagenOferta"][oferta] == resultados[final][3] and (df["urlOferta"][oferta] == resultados[final][4])):
                ofertaEncontrada = True
            else:
                final += 1

        if ofertaEncontrada == False:
            sql = "INSERT INTO ofertas (nombreOferta, precioActual, precioAnterior, imagenOferta, urlOferta, categoria) VALUES (%s, %s, %s, %s, %s, %s);"
            nombreOferta = str(df["nombreOferta"][oferta])
            precioActual = str(df["precioActual"][oferta])
            precioAnterior = str(df["precioAnterior"][oferta])
            imagenOferta = str(df["imagenOferta"][oferta])
            urlOferta = str(df["urlOferta"][oferta])
            categoria = str(df["categoria"][oferta])

            sqlTrasInserccion = "SELECT id FROM ofertas ORDER BY id DESC LIMIT 1"
            cursor.execute(sqlTrasInserccion)
            resultadosTrasLaInserccion = cursor.fetchone()



else:
    for oferta in range(len(df[:2])):
        sql = "INSERT INTO ofertas (nombreOferta, precioActual, precioAnterior, imagenOferta, urlOferta, categoria) VALUES (%s, %s, %s, %s, %s, %s);"
        nombreOferta = str(df["nombreOferta"][oferta])
        precioActual = str(df["precioActual"][oferta])
        precioAnterior = str(df["precioAnterior"][oferta])
        imagenOferta = str(df["imagenOferta"][oferta])
        urlOferta = str(df["urlOferta"][oferta])
        categoria = str(df["categoria"][oferta])

        sqlTrasInserccion = "SELECT id FROM ofertas ORDER BY id DESC LIMIT 1"
        cursor.execute(sqlTrasInserccion)
        resultadosTrasLaInserccion = cursor.fetchone()


        conn.commit()
