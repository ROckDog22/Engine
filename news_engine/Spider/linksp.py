# -*- coding: utf-8 -*-
"""
@Author    : wfs2010
@Email     : 1337581543@qq.com
@License   : Copyright(C), KEDACOM
@Time      : 2019/11/5 下午3:50
@File      : linksp.py
@Version   : 1.0
@Desciption:  
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


if __name__=='__main__':
    driver = webdriver.Firefox()
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()