import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.avito.ru/moskva/avtomobili?cd=1&radius=0"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51", "accept": "*/*"}
HOST = "https://www.avito.ru"
FILE = "cars.csv"


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages(html):
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find_all("span", class_="pagination-item-1WyVp")
    return int(pagination[-2].get_text())


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="item__line")
    cars1 = []
    for item in items:
        cars1.append({
            "title": item.find("span", class_="snippet-link-name").get_text(strip=True),
            "link": HOST + item.find("a", class_="snippet-link").get("href"),
            "price": item.find("div", class_="snippet-price-row").get_text(strip=True),
            "location": item.find("span", class_="item-address-georeferences-item__content").get_text(),
        })
    return cars1


def save_file(items, path):
    with open(path, "w", newline="", encoding="utf-16") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Name", "Ссылка", "Цена", "Место"])
        for item in items:
            writer.writerow([item["title"], item["link"], item["price"], item["location"]])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages = get_pages(html.text)
        for page in range(1, pages - 98):
            print(f"Парсинг страницы {page} из {pages}...")
            html = get_html(URL, params={"p": page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
    else:
        print("Ответ не получен.")



parse()