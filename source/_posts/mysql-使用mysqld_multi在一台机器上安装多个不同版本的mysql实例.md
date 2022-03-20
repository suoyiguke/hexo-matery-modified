---
title: mysql-使用mysqld_multi在一台机器上安装多个不同版本的mysql实例.md
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
title: mysql-使用mysqld_multi在一台机器上安装多个不同版本的mysql实例.md
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
>本篇在上篇文章https://www.jianshu.com/p/88adb36bbca9基础上继续演示，如何使用mysqld_multi做到在一台机器上安装不同版本的mysql实例。

###增加5.6版本实例
1、对5.6的mysql目录进行授权。
~~~
chown -R mysql:mysql mysql-5.6.51-linux-glibc2.12-x86_64
~~~
2、初始化mysql5.6。
~~~
./scripts/mysql_install_db --user=mysql --datadir=/mdata/mysql56-3309
~~~
>注意： 5.6的初始化数据命令和 5.7、8.0的不同。5.6使用的是scripts，5.7/8.0 使用mysqld --initialize。


3、my.cnf配置。如果要使用mysqld_multi同时安装5.6和5.7的话。在之前已经安装了mysqld3306、mysqld3307、mysqld3308、mysqld3309 4个5.7实例的基础上再加上一个5.6版本的mysqld563309实例：

新配置的[mysqld563309]内增加了一个`basedir=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64`的配置。因为[mysqld]的basedir值为/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64，指向了5.7版本，故[mysqld563309]中必须要显式指定5.6的basedir，否则默认继承了5.7的basedir。

~~~
[mysqld]
user = mysql
basedir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64
log_error=error.log
plugin-load=validate_password.so
port=3305
datadir=/mdata/mysql57
socket= /tmp/mysql.sock3305
server-id=10
innodb_buffer_pool_size = 32M

[mysqld_multi]
mysqld=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld_safe
mysqladmin=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqladmin
log=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/mysqld_multi.log


[mysqld3306]
server-id=11
port=3306
datadir=/mdata/mysql57-3306
socket= /tmp/mysql.sock3306
innodb_buffer_pool_size = 32M


[mysqld3307]
server-id=12
port=3307
datadir=/mdata/mysql57-3307
socket= /tmp/mysql.sock3307
innodb_buffer_pool_size = 32M

[mysqld3308]
server-id=13
port=3308
datadir=/mdata/mysql57-3308
socket= /tmp/mysql.sock3308
innodb_buffer_pool_size = 32M

[mysqld563309]
server-id=14
port=3309
datadir=/mdata/mysql56-3309
socket= /tmp/mysql.sock3309
basedir=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64
innodb_buffer_pool_size = 32M

[client]
socket= /tmp/mysql.sock3306
user=root
password=1111aaA_
~~~



4、使用mysqld_multi 启动mysql5.6实例，如下/mysqld_multi report 563309 命令得到了mysqld563309 is running的结果。mysql 5.6,5.7  混合的多实例安装成功。
~~~
[root@localhost bin]# ./mysqld_multi start 563309
[root@localhost bin]# ./mysqld_multi report 563309
Reporting MySQL servers
MySQL server from group: mysqld563309 is running
[root@localhost bin]# 
~~~


5、我们可以通过ps -ef |grep mysql来查看下进程信息：
值得注意的是此时使用的mysqld_safe使用的是5.7的mysqld_safe。但是呢运行的mysqld只能是5.6版本的了。
~~~
[root@localhost ~]# ps -ef |grep mysql
root      18720      1  0 12:48 pts/2    00:00:00 /bin/sh /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld_safe --server-id=14 --port=3309 --datadir=/mdata/mysql56-3309 --socket=/tmp/mysql.sock3309 --basedir=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64 --innodb_buffer_pool_size=32M
mysql     18992  18720  0 12:48 pts/2    00:00:00 /home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/bin/mysqld --basedir=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64 --datadir=/mdata/mysql56-3309 --plugin-dir=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/lib/plugin --user=mysql --server-id=14 --innodb-buffer-pool-size=32M --log-error=error.log --pid-file=localhost.localdomain.pid --socket=/tmp/mysql.sock3309 --port=3309
~~~

当然我们也可以给[mysqld563309]节点配置mysqld和mysqladmin，让mysql5.6使用自己版本的。`其实是没有必要的5.7版本的mysqld_safe可以兼容5.6版本`。
~~~
[mysqld563309]
server-id=14
port=3309
datadir=/mdata/mysql56-3309
socket= /tmp/mysql.sock3309
basedir=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64
innodb_buffer_pool_size = 32M
mysqld=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/bin/mysqld_safe
mysqladmin=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/bin/mysqladmin
~~~

如下，再次查看进程信息，mysqld_safe 已经使用了5.6的版本。
~~~
[root@localhost bin]# ps -ef |grep mysql
root      20611      1  0 13:15 pts/4    00:00:00 /bin/sh /home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/bin/mysqld_safe --server-id=14 --port=3309 --datadir=/mdata/mysql56-3309 --socket=/tmp/mysql.sock3309 --basedir=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64 --innodb_buffer_pool_size=32M
mysql     20883  20611  0 13:15 pts/4    00:00:00 /home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/bin/mysqld --basedir=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64 --datadir=/mdata/mysql56-3309 --plugin-dir=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/lib/plugin --user=mysql --server-id=14 --innodb-buffer-pool-size=32M --log-error=error.log --pid-file=localhost.localdomain.pid --socket=/tmp/mysql.sock3309 --port=3309
root      20978  14941  0 13:16 pts/4    00:00:00 grep --color=auto mysql
~~~

