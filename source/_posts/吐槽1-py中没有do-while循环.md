---
title: 吐槽1-py中没有do-while循环.md
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
title: 吐槽1-py中没有do-while循环.md
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
如下代码想要实现先执行一次后循环。只能这样做

    x = input()
    while not is_number(x):
        print("请输入抓取页大小，输入数字后回车")
        x = input()
    else:
        pageSize = int(x)


没有do while却有while else
