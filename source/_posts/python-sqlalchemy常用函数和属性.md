---
title: python-sqlalchemy常用函数和属性.md
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
title: python-sqlalchemy常用函数和属性.md
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
sqlalchemy的中文文档
https://www.osgeo.cn/sqlalchemy/core/connections.html#multiple-result-sets

**使用事务**
~~~
connection = engine.connect()
trans = connection.begin()
try:
    r1 = connection.execute(table1.select())
    connection.execute(table1.insert(), col1=7, col2='this is some data')
    trans.commit()
except:
    trans.rollback()
    raise
~~~

**结果集解析**
1、first()
获取第一行，然后无条件关闭结果集。如果不存在行，则返回“无”。调用此方法后，对象将完全关闭;
结果集是`(1,)` 元组的形式
~~~
cur = _instance.execute("SELECT max(category_id) FROM category")
rowProxy = cur.first()
value = rowProxy.values();
#存在则返回对应名字的id
return value[0]
~~~


2、fetchall()
获取所有行，就像db-api一样 cursor.fetchall() .  在所有行用完之后，将释放底层DBAPI光标资源，并且可以安全地丢弃该对象。  后续调用 ResultProxy.fetchall() 将返回空列表。结果集是
[(1,),(2,)]　的形式==>列表里面套元组

~~~
# 执行SQL
cur = _instance.execute(
    "SELECT  "+id_name+" FROM "+tabel_name
)
list = cur.fetchall()
cur.close();

for item in  list:
    print(item.values()[0])
~~~

3、rowcount

返回结果的“行数”。“rowcount”报告行数 匹配的 按UPDATE或DELETE语句的WHERE条件。
