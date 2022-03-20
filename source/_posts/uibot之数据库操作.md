---
title: uibot之数据库操作.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: uibot
categories: uibot
---
---
title: uibot之数据库操作.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: uibot
categories: uibot
---
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f57058ff38e4a270.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1、简单查询test表， 选择 `执行全sql查询`
~~~
dim sText = ""
dim iRet = ""
dim objDatabase = ""
dim sRet = ""
dim objPoint = ""
objDatabase = Database.CreateDB("MySQL",{"charset":"utf8","database":"test","host":"localhost","password":"Sgl20@14","port":"3306","user":"root"})
iRet = Database.QueryAll(objDatabase ,"select * from test" ,{"rdict":false,"args":[]})
iRet1 = Dialog.MsgBox(iRet,"UiBot","0","1",0)


~~~

2、插入数据，选择  `执行sql语句` 。注意mysql使用%s占位符
~~~
dim sText = ""
dim iRet = ""
dim objDatabase = ""
dim sRet = ""
dim objPoint = ""
dim iRet1 = ""
objDatabase = Database.CreateDB("MySQL",{"charset":"utf8","database":"test","host":"localhost","password":"Sgl20@14","port":"3306","user":"root"})
iRet = Database.ExecuteSQL(objDatabase ,"INSERT INTO `test`.`test`(`name`) VALUES ( %s);", {"args":["凯凯"]})
iRet = Database.QueryAll(objDatabase ,"select * from test" ,{"rdict":false,"args":[]})
iRet1 = Dialog.MsgBox(iRet,"UiBot","0","1",0)
Database.CloseDB(objDatabase)
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-81ff06e639355277.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、update操作，选择  `执行sql语句` 。注意mysql使用%s占位符
~~~
dim sText = ""
dim iRet = ""
dim objDatabase = ""
dim sRet = ""
dim objPoint = ""
dim iRet1 = ""
objDatabase = Database.CreateDB("MySQL",{"charset":"utf8","database":"test","host":"localhost","password":"Sgl20@14","port":"3306","user":"root"})
iRet = Database.ExecuteSQL(objDatabase ,"UPDATE `test`.`test` SET `name` = %s WHERE `id` = %s;", {"args":["zzz",4]})
iRet = Database.QueryAll(objDatabase ,"select * from test" ,{"rdict":false,"args":[]})
iRet1 = Dialog.MsgBox(iRet,"UiBot","0","1",0)
Database.CloseDB(objDatabase)
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-938338fec4327ab2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、delete操作，选择  `执行sql语句` 。注意mysql使用%s占位符
~~~
dim sText = ""
dim iRet = ""
dim objDatabase = ""
dim sRet = ""
dim objPoint = ""
dim iRet1 = ""
objDatabase = Database.CreateDB("MySQL",{"charset":"utf8","database":"test","host":"localhost","password":"Sgl20@14","port":"3306","user":"root"})
iRet = Database.QueryAll(objDatabase ,"select * from test where id = %s" ,{"rdict":false,"args":[4]})
iRet1 = Dialog.MsgBox(iRet,"UiBot","0","1",0)
iRet = Database.ExecuteSQL(objDatabase ,"DELETE FROM test WHERE id = %s", {"args":[4]})
iRet = Database.QueryAll(objDatabase ,"select * from test where id = %s" ,{"rdict":false,"args":[4]})
iRet1 = Dialog.MsgBox(iRet,"UiBot","0","1",0)
Database.CloseDB(objDatabase)
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-056e11410a530012.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
