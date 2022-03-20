---
title: python-修改excel的某一列为一个字段.md
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
title: python-修改excel的某一列为一个字段.md
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
import os
from openpyxl.reader.excel import load_workbook

rootdir = u'D:\\搜狗高速下载\\data\\excel\\'
for parent, dirnames, filenames in os.walk(rootdir):
    for fn in filenames:
        filedir = os.path.join(parent, fn)
        print(filedir)

        wb = load_workbook(filename=filedir)  # 打开excel文件
        sheet_ranges = wb['模板文件']

        max_row = sheet_ranges.max_row
        max_cow = sheet_ranges.max_column
        print('最大的行值：', max_row)  # 输出6
        print('最大的列值：', max_cow)  # 输出7

        a = list(range(2, max_row))
        for i in a:
            if (sheet_ranges.cell(i, 10).value is not None):
                sheet_ranges.cell(i, 10).value = "身份证"
            else:
                break
        wb.save(filedir)  # 保存修改后的excel

~~~
