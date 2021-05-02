---
title: mysql 使用mysqld_multi在一台机器上安装多个mysql实例（多实例安装）
top: true
cover: false
toc: true
mathjax: true
date: 2021-05-02 19:08:12
password:
summary:
tags:
categories:
---

https://dev.mysql.com/doc/refman/5.7/en/mysqld-multi.html

多实例安装即是一台服务器安装多个mysql实例；这样可以充分利用硬件资源；通过mysqld_multi程序即可。

例如我们现在有一台配置较高的机器：32C，512G，8SSD做RIAND5，而4C 8G才是主流服务器配置。这么一台服务器仅仅跑一个mysql是非常奢侈的。现在我们就可以在这台机器上同时部署三个mysql实例：mysqld3306、mysqld3307、mysqld3308。




## mysqld_multi配置
1、配置mysqld_multi节点；mysqld_safe启动、mysqladmin停止、mysqld_multi.log日志（有问题都可以到这里排查）。
2、配置三个实例：mysqld3306、mysqld3307、mysqld3308；分别指定port、datadir、socket。
3、此时的[mysqld]节点下的配置是mysqld3306、mysqld3307、mysqld3308三个实例所共享的。
4、[client] 节点配置了默认客户端连接参数。我这里配置了root用户、密码还有指定socket为/tmp/mysql.sock3306。则随后可以直接使用mysql命令连接到mysql3306实例而不需要额外指定参数。
~~~
[mysqld]
user = mysql
basedir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64
log_error=error.log
plugin-load=validate_password.so

[mysqld_multi]
mysqld=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld_safe
mysqladmin=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqladmin
log=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/mysqld_multi.log

[mysqld3306]
port=3306
datadir=/mdata/mysql57-3306
socket= /tmp/mysql.sock3306

[mysqld3307]
port=3307
datadir=/mdata/mysql57-3307
socket= /tmp/mysql.sock3307

[mysqld3308]
port=3308
datadir=/mdata/mysql57-3308
socket= /tmp/mysql.sock3308

[client]
user=root
password=1111aaA_
socket= /tmp/mysql.sock3306
[mysql]
prompt=(\\u@\\h) [\\d]>\\
~~~



## 启动过程

1、以mysqld3306实例为例，初始化数据如下。注意指定datadir。
~~~
[root@localhost bin]# ./mysqld --initialize --datadir=/mdata/mysql57-3306
~~~
>注意：[mysqld]下配置了plugin-load=validate_password.so 密码插件的话就不能使用--initialize-insecure，请使用--initialize。否则初始化后密码是空的，然后连不上。

mysqld3306实例生成密码如下：
~~~
[root@localhost mysql57-3306]# cat error.log 
2021-05-01T03:22:15.245117Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2021-05-01T03:22:16.562503Z 0 [Warning] InnoDB: New log files created, LSN=45790
2021-05-01T03:22:16.692390Z 0 [Warning] InnoDB: Creating foreign key constraint system tables.
2021-05-01T03:22:16.750221Z 0 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: 6e1b5ce4-aa2c-11eb-befe-000c292882e9.
2021-05-01T03:22:16.751331Z 0 [Warning] Gtid table is not ready to be used. Table 'mysql.gtid_executed' cannot be opened.
2021-05-01T03:22:17.412496Z 0 [Warning] CA certificate ca.pem is self signed.
2021-05-01T03:22:17.657496Z 1 [Note] A temporary password is generated for root@localhost: Ye-7i!4-gtw)
~~~

2、使用mysqld_multi 命令启动实例，start后面跟的3306和[mysqld3306]中的3306对应起来，这里可以使用任何名字。如[mysqld1]就这样启动：./mysqld_multi start 1。
~~~
[root@localhost bin]# ./mysqld_multi start 3306
~~~
3、查看状态
~~~
[root@localhost bin]# ./mysqld_multi report 3306
Reporting MySQL servers
MySQL server from group: mysqld3306 is running
~~~

