import pandas as pd

# Cargar el primer DataFrame
df_hola_todo = pd.read_csv('df_hola/df_hola_final_0.csv', sep=';')

# Iterar sobre los demás DataFrames y concatenarlos
for i in range(1, 23):
    filename = f'df_hola/df_hola_final_{i}.csv'
    df = pd.read_csv(filename, sep=';')
    df_hola_todo = pd.concat([df_hola_todo, df])

# Mostrar el resultado final
print(df_hola_todo)
df_hola_todo.to_csv('df_hola_todo.csv', index=False, sep=';')