import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse

header = {
    'User-Agent': 'Chrome 108.0.5359.125',
    'Accept-Language': 'es'
}
# Dataframe que guarda la informacion
df_dia = pd.DataFrame(columns=['nombre', 'precio_original', 'precio_actual', 'imagen', 'url', 'categoria'])
# link de la pagina principal de dia
url_original = 'https://www.dia.es'
# link de la pagina web de ofertas para dia
url = 'https://www.dia.es/compra-online/ofertas-DIA-online'
# lista que guarda las diferentes categorias que existen en alimentacion
words = ['/bebidas/', '/frescos/', '/congelados/', '/despensa/', '/bodega/', '/platos-preparados/']

# lista que guardara el numero total de paginas que hay en las ofertas
lista_hojas_ofertas_dia = []
# se aniade la priemra url
lista_hojas_ofertas_dia.append(url)

final_ofertas_dia = False

# Bucle que comprueba que no se haya llegado al final de las paginas de las ofertas
while (final_ofertas_dia==False):
    
    response = requests.get(url, headers=header)
    soup_dia = BeautifulSoup(response.content, 'html.parser')
    # Se comprueba que exista el marcador que comprueba que existe una siguiente hoja de ofertas
    next_button = soup_dia.find('a', class_="btn-pager btn-pager--next")
    # Si este marcador es nulo, significa que hemos llegado al final de las hojas de ofertas
    if next_button is None:
        final_ofertas_dia = True
    else:
        # Se obtiene la url para el marcador, que es la siguiente hoja de ofertas
        next_button = soup_dia.find('a', class_="btn-pager btn-pager--next").get('href') 
        # Se une el link de la pagina principal de dia y la url obtenida anteriormente, ya que este href obtenido es un
        # link que se basa en el link de la principal
        link_unido = url_original+next_button
        # Se aniade a la lista de hojas de las ofertas
        lista_hojas_ofertas_dia.append(link_unido)
        # Se reemplaza el link nuevo para que sea el siguiente a evaluar
        url = link_unido

        
# listas que guardaran los diferentes productos   
nombre_producto = []        
precios_original = []
precios_descuento = []
imagenes_producto = []
productos_urls = []
categorias_producto = []  # lista que guarda la categoría para cada producto

# Se recorre la lista de hojas de las ofertas
for link in lista_hojas_ofertas_dia:
    response = requests.get(link, headers=header)
    soup_dia_ofertas = BeautifulSoup(response.content, 'html.parser')
    # Se obtienen todos los productos que se encuentren en

    # Se obtienen todos los productos que se encuentren en esa hoja
    productos = soup_dia_ofertas.find_all('div', class_="product-list__item")


# Se recorre cada producto para ser analziado, ya que en la pagina de ofertas tambien se encuentran elementos que no
# pertencen a alimentacion, por lo que se debe realizar un filtro. Para ello se va hacer uso de la lista 'words' que
# comprueba que en la url de cada producto aparezca alguno de esas categorias, ya que asi se puede determinar que
# producto pertenece a alimentacion y a que categoria.
# Se recorre la lista de hojas de las ofertas
for link in lista_hojas_ofertas_dia:
    response = requests.get(link, headers=header)
    soup_dia_ofertas = BeautifulSoup(response.content, 'html.parser')
    # Se obtienen todos los productos que se encuentren en
    # esa hoja
    productos = soup_dia_ofertas.find_all('div', class_="product-list__item")

    for product in productos:
        for i, word in enumerate(words):
            # Aqui se comprueba que exista en la url alguna de las categorias
            if word in product.find('a').get('href'):
                

                # Se obtiene el precio del producto
                precio = product.find('p', class_='price')
                # Se comprueba que la longitud del precio devuelto sea mayor a 1, ya que para los productos que se encuentran
                # en oferta disponen del precio original y el precio con la oferta aplicada.
                # Si un producto tiene el precio reducido en su tag <p> se encuentran los dos precios
                if len(precio) > 1:
                    # Se obtiene el nombre del producto
                    nombre = product.find('span', class_='details').text.strip()
                    nombre_producto.append(nombre)
                    # Se obtiene el precio original
                    precio_original = precio.find('s').get_text()
                    precios_original.append(precio_original)
                    # Se obtiene el precio con descuento
                    precio_oferta = precio.find('span').get_text()
                    precios_descuento.append(precio_oferta)
                    # Se obtiene la imagen del producto
                    imagen = product.find('img', class_="crispImage").get('src')
                    imagenes_producto.append(imagen)

                    producto_url = product.find('a').get('href')
                    productos_urls.append(url_original+producto_url)
                   
                    url_tratada = urlparse(producto_url)
                    componente = url_tratada.path.split("/")
                    categoria = componente[2]
                    categorias_producto.append(categoria)





df_dia = pd.DataFrame({'nombre': nombre_producto, 
                       'precio_original': precios_original, 
                       'precio_actual': precios_descuento, 
                       'imagen': imagenes_producto, 
                       'url': productos_urls, 
                       'categoria': categorias_producto})

df_dia["categoria"] = df_dia["categoria"].str.replace("bodega", "3")
df_dia["categoria"] = df_dia["categoria"].str.replace("bebidas", "3")
df_dia["categoria"] = df_dia["categoria"].str.replace("platos-preparados", "1")
df_dia["categoria"] = df_dia["categoria"].str.replace("frescos", "1")
df_dia["categoria"] = df_dia["categoria"].str.replace("congelados", "2")
df_dia["categoria"] = df_dia["categoria"].str.replace("despensa", "2")
pd.set_option('display.max_rows', None)

def scraper_dia():
    df_dia['nombre'] = nombre_producto
    df_dia['precio_original'] = precios_original
    df_dia['precio_actual'] = precios_descuento
    df_dia['imagen'] = imagenes_producto
    df_dia['url'] = productos_urls
    df_dia['categoria'] = categorias_producto
    
    return df_dia

# Se escribe el contenido del dataframe a un csv
#df_dia.to_csv('ofertas/dia-ofertas.csv', sep=';', index=False)