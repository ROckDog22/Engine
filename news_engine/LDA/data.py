# -*- coding: utf-8 -*-
"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 2019/11/18 上午9:18
@File      : data.py
@Version   : 1.0
@Desciption:  
"""
import os
import configparser
import xml.etree.ElementTree as ET
def data_toge():
    config = configparser.ConfigParser()
    config.read('../config.ini', 'utf-8')
    files = os.listdir(config['DEFAULT']['doc_dir_path'])
    files = files[:300]
    f = open('./han.txt',"w")
    f.write('content\n')
    num = 0
    for m in range(len(files)):
        i = files[m]
        if m%50==0:
            num=0
        root = ET.parse(config['DEFAULT']['doc_dir_path'] + i).getroot()
        body = root.find('text').text
        body = body.replace('\n','').replace('\t','').replace(',','，')
        body = body.split('。')
        # print(body)
        # docid = int(root.find('id').text)
        for j in body:
            num+=1
            if len(j)>5:
                f.write(str(num)+","+j+'。'+'\n')

    f.close()

if __name__ == '__main__':
    data_toge()