4、查看进程。如下启动mysqld3306 实例后就出现了两个进程：mysqld_safe 和 mysqld 。
~~~
[root@localhost bin]# ps -ef |grep mysql
root      11675      1  0 10:55 pts/0    00:00:00 /bin/sh /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld_safe --port=3306 --datadir=/mdata/mysql57-3306 --socket=/tmp/mysql.sock3306
mysql     11827  11675  2 10:55 pts/0    00:00:00 /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld --basedir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64 --datadir=/mdata/mysql57-3306 --plugin-dir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/lib/plugin --user=mysql --log-error=error.log --pid-file=localhost.localdomain.pid --socket=/tmp/mysql.sock3306 --port=3306
root      11874   7035  0 10:55 pts/0    00:00:00 grep --color=auto mysql
~~~

5、继续初始化和启动其它进程。
./mysqld_multi start 3307
./mysqld_multi start 3308

6、最终的mysql相关进程有6个。如下，分别3个mysqld、3个mysqld_safe 。
~~~
[root@localhost bin]# ps -ef |grep mysql
root      11675      1  0 10:55 pts/0    00:00:00 /bin/sh /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld_safe --port=3306 --datadir=/mdata/mysql57-3306 --socket=/tmp/mysql.sock3306
mysql     11827  11675  0 10:55 pts/0    00:00:00 /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld --basedir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64 --datadir=/mdata/mysql57-3306 --plugin-dir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/lib/plugin --user=mysql --log-error=error.log --pid-file=localhost.localdomain.pid --socket=/tmp/mysql.sock3306 --port=3306
root      11948      1  0 10:56 pts/0    00:00:00 /bin/sh /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld_safe --port=3307 --datadir=/mdata/mysql57-3307 --socket=/tmp/mysql.sock3307
mysql     12104  11948  2 10:56 pts/0    00:00:00 /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld --basedir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64 --datadir=/mdata/mysql57-3307 --plugin-dir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/lib/plugin --user=mysql --log-error=error.log --pid-file=localhost.localdomain.pid --socket=/tmp/mysql.sock3307 --port=3307
root      12199      1  0 10:57 pts/0    00:00:00 /bin/sh /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld_safe --port=3308 --datadir=/mdata/mysql57-3308 --socket=/tmp/mysql.sock3308
mysql     12352  12199  7 10:57 pts/0    00:00:00 /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld --basedir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64 --datadir=/mdata/mysql57-3308 --plugin-dir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/lib/plugin --user=mysql --log-error=error.log --pid-file=localhost.localdomain.pid --socket=/tmp/mysql.sock3308 --port=3308
root      12398   7035  0 10:57 pts/0    00:00:00 grep --color=auto mysql

~~~


7、 netstat -anl 看下端口。3306、3307、3308 都被占用了。

~~~
[root@localhost tmp]# netstat -anl
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 192.168.6.128:22        192.168.6.1:1042        ESTABLISHED
tcp        0      0 192.168.6.128:22        192.168.6.1:1410        ESTABLISHED
tcp        0      0 192.168.6.128:22        192.168.6.1:2135        ESTABLISHED
tcp        0      0 192.168.6.128:22        192.168.6.1:1043        ESTABLISHED
tcp6       0      0 :::3306                 :::*                    LISTEN     
tcp6       0      0 :::3307                 :::*                    LISTEN     
tcp6       0      0 :::3308                 :::*                    LISTEN     
tcp6       0      0 :::22                   :::*                    LISTEN     
udp        0      0 127.0.0.1:323           0.0.0.0:*                          
udp6       0      0 ::1:323                 :::*                               
Active UNIX domain sockets (servers and established)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  2      [ ACC ]     STREAM     LISTENING     75933    /tmp/mysql.sock3306
unix  3      [ ]         DGRAM                    11503    /run/systemd/notify
unix  2      [ ACC ]     STREAM     LISTENING     48932    /tmp/mysql.sock3307
unix  2      [ ]         DGRAM                    11505    /run/systemd/cgroups-agent
unix  2      [ ACC ]     STREAM     LISTENING     19191    /run/systemd/private
unix  2      [ ACC ]     STREAM     LISTENING     76809    /tmp/mysql.sock3308
unix  2      [ ]         DGRAM                    33496    

