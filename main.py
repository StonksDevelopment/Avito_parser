import requests
from bs4 import BeautifulSoup

URL = "https://youla.ru/moskva/nedvijimost/arenda-kvartiri"


def get_html():
    r = requests.get(URL)
    return r


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("figure", class_="product_figure")
    print(f"Найдено {len(items)} вариантов")
    print("Начинаю парсить")
    house1 = []
    for item in items:
        house1.append({
            ""
        })


def parse():
    html = get_html()
    if html.status_code == 200:
        print("Хорошая работа,Олег!")
        get_content(html.text)
    elif html.status_code == 404:
        print("There was no answer.")
    else:
        print("Error")


parse()
