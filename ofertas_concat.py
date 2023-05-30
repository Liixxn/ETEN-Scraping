from carrefour import scraper_carrefour
from Dia import scraper_dia
import pandas as pd
import pymysql
import datetime

def main():
    # Llama a la función de scraping de Carrefour y guarda el resultado en un DataFrame
    df_carrefour = scraper_carrefour()

    # Llama a la función de scraping de DIA y guarda el resultado en un DataFrame
    df_dia = scraper_dia()

    df_dia['precioAnterior'] = df_dia['precioAnterior'].astype(str)
    df_dia['precioActual'] = df_dia['precioActual'].astype(str)

    df_dia['precioAnterior'] = df_dia['precioAnterior'].str.replace('€', '').str.strip()
    df_dia['precioActual'] = df_dia['precioActual'].str.replace('€', '').str.strip()
    df_dia['precioAnterior'] = df_dia['precioAnterior'].str.replace(',', '.').str.strip()
    df_dia['precioActual'] = df_dia['precioActual'].str.replace(',', '.').str.strip()
    #df_dia['precioAnterior'] = df_dia['precioAnterior'].str.replace('€', '')
    #df_dia['precioActual'] = df_dia['precioActual'].str.replace('€', '')
    #df_dia['precioAnterior'] = str(df_dia['precioAnterior'])
    #df_dia['precioActual'] =str(df_dia['precioActual'])


    # Renombrar las columnas de df_dia para que coincidan con las de df_carrefour
    df_dia.columns = ['nombreOferta', 'precioActual', 'precioAnterior', 'imagenOferta', 'urlOferta', 'categoria']
    df_carrefour.columns = ['nombreOferta', 'precioActual', 'precioAnterior', 'imagenOferta', 'urlOferta', 'categoria']

    #Cambiar el tipo de dato de las columnas de precioActual y precioAnterior a float
    df_dia['precioActual'] = df_dia['precioActual'].astype(float)
    df_dia['precioAnterior'] = df_dia['precioAnterior'].astype(float)

    #merge de los dos dataframes
    df = pd.concat([df_carrefour, df_dia], ignore_index=True)

    conn = pymysql.connect(host='195.235.211.197', user='pc2_grupo3', password='PComputacion.23', database='pc2_grupo3')
    cursor = conn.cursor()

    sql_obtenerDatos = "SELECT * FROM ofertas"

    cursor.execute(sql_obtenerDatos)
    resultados = cursor.fetchall()

    for oferta in range(len(df)):
        sql = "INSERT INTO ofertas (nombreOferta, precioActual, precioAnterior, imagenOferta, urlOferta, categoria, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        nombreOferta = str(df["nombreOferta"][oferta])
        precioActual = float(df["precioActual"][oferta])
        precioAnterior = float(df["precioAnterior"][oferta])
        imagenOferta = str(df["imagenOferta"][oferta])
        urlOferta = str(df["urlOferta"][oferta])
        categoria = str(df["categoria"][oferta])
        fecha_inserccion = datetime.datetime.now()

        cursor.execute(sql, (
        nombreOferta, precioActual, precioAnterior, imagenOferta, urlOferta, categoria, fecha_inserccion))

        sqlTrasInserccion = "SELECT id FROM ofertas ORDER BY id DESC LIMIT 1"
        cursor.execute(sqlTrasInserccion)
        resultadosTrasLaInserccion = cursor.fetchone()

        conn.commit()

    print("Se han obtenido las ofertas con éxito")

if __name__ == '__main__':
    main()
