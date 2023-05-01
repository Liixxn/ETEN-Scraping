import mysql.connector
import pandas as pd
from numpy import double
import re
import pymysql
import json

df = pd.read_csv("recetas_csv/df_hola_todo.csv", sep=";")

for receta in range(len(df["titulo"])):

    ingredientes = df["ingredientes"][receta]

    ingredientes = ingredientes.replace("[", "").replace("]", "")
    # esto para el de df_hola_todo.csv
    arrayIngredientes = ingredientes.split("', '")

    arrayIngredientes[0] = arrayIngredientes[0].replace("'", "")
    arrayIngredientes[len(arrayIngredientes) - 1] = arrayIngredientes[len(arrayIngredientes) - 1].replace("'",
                                                                                                          "")
    print(arrayIngredientes[0])



    #arrayIngredientes = arrayIngredientes.replace("'", "")

    print(arrayIngredientes)


    # ingredientes = ingredientes.replace("[", "").replace("]", "")
    # asi para el df_online
    # arrayIngredientes = ingredientes.split('", "')
    # arrayIngredientes[0] = arrayIngredientes[0].replace("', '", "")

    #print(arrayIngredientes)
    #print(len(arrayIngredientes))

