---
title: BeautifulSoup-选择器.md
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
title: BeautifulSoup-选择器.md
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
soup = BeautifulSoup(browser.page_source, 'lxml')
input_str = soup.select('[placeholder="图形验证码"]')
拿到的是数组


2、contents 数组 拿取不在标签内的内容
~~~
  file = open('C:\\Users\\yinkai\\Desktop\\zzz.txt', encoding='UTF-8')  # 打开文件
    soup = BeautifulSoup(file.read(), 'lxml')
    divList = soup.select("div[class='ant-col ant-col-12']")
    a = divList[0].contents[1] # 客户名称
    b = divList[1].contents[1] # 客户手机号
    c = divList[2].contents[1] # 地址
    print(c)
~~~


3、这种span,div并列的css选择不支持
span = soup.select_one("tbody[class='ant-table-tbody']").find_all("span,div")


4、找儿子
find_all找数组PY
find 找第一个
ly = soup.select_one("div[class='basic-info']").find_all("div")
