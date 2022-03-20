---
title: mysql-两种连接方式和SSL连接、x509认证.md
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
title: mysql-两种连接方式和SSL连接、x509认证.md
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
mysql连接可分为socket连接和TCP|IP连接两种。

### 1、本地socket连接
[root@localhost bin]# mysql -uroot -p123456 -S/tmp/mysql.sock
-S/tmp/mysql.sock可以省略，因为默认参数如下：
~~~
(root@localhost) [mysql]>show variables like 'sock%';
+---------------+-----------------+
| Variable_name | Value           |
+---------------+-----------------+
| socket        | /tmp/mysql.sock |
+---------------+-----------------+
~~~
假如sock文件另有其它，那么就后面不能省略，需要指定下。

### 2、TCP|IP协议远程连接
mysql -h127.0.0.1 -P3306 -uroot -p123456


>可以通过配置my.cnf免密登录
[client]
user=root
password=123456
socket=/tmp/mysql.sock


那么问题来了，如何知道当前连接的连接方式？

**查看当前连接方式，使用\s 或者status命令**
Connection:     Localhost via UNIX socket 表示使用 socket 进行本地的连接
SSL:            Not in use 没有使用SSL
~~~
[root@localhost bin]# mysql -uoot -p123456 -S/tmp/mysql.sock
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 15
Server version: 5.7.33 MySQL Community Server (GPL)
Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(root@localhost) [(none)]>status;

mysql  Ver 14.14 Distrib 5.7.33, for linux-glibc2.12 (x86_64) using  EditLine wrapper

Connection id:		15
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
UNIX socket:		/tmp/mysql.sock
Uptime:			8 hours 15 min 5 sec

Threads: 4  Questions: 436  Slow queries: 0  Opens: 261  Flush tables: 1  Open tables: 254  Queries per second avg: 0.014
--------------
~~~

Connection:     127.0.0.1 via TCP/IP 使用TCP/IP 协议进行远程连接
SSL:            Cipher in use is ECDHE-RSA-AES128-GCM-SHA256 使用了SSL加密

~~~
root@localhost bin]# mysql -h127.0.0.1 -uroot -p123456 
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 16
Server version: 5.7.33 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

root@localhost) [(none)]>\s
--------------
mysql  Ver 14.14 Distrib 5.7.33, for linux-glibc2.12 (x86_64) using  EditLine wrapper

Connection id:		17
Current database:	
Current user:		root@localhost
SSL:			Cipher in use is ECDHE-RSA-AES128-GCM-SHA256
Current pager:		stdout
Using outfile:		''
Using delimiter:	;
Server version:		5.7.33 MySQL Community Server (GPL)
Protocol version:	10
Connection:		127.0.0.1 via TCP/IP
Server characterset:	latin1
Db     characterset:	latin1
Client characterset:	utf8
Conn.  characterset:	utf8
TCP port:		3306
Uptime:			8 hours 16 min 31 sec

Threads: 4  Questions: 448  Slow queries: 0  Opens: 261  Flush tables: 1  Open tables: 254  Queries per second avg: 0.015
--------------
~~~

### 给连接进行一些加密

#### 1、配置mysql进行SSL连接
mysql5.7默认是使用SSL的方式来进行通讯的。
/s输出SSL: Not in use，说明当前没有使用SSL连接。
再看下error.log有一个waning：failed to set up SSL because of the following SSL liberary error：SSL context is not usable withut certificate and private key。公密钥文件不存在，所以无法启用SSL的连接方式。

1、进入bin目录执行命令： mysql_ssl_rsa_setup 在/data 根目录 生成相关的*.pem 密钥文件。
2、对新生成到pem文件授权chown mysql:mysql *.pem
3、 /etc/init.d/mysqld restart 重启mysql
4、进入命令客户端执行\s

