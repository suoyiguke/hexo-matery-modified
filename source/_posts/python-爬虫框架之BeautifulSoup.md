---
title: python-爬虫框架之BeautifulSoup.md
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
title: python-爬虫框架之BeautifulSoup.md
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
html解析器 BeautifulSoup

1、安装
pip install beautifulsoup4 

pip3 install lxml

2、使用


CSS选择器 优先使用了
~~~
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.select('.panel .panel-heading'))
print(soup.select('ul li'))
print(soup.select('#list-2 .element'))
print(type(soup.select('ul')[0]))
~~~
获取内容
通过get_text()就可以获取文本内容

获取属性
或者属性的时候可以通过[属性名]或者attrs[属性名]
~~~
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
for ul in soup.select('ul'):
print(ul['id'])
~~~
不仅可以对soup 对象使用，还可以对tag对象使用：




父节点和祖先节点
通过soup.a.parent就可以获取父节点的信息
通过list(enumerate(soup.a.parents))可以获取祖先节点，这个方法返回的结果是一个列表，会分别将a标签的父节点的信息存放到列表中，以及父节点的父节点也放到列表中，并且最后还会讲整个文档放到列表中，所有列表的最后一个元素以及倒数第二个元素都是存的整个文档的信息
兄弟节点
soup.a.next_siblings 获取后面的兄弟节点
soup.a.previous_siblings 获取前面的兄弟节点
soup.a.next_sibling 获取下一个兄弟标签
souo.a.previous_sibling 获取上一个兄弟标签


子节点
children的使用	
通过下面的方式也可以获取p标签下的所有子节点内容和通过contents获取的结果是一样的，但是不同的地方是soup.p.children是一个迭代对象，而不是列表，只能通过循环的方式获取素有的信息
print(soup.p.children)
for i,child in enumerate(soup.p.children):
    print(i,child)
通过contents以及children都是获取子节点，如果想要获取子孙节点可以通过descendants
print(soup.descendants)同时这种获取的结果也是一个迭代器



Python 用Beautiful Soup解析选择的节点元素
~~~
# 子节点和子孙节点
html = """
<html>
<head>
<title>The Dormouse's story</title>
</head>
<body>
<p class="story">
    Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">
<span>Elsie</span>
</a>
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
and they lived at the bottom of a well.
</p>
<p class="story">...</p>
"""
~~~
~~~
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.p.contents)
print(soup.p.children)
for i, child in enumerate(soup.p.children, start=1):
    print(i, child)

#所有的子孙节点
print(soup.p.descendants)
for i, child in enumerate(soup.p.descendants, start=1):
    print(i, child)

print（’----------------------------------------------‘—)
# 父节点和祖先节点
html = """
<html>
<head>
<title>The Dormouse's story</title>
</head>
<body>
<p class="story">
            Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"
<span>Elsie</span>
</a>
</p>
<p class="story">...</p>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.a.parent)

# 所有的祖先节点
print("------------------------------------------------------")
html = """
<html>
<body>
<p class="story">
<a href="http://example.com/elsie" class="sister" id="link1">
<span>Elsie</span>
</a>
</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(type(soup.a.parents))
print(list(enumerate(soup.a.parents)))

# 兄弟节点
print("--------------------------------------------------------")
html = """
<html>
<body>
<p class="story">
            Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">
<span>Elsie</span>
</a>
            Hello
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
            and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            and they lived at the bottom of a well.
</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print('Next Sibling', soup.a.next_sibling)
print('Prev Sibling', soup.a.previous_sibling)
print('Next Siblings', list(enumerate(soup.a.next_siblings)))
print('Prev Siblings', list(enumerate(soup.a.previous_siblings)))

# 提取信息
print('------------------------------------------------------------')
html = """
<html>
<body>
<p class="story">
            Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Bob</a><a href="http://example.com/locie"
class="sister" id="link2">Locie</a>
</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print('Next Sibling:')
print(type(soup.a.next_sibling))
print(soup.a.next_sibling)
print(soup.a.next_sibling.string)
print('Parent')
print(type(soup.a.parents))
print(list(soup.a.parents)[0])
print(list(soup.a.parents)[0].attrs['class'])

~~~

###我的使用经验

1、只有父亲的父亲的子节点可以

  父亲的兄弟节点不可以 a.parent.previous_sinbling 这个的值是 none！




2、这样居然也可以  找到a标签里面的img






3、img的src 的拿法、
 object['video_pic'] = a.parent.parent.a.img.src
 
  而不是 img.attrs[‘src’] ，这样取不到的



4、取到h2的内容
select = s.select("h2[class='fltL']")
print(select[0].text)



5、获得指定id的元素
select = soup.find(id='__CHANNELNAME__')

6、获得表达input的value
   find_v.attrs['value']

7、获得vidi的src
for video in soup_i.select("video[class='dplayer-video']"):
    print(video.attrs['src'])


8、xxx.select()函数返回的是一个list，如果只匹配一个的话就这样：
  
soup = BeautifulSoup(gofor.zidonghua_html(url), 'lxml')
select = soup.select("video[preload='meta']")
print(select[0].attrs["src"])



9、一个元素内容如果里有多个a标签，那么这样拿的只是第一个a标签:
  a = soup.select("div[class='crumb']")[0].a




这样用select css选择器拿的就是一个list




10、一般使用连续两个parent.parent 了！





  
Gofor
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

~~~



#不显示浏览器窗口的自动化爬取
~~~
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

~~~


~~~
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




~~~
检测ip是否有效
import random
import requests

IPAgents = [
    "182.92.105.136:3128",
   ]

try:
    requests.adapters.DEFAULT_RETRIES = 3
    IP = random.choice(IPAgents)
    thisProxy = "http://" + IP
    thisIP = "".join(IP.split(":")[0:1])
    #print(thisIP)
    res = requests.get(url="http://icanhazip.com/",timeout=8,proxies={"http":thisProxy})
    proxyIP = res.text.strip().replace("\n", "")
    if(thisProxy.find(proxyIP)!=-1):
        print("代理IP:'"+ proxyIP + "'有效！")
    else:
        print("代理IP无效！")
except:
    print("代理IP无效！")
~~~
