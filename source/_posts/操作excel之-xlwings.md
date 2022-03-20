---
title: 操作excel之-xlwings.md
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
title: 操作excel之-xlwings.md
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
import xlwings as xw
import time

# 记录打开表单开始时间
start_open_time = time.time()

# 指定不显示地打开Excel，读取Excel文件
app = xw.App(visible=False, add_book=False)
wb = app.books.open('C:\\Users\\yinkai\\Desktop\\test\\目标文件\\2021-11-15 --沙漠白金  贺方庆.xlsx')  # 打开Excel文件
sheet = wb.sheets[0]  # 选择第0个表单



row_content = []
list_value = sheet.range('A1').value
print(list_value)



# 保存并关闭Excel文件
wb.save()
wb.close()
app.kill()
~~~
