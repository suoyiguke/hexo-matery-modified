---
title: mysql-使用binlog备份和恢复数据.md
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
title: mysql-使用binlog备份和恢复数据.md
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
binlog 它记录了所有的DDL和DML(除了数据查询语句)语句，以`事件`形式记录，还包含语句所执行的消耗的时间，MySQL的二进制日志是事务安全型的。 一般来说开启二进制日志大概会有1%的性能损耗(参见MySQL官方中文手册 5.1.24版)。binlog写入效率由sync_binlog参数控制,我们可以调整它来降低记录binlog的性能损耗  https://www.jianshu.com/p/67ebd0d2bb2f

**使用场景**
  1、mysql的主从复制；MySQL Replication在Master端开启binlog，Mster把它的二进制日志传递给slaves来达到master-slave数据一致的目的。 
  2、数据恢复；通过使用mysqlbinlog工具来使恢复数据。
    
**bin_log文件组成**
1、二进制日志索引文件（文件名后缀为.index）用于记录所有的二进制文件
2、二进制日志文件（文件名后缀为.00000*）记录数据库所有的DDL和DML(除了数据查询语句)语句事件。
###binlog文件保存和传输的形式
1、Statement 
每一条会修改数据的sql都会记录在binlog中。
优点：解决了row level的缺点，不需要记录每一行的变化；日志量少，节约IO，从库应用日志块。
缺点：一些新功能同步可能会有障碍,比如函数、触发器等。

2、Row
优点：记录详细；兼容性好，解决statement level模式无法解决的复制问题。
缺点：日志量大，因为是按行来拆分。
> 一般情况下，请配置为Row类型

3、Mixed
实际上就是前两种模式的结合，在mixed模式下，mysql会根据执行的每一条具体的sql语句来区分对待记录的日志形式，也是在statement和row之间选择一种。新版本中的mysql中对row level模式也做了优化，并不是所有的修改都会以row level来记录，像遇到表结构变更的时候就会以statement模式来记录，如果sql语句确实就是update或者delete等修改数据的语句，那么还是会记录所有行的变更。

**1、配置**

1、查看是否启用bin_log
默认关闭的
~~~
 show variables like '%log_bin%';
~~~

2、修改配置文件；重启
~~~
#开启二进制日志
server_id=1918
log_bin = mysql-bin
binlog_format = ROW
~~~

3、再次查看
~~~
mysql>  show variables like '%log_bin%';
+---------------------------------+-----------------------------------+
| Variable_name                   | Value                             |
+---------------------------------+-----------------------------------+
| log_bin                         | ON                                |
| log_bin_basename                | C:\mysql5715\data\mysql-bin       |
| log_bin_index                   | C:\mysql5715\data\mysql-bin.index |
| log_bin_trust_function_creators | OFF                               |
| log_bin_use_v1_row_events       | OFF                               |
| sql_log_bin                     | ON                                |
+---------------------------------+-----------------------------------+
6 rows in set (0.02 sec)

mysql> 
~~~

4、发现有很多bin文件，说明binlog日志开启成功
~~~
mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |      9190 |
+------------------+-----------+
1 row in set (0.01 sec)
~~~
**2、使用mysqlbinlog导出binlog**

创建一个用于备份的账号并赋予 replication slave 权限
~~~
grant replication slave on *.* to 'repl'@'localhost' identified by '123456'
~~~
然后在window下使用管理员身份cmd执行备份命令

~~~
mysqlbinlog  --no-defaults  --read-from-remote-server --raw --host=localhost  --port=3306 --user=repl --password=123456 --stop-never   mysql-bin.000012
~~~

更多mysqlbinlog命令的使用 https://www.jianshu.com/p/f29d33f3dff1


**3、使用binlog进行备份恢复**
如果不小心删除库了，可以使用binlog恢复；现在可以模拟一下删除cms库
1、删除cms库
~~~
DROP DATABASE cms;
~~~

2、直接在navicat中执行命令，查看当前binlog文件和节点信息
~~~
show master status;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ae8cf6c887ed6d72.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看出binlog的名字是mysql-bin.000012
3、然后执行查看binlog详细的命令
刚执行的drop命令在最后面，直接下拉到最低。最后一条就是了
~~~
show binlog events in 'mysql-bin.000012'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8124dd044d0fff6a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

得出了执行删除命令的之前pos节点：2279830

4、导出binlog的sql文件
打开cmd，执行下面的命令，将2279830节点之前的所有数据导出为sql文件
~~~
mysqlbinlog --no-defaults  mysql-bin.000012 -d cms  --skip-gtids --stop-position=2279830>huifu.sql
~~~
生成的文件就在当前目录下；

5、进行数据恢复
打开cmd，登陆mysql后执行：
~~~
source C:/Users/yinkai/huifu.sql;
~~~


注意：
1、在navicat的命令行中直接执行source命令恢复总是失败，放到cmd下就可以。不知道为什么会这样，一直以为navicat的命令行就等同于直接在cmd中连mysql

2、navicat中的“运行SQL文件”功能来运行binlog生成的sql文件，结果是无效的，只能通过source 命令来完成恢复数据！
普通导出的sql文件和binlog导出的sql文件是不同的。
