---
title: mysql-几种启动和关闭mysql方法介绍.md
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
title: mysql-几种启动和关闭mysql方法介绍.md
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
https://dev.mysql.com/doc/refman/5.7/en/programs-server.html

###mysql几种启动方法

方法1、mysqld
mysqld指定读取my.cnf配置文件启动，加一个 & 实现后台启动。终端不会被阻塞
~~~
./mysqld --defaults-file=/etc/my.cnf &
~~~

方法2、mysqld_safe
~~~
  ./mysqld_safe –defaults-file=/etc/my.cnf  & 
~~~

方法3、mysql.server 
将support-files/mysql.server 脚本做成一个linux服务。使用服务的方式启动
~~~
cp -v /usr/local/mysql/support-files/mysql.server /etc/init.d/ 
chkconfig –add mysql.server 
service mysql.server {start|stop|restart|reload|force-reload|status} 
~~~
方法4、./etc/init.d/mysqld start

这种方式其实和support-files一样。不过更清晰点，我比较喜欢用这个。

方法5、mysqld_multi 
mysqld_multi 主要用来多实例启动的。见 https://www.jianshu.com/p/88adb36bbca9


###mysqld和mysqld_safe启动有什么区别？
1、使用file命令分别查看mysqld和mysqld_safe两个执行文件。可见
mysqld是一个64位的 dynamically linked ；
mysqld_safe 是一个shell script；shell脚本。可以直接编辑的。
~~~
[root@localhost bin]# file mysqld
mysqld: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.18, BuildID[sha1]=e1d1f6fd34afae9ac33181c12d605976c81cc6e1, not stripped
[root@localhost bin]# file mysqld_safe 
mysqld_safe: POSIX shell script, ASCII text executable
~~~


2、使用ps-ef查看下二者区别
mysqld
~~~
[root@localhost bin]# ps -ef |grep mysql
mysql      9294   8364 12 11:12 pts/2    00:00:00 ./mysqld --defaults-file=/etc/my.cnf
~~~
mysqld_safe
~~~
[root@localhost ~]# ps -ef |grep mysql
root       9399   8364  0 11:13 pts/2    00:00:00 /bin/sh ./mysqld_safe --defaults-file=/etc/my.cnf
mysql      9555   9399  2 11:13 pts/2    00:00:00 /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld --defaults-file=/etc/my.cnf --basedir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64 --datadir=/mdata/mysql57 --plugin-dir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/lib/plugin --user=mysql --log-error=error.log --pid-file=localhost.localdomain.pid --socket=/tmp/mysql.sock3
~~~

>mysqld_safe命令启动的方式要比mysqld启动多了一个`mysqld_safe `的进程；mysqld_safe 其实就是mysqld服务的一个守护进程；它的作用是当mysql宕机后会自动重启mysqld服务。所以平时应该使用mysqld_safe。

如下我手动kill掉9555这个mysql进程，随后再次执行ps -ef |grep mysql 发现又生成了一个pid为9918 的mysql进程。
~~~
[root@localhost ~]# kill -9 9555
[root@localhost ~]# ps -ef |grep mysql
root       9399   8364  0 11:13 pts/2    00:00:00 /bin/sh ./mysqld_safe --defaults-file=/etc/my.cnf
mysql      9918   9399  8 11:19 pts/2    00:00:00 /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld --defaults-file=/etc/my.cnf --basedir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64 --datadir=/mdata/mysql57 --plugin-dir=/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/lib/plugin --user=mysql --log-error=error.log --pid-file=localhost.localdomain.pid --socket=/tmp/mysql.sock3305 --port=3305
root       9950   8476  0 11:19 pts/3    00:00:00 grep --color=auto mysql
~~~







### mysql几种关闭方法
`mysql终端使用，需要密码` 方法1、进入mysql终端执行shutdown命令可以关闭mysql服务
~~~
[root@localhost bin]# mysql -S /tmp/mysql.sock3305 -p123456
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.33 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

(root@localhost) [(none)]>shutdown;
Query OK, 0 rows affected (0.00 sec)

(root@localhost) [(none)]>show variables like '%port%';
ERROR 2006 (HY000): MySQL server has gone away
No connection. Trying to reconnect...
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock3305' (2)
ERROR: 
Can't connect to the server

(root@not_connected) [(none)]>exit;
Bye
[root@localhost bin]# 

~~~

`mysql终端使用，需要密码` 方法2、在mysql终端关闭mysql的另一种命令：
mysqladmin可以做到在mysql终端无需真正登录进去就可stop mysql server
~~~
[root@localhost bin]# ./mysqladmin -uroot -p1111aaA_ -S /tmp/mysql.sock3305 shutdown
mysqladmin: [Warning] Using a password on the command line interface can be insecure.
~~~

`在部署mysql的服务器上使用，不需要密码` 方法3、./support-files/mysql.server stop
使用file命令查看下
~~~
[root@localhost ~]# file /home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/support-files/mysql.server
/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/support-files/mysql.server: POSIX shell script, ASCII text executable
~~~
mysql.server 是一个 shell script。那么我们查看一下它:
~~~
....
 'stop')
    # Stop daemon. We use a signal here to avoid having to know the
    # root password.

    if test -s "$mysqld_pid_file_path"
    then
      # signal mysqld_safe that it needs to stop
      touch "$mysqld_pid_file_path.shutdown"

      mysqld_pid=`cat "$mysqld_pid_file_path"`

      if (kill -0 $mysqld_pid 2>/dev/null)
      then
        echo $echo_n "Shutting down MySQL"
        kill $mysqld_pid
        # mysqld should remove the pid file when it exits, so wait for it.
        wait_for_pid removed "$mysqld_pid" "$mysqld_pid_file_path"; return_value=$?
      else
        log_failure_msg "MySQL server process #$mysqld_pid is not running!"
        rm "$mysqld_pid_file_path"
      fi

      # Delete lock for RedHat / SuSE
      if test -f "$lock_file_path"
      then
        rm -f "$lock_file_path"
      fi
      exit $return_value
    else
      log_failure_msg "MySQL server PID file could not be found!"
    fi
    ;;
...
~~~
可见，mysql.server stop使用`kill -0 pid` 来实现关闭的。
利用了linux中的一个`信号机制`。kill -9 表示强制关闭。若使用的是kill -0 表示发生一个信号给进程，若应用程序中有负责接收处理信号的话，就会走正常关闭的代码流程。故linux的kill -0 命令在mysql中是一个正常的安全关闭。可以做到不需要密码也可以把mysql关闭。

>请使用`kill -0 pid` 来关闭mysql而不是kill -9 pid
