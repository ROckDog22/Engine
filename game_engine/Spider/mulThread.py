"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 19-10-9 下午7:01
@File      : mulThread.py
@Version   : 1.0
@Desciption:
"""
import threading
import random
import queue
from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET
import configparser
import concurrent
from concurrent.futures import ThreadPoolExecutor

Heads = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
}


def get_news_pool(root, start, end):
    '''

    :param root: url
    :param start: 开始页数
    :param end:  结尾页数
    :return:
    '''
    news_pool = []
    for i in range(start, end):
        page_url = ''
        if i == 0:
            page_url = root + 'news/'
        else:
            page_url = root + 'news_all_%d/' % (i)
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
            news_pool.append(news_info)
    return news_pool

def crawl_news(news):
    config = configparser.ConfigParser()
    config.read('../config.ini', 'utf-8')
    min_number = 10
    doc_dir_path = config['DEFAULT']['doc_dir_path']
    doc_encoding = config['DEFAULT']['doc_encoding']
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
    tree = ET.ElementTree(doc)
    tree.write(doc_dir_path + "%s.xml" % id, encoding=doc_encoding, xml_declaration=True)


class Consumer(threading.Thread):
    def __init__(self, name, queue, event, lock, num):
        threading.Thread.__init__(self)
        self.name = "消费者" + str(name)
        self.queue = queue
        self.event = event
        self.lock = lock
        self.num = num
        self.count = 0

    def run(self):
        while self.count < self.num:
            if self.queue.empty():
                self.event.wait()
                if self.event.isSet():
                    self.event.clear()
            else:
                if self.queue.full():
                    self.lock.acquire()
                    data = self.queue.get()
                    for i in data:
                        crawl_news(i)
                    self.queue.task_done()
                    self.lock.release()
                    print(self.name + " Spend data " + str(data))
                    self.event.set()
                else:
                    self.lock.acquire()
                    data = self.queue.get()
                    for i in data:
                        crawl_news(i)
                    self.queue.task_done()
                    self.lock.release()
                    print(self.name + " Spend data " + str(data))

            self.count += 1




class Producer(threading.Thread):
    def __init__(self, root,name, queue, event, num):
        threading.Thread.__init__(self)
        self.name = "生产者" + str(name)
        self.queue = queue
        self.event = event
        self.num = num
        self.count = num-10
        self.root = root

    def run(self):
        while self.count < self.num:
            if self.queue.full():
                self.event.wait()
                if self.event.isSet():
                    self.event.clear()
            else:
                if self.queue.empty():
                    data = get_news_pool(root,self.count,self.count+1)
                    self.queue.put(data)
                    print(self.name + " produced data " + str(data))
                    self.event.set()
                else:
                    data = get_news_pool(root,self.count,self.count+1)
                    self.queue.put(data)
                    print(self.name + " produced data " + str(data))

            self.count += 1


if  __name__ == "__main__":
    # 初始化
    root = 'https://www.3dmgame.com/'

    q_data = queue.Queue(maxsize=100)
    event = threading.Event()
    lock = threading.Lock()

    if event.isSet:
        event.clear()

    for each in range(2):
        c = Consumer(each, q_data, event, lock, 10)
        p = Producer(root,each, q_data, event, 10+each*10)
        c.start()
        p.start()

    q_data.join()