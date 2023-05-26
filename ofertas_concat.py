#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from carrefour import scraper_carrefour
from Dia import scraper_dia
import pandas as pd

def main():
    # Llama a la función de scraping de Carrefour y guarda el resultado en un DataFrame
    df_carrefour = scraper_carrefour()

    # Llama a la función de scraping de DIA y guarda el resultado en un DataFrame
    df_dia = scraper_dia()

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
    df_mergeado = pd.concat([df_carrefour, df_dia], ignore_index=True)

    # Guarda el DataFrame concatenado en un archivo CSV
    df_mergeado.to_csv('ofertas/ofertas_concatenadas.csv', sep=';', index=False)

if __name__ == '__main__':
    main()
