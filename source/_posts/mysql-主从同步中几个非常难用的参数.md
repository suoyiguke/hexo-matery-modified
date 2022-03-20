---
title: mysql-主从同步中几个非常难用的参数.md
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
title: mysql-主从同步中几个非常难用的参数.md
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
>其实不用这些参数也能保证主从同步的顺利执行

我们知道mysql主从同步可以选择性同步某几个数据库，并且要想实现这个目的可以借助如下几个参数：
- binlog-do-db=需要复制的数据库名，如果复制多个数据库，重复设置这个选项即可
- binlog-ignore-db=不需要复制的数据库苦命，如果复制多个数据库，重复设置这个选项即可
- replicate-do-db=需要复制的数据库名，如果复制多个数据库，重复设置这个选项即可
- replicate-ignore-db=不需要复制的数据库名，如果要忽略多个数据库，重复设置这个选项即可
>注意这些参数只能通过show master STATUS或者show slave STATUS查看，不能通过show variables like  'binlog%'查看。

**这四个参数一般不使用用，非常危险，可能会导致主从不一致，慎用！！！**

###那么怎么实现这个选择性同步某几个库的目的呢？？？
在从库设置参数replicate-wild-do-table或者Replicate-Ignore-Table
slave上配置过滤, 使用基于查询中真正涉及到的表的选项,  避免复制 dbname 数据库中的数据的安全的方案是 配置:  replicate-wild-ignore-table=dbname .%. 这样做仍然有一些特殊的情况, 不能正常工作,但可以在更多的情况下正常工作,并且会遇到更少的意外。

>例如replicate-wild-do-table=dbname .% ，可以设置多个，这样就可以解决跨库更新的问题。

###下面说下replicate_do_db的在线修改
mysql 在线修改replicate-do-db等参数

~~~
#必须先停止sql_thread进程
mysql> stop slave sql_thread;
Query OK, 0 rows affected (0.01 sec)
 
mysql> change replication filter replicate_do_db=(db1);
Query OK, 0 rows affected (0.00 sec)

~~~

设置为空

~~~

mysql> stop slave sql_thread;
Query OK, 0 rows affected (0.00 sec)
 
mysql> change replication filter replicate_do_db=();
Query OK, 0 rows affected (0.00 sec)
 
mysql> start slave sql_thread;
Query OK, 0 rows affected (0.01 sec
~~~
