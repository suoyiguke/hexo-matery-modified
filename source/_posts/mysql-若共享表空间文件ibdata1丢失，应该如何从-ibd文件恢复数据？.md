---
title: mysql-若共享表空间文件ibdata1丢失，应该如何从-ibd文件恢复数据？.md
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
title: mysql-若共享表空间文件ibdata1丢失，应该如何从-ibd文件恢复数据？.md
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
mysql把共享表空间文件删除后重建，导致数据表直接没了。navicat中查不到，其实frm和ibd文件都是存在的，只是此时无法识别数据表而已。我们可以利用它们来恢复数据。

>思路就是创建一张表结构和目标表相同的数据表，然后指定该表的表空间为需要恢复的目标表的表空间即可。

###材料准备
1、需要恢复目标表的建表语句，或者frm文件也可。可以通过frm文件创建表结构相同的表（通过mysql-utilities得到frm文件中得到建表语句）

###从frm中恢复表结构


###从.ibd文件恢复数据
1、创建一张表，表结构与原表结构一致：
~~~
CREATE TABLE <table_name> ...;
~~~
2、删除新建的表空间: 
~~~
ALTER TABLE <table_name> DISCARD TABLESPACE;
~~~
3、将待恢复的<table_name>.ibd文件copy到目标数据库文件夹下，并修改文件权限:
~~~
cp <table_name>.ibd /var/lib/mysql/<database_name>
cd /var/lib/mysql/<database_name>
chown mysql:mysql <table_name>.ibd
~~~
4、重新导入表空间:
~~~
ALTER TABLE <table_name> IMPORT TABLESPACE;
~~~


###也可能出现如下问题：

1、mysql 1808错误：

Error Code: 1808. Schema mismatch (Table has ROW_TYPE_DYNAMIC row format, <table_name>.ibd file has ROW_TYPE_COMPACT row format.)
这是由于mysql 5.6的文件恢复到mysql 5.7版本导致的错误，需要在建表语句后面添加ROW_FORMAT=COMPACT，如下所示：

create table test(id int, name varchar(10)) row_format=compact;
2.mysql 1812错误：

Error Code:1812. Tablespace is missing for table <table_name>
copy的ibd文件没有赋权，请按照第二步执行权限

