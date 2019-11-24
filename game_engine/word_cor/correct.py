# -*- coding: utf-8 -*-
"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 2019/10/24 下午9:48
@File      : correct.py
@Version   : 1.0
@Desciption:  
"""
import urllib.request ,sys
import ssl
import json
client_id ='8xS9undSFRQSnq5lFStwdvVI'
client_secret ='DIGnl9D4oTBAoYOMhEfp9GRT5IifTHVX'

#获取token
def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key


def txt_correction(content):
    # print('原文：', content)
    token = get_token()
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/ecnet'
    params = dict()
    params['text'] = content
    params = json.dumps(params).encode('utf-8')
    access_token = token
    url = url + "?access_token=" + access_token
    request = urllib.request.Request(url=url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        content = content.decode('GB2312')
        data = json.loads(content)

        item = data['item']
        # print('纠错后：', item['correct_query'])
        # print('Score：', item['score'])
        return item['correct_query']
# client_id 为官网获取的AK， client_secret 为官网获取的SK
# if __name__=="__main__":
#     txt_correction('汽车形式在这条道路上')