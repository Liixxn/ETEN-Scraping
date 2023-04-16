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
    
    df_dia['precio_original'] = df_dia['precio_original'].str.replace('€', 'EUR')
    df_dia['precio_actual'] = df_dia['precio_actual'].str.replace('€', 'EUR')
    
    # Renombrar las columnas de df_dia para que coincidan con las de df_carrefour
    df_dia.columns = ['titulo', 'price', 'price_less', 'url_img', 'url']
    
    # Concatenar los dos DataFrames
    df_concatenado = pd.concat([df_carrefour, df_dia], ignore_index=True)
    
    # Guarda el DataFrame concatenado en un archivo CSV
    df_concatenado.to_csv('ofertas/ofertas_concatenadas.csv', sep=';', index=False, encoding='ISO 8859-1')

if __name__ == '__main__':
    main()