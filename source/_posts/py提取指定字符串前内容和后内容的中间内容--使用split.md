---
title: py提取指定字符串前内容和后内容的中间内容--使用split.md
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
title: py提取指定字符串前内容和后内容的中间内容--使用split.md
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
1、   
 split = html.split(',mark_content:\"')
    split_ = split[1]
    split__split = split_.split('\",display_count')
    split__split_ = split__split[0]
    print(split__split_)

2、正则表达式

~~~
import re
str = "积分：7931111111111111112226、现金：1231231.00"

# [('7931111111111111112226', '1231231.00')]
print(re.findall("积分：(.+)、现金：(.+)", str))
~~~
