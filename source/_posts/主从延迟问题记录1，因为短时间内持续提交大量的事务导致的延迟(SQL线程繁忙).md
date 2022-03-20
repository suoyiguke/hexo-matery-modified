---
title: 主从延迟问题记录1，因为短时间内持续提交大量的事务导致的延迟(SQL线程繁忙).md
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
title: 主从延迟问题记录1，因为短时间内持续提交大量的事务导致的延迟(SQL线程繁忙).md
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
主库使用存储过程持续循环的做了100万次的insert，开启了自动提交。没个insert都是一个独立事务。

~~~
mysql>  show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: localhost
                  Master_User: root
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000001
          Read_Master_Log_Pos: 286503606
               Relay_Log_File: replicas-mysql-relay-bin.000006
                Relay_Log_Pos: 18482634
        Relay_Master_Log_File: mysql-bin.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB: test
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 279483737
              Relay_Log_Space: 25503649
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 2340
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 1
                  Master_UUID: 798f6aeb-2311-11e7-b1d0-1fd5d091664d
             Master_Info_File: D:\yinkai\mysql5715\data\master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Reading event from the relay log
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
1 row in set (0.00 sec)
~~~
>差不多 相差了这么多的位置 326587498-303620658=22 966 840

因为IO线程的工作，Read_Master_Log_Pos会一直增加直到等于主库的pos，如上 Read_Master_Log_Pos读取的主库pos为 286503606；
而现在从库的 Exec_Master_Log_Pos还只是279483737，因为从机的SQL线程一直在工作，这个Exec_Master_Log_Pos数值在不断地增加。直到等于Read_Master_Log_Pos的时候，同步就完成了；

如下，SQL线程的状态为Reading event from the relay log ，表示SQL线程正努力地在应用同步过来的relay log中继日志；
~~~
mysql> show processlist;
+----+-------------+-----------------+------+---------+------+----------------------------------+------------------+
| Id | User        | Host            | db   | Command | Time | State                            | Info             |
+----+-------------+-----------------+------+---------+------+----------------------------------+------------------+
| 28 | root        | localhost:58816 | test | Sleep   | 4100 |                                  | NULL             |
| 29 | root        | localhost:58818 | test | Sleep   | 2827 |                                  | NULL             |
| 32 | root        | localhost:59028 | test | Query   |    0 | starting                         | show processlist |
| 38 | root        | localhost:59344 | test | Sleep   | 1285 |                                  | NULL             |
| 39 | root        | localhost:59473 | test | Sleep   | 1124 |                                  | NULL             |
| 40 | root        | localhost:59474 | test | Sleep   | 1124 |                                  | NULL             |
| 41 | root        | localhost:59476 | test | Sleep   |  973 |                                  | NULL             |
| 42 | system user |                 | NULL | Connect | 1171 | Waiting for master to send event | NULL             |
| 43 | system user |                 | NULL | Connect | 2620 | Reading event from the relay log | NULL             |
+----+-------------+-----------------+------+---------+------+----------------------------------+------------------+
9 rows in set (0.00 sec)
~~~

过了接近1小时候，终于从库同步完成了。。如下          Exec_Master_Log_Pos终于也是等于 286503606了。看来从库的SQL线程对于alert table操作是相当的不给力啊。有什么办法可以解决呢？
~~~
mysql>  show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: localhost
                  Master_User: root
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000001
          Read_Master_Log_Pos: 286503606
               Relay_Log_File: replicas-mysql-relay-bin.000008
                Relay_Log_Pos: 320
        Relay_Master_Log_File: mysql-bin.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB: test
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 286503606
              Relay_Log_Space: 1696
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 1
                  Master_UUID: 798f6aeb-2311-11e7-b1d0-1fd5d091664d
             Master_Info_File: D:\yinkai\mysql5715\data\master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
1 row in set (0.00 sec)

ERROR:
No query specified

mysql>
~~~



通过自己的实验才知道mysql'同步居然这么慢的。得找找其他方法来优化下同步效率啊。
通过在从库中执行多次 show slave status。Read_Master_Log_Pos并没有继续增加，而Exec_Master_Log_Pos却一直在增加；且Slave_SQL_Running_State的值为Slave has read all relay log; waiting for more updates，这就说明了是SQL线程执行太慢跟不上呀。

问题就定位在sql线程上了

###解决方法

