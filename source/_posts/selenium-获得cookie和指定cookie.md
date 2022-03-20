---
title: selenium-获得cookie和指定cookie.md
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
title: selenium-获得cookie和指定cookie.md
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
1、获得cookie
driver.get_cookies()

2、指定cookie
需要先访问后设置cookie。不然会出问题
    driver.delete_all_cookies()
    url = "https://pro.similarweb.com/#/website/worldwide-overview/snailtoday.com/*/999/3m?webSource=Total" if url is None else url
    driver.get(url)


    for cookie in cookies:
        driver.add_cookie(cookie)


~~~
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import pickle

def save_cookies(driver,location):
    pickle.dump(driver.get_cookies(),open(location,"wb"))


print("启动浏览器，打开SimiliarWeb登录界面")
#用webdriver启动谷歌浏览器
driver = webdriver.Chrome(executable_path = "C:\\Users\xxx\AppData\Local\Google\Chrome\Application\chromedriver.exe")
#打开目标页面
driver.get('https://pro.similarweb.com/#/website/worldwide-overview/snailtoday.com/*/999/3m?webSource=Total')
author = 你的用户名
passowrd = 你的密码

#自动填入登录用户名
driver.find_element_by_xpath("./*//input[@name='UserName']").send_keys(author)
#自动填入登录密码
driver.find_element_by_xpath("./*//input[@name='Password']").send_keys(passowrd)
#自动点击登录按钮进行登录
driver.find_element_by_xpath("./*//button[@class='form__submit']").click()
print("登陆成功")
# 休息150秒
time.sleep(150)
# 保存cookie
save_cookies(driver,"H:\py_project\similiarweb\cookies.txt")
~~~

~~~
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import pickle
from bs4 import BeautifulSoup

def load_cookies(driver,location,url=None):
    cookies = pickle.load(open(location,"rb"))
    driver.delete_all_cookies()
    url = "https://pro.similarweb.com/#/website/worldwide-overview/snailtoday.com/*/999/3m?webSource=Total" if url is None else url
    driver.get(url)
    for cookie in cookies:
        driver.add_cookie(cookie)

print("启动浏览器，打开SimiliarWeb登录界面")
#用webdriver启动谷歌浏览器
driver = webdriver.Chrome(executable_path = "C:\\Users\xxx\AppData\Local\Google\Chrome\Application\chromedriver.exe")
load_cookies(driver,"H:\py_project\similiarweb\cookies.txt")
#打开目标 页面
driver.get('https://pro.similarweb.com/#/website/worldwide-overview/snailtoday.com/*/999/3m?webSource=Total')
time.sleep(30)

html=driver.page_source
soup=BeautifulSoup(html,'lxml')
visitors = soup.find_all('div', class_='big-text u-blueMediumMedium')[0].text
print(visitors)

#打开新的标签页
js = 'window.open("https://pro.similarweb.com/#/website/worldwide-overview/baidu.com/*/999/3m?webSource=Total");'
driver.execute_script(js)
time.sleep(30)
handles = driver.window_handles
driver.switch_to_window(handles[2])
html=driver.page_source
soup=BeautifulSoup(html,'lxml')
visitors = soup.find_all('div', class_='big-text u-blueMediumMedium')[0].text
print(visitors)

print("发布文章成功")
~~~
