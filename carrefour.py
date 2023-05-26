import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept-Language': 'es'
}


def leerHtml(url):
    r = requests.get(url, headers=header)
    return BeautifulSoup(r.content, "html.parser")


def paginacion(url_carrefour):
    page_carrefour_ofertas = requests.get(url_carrefour, headers=header)
    soup_carrefour_ofertas = BeautifulSoup(page_carrefour_ofertas.content, 'html.parser')
    pagination = soup_carrefour_ofertas.find('select', attrs={'class': 'selectPagination'}).find_all('option')

    df = pd.DataFrame()
    df['titulo'] = ""
    df['price'] = ""
    df['price_less'] = ""
    df['url_img'] = ""
    df['url'] = ""
    df['category'] = ""

    for i in pagination:
        pag = leerHtml("https://www.carrefour.es" + i['value'])
        product_cards = pag.find_all('article', {'class': 'product-card-item'})
        for card in product_cards[:-1]:

            badge = card.find('div', {'class': 'bg-promocion-copy'})

            if badge is None:

                name = card.find('p', {'class': 'title-product'}).text.strip()
                # Imprimo todos los productos que no tienen descuentos especiales (los que nos interesan)

                try:
                    price = card.find('span', {'class': 'price'}).text.strip()
                    continue
                except:
                    price = card.find('span', {'class': 'strike-price'}).text.strip()
                    price_less = card.find('span', {'class': 'price-less'}).text.strip()

                image_url = card.find('img')['src']

                url = card.find('a')['href']
                url_oferta = "https://www.carrefour.es" + url

                parsed_url = urlparse(url)

                query_parms = parse_qs(parsed_url.query)

                prt_id = query_parms['prtId'][0]

                df.loc[len(df)] = {'titulo': name, 'price': price, 'price_less': price_less, 'url_img': image_url, 'url': url_oferta, 'category': prt_id}
            else:

                # Imprime los productos que tienen descuentos en plan 3x2 o 50% descuento
                name = card.find('p', {'class': 'title-product'}).text.strip()
                #print('------------------- Product Name:', name)

    return df

def scraper_carrefour():

    df_productos_frescos = paginacion(
        "https://www.carrefour.es/supermercado/ofertas/N-177ap79Zwhajzd?No=0&Nr%3DAND%28product.shopCodes%3A004320%2Cproduct.salepointWithActivePrice_004320%3A1%2COR%28product.siteId%3AbasicSite%29%29OR%29=&prtId=cat20002")
    df_despensa = paginacion(
        "https://www.carrefour.es/supermercado/ofertas/N-177ap79Zv6agxv?Nr=AND%28product.shopCodes%3A004320%2Cproduct.salepointWithActivePrice_004320%3A1%2COR%28product.siteId%3AbasicSite%29%2ConSaleSalePoints%3A004320%29&prtId=cat20001")
    df_bebidas = paginacion(
        "https://www.carrefour.es/supermercado/ofertas/N-177ap79Zc7a800?Nr=AND%28product.shopCodes%3A004320%2Cproduct.salepointWithActivePrice_004320%3A1%2COR%28product.siteId%3AbasicSite%29%2ConSaleSalePoints%3A004320%29&prtId=cat20003")

    df_ofertas = pd.concat([df_productos_frescos, df_despensa, df_bebidas])

    #Productos frescos
    df_ofertas['category'] = df_ofertas['category'].str.replace('cat20002', '1')
    #Despensa
    df_ofertas['category'] = df_ofertas['category'].str.replace('cat20001', '2')
    #Bebidas
    df_ofertas['category'] = df_ofertas['category'].str.replace('cat20003', '3')
    df_ofertas['price'] = df_ofertas['price'].str.replace('€', '').str.strip()
    df_ofertas['price_less'] = df_ofertas['price_less'].str.replace('€', '').str.strip()
    df_ofertas['price'] = df_ofertas['price'].str.replace(',', '.').str.strip()
    df_ofertas['price_less'] = df_ofertas['price_less'].str.replace(',', '.').str.strip()
    df_ofertas['price'] = df_ofertas['price'].astype(float)
    df_ofertas['price_less'] = df_ofertas['price_less'].astype(float)

    df_ofertas.columns = ['nombreOferta', 'precioActual', 'precioAnterior', 'imagenOferta', 'urlOferta', 'categoria']

    return df_ofertas
