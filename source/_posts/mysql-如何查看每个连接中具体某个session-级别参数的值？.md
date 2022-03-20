---
title: mysql-如何查看每个连接中具体某个session-级别参数的值？.md
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
title: mysql-如何查看每个连接中具体某个session-级别参数的值？.md
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
我们知道mysql中参数变量分为**session 会话级别和global 全局级别**。
如long_query_time 就是一个典型的会话级别参数。
set session long_query_time = 1.5; 设置后仅仅在当前会话中有效。重新打开一个会话仍然是默认值。session 可以省略
set global long_query_time =1.5 ；设置后重新打开一个会话，重新打开一个会话，值是1.5


>注意：我们将一个会话级别的参数如long_query_time 的global 全局范围值修改为新的值，那么以后新创建的会话会是这个新的值。但是对于原来已经创建的连接，它们的参数值还是老样子。很多线上修改话级别的参数不生效就是这个原因（需要set session一下才能影响到当前会话）。





通过这样来查看当前会话和全局的参数值：
show  session variables like '%long_query_time%';
show global variables like '%long_query_time %';

但是这样的show session variables  只能查看自己会话的参数值，而别的会话的参数值是什么情况我们不知道呀，所以5.7版本推出了一种方式来查询：
~~~
(root@localhost) [performance_schema]>select * from performance_schema.variables_by_thread where variable_name='long_query_time';
+-----------+-----------------+----------------+
| THREAD_ID | VARIABLE_NAME   | VARIABLE_VALUE |
+-----------+-----------------+----------------+
|        29 | long_query_time | 10.000000      |
|        30 | long_query_time | 1.500000       |
|        31 | long_query_time | 10.000000      |
+-----------+-----------------+----------------+
3 rows in set (0.00 sec)

~~~
thread_id 为30的线程对应long_query_time值为1.5，我们还想知道具体是哪个process 连接的值是1.5？
5.7提供了这个performance_schema.threads表，它保存了THREAD_ID和PROCESSLIST_ID还有THREAD_OS_ID的对应关系。
~~~
(root@localhost) [performance_schema]>select * from performance_schema.threads limit 1 \G
*************************** 1. row ***************************
          THREAD_ID: 1
               NAME: thread/sql/main
               TYPE: BACKGROUND
     PROCESSLIST_ID: NULL
   PROCESSLIST_USER: NULL
   PROCESSLIST_HOST: NULL
     PROCESSLIST_DB: NULL
PROCESSLIST_COMMAND: NULL
   PROCESSLIST_TIME: 22857
  PROCESSLIST_STATE: NULL
   PROCESSLIST_INFO: NULL
   PARENT_THREAD_ID: NULL
               ROLE: NULL
       INSTRUMENTED: YES
            HISTORY: YES
    CONNECTION_TYPE: NULL
       THREAD_OS_ID: 26446
1 row in set (0.00 sec)


~~~

那么我们查下THREAD_ID =30 的记录
~~~
(root@localhost) [performance_schema]>select * from threads where THREAD_ID =30  limit 1 \G
*************************** 1. row ***************************
          THREAD_ID: 30
               NAME: thread/sql/one_connection
               TYPE: FOREGROUND
     PROCESSLIST_ID: 5
   PROCESSLIST_USER: root
   PROCESSLIST_HOST: localhost
     PROCESSLIST_DB: NULL
PROCESSLIST_COMMAND: Sleep
   PROCESSLIST_TIME: 333
  PROCESSLIST_STATE: NULL
   PROCESSLIST_INFO: set session long_query_time = 1.5
   PARENT_THREAD_ID: NULL
               ROLE: NULL
       INSTRUMENTED: YES
            HISTORY: YES
    CONNECTION_TYPE: Socket
       THREAD_OS_ID: 26480
1 row in set (0.00 sec)

~~~
得到了  THREAD_ID: 30对应的 PROCESSLIST_ID: 5

得出结论：那么show processlist 结果的第二条连接的long_query_time的值是1.5


~~~
(root@localhost) [performance_schema]>show processlist;
+----+------+-------------------+--------------------+---------+-------+----------+------------------+
| Id | User | Host              | db                 | Command | Time  | State    | Info             |
+----+------+-------------------+--------------------+---------+-------+----------+------------------+
|  4 | root | 192.168.6.1:20193 | mysql              | Sleep   | 17649 |          | NULL             |
|  5 | root | localhost         | NULL               | Sleep   |  2500 |          | NULL             |
|  6 | root | localhost         | performance_schema | Query   |     0 | starting | show processlist |
+----+------+-------------------+--------------------+---------+-------+----------+------------------+
~~~
>processlistId 对应thread id，然后又对应操作系统进程的线程id  thread_os_id


那么上面操作可以使用join来直接完成：
~~~
select a.processlist_id,
a.thread_id,
a.thread_os_id,
a.processlist_user,
a.processlist_host,
a.processlist_db,
a.processlist_command,
a.processlist_state,
a.processlist_info,
b.* from performance_schema.threads a ,performance_schema.variables_by_thread b where a.thread_id=b.thread_id and b.variable_name='long_query_time';
~~~

结果如下
~~~
(root@localhost) [performance_schema]>select a.processlist_id, a.thread_id, a.thread_os_id, a.processlist_user, a.processlist_host, a.processlist_db, a.processlist_command, a.processlist_state, a.processlist_info, b.* from performance_schema.threads a ,performance_schema.variables_by_thread b where a.thread_id=b.thread_id and b.variable_name='long_query_time' limit 1\G
*************************** 1. row ***************************
     processlist_id: 4
          thread_id: 29
       thread_os_id: 26605
   processlist_user: root
   processlist_host: 192.168.6.1
     processlist_db: mysql
processlist_command: Sleep
  processlist_state: NULL
   processlist_info: SELECT STATE AS `Status`, ROUND(SUM(DURATION),7) AS `Duration`, CONCAT(ROUND(SUM(DURATION)/0.003109*100,3), '') AS `Percentage` FROM INFORMATION_SCHEMA.PROFILING WHERE QUERY_ID=152 GROUP BY SEQ, STATE ORDER BY SEQ
          THREAD_ID: 29
      VARIABLE_NAME: long_query_time
     VARIABLE_VALUE: 10.000000
1 row in set (0.00 sec)

~~~



