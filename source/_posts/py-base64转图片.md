---
title: py-base64转图片.md
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
title: py-base64转图片.md
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
import base64

import openpyxl

# 打开excel文件,获取工作簿对象
wb = openpyxl.load_workbook("C:\\Users\\Administrator\\Desktop\\工作文档\\zz.xlsx")

# 从工作薄中获取一个表单(sheet)对象
sheet = wb['test']
# 转为元祖
data_tuple = tuple(sheet.iter_rows())
for row in data_tuple:

    try:
        fileName = "C:\\Users\\Administrator\\Desktop\\工作文档\\新建文件夹\\" + row[0].value + "_" + row[1].value + ".jpg"
        imgdata = base64.b64decode(row[2].value)
        file = open(fileName, 'wb')
        file.write(imgdata)
        file.close()
    except BaseException as err:
        print(err)

~~~