~~~


8、连接后修改密码。
使用sock连接。如mysql3306则指定/tmp/mysql.sock3306。
并set password = '1111aaA_'; 修改当前用户密码。
~~~
[root@localhost bin]# ./mysql -S /tmp/mysql.sock3306 -p
Enter password: 
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
[root@localhost bin]# ./mysql -S /tmp/mysql.sock3306 -pYe-7i!4-gtw)
-bash: !4: event not found
[root@localhost bin]# ./mysql -S /tmp/mysql.sock3306 -p'Ye-7i!4-gtw)'
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 6
Server version: 5.7.33

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(root@localhost) [(none)]>set password = '1111aaA_';

~~~

9、随后可以直接输入mysql登录了。
~~~
[root@localhost /]# mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 5.7.33 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(root@localhost) [(none)]>\s
--------------
mysql  Ver 14.14 Distrib 5.7.33, for linux-glibc2.12 (x86_64) using  EditLine wrapper

Connection id:		9
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
UNIX socket:		/tmp/mysql.sock3306
Uptime:			14 min 19 sec

Threads: 2  Questions: 22  Slow queries: 0  Opens: 106  Flush tables: 1  Open tables: 99  Queries per second avg: 0.025
--------------


~~~





拓展：
1、同理，其它的mysql3307、mysql3308也是一样的操作。另外想要直接使用mysql -S /tmp/mysql.sock3307、mysql -S /tmp/mysql.sock3308 直接登录。那么需要将其它两个实例的密码都改为1111aaA_。

2、有人喜欢使用mysqld –defaults-file=/etc/my.cnf 的defaults-file参数来指定特定的my.cnf配置文件来实现多实例安装。但是这样的话实例一多就不好管理了。所以推荐使用mysqld_multi。

3、多实例IO竞争问题怎么解决？
对于资源管理、资源调度问题可以通过操作系统层面的技术解决。
LXC 
docker
Cgroup


4、MHA、keepalive 这些集群软件请不要使用多实例安装，这种高可用软件肯定是要部署到多个机器上。


5、每次初始化会不会对已经存在的实例有影响？
初始化实例时请指定datadir：
./mysqld --initialize --datadir=/mdata/mysql57-3306
当然不指定的话，就算原来目录已经存在数据。那么此次执行会失败的。并不会对已经存在的数据目录产生影响。
~~~
[root@localhost bin]# ./mysqld --initialize --datadir=/mdata/mysql57-3308
2021-05-01T04:18:01.028139Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2021-05-01T04:18:01.029870Z 0 [ERROR] --initialize specified but the data directory has files in it. Aborting.
2021-05-01T04:18:01.029901Z 0 [ERROR] Aborting

~~~

6、使用mysqld_multi stop 3306 停止实例时可能会失败，因为实际上是去调用mysqladmin来停止，mysqladmin会去读取[client]下的用户名和密码 ，若不符合自然是关闭不了。可以选择使用kill来停止，或者去修改[client]配置。
~~~
[root@localhost bin]# ./mysqld_multi stop 3307
[root@localhost bin]# ./mysqld_multi report 3307
Reporting MySQL servers
MySQL server from group: mysqld3307 is running
~~~


7、选择单机多实例，还是建立多个虚拟机？
这就是不同的资源调度的方式。
像淘宝的RDS云数据库就是使用LXC Container 来进行资源隔离的，其实就是安装多个实例，这种方式性能会更好。当然虚拟机也有它的好处。

8、一个实例建立多个数据库。或者多个数据库分别放到不同实例下。
这个还是得看业务。