---
title: mysql-使用mysqlbinlog命令导出和分析binlog文件.md
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
title: mysql-使用mysqlbinlog命令导出和分析binlog文件.md
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
**简单执行**
话不多说，我们直接上手使用这个命令试下
>C:\mysql5715\data>C:\mysql5715\bin\mysqlbinlog.exe --no-defaults --database=test --base64-output=decode-rows -v   mysql-bin.000001 >binlog007.sql
WARNING: The option --database has been used. It may filter parts of transactions, but will include the GTIDs in any case. If you want to exclude or include transactions, you should use the options --exclude-gtids or --include-gtids, respectively, instead.

结果被输入到binlog007.sql文件里
~~~
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=1*/;
/*!50003 SET @OLD_COMPLETION_TYPE=@@COMPLETION_TYPE,COMPLETION_TYPE=0*/;
DELIMITER /*!*/;
# at 4
#210220 13:35:07 server id 1  end_log_pos 123 CRC32 0x4711132f 	Start: binlog v 4, server v 5.7.15-log created 210220 13:35:07 at startup
# Warning: this binlog is either in use or was not closed properly.
ROLLBACK/*!*/;
# at 123
#210220 13:35:07 server id 1  end_log_pos 154 CRC32 0xda13f808 	Previous-GTIDs
# [empty]
# at 154
#210220 13:41:00 server id 1  end_log_pos 219 CRC32 0x0fa7a827 	Anonymous_GTID	last_committed=0	sequence_number=1
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 219
#210220 13:41:00 server id 1  end_log_pos 291 CRC32 0x31a77419 	Query	thread_id=3	exec_time=0	error_code=0
SET TIMESTAMP=1613799660/*!*/;
SET @@session.pseudo_thread_id=3/*!*/;
SET @@session.foreign_key_checks=1, @@session.sql_auto_is_null=0, @@session.unique_checks=1, @@session.autocommit=1/*!*/;
SET @@session.sql_mode=1344274432/*!*/;
SET @@session.auto_increment_increment=1, @@session.auto_increment_offset=1/*!*/;
/*!\C utf8mb4 *//*!*/;
SET @@session.character_set_client=45,@@session.collation_connection=45,@@session.collation_server=33/*!*/;
SET @@session.lc_time_names=0/*!*/;
SET @@session.collation_database=DEFAULT/*!*/;
BEGIN
/*!*/;
# at 291
#210220 13:41:00 server id 1  end_log_pos 338 CRC32 0x162b6ba3 	Table_map: `test`.`test` mapped to number 202
# at 338
#210220 13:41:00 server id 1  end_log_pos 378 CRC32 0xa44d4b07 	Write_rows: table id 202 flags: STMT_END_F
### INSERT INTO `test`.`test`
### SET
###   @1=6
# at 378
#210220 13:41:00 server id 1  end_log_pos 409 CRC32 0xaf397320 	Xid = 71
COMMIT/*!*/;
SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;
DELIMITER ;
# End of log file
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;

~~~

对比下直接使用show binlog events命令的binlog输出，显然mysqlbinlog输出更加详细；包含了简化的DML语句
~~~
mysql> show binlog events in 'mysql-bin.000001';
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                                  |
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
| mysql-bin.000001 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.15-log, Binlog ver: 4 |
| mysql-bin.000001 | 123 | Previous_gtids |         1 |         154 |                                       |
| mysql-bin.000001 | 154 | Anonymous_Gtid |         1 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
| mysql-bin.000001 | 219 | Query          |         1 |         291 | BEGIN                                 |
| mysql-bin.000001 | 291 | Table_map      |         1 |         338 | table_id: 202 (test.test)             |
| mysql-bin.000001 | 338 | Write_rows     |         1 |         378 | table_id: 202 flags: STMT_END_F       |
| mysql-bin.000001 | 378 | Xid            |         1 |         409 | COMMIT /* xid=71 */                   |
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
7 rows in set (0.02 sec)

~~~


**指定导出数据库**
默认情况下，mysqlbinlog会显示所有的内容，太过于杂乱。使用 -d 选项，可以指定一个数据库名称，将只显示在该数据库上所发生的事件。
~~~
mysqlbinlog -d crm mysqld-bin.000001 > crm-events.txt
~~~
也可以使用 --database 命令，效果相同。



