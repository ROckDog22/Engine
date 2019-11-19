from tqdm import tqdm
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests
import configparser
import concurrent
from concurrent.futures import ThreadPoolExecutor
import re
Heads = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
}


if __name__ == '__main__':
    root = 'http://wufazhuce.com/article/'
    try:
        html = requests.get(root+'166', headers=Heads)
    except Exception as e:
        print("-----%s: %s-----" % (type(e), root))

    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    try:
        text = soup.find('div', class_="one-articulo")
        title = text.find('h2', class_='articulo-titulo')
        author = text.find('p', class_='articulo-autor')
        text = text.find('div', class_='articulo-contenido')
    except Exception as e:
        print("-----%s: %s" % (type(e), root))

    else:
        content = text.text
        print(text)
