#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-10-8 下午7:44
# @Author  : wfs2010 +_+
# @require  : 
# @File    : spider.py

from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET
import configparser
import concurrent
from concurrent.futures import ThreadPoolExecutor
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
        self.min_number = 5  # 文本大小

    def get_news_pool(self, root, start, end):
        '''

        :param root: url
        :param start: 开始页数
        :param end:  结尾页数
        :return:
        '''
        news_pool = []
        for i in range(start, end):
            page_url = ''
            if i != start:
                page_url = root + 'news_all_%d/' % (i)
            else:
                page_url = root + 'news/'
            try:
                html = requests.get(page_url, headers=Heads)
            except Exception as e:
                print("-----%s: %s-----" % (type(e), page_url))
                continue
            html.encoding = 'utf-8'
            soup = BeautifulSoup(html.text, 'lxml')
            news_div = soup.find('div', class_="Revision_list")
            li = news_div.find_all('li')
            for i in li:
                date_time = i.span.text
                url = i.a['href']
                title = i.find('div', class_="text").a.text
                news_info = [date_time[0:4] + date_time[4:-1], url, title]
                print(news_info)
                news_pool.append(news_info)
        return news_pool

    def crawl_news(self,news):
        min_number = 10
        doc_dir_path = self.config['DEFAULT']['doc_dir_path']
        doc_encoding = self.config['DEFAULT']['doc_encoding']
        try:
            html = requests.get(news[1], headers=Heads)
        except Exception as e:
            print("-----%s: %s-----" % (type(e), news[1]))

        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        try:
            text = soup.find('div', class_="news_warp_center")
        except Exception as e:
            print("-----%s: %s-----" % (type(e), news[1]))

        image =text.find_all('img')
        video =text.find_all('iframe')
        url_img=""
        url_video=""
        for t in image:
            url_img=url_img+str(t['src'])+"\t"
        for v in video:
            url_video = url_video + str(v['src']) + "\t"
        content = ""
        for t in text.find_all('p'):
            content += t.text + "\n"
        id = str(news[1]).split('/')
        id = id[-2] + '' + id[-1]
        id = id[:-5]
        if len(text) <= min_number:
            return
        doc = ET.Element("doc")
        ET.SubElement(doc, "id").text = "%s" % id
        ET.SubElement(doc, "url").text = news[1]
        ET.SubElement(doc, "title").text = news[2]
        ET.SubElement(doc, "datetime").text = news[0]
        ET.SubElement(doc, "text").text = content
        ET.SubElement(doc, "imageurl").text = url_img
        ET.SubElement(doc, "videourl").text = url_video
        tree = ET.ElementTree(doc)
        tree.write(doc_dir_path + "%s.xml" % id, encoding=doc_encoding, xml_declaration=True)

    def runner(self,root):
        thread_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix='DEMO')
        futures = dict()
        urls = self.get_news_pool(root,0,2000)
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
    root = 'https://www.3dmgame.com/'
    spider_man = spider_man()
    spider_man.runner(root)