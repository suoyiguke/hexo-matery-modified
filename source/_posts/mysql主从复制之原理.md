---
title: mysql主从复制之原理.md
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
title: mysql主从复制之原理.md
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

**三个线程各司其职**

MySQL通过3个线程来完成主从库间的数据复制:其中 Binlog Dump线程 跑在主库上，I/O线程和SQL线程跑在从库上;
每个从机连上主机都会维护一个Binlog Dump，有多少个从机就有多少个Binlog Dump线程； 




**流程**

1、首先Binlog Dump线程会持续记录主库的所有事务事件到binlog
2、从库发起START SLAVE时，IO线程会去发起一个请求到主库
3、主库接收到请求后Binlog Dump线程推送binlog事件到从库
4、从库IO线程接收binlog事件，并将之应用到Relay Log中
5、从库SQL线程读取Relay Log变更并应用到数据库
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6c8e632021193352.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**观察**

分别在主机和从机中执行SHOW PROCESSLIST;可以观察到三个线程的情况：
主机
~~~
mysql> SHOW PROCESSLIST;
+----+------+-----------------+--------+-------------+------+---------------------------------------------------------------+------------------+
| Id | User | Host            | db     | Command     | Time | State                                                         | Info             |
+----+------+-----------------+--------+-------------+------+---------------------------------------------------------------+------------------+
|  2 | root | localhost:54886 | chgdzc | Sleep       |  235 |                                                               | NULL             |
|  3 | root | localhost:54887 | test   | Query       |    0 | starting                                                      | SHOW PROCESSLIST |
|  4 | root | localhost:54991 | NULL   | Binlog Dump |  395 | Master has sent all binlog to slave; waiting for more updates | NULL             |
|  5 | root | localhost:55204 | test   | Sleep       |  173 |                                                               | NULL             |
+----+------+-----------------+--------+-------------+------+---------------------------------------------------------------+------------------+
4 rows in set (0.01 sec)
~~~
id为4的是Binlog Dump线程
从机
~~~
mysql> SHOW PROCESSLIST;
+----+-------------+-----------------+----------+---------+------+--------------------------------------------------------+------------------+
| Id | User        | Host            | db       | Command | Time | State                                                  | Info             |
+----+-------------+-----------------+----------+---------+------+--------------------------------------------------------+------------------+
|  2 | root        | localhost:54962 | qwjjspxt | Sleep   |  235 |                                                        | NULL             |
|  3 | root        | localhost:54963 | test     | Query   |    0 | starting                                               | SHOW PROCESSLIST |
|  4 | system user |                 | NULL     | Connect |  328 | Waiting for master to send event                       | NULL             |
|  5 | system user |                 | NULL     | Connect |  101 | Slave has read all relay log; waiting for more updates | NULL             |
|  6 | root        | localhost:55159 | test     | Sleep   |   93 |                                                        | NULL             |
+----+-------------+-----------------+----------+---------+------+--------------------------------------------------------+------------------+
5 rows in set (0.02 sec)
~~~
id为4的是IO线程，id为5的是SQL线程


**根据原理可以得出结论**
1、主库必须开启binlog
2、从库必须开启Relay Log，可以不开启 binlog（但是若该从机还要充当另一台从机的主机的话就必须要开启binlog）


**mysql从机crash之后重启是如何保证继续从之前的位置开始同步呢？**
从库上默认还会创建两个日志文件master.info和relay-log.info用来保存复制的进度。这两个文件在磁盘上以文件形式分别记录了从库的IO线程当前读取主库二进制日志 Binlog 的进度和SQL线程应用中继日志Relay Log 的进度。
master.info
~~~
25
mysql-bin.000001
409
localhost
root
Sgl20@14
3306
60
0





0
30.000

0
798f6aeb-2311-11e7-b1d0-1fd5d091664d
86400


0

~~~

relay-log.info
~~~
7
.\replicas-mysql-relay-bin.000002
575
mysql-bin.000001
409
0
0
1

~~~


例如，通过SHOW SLAVE STATUS命令能够看到当前从库复制的状态：

~~~
mysql> SHOW SLAVE STATUS\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: localhost 主库ip
                  Master_User: root  主库用户
                  Master_Port: 3306  主库端口
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000001  IO线程当前读取到主库binlog的文件名
          Read_Master_Log_Pos: 409 IO线程当前读取到主库binlog的位置
               Relay_Log_File: replicas-mysql-relay-bin.000002  SQL线程当前应用的Relay Log文件名
                Relay_Log_Pos: 575   SQL线程当前应用的Relay Log的位置
        Relay_Master_Log_File: mysql-bin.000001   SQL线程当前应用的Relay Log 对应的binlog文件名
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
          Exec_Master_Log_Pos: 409 SQL线程当前应用Relay Log的位置对应于主库binlog文件的位置
              Relay_Log_Space: 791
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
~~~
Master_Log_File的值就是从库中SHOW SLAVE STATUS的Position字段；
我们可以通过观察Exec_Master_Log_Pos的值和Master_Log_File的值来判断当前从库的复制进度：
Exec_Master_Log_Pos<Master_Log_File 则是说明数据仍未同步完成。
Exec_Master_Log_Pos一直增长说明从库的SQL线程一直在努力地同步中继日志；
Master_Log_File 一直增长说明主库在源源不断地进行事务提交；
