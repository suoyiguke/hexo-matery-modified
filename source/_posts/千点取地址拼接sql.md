---
title: 千点取地址拼接sql.md
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
title: 千点取地址拼接sql.md
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
import openpyxl

insertString = "INSERT INTO `tp_site_info` ( `code`, `name`, `type_code`, `type_name`, `region`, `region_code`, `areas1`, `areas2`, `address`, `dispatch_address`, `delete_flag`, `create_date`, `modify_date` ) VALUES ";
sql="(\'{code}\',\'{name}\','1',\'{type_name}\',\'香港\','HK',\'{areas1}\',\'{areas2}\',\'{address}\',\'{dispatch_address}\','0',now( ),NULL)"
# 打开excel文件,获取工作簿对象
wb = openpyxl.load_workbook("D:\\Users\\Use'r\\Desktop\\_AddressList20210803.xlsx")

# 从工作薄中获取一个表单(sheet)对象
sheet = wb['網點代碼']
# 转为元祖
data_tuple = tuple(sheet.iter_rows())
i = 0
print(len(data_tuple))
for row in data_tuple:
    if i == 0:
        i = i + 1
        continue
    str = sql.format(
        code=row[5].value,
        name=row[6].value,
        type_name=row[4].value,
        areas1=row[2].value,
        areas2=row[3].value,
        address=row[7].value,
        dispatch_address=row[5].value + row[6].value + row[7].value + row[4].value
    )
    if i != len(data_tuple)-1:
        insertString = insertString + str + ","
    else:
        insertString = insertString + str
    i = i + 1


print(insertString)


~~~
