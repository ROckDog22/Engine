# !/usr/bin/env python
import sys
from sanic import Sanic
from sanic.log import logger
from game_engine.src.views import json_bp, html_bp
from game_engine.src.config import CONFIG
from sanic.exceptions import NotFound
from sanic.response import redirect, text
from sanic import response
from sanicdb import SanicDB
from os import listdir
import configparser
import xmltodict
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic.response import html
from game_engine.word_cor import correct
import jieba
import numpy as np

from bs4 import BeautifulSoup
import requests
Heads = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
}

sys.path.append('../')
app = Sanic(__name__)
app.blueprint(json_bp)
app.blueprint(html_bp)
app.static('/statics/rss_html', CONFIG.BASE_DIR + '/statics/rss_html')
db = SanicDB('localhost', 'engine', 'root', '525926', sanic=app)

config = configparser.ConfigParser()
config.read('../config.ini', 'utf-8')

# @app.route('/html/<string_arg:string>')
# async def string_handler(request, string_arg):
#     sql = "select * from postings where term='%s'" % string_arg
#     data = await app.db.query(sql)
#
#     return response.text(data[0]['docs'])
# 对基础环境(jinja2模版)进行一个配置
# 开启异步特性  要求3.6+


enable_async = sys.version_info >= (3, 6)
# jinjia2 config
env = Environment(
    loader=PackageLoader('run', './templates'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=enable_async)

async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    rendered_template = await template.render_async(**kwargs)
    return html(rendered_template)

@app.route('/html/search')
async def string_handler(request):
    N = 19469
    wd = request.args.get('wd')
    page = request.args.get('page')
    if page is None:
        page = 1
    page=int(page)
    search = jieba.lcut_for_search(wd)
    search = list(set(search))
    c_wd = correct.txt_correction(wd)
    data_all = None
    tf = {}
    # one problem

    for zzz in search:
        sql = "select count(*) c from postings where term='%s'" % zzz
        count = await app.db.query(sql)
        if count[0]['c'] == 0:
            search.remove(zzz)

    #我要计算每个单词求和
    for eve in search:
        sql = "select * from postings where term='%s'" % eve
        data_all = await app.db.query(sql)
        data = data_all[0]['docs'].split('\n')
        idf = data_all[0]['id']
        score = np.log(N / idf)
        for i in data:
            i = i.split('\t')
            # logger.info(len[0]['length'])
            if i[0] in tf:
                tf[i[0]] += score * score * np.log(int(i[2]) + int(np.e))   # tf
            else:
                tf[i[0]] = score * score * np.log(int(i[2]) + int(np.e))   # tf

    for name,vo in tf.items():
        sql1 = "select length from doc_len where id='%s'" % name
        length = await app.db.query(sql1)
        tf[name] = vo / length[0]['length']

    if not data_all:
        data = {}
        data['key'] = wd
        data['page'] = page
        data['new_cw'] = c_wd
        data['doc'] = None
        return await template('search.html', data=data)

    # 对字典里的数据将序排列
    new_tf = sorted(tf.items(), key=lambda x: x[1], reverse=True)  # 按字典集合中，每一个元组的第二个元素排列。
    # x相当于字典集合中遍历出来的一个元组。
    data = {}
    data['key'] = wd
    data['new_cw'] = None
    if c_wd != wd:
        data['new_cw'] = c_wd
    data['doc'] = []
    data['page'] = page
    new_tf = new_tf[(page-1)*10:page*10]
    for doooo in new_tf:
        id = doooo[0]
        with open(config['DEFAULT']['doc_dir_path'] + id+".xml")as f:
            root = f.read()
        xml_parse = xmltodict.parse(root)
        if len(xml_parse['doc']['text'])>300:
            xml_parse['doc']['text'] = xml_parse['doc']['text'][0:300]+"......"
        data['doc'].append(xml_parse)
    return await template('search.html', data=data)

@app.route('/html/textsearch')
async def string_handler(request):
    N = 4056
    wd = request.args.get('wd')
    page = request.args.get('page')
    if page is None:
        page = 1
    page=int(page)
    search = jieba.lcut_for_search(wd)
    search = list(set(search))
    c_wd = correct.txt_correction(wd)
    data_all = None
    tf = {}
    # one problem

    for zzz in search:
        sql = "select count(*) c from postings_text where term='%s'" % zzz
        count = await app.db.query(sql)
        if count[0]['c'] == 0:
            search.remove(zzz)

    #我要计算每个单词求和
    for eve in search:
        sql = "select * from postings_text where term='%s'" % eve
        data_all = await app.db.query(sql)
        data = data_all[0]['docs'].split('\n')
        idf = data_all[0]['id']
        score = np.log(N / idf)
        for i in data:
            i = i.split('\t')
            # logger.info(len[0]['length'])
            if i[0] in tf:
                tf[i[0]] += score * score * np.log(int(i[2]) + int(np.e))   # tf
            else:
                tf[i[0]] = score * score * np.log(int(i[2]) + int(np.e))   # tf

    for name,vo in tf.items():
        sql1 = "select length from text_len where id='%s'" % name
        length = await app.db.query(sql1)
        tf[name] = vo / length[0]['length']

    if not data_all:
        data = {}
        data['key'] = wd
        data['page'] = page
        data['new_cw'] = c_wd
        data['doc'] = None
        return await template('search.html', data=data)

    # 对字典里的数据将序排列
    new_tf = sorted(tf.items(), key=lambda x: x[1], reverse=True)  # 按字典集合中，每一个元组的第二个元素排列。
    # x相当于字典集合中遍历出来的一个元组。
    data = {}
    data['key'] = wd
    data['new_cw'] = None
    if c_wd != wd:
        data['new_cw'] = c_wd
    data['doc'] = []
    data['page'] = page
    new_tf = new_tf[(page-1)*10:page*10]
    for doooo in new_tf:
        id = doooo[0]
        with open(config['DEFAULT']['text_dir_path'] + id+".xml")as f:
            root = f.read()
        xml_parse = xmltodict.parse(root)
        if len(xml_parse['doc']['text'])>300:
            xml_parse['doc']['text'] = xml_parse['doc']['text'][0:300]+"......"
        data['doc'].append(xml_parse)
    return await template('text.html', data=data)

@app.route('/html/imagesearch')
async def string_handler(request):
    wd = request.args.get("wd")
    # logger.info(wd)
    data={}
    data['key'] = wd
    N = 19469
    wd = request.args.get('wd')
    search = jieba.lcut_for_search(wd)
    search = list(set(search))
    c_wd = correct.txt_correction(wd)
    data_all = None
    tf = {}
    # one problem
    for zzz in search:
        sql = "select count(*) c from postings where term='%s'" % zzz
        count = await app.db.query(sql)
        if count[0]['c'] == 0:
            search.remove(zzz)
    # 我要计算每个单词求和
    for eve in search:
        sql = "select * from postings where term='%s'" % eve
        data_all = await app.db.query(sql)
        data = data_all[0]['docs'].split('\n')
        idf = data_all[0]['id']
        score = np.log(N / idf)
        for i in data:
            i = i.split('\t')
            # logger.info(len[0]['length'])
            if i[0] in tf:
                tf[i[0]] += score * score * np.log(int(i[2]) + int(np.e))  # tf
            else:
                tf[i[0]] = score * score * np.log(int(i[2]) + int(np.e))  # tf

    for name, vo in tf.items():
        sql1 = "select length from doc_len where id='%s'" % name
        length = await app.db.query(sql1)
        tf[name] = vo / length[0]['length']

    if not data_all:
        data = {}
        data['key'] = wd
        data['new_cw'] = c_wd
        return await template('image.html',data=data)

    # 对字典里的数据将序排列
    new_tf = sorted(tf.items(), key=lambda x: x[1], reverse=True)  # 按字典集合中，每一个元组的第二个元素排列。
    # x相当于字典集合中遍历出来的一个元组。
    data = {}
    data['key'] = wd
    data['new_cw'] = None
    data['url_all'] =[]
    if c_wd != wd:
        data['new_cw'] = c_wd
    data['doc'] = []
    data['url']= []
    for doooo in new_tf:
        id = doooo[0]
        with open(config['DEFAULT']['doc_dir_path'] + id + ".xml")as f:
            root = f.read()
        xml_parse = xmltodict.parse(root)
        data['url'].append(xml_parse['doc']['imageurl'])

    for mmmm in data['url']:
        if mmmm is None:
            continue
        src = mmmm.split('\t')
        for url in src:
            data['url_all'] .append(url)
    return await template('image.html',data=data)


@app.route('/html/videosearch')
async def string_handler(request):
    wd = request.args.get("wd")
    data={}
    data['key'] = wd
    N = 19469
    wd = request.args.get('wd')
    search = jieba.lcut_for_search(wd)
    search = list(set(search))
    c_wd = correct.txt_correction(wd)
    data_all = None
    tf = {}
    for zzz in search:
        sql = "select count(*) c from postings where term='%s'" % zzz
        count = await app.db.query(sql)
        if count[0]['c'] == 0:
            search.remove(zzz)
    for eve in search:
        sql = "select * from postings where term='%s'" % eve
        data_all = await app.db.query(sql)
        data = data_all[0]['docs'].split('\n')
        idf = data_all[0]['id']
        score = np.log(N / idf)
        for i in data:
            i = i.split('\t')
            if i[0] in tf:
                tf[i[0]] += score * score * np.log(int(i[2]) + int(np.e))  # tf
            else:
                tf[i[0]] = score * score * np.log(int(i[2]) + int(np.e))  # tf


    for name, vo in tf.items():
        sql1 = "select length from doc_len where id='%s'" % name
        length = await app.db.query(sql1)
        tf[name] = vo / length[0]['length']

    if not data_all:
        data = {}
        data['key'] = wd
        data['new_cw'] = c_wd
        return await template('image.html',data=data)

    new_tf = sorted(tf.items(), key=lambda x: x[1], reverse=True)  # 按字典集合中，每一个元组的第二个元素排列。
    data = {}
    data['key'] = wd
    data['new_cw'] = None
    data['url_all'] ={}
    if c_wd != wd:
        data['new_cw'] = c_wd
    data['doc'] = []
    data['url']= {}
    for doooo in new_tf:
        id = doooo[0]
        with open(config['DEFAULT']['doc_dir_path'] + id + ".xml")as f:
            root = f.read()
        xml_parse = xmltodict.parse(root)
        if xml_parse['doc']['videourl'] is None:
            continue
        data['url'][xml_parse['doc']['title']]=xml_parse['doc']['videourl']
    for title,mmmm in data['url'].items():
        url = mmmm.split('\t')
        for yyy in url:
            if 'store' in yyy or 'sonkwo' in yyy:
                continue
            data['url_all'][title] = yyy
    # data['url_all'] = dict(list(data['url_all'].items())[:3])
    return await template('video.html', data=data)

@app.exception(NotFound)
def ignore_404s(request, exception):
    return redirect('/html')


if __name__ == "__main__":
    # app.config['JSON_AS_ASCII']=False
    app.run(host="0.0.0.0", port=8000)
