# -*- coding: utf-8 -*-
"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 2019/11/18 上午8:35
@File      : main.py
@Version   : 1.0
@Desciption:  
"""
import jieba
import pandas as pd
from gensim import corpora
import gensim
import gensim
import jieba
import pandas as pd
from gensim import corpora
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

myfont = fm.FontProperties(fname=r'./simhei.ttf')
#设置文件路径
def fun():
    dir = "./"
    file_desc = "".join([dir,'han.csv'])
    stop_words = "".join([dir,'stopwords.txt'])
    #定义停用词
    stopwords=pd.read_csv(stop_words,index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')
    stopwords=stopwords['stopword'].values
    #加载语料
    df = pd.read_csv(file_desc, encoding='utf-8')
    #删除nan行
    df.dropna(inplace=True)
    #转化为list
    lines=df.content.values.tolist()
    #开始分词
    sentences=[]
    for line in lines:
        try:
            segs=jieba.lcut(line)
            segs = [v for v in segs if not str(v).isdigit()]#去数字
            segs = list(filter(lambda x:x.strip(), segs))   #去左右空格
            segs = list(filter(lambda x:x not in stopwords, segs)) #去掉停用词
            sentences.append(segs)
        except Exception:
            print(line)
            continue
    #构建词袋模型
    dictionary = corpora.Dictionary(sentences)
    corpus = [dictionary.doc2bow(sentence) for sentence in sentences]
    #lda模型，num_topics是主题的个数，这里定义了5个
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)
    #我们查一下第1号分类，其中最常出现的5个词是：
    print(lda.print_topic(1, topn=5))
    print(lda.get_document_topics(corpus[0]))
    #我们打印所有5个主题，每个主题显示8个词
    for topic in lda.print_topics(num_topics=10, num_words=8):
        print(topic[1])
    # plt.rcParams['font.sans-serif'] = [u'SimHei']
    # plt.rcParams['axes.unicode_minus'] = False

    # 在可视化部分，我们首先画出了九个主题的7个词的概率分布图
    num_show_term = 8  # 每个主题下显示几个词
    num_topics = 10
    for i, k in enumerate(range(num_topics)):
        ax = plt.subplot(2, 5, i + 1)
        item_dis_all = lda.get_topic_terms(topicid=k)
        item_dis = np.array(item_dis_all[:num_show_term])
        ax.plot(range(num_show_term), item_dis[:, 1], 'b*')
        item_word_id = item_dis[:, 0].astype(np.int)
        word = [dictionary.id2token[i] for i in item_word_id]
        ax.set_ylabel(u"概率",fontproperties=myfont)
        for j in range(num_show_term):
            ax.text(j, item_dis[j, 1], word[j], bbox=dict(facecolor='green', alpha=0.1),fontproperties=myfont)
    plt.suptitle(u'10个主题及其8个主要词的概率', fontsize=18,fontproperties=myfont)
    plt.show()

if __name__ == '__main__':
    fun()