**配置输出格式**
使用base64-output选项，可以控制输出语句何时是输出base64编码的BINLOG语句。以下是base64输出设置的可能值：
never  当指定如下所示的“never”时，它将在输出中显示base64编码的BINLOG语句。
always 当指定“always”选项时，只要有可能，它将只显示BINLOG项。因此，只有在专门调试一些问题时才使用它
decode-rows 这个选项将把基于行的事件解码成一个SQL语句，特别是当指定-verbose选项时，如下所示。
auto 这是默认选项。当没有指定任何base64解码选项时，它将使用auto。在这种情况下

 >如果想要输出能看得懂的sql 信息，请指定 --base64-output=decode-rows  -v 


**导出精确POS范围**
 -- start-position   --stop-position

>C:\mysql5715\data>C:\mysql5715\bin\mysqlbinlog.exe --no-defaults --database=test --base64-output=decode-rows -v  --start-position=5639   --stop-position=5940   mysql-bin.000001 >C:\mysql5715\data\binlog007.sql



**在输出中只显示语句**

默认情况下，正如在前面的示例输出中看到的一样，除了SQL语句之外，在mysqlbinlog输出中还会有一些附加信息。如果只想查看常规的SQL语句，而不需要其他内容，那么可以使用 -s 选项，如下所示。
也可以使用 --short-form 选项，效果相同。
~~~
mysqlbinlog -s mysqld-bin.000001
~~~


**限定时间**
~~~
mysqlbinlog --start-datetime="2017-08-16 10:00:00"  --stop-datetime="2017-08-16 15:00:00"  mysqld-bin.000001
~~~


**mysqlbinlog输出调试信息**
下面的调试选项，在完成处理给定的二进制日志文件之后，将检查文件打开和内存使用。
~~~
mysqlbinlog --debug-check mysqld-bin.000001
~~~
如下所示，在完成处理给定的二进制日志文件之后，下面的调试信息选项将显示额外的调试信息。




**禁止恢复过程产生日志** 
在使用二进制日志文件进行数据库恢复时，该过程中也会产生日志文件，就会进入一个循环状态，继续恢复该过程中的数据。因此，当使用mysqlbinlog命令时，要禁用二进制日志，请使用下面所示的-D选项：
~~~
mysqlbinlog -D mysqld-bin.000001
~~~
也可以使用 --disable-log-bin 命令，效果相同。
备注：在输出中，当指定-D选项时，将看到输出中的第二行。也就是SQL_LOG_BIN=0
当使用-to-last-log选项时，这个选项也会有所帮助。另外，请记住，该命令需要root权限来执行。


**刷新日志以清除Binlog输出**
当二进制日志文件没有被正确地关闭时，将在输出中看到一个警告消息，如下所示。
~~~
mysqlbinlog mysqld-bin.000001 > output.out
~~~

如下所示，报告中提示binlog文件没有正确地关闭。
Warning: this binlog is either in use or was not closed properly.

当看到这个提示时，需要连接到mysql并刷新日志，如下所示。
mysql> flush logs;
1
mysql> flush logs;

刷新日志之后，再次执行mysqlbinlog命令，将不会看到在mysqlbinlog输出中binlog未正确关闭的警告消息。


**从远程服务器获取二进制日志**
在本地机器上，还可以读取位于远程服务器上的mysql二进制日志文件。为此，需要指定远程服务器的ip地址、用户名和密码，如下所示。
此处使用-R选项。-R选项与-read-from-remote-server相同。
~~~
mysqlbinlog -R -h 192.168.101.2 -p mysqld-bin.000001
~~~
在上面命令中：
-R 选项指示mysqlbinlog命令从远程服务器读取日志文件
-h 指定远程服务器的ip地址
-p 将提示输入密码。默认情况下，它将使用“root”作为用户名。也可以使用 -u 选项指定用户名。
mysqld-bin.000001 这是在这里读到的远程服务器的二进制日志文件的名称。
下面命令与上面的命令完全相同：

下面的示例显示，还可以使用-u选项指定mysqlbinlog应该用于连接到远程MySQL数据库的用户名。请注意，这个用户是mysql用户（不是Linux服务器用户）。
~~~
mysqlbinlog -R --host=192.168.101.2 -u root -p mysqld-bin.000001
~~~