~~~
[root@localhost bin]# ./mysql_ssl_rsa_setup
[root@localhost bin]# ll
总用量 1347960
-rwxr-xr-x. 1 mysql mysql   8107712 12月 10 11:23 innochecksum
-rwxr-xr-x. 1 mysql mysql    236710 12月 10 11:23 lz4_decompress
-rwxr-xr-x. 1 mysql mysql  10043637 12月 10 11:24 myisamchk
-rwxr-xr-x. 1 mysql mysql   9588122 12月 10 11:24 myisam_ftdump
-rwxr-xr-x. 1 mysql mysql   7487512 12月 10 11:24 myisamlog
-rwxr-xr-x. 1 mysql mysql   9712786 12月 10 11:24 myisampack
-rwxr-xr-x. 1 mysql mysql   7401199 12月 10 11:23 my_print_defaults
-rwxr-xr-x. 1 mysql mysql  10366606 12月 10 11:24 mysql
-rwxr-xr-x. 1 mysql mysql   9223981 12月 10 11:24 mysqladmin
-rwxr-xr-x. 1 mysql mysql  11195779 12月 10 11:24 mysqlbinlog
-rwxr-xr-x. 1 mysql mysql   9595053 12月 10 11:24 mysqlcheck
-rwxr-xr-x. 1 mysql mysql 219791001 12月 10 11:28 mysql_client_test_embedded
-rwxr-xr-x. 1 mysql mysql      5245 12月 10 11:23 mysql_config
-rwxr-xr-x. 1 mysql mysql   7577740 12月 10 11:23 mysql_config_editor
-rwxr-xr-x. 1 mysql mysql 255061158 12月 10 11:28 mysqld
-rwxr-xr-x. 1 mysql mysql 207729722 12月 10 11:21 mysqld-debug
-rwxr-xr-x. 1 mysql mysql     27139 12月 10 11:23 mysqld_multi
-rwxr-xr-x. 1 mysql mysql     27836 12月 10 11:23 mysqld_safe
-rwxr-xr-x. 1 mysql mysql   9497744 12月 10 11:24 mysqldump
-rwxr-xr-x. 1 mysql mysql      7865 12月 10 11:23 mysqldumpslow
-rwxr-xr-x. 1 mysql mysql 219359082 12月 10 11:28 mysql_embedded
-rwxr-xr-x. 1 mysql mysql   9246562 12月 10 11:24 mysqlimport
-rwxr-xr-x. 1 mysql mysql   9727964 12月 10 11:24 mysql_install_db
-rwxr-xr-x. 1 mysql mysql   7464232 12月 10 11:24 mysql_plugin
-rwxr-xr-x. 1 mysql mysql  17480316 12月 10 11:25 mysqlpump
-rwxr-xr-x. 1 mysql mysql   9175578 12月 10 11:24 mysql_secure_installation
-rwxr-xr-x. 1 mysql mysql   9183463 12月 10 11:24 mysqlshow
-rwxr-xr-x. 1 mysql mysql   9287213 12月 10 11:24 mysqlslap
-rwxr-xr-x. 1 mysql mysql   7785427 12月 10 11:23 mysql_ssl_rsa_setup
-rwxr-xr-x. 1 mysql mysql 218947689 12月 10 11:28 mysqltest_embedded
-rwxr-xr-x. 1 mysql mysql   5109314 12月 10 11:23 mysql_tzinfo_to_sql
-rwxr-xr-x. 1 mysql mysql  12433225 12月 10 11:24 mysql_upgrade
-rwxr-xr-x. 1 mysql mysql  24487998 12月 10 11:24 mysqlxtest
-rwxr-xr-x. 1 mysql mysql   7539954 12月 10 11:23 perror
-rwxr-xr-x. 1 mysql mysql   5326743 12月 10 11:23 replace
-rwxr-xr-x. 1 mysql mysql   7397397 12月 10 11:23 resolveip
-rwxr-xr-x. 1 mysql mysql   7486857 12月 10 11:23 resolve_stack_dump
-rwxr-xr-x. 1 mysql mysql    112339 12月 10 11:23 zlib_decompress
[root@localhost bin]# ./mysql_ssl_rsa_setup 
[root@localhost bin]# cd ..
[root@localhost mysql-5.7.33-linux-glibc2.12-x86_64]# ll
总用量 300
drwxr-xr-x.  2 mysql mysql   4096 4月  18 10:16 bin
drwxr-xr-x.  2 mysql mysql     55 4月  18 10:16 docs
-rw-r-----.  1 mysql mysql  33756 4月  18 11:08 error.log
drwxr-xr-x.  3 mysql mysql   4096 4月  18 10:16 include
drwxr-xr-x.  5 mysql mysql    230 4月  18 10:16 lib
-rw-r--r--.  1 mysql mysql 250129 12月 10 11:01 LICENSE
drwxr-xr-x.  4 mysql mysql     30 4月  18 10:16 man
-rw-r--r--.  1 mysql mysql    566 12月 10 11:01 README
drwxr-xr-x. 28 mysql mysql   4096 4月  18 10:16 share
drwxr-xr-x.  2 mysql mysql     90 4月  18 10:16 support-files
[root@localhost mysql-5.7.33-linux-glibc2.12-x86_64]# cd /mdata/mysql57/
[root@localhost mysql57]# ll
总用量 122988
-rw-r-----. 1 mysql mysql       56 4月  18 10:36 auto.cnf
-rw-------. 1 mysql mysql     1680 4月  18 10:36 ca-key.pem
-rw-r--r--. 1 mysql mysql     1112 4月  18 10:36 ca.pem
-rw-r--r--. 1 mysql mysql     1112 4月  18 10:36 client-cert.pem
-rw-------. 1 mysql mysql     1680 4月  18 10:36 client-key.pem
-rw-r-----. 1 mysql mysql    36046 4月  18 19:33 error.log
-rw-r-----. 1 mysql mysql      325 4月  18 11:20 ib_buffer_pool
-rw-r-----. 1 mysql mysql 12582912 4月  18 11:20 ibdata1
-rw-r-----. 1 mysql mysql 50331648 4月  18 11:20 ib_logfile0
-rw-r-----. 1 mysql mysql 50331648 4月  18 10:36 ib_logfile1
-rw-r-----. 1 mysql mysql 12582912 4月  18 12:37 ibtmp1
-rw-r-----. 1 mysql mysql        6 4月  18 11:20 localhost.localdomain.pid
-rw-r--r--. 1 root  root         0 4月  18 11:20 localhost.localdomain.pid.shutdown
drwxr-x---. 2 mysql mysql     4096 4月  18 10:36 mysql
drwxr-x---. 2 mysql mysql     8192 4月  18 10:36 performance_schema
-rw-------. 1 mysql mysql     1680 4月  18 10:36 private_key.pem
-rw-r--r--. 1 mysql mysql      452 4月  18 10:36 public_key.pem
-rw-r--r--. 1 mysql mysql     1112 4月  18 10:36 server-cert.pem
-rw-------. 1 mysql mysql     1680 4月  18 10:36 server-key.pem
drwxr-x---. 2 mysql mysql     8192 4月  18 10:36 sys
drwx------. 2 mysql mysql        6 4月  18 16:47 test
[root@localhost mysql57]# cd test
[root@localhost test]# cd ..
[root@localhost mysql57]# ll *.pem
-rw-------. 1 mysql mysql 1680 4月  18 10:36 ca-key.pem
-rw-r--r--. 1 mysql mysql 1112 4月  18 10:36 ca.pem
-rw-r--r--. 1 mysql mysql 1112 4月  18 10:36 client-cert.pem
-rw-------. 1 mysql mysql 1680 4月  18 10:36 client-key.pem
-rw-------. 1 mysql mysql 1680 4月  18 10:36 private_key.pem
-rw-r--r--. 1 mysql mysql  452 4月  18 10:36 public_key.pem
-rw-r--r--. 1 mysql mysql 1112 4月  18 10:36 server-cert.pem
-rw-------. 1 mysql mysql 1680 4月  18 10:36 server-key.pem
[root@localhost mysql57]# chown mysql:mysql *.pem
[root@localhost mysql57]# /etc/init.d/mysqld restart
Shutting down MySQL.... SUCCESS! 
Starting MySQL.. SUCCESS! 
[root@localhost mysql57]# mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.33 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(root@localhost) [(none)]>show variables like '%ssl%';
+---------------+-----------------+
| Variable_name | Value           |
+---------------+-----------------+
| have_openssl  | YES             |
| have_ssl      | YES             |
| ssl_ca        | ca.pem          |
| ssl_capath    |                 |
| ssl_cert      | server-cert.pem |
| ssl_cipher    |                 |
| ssl_crl       |                 |
| ssl_crlpath   |                 |
| ssl_key       | server-key.pem  |
+---------------+-----------------+
9 rows in set (0.01 sec)
~~~
>注意：若是使用本地socket连接，则不会进行SSL加密。\s还是输出SSL: Not in use；只有在使用IP/TCP远程连接时才会进行SSL加密。如下：

