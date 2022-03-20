---
title: selenium指定路径.md
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
title: selenium指定路径.md
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
3点版本
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.binary_location = "C:\\chrome_x32\\Chrome-bin\\chrome.exe"
driver = webdriver.Chrome(chrome_options=options,executable_path="C:/chrome_x32/chromedriver_win32/chromedriver")
driver.get('http://www.baidu.com')


新版 4.1.2
import pandas as pd
import requests
import yaml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

        options = Options()
        options.binary_location = browserSrc
        s = Service(driverSrc)
        browser = webdriver.Chrome(service=s,options=options)
        # 隐式等待10秒。响应式等待优先级比它高。这里作为兜底。如果不加可能就出现因为找不到元素报错退出
