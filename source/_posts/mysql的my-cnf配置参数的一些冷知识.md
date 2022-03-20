---
title: mysql的my-cnf配置参数的一些冷知识.md
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
title: mysql的my-cnf配置参数的一些冷知识.md
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
###读取my.cnf顺序
mysql会依次读取这以下四个文件

~~~
[root@localhost bin]# ./mysqld --help --verbose | grep my.cnf
/etc/my.cnf /etc/mysql/my.cnf /usr/local/mysql/etc/my.cnf ~/.my.cnf 
                      my.cnf, $MYSQL_TCP_PORT, /etc/services, built-in default
~~~

>依次读取：
/etc/my.cnf > /etc/mysql/my.cnf> /usr/local/mysql/etc/my.cnf > ~/.my.cnf 

如果这些配置都中存在同一项配置，那么mysql会怎么做？
mysql会遵循`“参数替换原则”`。后面的配置文件中出现了之前配置文件中出现过的配置，则以后面的为准。
例如/etc/my.cnf中 port=3305，而 /etc/mysql/my.cnf中port=3306。那么mysql会以3306端口启动。
所以在安装过程中，请find / -name my.cnf 全局搜索下my.cnf，若出现了别的请将之删除或重命名。避免其它my.cnf的干扰。


###


###有些配置节点在一定时候才会被mysqld读取
- [mysqld-5.6]下的参数只会在你启动mysql5.6下才回去读取。如果启动mysql5.7就不会生效。同样[mysqld-5.7] 下的参数就只会在5.7版本下生效。

- [mysqld]下参数就是所有版本所有实例共有的。

- [mysqld1]、[mysqld2]就是在使用mysqld_multi时特定实例会去读取。如 ./mysqld_multi start 1 读取[mysqld1]下的； ./mysqld_multi start 2读取mysqld2]下的。


###错误日志
~~~
[mysqld]
log_err = mysql.err
~~~

1、log_err 默认 机器名.err。建议统一修改为固定名称
2、 可将配置错误日志到系统日志文件
~~~
[mysqld_safe]
syslog
syslog_tag=stock #mysqld_stock
~~~


###mysql绑定到固定ip上
mysql上只能绑定到一个ip上，不能绑定到多个ip上。如果需要多个只能指定*；
~~~
[mysqld]
bind-address = 192.168.6.128
~~~
bind-address 当前mysql绑定到192.168.6.128上。这个ip我们通过ifconfig得到。默认bind-address=*；这样做是有风险的，会允许外部用户连上mysql。


~~~
[root@localhost mysql]# netstat -anl
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp6       0      0 :::3305                 :::*                    LISTEN 
~~~
0 :::3305表示就是3305绑定在*上；

配置后
~~~
[root@localhost bin]# netstat -anl
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 192.168.6.128:3305      0.0.0.0:*               LISTEN     
~~~
192.168.6.128:3305 已经是绑定到192.168.6.128了

~~~
C:\Users\yinkai>telnet 192.168.6.128:3305
正在连接192.168.5.128:3305...无法打开到主机的连接。 在端口 23: 连接失败
~~~

然后防火墙策略上只允许指定ip来连我们这个端口。


###global和session级别参数
https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html
以long_query_time和slow_query_log为例。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8c56c64918c385e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8fb471315f195ee4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可见long_query_time的Scope= Global, Session，全局和会话级别；slow_query_log的Scop=Global只是全局级别;

二者在表现下有下面不同：
1、Global 设置SET SESSION报错。
~~~
(root@localhost) [mysql]>SET GLOBAL slow_query_log = ON;
Query OK, 0 rows affected (0.00 sec)

(root@localhost) [mysql]>SET SESSION slow_query_log = ON;
ERROR 1229 (HY000): Variable 'slow_query_log' is a GLOBAL variable and should be set with SET GLOBAL

(root@localhost) [mysql]>SET GLOBAL long_query_time = 2;
Query OK, 0 rows affected (0.00 sec)

(root@localhost) [mysql]>SET SESSION long_query_time = 2;
Query OK, 0 rows affected (0.00 sec)
~~~

2、SET GLOBAL 对于Global 参数修改后所有连接中都生效；SET GLOBAL 对于对于 Global, Session参数在session范围里不生效。想生效请用SET session。
~~~
(root@localhost) [mysql]>SET GLOBAL long_query_time = 4;
Query OK, 0 rows affected (0.00 sec)

(root@localhost) [mysql]>show SESSION variables like '%long_query_time';
+-----------------+----------+
| Variable_name   | Value    |
+-----------------+----------+
| long_query_time | 3.000000 |
+-----------------+----------+
1 row in set (0.00 sec)

(root@localhost) [mysql]>show GLOBAL variables like '%long_query_time';
+-----------------+----------+
| Variable_name   | Value    |
+-----------------+----------+
| long_query_time | 4.000000 |
+-----------------+----------+
1 row in set (0.01 sec)

(root@localhost) [mysql]>SET SESSION long_query_time = 4;
Query OK, 0 rows affected (0.00 sec)

