---
title: selenium基本使用类.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
---
title: selenium基本使用类.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
~~~
# coding=utf-8

import json
import random
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import logger

#必須引入這個，因爲需要输出报错信息！
import printError

log = logger.logger()


ip_port_zz = None


#获得代理ip
def getPxIp():
    r = requests.get('http://127.0.0.1:8000/')
    ip_ports = json.loads(r.text)
    randint_ = ip_ports[random.randint(0, len(ip_ports))]
    ip_port = str(randint_[0]) + ':' + str(randint_[1])
    return ip_port

#不显示浏览器窗口的自动化爬取
def zidonghua_html(url):


    ip_port = None
    global ip_port_zz
    if  ip_port_zz:
        ip_port = ip_port_zz
    else:

         ip_port = getPxIp()
    print(ip_port)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--proxy-server=http://' + ip_port)
    #chrome_options.add_argument('--proxy-server=http://111.164.177.131:8118')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    #设置异步js加载完成的超时时间1分钟
    browser.set_script_timeout(60)



    #selenium.common.exceptions.TimeoutException: Message: timeout
    try:

        browser.get(url)
        #跳到页面底部，触发加载更多
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        source = browser.page_source
        browser.quit()
        if source.find('<video')!= -1:
            ip_port_zz = ip_port
            print("找到了一个可用的ip=======================================")
        else:
            ip_port_zz = getPxIp();
            print("代理ip失效=======================================")

        return source

    except TimeoutException:
        # 报错后就强制停止加载
        # 这里是js控制
        # browser.execute_script('window.stop()')
        browser.quit()
        log.info('超时的url====>'+url)
        return "加载超时"





#不显示浏览器窗口的自动化爬取
def zidonghua_html_noproxy(url):

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    #设置异步js加载完成的超时时间1分钟
    browser.set_script_timeout(60)
    time.sleep(3)

    try:

        browser.get(url)
        #跳到页面底部，触发加载更多
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        source = browser.page_source
        browser.quit()
        return source

    except TimeoutException:
        # 报错后就强制停止加载
        # 这里是js控制
        # browser.execute_script('window.stop()')
        browser.quit()
        print('超时的url====>'+url)
        log.info('超时的url====>'+url)
        return "加载超时"













# 获取html文档
def get_html(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text


#进一步对结果集处理--如果结果中没有视频链接则干掉整条数据
# def filter(arrayList_new):
#     arrayList_too = copy.deepcopy(arrayList_new)
#     for item in arrayList_new:
#         if ('video_url' in item and 'video_title' in item and 'video_pic' in item):
#             log.info(item['video_url'])
#         else:arrayList_too.remove(item)
#
#     return arrayList_too





#测试
if __name__ == '__main__':
    # ip = getPxIp()

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Referer': 'http://jandan.net/ooxx',
        'Referer': 'http://jandan.net/ooxx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Cookie': '__cfduid=d0f8f8aef303ad3b55cd071a426e7a59c1504854664; _ga=GA1.2.986719823.1501079288; _gid=GA1.2.1585289570.1506061387',
    }

    response=requests.get('https://www.ixigua.com/a6621408542291132936/#mid=4126172301',headers=headers)
    text = response.text
    if text.find('<video')!=-1:
        print(text)
    else:
        print('没有')




~~~