使用IP/TCP远程连接时，\s输出 SSL: Cipher in use is ECDHE-RSA-AES128-GCM-SHA256。说明已经用上SSL加密。

~~~
[root@localhost bin]# mysql -h127.0.0.1 -uroot -p123456 
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.33 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(root@127.0.0.1) [(none)]>\s
--------------
mysql  Ver 14.14 Distrib 5.7.33, for linux-glibc2.12 (x86_64) using  EditLine wrapper

Connection id:		4
Current database:	
Current user:		root@localhost
SSL:			Cipher in use is ECDHE-RSA-AES128-GCM-SHA256
Current pager:		stdout
Using outfile:		''
Using delimiter:	;
Server version:		5.7.33 MySQL Community Server (GPL)
Protocol version:	10
Connection:		127.0.0.1 via TCP/IP
Server characterset:	latin1
Db     characterset:	latin1
Client characterset:	utf8
Conn.  characterset:	utf8
TCP port:		3306
Uptime:			4 min 18 sec

Threads: 2  Questions: 18  Slow queries: 0  Opens: 106  Flush tables: 1  Open tables: 99  Queries per second avg: 0.069
--------------

~~~

使用socket进行本地连接，就不会使用SSL加密。\s输出SSL: Not in use；
~~~
[root@localhost bin]# mysql 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.33 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(root@localhost) [(none)]>\s
--------------
mysql  Ver 14.14 Distrib 5.7.33, for linux-glibc2.12 (x86_64) using  EditLine wrapper

