---
title: mysql-线上ddl操作要注意的.md
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
title: mysql-线上ddl操作要注意的.md
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
###1、Waiting for table metadata lock
给一张表添加索引，迟迟得不到提交。此时连普通的查询都被阻塞了！
查看 `SHOW PROCESSLIST`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ea80b0ad34e6f776.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


>提示 Waiting for table metadata lock

SHOW PROCESSLIST居然没有给出导致阻塞原因的sql。

那么查看当前的事务，的却有一条记录。在2020-06-18 14:40:53就执行了现在是15:42。一个小时了。
~~~
select * from information_schema.innodb_trx
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-18cef5105327fe9d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

那么，再查看详细点的信息。比如引发阻塞的sql。
~~~
SELECT a.trx_id, d.SQL_TEXT, a.trx_state, a.trx_started, a.trx_query, b.ID, b.USER, b.DB, b.COMMAND, b.TIME, b.STATE, b.INFO, c.PROCESSLIST_USER, c.PROCESSLIST_HOST, c.PROCESSLIST_DB FROM information_schema.INNODB_TRX a LEFT JOIN information_schema.PROCESSLIST b ON a.trx_mysql_thread_id = b.id AND b.COMMAND = 'Sleep' LEFT JOIN PERFORMANCE_SCHEMA.threads c ON b.id = c.PROCESSLIST_ID LEFT JOIN PERFORMANCE_SCHEMA.events_statements_current d ON d.THREAD_ID = c.THREAD_ID;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b41c399f6e49da8f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

不要继续让它阻塞下去了，杀死事务线程
~~~
kill 线程id 30
~~~

得到的引发阻塞的sql如下：

>SELECT STATE AS `Status`, ROUND(SUM(DURATION),7) AS `Duration`, CONCAT(ROUND(SUM(DURATION)/0.000205*100,3), '') AS `Percentage` FROM INFORMATION_SCHEMA.PROFILING WHERE QUERY_ID=36 GROUP BY SEQ, STATE ORDER BY SEQ


如果以后再出现这种因为dll语句引发的阻塞怎么办？这种情况会锁住表后增删改查都不行的。这个sql事务居然执行了一个多小时，我们可以设置ddl语句事务的超时时间。
~~~
SELECT @@lock_wait_timeout -- 31536000 默认是一年
set session lock_wait_timeout = 1800 
set global lock_wait_timeout = 1800
~~~
