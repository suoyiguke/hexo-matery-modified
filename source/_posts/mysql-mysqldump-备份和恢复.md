---
title: mysql-mysqldump-备份和恢复.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: mysql-mysqldump-备份和恢复.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
###mysql备份库手段
1、全库备份
~~~
mysqldump -uroot -pyk123 --all-databases > /保存路径/文件名.sql
~~~

2、单独库
~~~
mysqldump -uroot -pyk123 --databases cms > cms.sql
~~~

3、多个库，空格分割
~~~
/usr/local/mysql/bin/mysqldump -u用户名 -p密码 --databases 数据库1 数据库2... > 保存路径/文件名.sql
~~~
4、备份压缩
~~~
mysqldump -h192.168.1.100 -p 3306 -uroot -ppassword --database cmdb | gzip > /data/backup/cmdb.sql.gz
~~~

5、还原sql文件备份
###使用source 命令恢复数据库
~~~
source cms.sql
~~~

###备份表
语法： mysqldump -u 用户名 -p 数据库名 表名1 表名2 >备份的文件名
~~~
mysqldump -u root -pyk123 test tb1 tb2 >table.sql
~~~


###定时备份
我的另一篇文章
https://www.jianshu.com/p/290fe76552d4
