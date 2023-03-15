#项目概述
* 就是一个游戏搜索引擎

[功能描述]：主要描述一下这个项目的主要功能列表。
1. 对3dm游戏的内容的相关信息的爬去
然后对近两年的游戏的消息，图片视频进行搜索。

[开发环境]：罗列使用本工程项目所需要安装的开发环境及配置，以及所需软件的版本说明和对应的下载链接。
1. ubuntu16.04
2. sanic
3. gensim
4. skit-learn

[项目结构简介]：简单介绍项目模块结构目录树，对用户可以修改的文件做重点说明。
```
|   |   data
│   ├── data_process
│   │   ├── csv_process.py
│   │   └── __init__.py
│   ├── docs
│   │   ├── 项目开发文档.md
│   │   └── readme.md
│   ├── __init__.py
│   ├── LDA
│   │   ├── car.csv
│   │   ├── data.py
│   │   ├── han.csv
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── simhei.ttf
│   │   └── stopwords.txt
│   ├── NLG
│   │   ├── fileall.py
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── pg1041.txt
│   │   ├── text_generator_400_0.2_400_0.2_400_0.2_100.h5
│   │   └── toge_all.txt
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   └── __init__.cpython-37.pyc
│   ├── Spider
│   │   ├── geckodriver.log
│   │   ├── index.py
│   │   ├── __init__.py
│   │   ├── linksp.py
│   │   ├── mulThread.py
│   │   ├── recommendation_module.py
│   │   ├── rename.py
│   │   ├── spider.py
│   │   ├── textindex.py
│   │   ├── textspider.py
│   │   └── tfidf.py
│   ├── src
│   │   ├── config
│   │   │   ├── config.py
│   │   │   ├── dev_config.py
│   │   │   ├── __init__.py
│   │   │   ├── pro_config.py
│   │   │   └── __pycache__
│   │   │       ├── config.cpython-36.pyc
│   │   │       ├── config.cpython-37.pyc
│   │   │       ├── dev_config.cpython-36.pyc
│   │   │       ├── dev_config.cpython-37.pyc
│   │   │       ├── __init__.cpython-36.pyc
│   │   │       └── __init__.cpython-37.pyc
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-36.pyc
│   │   │   ├── __init__.cpython-37.pyc
│   │   │   ├── run.cpython-36.pyc
│   │   │   └── run.cpython-37.pyc
│   │   ├── run.py
│   │   ├── statics
│   │   │   ├── rss_html
│   │   │   │   ├── css
│   │   │   │   │   └── main.css
│   │   │   │   └── image
│   │   │   │       ├── a.webp
│   │   │   │       ├── icon-search.svg
│   │   │   │       ├── logo.png
│   │   │   │       └── Q.png
│   │   │   └── rss_json
│   │   │       ├── css
│   │   │       │   └── main.css
│   │   │       └── js
│   │   │           └── main.js
│   │   ├── templates
│   │   │   ├── content.html
│   │   │   ├── image.html
│   │   │   ├── rss.html
│   │   │   ├── rss_html
│   │   │   │   └── index.html
│   │   │   ├── rss_json
│   │   │   │   ├── index.html
│   │   │   │   └── test.html
│   │   │   ├── search.html
│   │   │   ├── text.html
│   │   │   └── video.html
│   │   └── views
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-36.pyc
│   │       │   ├── __init__.cpython-37.pyc
│   │       │   ├── rss_html.cpython-36.pyc
│   │       │   ├── rss_html.cpython-37.pyc
│   │       │   ├── rss_json.cpython-36.pyc
│   │       │   └── rss_json.cpython-37.pyc
│   │       ├── rss_html.py
│   │       └── rss_json.py
│   └── word_cor
│       ├── correct.py
│       ├── __init__.py
│       └── __pycache__
│           ├── correct.cpython-37.pyc
│           └── __init__.cpython-37.pyc
├── requirements.txt
├── test
│   ├── heros.csv
│   ├── mul.py
│   ├── Q.png
│   └── test.py
├── text_generators-master
│   ├── a_deeper_model.ipynb
│   ├── a_gigantic_model.ipynb
│   ├── a_more_trained_model.ipynb
│   ├── a_wider_model.ipynb
│   ├── baseline_model.ipynb
│   ├── models
│   │   ├── text_generator_400_0.2_400_0.2_100.h5
│   │   ├── text_generator_400_0.2_400_0.2_400_0.2_100.h5
│   │   ├── text_generator_400_0.2_400_0.2_baseline.h5
│   │   └── text_generator_700_0.2_700_0.2_100.h5
│   ├── README.md
│   └── sonnets.txt
```
[测试DEMO]：此处可以简单介绍一下DEMO程序的思路，具体实现代码放在example文件夹中。
查询界面搜索

引擎界面
[运行结果]：
****
<img src="./1.png" width="400" height="400">
<img src="./2.png" width="400" height="400">
<img src="./3.png" width="400" height="400">



[作者列表]：对于多人合作的项目，可以在这里简单介绍并感谢所有参与开发的研发人员。

only myself wfs2010

[更新链接]：提供后续更新的代码链接。

以后再说

[历史版本]：对历史版本更改 记录做个简单的罗列，让用户直观的了解到哪些版本解决了哪些问题。

game_engine v1.0 

[联系方式]：可以提供微信、邮箱等联系方式，其他人对这个工程不明白的地方可以通过该联系方式与你联系。

blog:blog.laoding.online

qq:1337581543@qq.com
