# -*- coding: utf-8 -*-
"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 2019/11/9 下午6:24
@File      : textspider.py
@Version   : 1.0
@Desciption:  
"""

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


class spider_man:
    '''
    创建一个爬虫类
    '''

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../config.ini', 'utf-8')

    def crawl_news(self,news):
        text_dir_path = self.config['DEFAULT']['text_dir_path']
        doc_encoding = self.config['DEFAULT']['doc_encoding']
        try:
            html = requests.get(news, headers=Heads)
        except Exception as e:
            print("-----%s: %s-----" % (type(e), news))

        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        try:
            text = soup.find('div', class_="one-articulo")
            title =text.find('h2',class_ ='articulo-titulo')
            author =text.find('p', class_ = 'articulo-autor')
            text = text.find('div',class_ ='articulo-contenido')
            zzz = text.find('div',class_ ='one - articulo')

        except Exception as e:
            print("-----%s: %s" % (type(e), news))

        else:
            content= text.text
            doc = ET.Element("doc")
            ET.SubElement(doc, "title").text = title.text
            ET.SubElement(doc, "author").text = author.text
            ET.SubElement(doc, "text").text = content
            ET.SubElement(doc, "url").text = news
            tree = ET.ElementTree(doc)
            name = news.split('/')[4]
                   # +':'+str(title.text).replace('\t','').replace('\n','').rstrip()
            print(name)
            tree.write(text_dir_path + "%s.xml" % (name), encoding=doc_encoding, xml_declaration=True)

    def runner(self,root):
        thread_pool = ThreadPoolExecutor(max_workers=3, thread_name_prefix='DEMO')
        futures = dict()
        urls = []
        for i in tqdm(range(9,4057)):
            urls.append(root+str(i))

        for url in urls:
            future = thread_pool.submit(self.crawl_news, url)
            futures[future] = url

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print('brother,i"m too hard' + str(e))
        print('OJBK!')


if __name__ == '__main__':
    root = 'http://wufazhuce.com/article/'
    spider_man = spider_man()
    spider_man.runner(root)
