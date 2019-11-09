# -*- coding: utf-8 -*-
"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 2019/11/3 下午6:48
@File      : fileall.py
@Version   : 1.0
@Desciption:  
"""

from os import  listdir
import xml.etree.ElementTree as ET
import  configparser
def toge_all():
    config = configparser.ConfigParser()
    config.read('../config.ini', 'utf-8')
    files = listdir(config['DEFAULT']['doc_dir_path'])
    f = open('./toge_all.txt','a')
    z=0
    for i in files:
        z = z+1
        if z >400:
            break
        root = ET.parse(config['DEFAULT']['doc_dir_path'] + i).getroot()
        doc = root.find('text').text
        doc = doc.replace(' ','')
        doc = doc.replace('\n','')
        print(doc)
        f.write(doc)
    f.close()

def filre():
    f = open('./toge_all.txt', 'w')
    doc = f.read()
    doc.replace("\n",'')
    print(doc)
    f.close()
if __name__=='__main__':
    # filre()
    toge_all()