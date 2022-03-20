---
title: mysql-general-log.md
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
title: mysql-general-log.md
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
查询全局日志情况
~~~
(root@localhost) [mysql]>SHOW VARIABLES LIKE 'general_log%';
+------------------+------------------------------+
| Variable_name    | Value                        |
+------------------+------------------------------+
| general_log      | OFF                          |
| general_log_file | /mdata/mysql57/localhost.log |
+------------------+------------------------------+
2 rows in set (0.01 sec)

~~~
开启general log 就会记录所有提交到mysql的sql。包括连接、查询等全部log信息。因此会对mysql产生很大性能影响。性能下降会超过50%。一般只在测试中使用，线上请关闭！


online修改
~~~
set global general_log=ON;
set global general_log_file='general.log';
~~~

配置
~~~
[mysqld]
general_log=ON
general_log_file=general.log
~~~

再次查询参数
~~~
(root@localhost) [mysql]>SHOW VARIABLES LIKE 'general_log%';
+------------------+-------------+
| Variable_name    | Value       |
+------------------+-------------+
| general_log      | ON          |
| general_log_file | general.log |
+------------------+-------------+
2 rows in set (0.00 sec)
~~~

查看日志
~~~
[root@localhost mysql]# cat /mdata/mysql57/general.log
/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld, Version: 5.7.33 (MySQL Community Server (GPL)). started with:
Tcp port: 3305  Unix socket: /tmp/mysql.sock3305
Time                 Id Command    Argument
2021-05-09T12:17:02.260977Z	    2 Query	set global general_log_file='general.log'
/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld, Version: 5.7.33 (MySQL Community Server (GPL)). started with:
Tcp port: 3305  Unix socket: /tmp/mysql.sock3305
Time                 Id Command    Argument
2021-05-09T12:17:09.592320Z	    2 Query	set global general_log_file='general.log'
/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld, Version: 5.7.33 (MySQL Community Server (GPL)). started with:
Tcp port: 3305  Unix socket: /tmp/mysql.sock3305
Time                 Id Command    Argument
2021-05-09T12:17:19.171311Z	    2 Query	set global general_log_file='general.log'
/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld, Version: 5.7.33 (MySQL Community Server (GPL)). started with:
Tcp port: 3305  Unix socket: /tmp/mysql.sock3305
Time                 Id Command    Argument
2021-05-09T12:17:23.573165Z	    2 Query	SHOW VARIABLES LIKE 'general_log%'
2021-05-09T12:21:41.651436Z	    2 Query	select * from user

~~~

###应用场景
1、审计功能
像一些银行中需要保存所有sql语句。
general log作为审计。
mysql 企业版有审计功能。
procona 分支版本，开源审计插件。


2、想知道应用程序在干嘛
比如我们使用一个备份工具，然后开启general log。查看这个程序背后的运行机制。

3、开发时测试
想知道我们写的程序刚刚发出了什么sql