Connection id:		5
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
UNIX socket:		/tmp/mysql.sock
Uptime:			9 min 34 sec

Threads: 2  Questions: 24  Slow queries: 0  Opens: 106  Flush tables: 1  Open tables: 99  Queries per second avg: 0.041
--------------
~~~

因为SSL开启可能有性能影响。如果不希望使用ssl加密登录连接，那么可以使用下面命令进行禁用：mysql -h127.0.0.1  -uroot -p123456 --ssl-mode=DISABLED
~~~
[root@localhost bin]# mysql -h127.0.0.1  -uroot -p123456 --ssl-mode=DISABLED
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 6
Server version: 5.7.33 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(root@127.0.0.1) [(none)]>\s
--------------
mysql  Ver 14.14 Distrib 5.7.33, for linux-glibc2.12 (x86_64) using  EditLine wrapper

Connection id:		6
Current database:	
Current user:		root@localhost
SSL:			Not in use
Current pager:		stdout
Using outfile:		''
Using delimiter:	;
Server version:		5.7.33 MySQL Community Server (GPL)
Protocol version:	10
Connection:		127.0.0.1 via TCP/IP
Server characterset:	latin1
Db     characterset:	latin1
Client characterset:	utf8
Conn.  characterset:	utf8
TCP port:		3306
Uptime:			22 min 52 sec

Threads: 2  Questions: 30  Slow queries: 0  Opens: 106  Flush tables: 1  Open tables: 99  Queries per second avg: 0.021
--------------
~~~


**强制一个用户使用ssl**
~~~
(root@127.0.0.1) [(none)]>alter user david@'%' require ssl;
Query OK, 0 rows affected (0.03 sec)

(root@127.0.0.1) [(none)]>show grants for david@'%';

~~~

之后david用户就必须使用ssl登录了，否则报错如下：
~~~
[root@localhost ~]# mysql -h127.0.0.1 -udavid -p456 --ssl-mode=DISABLED
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1045 (28000): Access denied for user 'david'@'localhost' (using password: YES)

[root@localhost ~]# mysql  -udavid -p456  -S/tmp/mysql.sock
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1045 (28000): Access denied for user 'david'@'localhost' (using password: YES)
~~~

取消一个用户强制使用ssl
~~~

(root@localhost) [(none)]>alter user david@'%' require none;
Query OK, 0 rows affected (0.00 sec)

(root@localhost) [(none)]>exit;
Bye
[root@localhost ~]# mysql  -udavid -p456  -S/tmp/mysql.sock
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 14
Server version: 5.7.33 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(david@localhost) [(none)]>

~~~


#### 2、给SSL添加x509认证

x509认证在开启SSL的基础下，还强制指定用户必须使用client-cert.pem和client-key.pem证书、密钥文件来登录，否则登录不了。x509是mysql最高等级的认证机制。
~~~
alter user david@'%' require x509;
~~~


之前已经在data根目录生成了8个 *.pem文件
~~~
[root@localhost mysql57]# ll *.pem
-rw-------. 1 mysql mysql 1676 4月  18 20:08 ca-key.pem
-rw-r--r--. 1 mysql mysql 1112 4月  18 20:08 ca.pem
-rw-r--r--. 1 mysql mysql 1112 4月  18 20:08 client-cert.pem
-rw-------. 1 mysql mysql 1676 4月  18 20:08 client-key.pem
-rw-------. 1 mysql mysql 1676 4月  18 20:08 private_key.pem
-rw-r--r--. 1 mysql mysql  452 4月  18 20:08 public_key.pem
-rw-r--r--. 1 mysql mysql 1112 4月  18 20:08 server-cert.pem
-rw-------. 1 mysql mysql 1680 4月  18 20:08 server-key.pem
~~~
把其中client-cert.pem和client-key.pem导出


如下，再使用之前的命令登录。发现登录不了了。
~~~
[root@localhost mysql57]# mysql  -udavid -p456  -S/tmp/mysql.sock
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1045 (28000): Access denied for user 'david'@'localhost' (using password: YES)
~~~

此时想要登录必须在客户端指定SSL CERT File和SSL Key File 如下在navicat中
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a588a59f91c90420.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在mysql workbench中
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1f5eec930ebb97f9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
