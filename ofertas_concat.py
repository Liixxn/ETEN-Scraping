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
    #df_dia['precioAnterior'] = str(df_dia['precioAnterior']).trim()
    #df_dia['precioActual'] =str(df_dia['precioActual']).str.trim()

    
    # Renombrar las columnas de df_dia para que coincidan con las de df_carrefour
    df_dia.columns = ['nombreOferta', 'precioActual', 'precioAnterior', 'imagenOferta', 'urlOferta', 'categoria']
    df_carrefour.columns = ['nombreOferta', 'precioActual', 'precioAnterior', 'imagenOferta', 'urlOferta', 'categoria']

    # Concatenar los dos DataFrames
    
    df_concatenado = pd.merge(df_carrefour, df_dia, how='outer')
    
    # Guarda el DataFrame concatenado en un archivo CSV
    df_concatenado.to_csv('ofertas/ofertas_concatenadas.csv', sep=';', index=False, encoding='ISO 8859-1')

if __name__ == '__main__':
    main()