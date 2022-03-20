---
title: selenium-动作.md
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
title: selenium-动作.md
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
1、send_key  发送按键
https://www.selenium.dev/selenium/docs/api/py/index.html、

2、清除内容
// 首先定位到input，然后使用clear()
self.driver.find_element_by_xpath('xxxx').clear()

或者用注入js的方式
        browser.execute_script("$(\"input[placeholder='图形验证码']\").value = ''")
