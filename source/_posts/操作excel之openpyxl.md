---
title: 操作excel之openpyxl.md
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
title: 操作excel之openpyxl.md
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
利用openpyxl库遍历Sheet的方法
~~~
import base64

import openpyxl
import xlrd as xlrd

# 打开excel文件,获取工作簿对象
wb = openpyxl.load_workbook("C:\\Users\\Administrator\\Desktop\\工作文档\\zz.xlsx")

# 从工作薄中获取一个表单(sheet)对象
sheet = wb['test']
# 转为元祖
data_tuple = tuple(sheet.iter_rows())
for row in data_tuple:
    
    print(row[0].value+"_"+row[1].value+".jpg",row[2].value)

~~~


2、
安装pillow 模块可以解决load后save导致图片丢失的问题


3、问题  zipfile.BadZipFile: File is not a zip file  

# 写入 A、B、C、D 四个字段 数据
file_update.py---->  wb = load_workbook(path, data_only=True)

file_output.py---> wb = load_workbook(path, data_only=True)

 # 构造excel端数据字典
 code_update.py -->     wb = load_workbook(path + name, data_only=True)



在写代码的时候一定要未雨绸缪，用安全的方式打开和退出excel文件，就可以从根源上避免上面的这一类关于load/save的错误。
安全地打开excel
打开文件时，用以下方式打开excel：如果已经存在原文件，就直接load；如果不存在，就新建workbook准备最后save.
~~~
import os
from openpyxl import Workbook
from openpyxl import load_workbook
if os.path.exists(new_filename):
    new_wb = load_workbook(new_filename)
else:
    new_wb = Workbook()
~~~
安全地保存为excel

首先，文件一旦用完就要记得退出。
其次，退出文件时，对所有的workbook，如果需要save就save，如果不需要save（只读）就一定要close
~~~
wb.save(filename) # 对需要保存写入内容的workbook
wb.close() # 对程序中只读的workbook
~~~
