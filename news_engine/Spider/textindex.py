# -*- coding: utf-8 -*-
"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 2019/11/9 下午7:38
@File      : textindex.py
@Version   : 1.0
@Desciption:  
"""
# -*- coding: utf-8 -*-
"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 19-10-9 下午9:18
@File      : index.py
@Version   : 1.0
@Desciption:  统计要计算tfidf 必须要有词频以及文档的向量创建倒排索引 并加入到数据库中
"""
'''

'''


from os import listdir
import xml.etree.ElementTree as ET
import jieba
import MySQLdb
import configparser
import numpy as np
class Doc:
    docid = 0
    date_time = ''
    tf = 0
    ld = 0

    def __init__(self, docid, tf, ld):
        self.docid = docid
        self.tf = tf
        self.ld = ld

    def __repr__(self):
        return (str(self.docid) + '\t'  + str(self.tf) + '\t' + str(self.ld))

    def __str__(self):
        return (str(self.docid) + '\t'  + str(self.tf) + '\t' + str(self.ld))


class IndexModule:
    stop_words = set()
    #单词表
    postings_lists = {}
    w_ddic={}
    config_path = ''
    config_encoding = ''

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'], encoding=config['DEFAULT']['stop_words_encoding'])
        words = f.read()
        self.stop_words = set(words.split('\n'))

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False


# 去除停用词
    def clean_list(self, seg_list):
        cleaned_dict = {}
        n = 0
        for i in seg_list:
            i = i.strip().lower()
            if i != '' and not self.is_number(i) and i not in self.stop_words:
                n = n + 1
                # 计算词频
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return n, cleaned_dict


    def write_postings_to_db(self):
        # 建立数据库连接
        db = MySQLdb.connect("localhost", "root", "525926", "engine", charset='utf8')
        c = db.cursor()
        try:
            # 执行sql语句
            c.execute('''DROP TABLE IF EXISTS postings_text''')
            c.execute('''CREATE TABLE postings_text(id int primary key not null auto_increment,
                      term TEXT  not null,
                      df INT,
                      docs TEXT)''')
            c.execute('''alter table postings_text convert to character set utf8''')
            for key, value in self.postings_lists.items():
                doc_list = '\n'.join(map(str, value[1]))
                sql = "INSERT INTO postings_text(term,df,docs) VALUES ('%s', '%s', '%s')" % (key, value[0], doc_list)
                c.execute(sql)

            c.execute('''DROP TABLE IF EXISTS text_len''')
            c.execute('''CREATE TABLE text_len(id bigint unique not null ,
                                   length double(9,4) not null )''')
            c.execute('''alter table text_len convert to character set utf8''')
            for doc,cal in self.w_ddic.items():
                sql = "INSERT INTO text_len VALUES ('%s', '%s')" % (doc, cal)
                c.execute(sql)

            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误时回滚
            print("...mysql error",)
            db.rollback()

        # 关闭数据库连接
        db.close()

    def construct_postings_lists(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        N = config['DEFAULT']['doc_n']
        files = listdir(config['DEFAULT']['text_dir_path'])
        AVG_L = 0
        w_dic = {}# 计算tfidf
        w_ddic = {}# 计算tfidf
        for i in files:
            root = ET.parse(config['DEFAULT']['text_dir_path'] + i).getroot()
            title = root.find('title').text.strip().rstrip()
            body = root.find('text').text
            docid = i.split('.')[0]
            seg_list = jieba.lcut(title + '。' + body, cut_all=False)
            w_dic[docid] = {}#为每个文档创建一项
            #  ld 单词数 clean 词频
            ld, cleaned_dict = self.clean_list(seg_list)
            AVG_L = AVG_L + ld
            # 单词字典包含 number
            for key, value in cleaned_dict.items():
                w_dic[docid][key] = value
                d = Doc(docid, value, ld)
                if key in self.postings_lists:
                    self.postings_lists[key][0] = self.postings_lists[key][0] + 1  # df++
                    self.postings_lists[key][1].append(d)
                else:
                    self.postings_lists[key] = [1, [d]]  # [df, [Doc]]

        for doc_name,wordlist in w_dic.items():
            w_ddic[doc_name] = 0
            for w,n in wordlist.items():
                idf = self.postings_lists[w][0]
                tf = n
                w_ddic[doc_name]+=np.log(tf+np.e)*np.log(int(N)/idf)
            w_ddic[doc_name] = round(np.sqrt(w_ddic[doc_name]),4)
            # print(w_ddic[doc_name])

        self.w_ddic = w_ddic
        AVG_L = AVG_L / len(files)
        config.set('DEFAULT', 'N', str(len(files)))
        config.set('DEFAULT', 'avg_l', str(AVG_L))
        with open(self.config_path, 'w', encoding=self.config_encoding) as configfile:
            config.write(configfile)
        self.write_postings_to_db()

if __name__ == "__main__":
    im = IndexModule('../config.ini', 'utf-8')
    im.construct_postings_lists()