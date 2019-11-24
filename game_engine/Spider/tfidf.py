# # -*- coding: utf-8 -*-
# """
# @Author    : wfs2010
# @Email     : 1337581543@qq.com
# @License   : Copyright(C), KEDACOM
# @Time      : 2019/10/28 下午9:47
# @File      : tfidf.py
# @Version   : 1.0
# @Desciption:  专门负责计算文档的长度。
# """
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.feature_extraction.text import CountVectorizer
# import os
# import configparser
# import numpy as np
# import xml.etree.ElementTree as ET
#
# def cal_ti():
#     config = configparser.ConfigParser()
#     config.read('../config.ini', 'utf-8')
#     path = config['DEFAULT']['doc_dir_path']
#     files = os.listdir(path)
#     N = config['DEFAULT']['doc_n']
#     print(len(files))
#     #创建表 文件名，tfidf值。
#     sql =
#     # 计算每个表的tf.idf
#     #我需要 idf tf  idf = log N/df tf =  np.log(tf+e)
#     #通过查询得知 idf 但是tf不知道。
#     c.execute('''DROP TABLE IF EXISTS doc_len''')
#     c.execute('''CREATE TABLE doc_len(id int primary key not null auto_increment,
#                         length double(7,3) null )''')
#     c.execute('''alter table doc_len convert to character set utf8''')
#     number = 0;
#     for word in word_list:
#         tf =
#         idf = np.log(N/(self.postings_lists[word][0]))
#         number =  tf*idf
#         name = id.split('.')[0]
#         sql = "INSERT INTO doc_len VALUES ('%s', '%s')" % (name, number)
#     number = np.sqrt(number)
#         c.execute(sql)
#     pass
#
#
#
# if __name__== "__main__":
#     tfidf()