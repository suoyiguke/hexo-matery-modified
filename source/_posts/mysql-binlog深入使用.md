---
title: mysql-binlog深入使用.md
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
title: mysql-binlog深入使用.md
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
###配置和原理
1、如果未给出二进制日志的文件名，那么默认名为主机名-bin。如果给出了文件名，但没有包含路径，那么文件将被写入数据目录。建议最好指定一个文件名，语句如下。
~~~
[mysqld]
log-bin =/path/to/logmysql-bin
~~~

 查看binlog的目录
show global variables like "%log_bin%";


2、binlog过期时间
单位天，expire_logs_days设置会在运行flush logs命令后触发删除过期的日志，注意，不要用操作系统下的rm命令删除日志，这可能会导致你执行日志清理的命令失败，你可能需要手动编辑文件hostname-bin.index来反映实际的文件列表。虽然MySQL 5.1可以设置日志过期策略，但仍然存在一个可能，对于生产繁忙的系统，二进制日志可能会塞满磁盘，MySQL 5.6可以设置保留的二进制日志文件大小， 以免磁盘空间过满，这在一定程度上改善了日志的保留策略。
~~~
SHOW VARIABLES LIKE '%expire_logs_days%'
~~~

3、mysqld将在每个二进制日志名的后面添加一个数字扩展名。每次要启动服务器或刷新日志时，该数字将会增加。如果当前的日志大小达到了max_binlog_size参数 设置的值，那么mysqld会自动创建新的二进制日志。 
~~~
SHOW VARIABLES LIKE '%max_binlog_size%'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e2e1ac4fc3cad649.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
binlog文件达到1073741824字节时会自动生成新的binlog

4、mysqld还将创建一个二进制日志索引文件，其中包含了所有使用二进制日志文件的文件名。默认情况下该索引文件与二进制日志文件的文件名相同，扩展名 为“.index”。当mysqld正在运行时，不可手动编辑该文件，这样做可能会使mysqld发生异常。 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-872aab7af8b7e447.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




###binlog操作
1、 每次flush logs; 都会另新建一个binlog文件并切换到上面去；在进行删库等危险操作时，我们建议，马上再执行一次flush logs，也就是让出错的部分就集中在这么一个binlog日志文件中。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3d67ba8efc6cae09.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

flush logs;


2、 查看当前mysql的binlog具体数据

show master status;


3、查看具体binlog的详细操作数据

 >IN 'log_name' ：指定要查询的binlog文件名(不指定就是第一个binlog文件)
 FROM pos ：指定从哪个pos起始点开始查起(不指定就是从整个文件首个pos点开始算)
 LIMIT [offset,] ：偏移量(不指定就是0)
 row_count ：查询总条数(不指定就是所有行)
show binlog events [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count];



show binlog events in 'mysql-bin.000001' from 8771 limit 0,5



4、对于数据库的操作，经常需要暂时停止对bin-log日志的写入，那就需要这个命令：

set sql_log_bin=on/off 

这个操作在会话级别有效

5、查看所有binlog文件 

SHOW BINARY LOGS

![image.png](https://upload-images.jianshu.io/upload_images/13965490-5d141795607c4eb1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

6、删除历史二进制日志，一直到mysql-bin.000007这个文件为止。

 purge binary logs to 'mysql-bin.000007';

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f0557159f4f03b6d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

7、删除所有binlog

RESET MASTER

8、设置binlog文件保存事件，过期删除，单位天

set global expire_log_days=3;

9、删除slave的中继日志
reset slave;

10、删除指定日期前的日志索引中binlog日志文件
purge master logs before '2019-03-09 14:00:00';

11、删除指定日志文件
purge master logs to 'master.000003';

12、停止和启动从机sql线程
STOP SLAVE sql_thread;
START SLAVE sql_thread;
13、停止和启动从机IO线程
STOP SLAVE IO_thread;
START SLAVE IO_thread;

###我发现的一些规律

show binlog events in 'mysql-bin.000025'; 语句列出的两个字段：Pos和End_log_pos；其中End_log_pos就对应show master status; 语句产生的Position字段
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e5b0696179e42d71.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
