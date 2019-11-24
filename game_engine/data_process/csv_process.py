# -*- coding: utf-8 -*-
"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 19-10-19 下午10:10
@File      : csv_process.py
@Version   : 1.0
@Desciption:  
"""


import pandas as pd
import numpy as np
import configparser
# 读取整个csv文件


class csv_process:
    csv_path = ""

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        self.csv_path = config['DEFAULT']['csv_path']

    def read(self,url):
        csv_data = pd.read_csv(self.csv_path+''+url)
        df = pd.DataFrame(csv_data)
        for index, row in df.iterrows():
            print(row[0],row[1],row[2])

if __name__=="__main__":
    a = csv_process('../config.ini', 'utf-8')
    a.read("heros.csv")