(root@localhost) [mysql]>show SESSION variables like '%long_query_time';
+-----------------+----------+
| Variable_name   | Value    |
+-----------------+----------+
| long_query_time | 4.000000 |
+-----------------+----------+
1 row in set (0.00 sec)
~~~

###mysql密码这里有个坑
https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_default_password_lifetime

mysql在版本 57.4-5.7.10之间 `default_password_lifetime`默认值的值为360。也就是说360天(接近一年)之后用户所有的密码就过期了。

故建议配置到配置文件。设置为0这样确保我们的密码永不过期。而且注意要放在[mysqld-5.7]节点下，不这么做的话5.6版本不识别这个参数会报错的！
~~~
[mysqld-5.7]
default_password_lifetime=0
~~~



###可修改参数和只读参数

datadir就是一个read only 参数，它是不能进行在线修改的。Dynamic=NO; 需要在my.cnf中修改，停机重启生效。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b87f686d5697edfb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
(root@localhost) [mysql]>set global datadir='/etc/data';
ERROR 1238 (HY000): Variable 'datadir' is a read only variable
~~~

还有忽略大小写配置lower_case_table_names。这个参数我经常用，修改之后每次都得重启所以印象深刻。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b3065cbc8f4f5546.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###配置参数什么时候用下划线_，什么时候用减号-？
1、my.cnf中的配置、命令客户端中的参数都用下划线_
2、mysqld 注入参数时使用减号-
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e18c2c6095353379.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
我曾经对这个问题很郁闷很不解... 其实官网上就有答案。

###配置[client]节点
mysql客户端连接时会去找这个配置；做到无需使用用户名密码可以直接使用mysql命令登录。
~~~
[client]
user=root
password=123456
socket= /tmp/mysql.sock
~~~

如下直接输入mysql回着即可登录。
~~~
[root@localhost ~]# mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.33 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(root@localhost) [(none)]>\s
--------------
mysql  Ver 14.14 Distrib 5.7.33, for linux-glibc2.12 (x86_64) using  EditLine wrapper

Connection id:		3
Current database:	
Current user:		root@localhost
SSL:			Not in use
Current pager:		stdout
Using outfile:		''
Using delimiter:	;
Server version:		5.7.33 MySQL Community Server (GPL)
Protocol version:	10
Connection:		Localhost via UNIX socket
Server characterset:	latin1
Db     characterset:	latin1
Client characterset:	utf8
Conn.  characterset:	utf8
UNIX socket:		/tmp/mysql.sock3305
Uptime:			1 hour 43 min 34 sec

Threads: 2  Questions: 88  Slow queries: 0  Opens: 141  Flush tables: 1  Open tables: 134  Queries per second avg: 0.014
--------------

(root@localhost) [(none)]>

~~~

2、通过下面配置，丰富mysql命令行前缀提示内容。如果不加就只是mysql而已。
~~~
[mysql]
prompt=(\u@\h) [\d]>\
~~~

这样客户端就是这样了，信息更加全。
~~~
(root@localhost) [mysql]>
~~~


###禁用Tab补全

导大表时去按Tab补全会导致卡住；或者库下面表有很多时也会导致卡住，或者磁盘太慢。
如下，在导表时使用use都被卡住：
~~~
(root@localhost) [(none)]>use dbt3
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
~~~

所以建议大家不要去使用补全；

连接时使用`-A`也就会禁止补全了
~~~
mysql -A
~~~


也可以直接在配置文件中禁用，查找有关配置
~~~
[root@localhost ~]# mysql --help --verbose |grep A
  -A, --no-auto-rehash 
                      Automatically switch to vertical output mode if the
  --histignore=name   A colon-separated list of patterns to keep statements
  --local-infile      Enable/disable LOAD DATA LOCAL INFILE.
                      PAGER. Valid pagers are less, more, cat [> filename],
  --ssl-ca=name       CA file in PEM format.
  --ssl-capath=name   CA directory.
                      File path to the server public RSA key in PEM format.
  --tee=name          Append everything into outfile. See interactive help (\h)
  -U, --safe-updates  Only allow UPDATE and DELETE that uses keys.
  --select-limit=#    Automatic limit for SELECT when using --safe-updates.
  --max-join-size=#   Automatic limit for rows in a join when using
                      (pre-4.1.1) protocol. Deprecated. Always TRUE
  --binary-mode       By default, ASCII '\0' is disallowed and '\r\n' is
                        Also read groups with concat(group, suffix)
~~~

~~~
[mysql]
no_auto_rehash 
~~~





###表默认字符集设置
默认是latin1，我们要改为utf8mb4
~~~
[mysqld]
character_set_server=utf8mb4
~~~
重启后mysql建立的每张表默认的字符集都是uf8mb4了。
~~~
(root@localhost) [test]>create table zz ( a int(11) );
Query OK, 0 rows affected (0.01 sec)

(root@localhost) [test]>show create table zz;
+-------+----------------------------------------------------------------------------------------+
| Table | Create Table                                                                           |
+-------+----------------------------------------------------------------------------------------+
| zz    | CREATE TABLE `zz` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 |
+-------+----------------------------------------------------------------------------------------+
1 row in set (0.02 sec)
~~~

>字段、表、库字符集都设置为utf8mb4就行，设置为latin1省空间的思想没什么必要。