###增加8.0版本实例
对8.0的mysql目录进行授权。
~~~
chown -R mysql:mysql mysql-8.0.24-linux-glibc2.12-x86_64
~~~
初始化8.0版本的数据到/mdata/mysql80-3310下，命令和5.7的一致：
~~~
./bin/mysqld --initialize --user=mysql --datadir=/mdata/mysql80-3310
~~~
my.cnf配置，在上面的基础上再加上一个[mysqld563309]节点，具体配置和上面加的[mysqld563309]配置大同小异。基本拿过来改下路径和端口、socket就行了。
~~~
[mysqld]
user = mysql
basedir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64
log_error=error.log
plugin-load=validate_password.so
port=3305
datadir=/mdata/mysql57
socket= /tmp/mysql.sock3305
server-id=10
innodb_buffer_pool_size = 32M

[mysqld_multi]
mysqld=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld_safe
mysqladmin=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqladmin
log=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/mysqld_multi.log


[mysqld3306]
server-id=11
port=3306
datadir=/mdata/mysql57-3306
socket= /tmp/mysql.sock3306
innodb_buffer_pool_size = 32M


[mysqld3307]
server-id=12
port=3307
datadir=/mdata/mysql57-3307
socket= /tmp/mysql.sock3307
innodb_buffer_pool_size = 32M

[mysqld3308]
server-id=13
port=3308
datadir=/mdata/mysql57-3308
socket= /tmp/mysql.sock3308
innodb_buffer_pool_size = 32M

[mysqld563309]
server-id=14
port=3309
datadir=/mdata/mysql56-3309
socket= /tmp/mysql.sock3309
basedir=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64
innodb_buffer_pool_size = 32M
mysqld=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/bin/mysqld_safe
mysqladmin=/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/bin/mysqladmin

[mysqld803310]
server-id=15
port=3310
datadir=/mdata/mysql80-3310
socket= /tmp/mysql.sock3310
basedir=/home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64
innodb_buffer_pool_size = 32M
mysqld=/home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64/bin/mysqld_safe
mysqladmin=/home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64/bin/mysqladmin

[client]
socket= /tmp/mysql.sock3306
user=root
password=1111aaA_

[mysql]
prompt=(\\u@\\h) [\\d]>\\
~~~


通过mysqld_multi 启动和停止新创建的mysql8.0实例 [mysqld803310] 如下：
~~~
[root@localhost bin]# ./mysqld_multi start 803310
[root@localhost bin]# ./mysqld_multi report 803310
Reporting MySQL servers
MySQL server from group: mysqld803310 is running
[root@localhost bin]# ps -ef |grep  mysql
root       7760      1  1 16:26 pts/3    00:00:00 /bin/sh /home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64/bin/mysqld_safe --server-id=15 --port=3310 --datadir=/mdata/mysql80-3310 --socket=/tmp/mysql.sock3310 --basedir=/home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64 --innodb_buffer_pool_size=32M
mysql      8019   7760 25 16:26 pts/3    00:00:01 /home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64/bin/mysqld --basedir=/home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64 --datadir=/mdata/mysql80-3310 --plugin-dir=/home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64/lib/plugin --user=mysql --server-id=15 --innodb-buffer-pool-size=32M --log-error=error.log --pid-file=localhost.localdomain.pid --socket=/tmp/mysql.sock3310 --port=3310
root       8071   7708  0 16:26 pts/3    00:00:00 grep --color=auto mysql
[root@localhost bin]# ./mysqld_multi stop 803310
[root@localhost bin]# ps -ef |grep  mysql
root       7760      1  0 16:26 pts/3    00:00:00 /bin/sh /home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64/bin/mysqld_safe --server-id=15 --port=3310 --datadir=/mdata/mysql80-3310 --socket=/tmp/mysql.sock3310 --basedir=/home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64 --innodb_buffer_pool_size=32M
mysql      8019   7760  0 16:26 pts/3    00:00:03 /home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64/bin/mysqld --basedir=/home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64 --datadir=/mdata/mysql80-3310 --plugin-dir=/home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64/lib/plugin --user=mysql --server-id=15 --innodb-buffer-pool-size=32M --log-error=error.log --pid-file=localhost.localdomain.pid --socket=/tmp/mysql.sock3310 --port=3310
root       8112   8082  0 16:29 pts/4    00:00:00 mysql -S /tmp/mysql.sock3310
root       8153      1  0 16:35 pts/3    00:00:00 /home/mysql8.0/mysql-8.0.24-linux-glibc2.12-x86_64/bin/mysqladmin -u root --port=3310 --socket=/tmp/mysql.sock3310 shutdown
root       8156   7708  0 16:35 pts/3    00:00:00 grep --color=auto mysql
[root@localhost bin]# ./mysqld_multi report 803310
Reporting MySQL servers
MySQL server from group: mysqld803310 is not running
[root@localhost bin]# ps -ef |grep  mysql
root       8112   8082  0 16:29 pts/4    00:00:00 mysql -S /tmp/mysql.sock3310
root       8170   7708  0 16:35 pts/3    00:00:00 grep --color=auto mysql
~~~
