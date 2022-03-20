---
title: mysql5-6、5-7、8-0-在linux下的安装配置.md
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
title: mysql5-6、5-7、8-0-在linux下的安装配置.md
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
###安装前准备
1、先卸载自带的
有很多linux系统自带安装了mysql，但是并不是我们需要的，所以我们先得将他们卸载干净。
~~~
rpm -qa | grep mysql
rpm -e --nodeps mysql-libs-5.1.73-5.el6_6.x86_64
~~~

2、find / -name mysql找到一下路径，逐个删除之。特别是其它多余的my.cnf文件都要删除！否则的可能影响mysql运行时读取配置。
~~~
[root@localhost mysql-5.7.31-linux-glibc2.12-x86_64]#
/etc/selinux/targeted/active/modules/100/mysql
/var/lib/mysql
/usr/bin/mysql
/usr/lib64/mysql
/usr/lib64/perl5/vendor_perl/auto/DBD/mysql
/usr/lib64/perl5/vendor_perl/DBD/mysql
/usr/share/mysql
~~~

###mysql5.7安装
https://dev.mysql.com/doc/refman/5.7/en/binary-installation.html

~~~
shell> groupadd mysql
shell> useradd -r -g mysql -s /bin/false mysql
shell> cd /usr/local
shell> tar zxvf /path/to/mysql-VERSION-OS.tar.gz
shell> ln -s full-path-to-mysql-VERSION-OS mysql
shell> cd mysql
shell> mkdir mysql-files
shell> chown mysql:mysql mysql-files
shell> chmod 750 mysql-files
shell> bin/mysqld --initialize --user=mysql
shell> bin/mysql_ssl_rsa_setup
shell> bin/mysqld_safe --user=mysql &
# Next command is optional
shell> cp support-files/mysql.server /etc/init.d/mysql.server
~~~

1、创建linux用户组`重要` 
linux里需要使用support-files脚本启动，这个脚本里指定了mysql用户组所以必须进行这一步的操作！下面的报 pid、log文件不能update的问题。创建文件后，执行这个步骤授权后再重启即可解决！
~~~
groupadd mysql
useradd -r -g mysql mysql
~~~
2、给mysql安装目录授权
~~~
chown -R mysql:mysql /soft/mysql-5.7.31-linux-glibc2.12-x86_64
~~~
3、配置文件 vi /etc/my.cnf
- basedir指定mysql安装目录。
- datadir指定mysql的数据目录，这个最好指定到单独挂载的磁盘上。切记不要直接放到mysql安装根目录下，这不是一个好习惯！因为mysql可能需要升级，而data目录其实不需要动的，如果这个时候你放到mysql安装根目录下会很麻烦。
- socket 使用本地socket登录mysql时会用到这个。
- log-error指定错误日志路径，不配置默认使用系统主机名，最好配置为error.log，这样会更直观些。记住：初始化和启动日志也会打印到这个文件里，如果安装启动有问题请来查看这个文件以便获得更多信息定位问题。
- user=mysql指定启动mysqld程序的用户是mysql，指的是运行mysqld进程用户名，这个是可变的，不一定非要是mysql，设置这个用户以后，所有通过mysqld进程创建的文件都会属于这个用户。注意这个指linux系统的用户而非mysql用户，它的值请不要直接设置为超级用户root，因为存在一些安全隐患。详见官方文档https://dev.mysql.com/doc/refman/5.7/en/server-options.html#option_mysqld_user。

~~~
[mysqld]
basedir=/data/mysql/mysql-5.7.31-linux-glibc2.12-x86_64
datadir=/mdata
port = 3306
socket=/tmp/mysql.sock
log-error=error.log
user = mysql
~~~


4、初始化mysql元数据（基础用户表权限表等等）
./mysqld --initialize 会去读取my.cnf找到数据目录datadir指定路径，然后写入元数据文件。因为设置了--user=mysql则会以mysql这个系统用户的身份去创建。



~~~
./mysqld --defaults-file=/etc/my.cnf --initialize --user=mysql
~~~

生成文件如下：注意属于mysql mysql而不是root root。若不指定--user=mysql且mysql.cnf的[mysql]节点下也没配置user=mysql那么就会是root root了。
~~~
[root@localhost mdata]# cd mysql57
[root@localhost mysql57]# ll
总用量 123312
-rw-r-----. 1 mysql mysql       56 4月  18 10:36 auto.cnf
-rw-------. 1 mysql mysql     1676 4月  18 20:08 ca-key.pem
-rw-r--r--. 1 mysql mysql     1112 4月  18 20:08 ca.pem
-rw-r--r--. 1 mysql mysql     1112 4月  18 20:08 client-cert.pem
-rw-------. 1 mysql mysql     1676 4月  18 20:08 client-key.pem
-rw-r-----. 1 mysql mysql   362670 5月   5 16:00 error.log
-rw-r-----. 1 mysql mysql      282 5月   3 12:09 ib_buffer_pool
-rw-r-----. 1 mysql mysql 12582912 5月   5 16:00 ibdata1
-rw-r-----. 1 mysql mysql 50331648 5月   5 16:00 ib_logfile0
-rw-r-----. 1 mysql mysql 50331648 4月  18 10:36 ib_logfile1
-rw-r-----. 1 mysql mysql 12582912 5月   5 16:00 ibtmp1
-rw-r-----. 1 mysql mysql        5 5月   5 16:00 localhost.localdomain.pid
drwxr-x---. 2 mysql mysql     4096 4月  18 10:36 mysql
drwxr-x---. 2 mysql mysql     8192 4月  18 10:36 performance_schema
-rw-------. 1 mysql mysql     1676 4月  18 20:08 private_key.pem
-rw-r--r--. 1 mysql mysql      452 4月  18 20:08 public_key.pem
-rw-r--r--. 1 mysql mysql     1112 4月  18 20:08 server-cert.pem
-rw-------. 1 mysql mysql     1680 4月  18 20:08 server-key.pem
drwxr-x---. 2 mysql mysql     8192 4月  18 10:36 sys
drwx------. 2 mysql mysql        6 4月  18 16:47 test
~~~

>注意 1、这里最好请使用`--initialize` 而不是 `--initialize-insecure`，否则初始化时会生成空密码。
2、--defaults-file=/etc/my.cnf 是默认的，可以省略。


5、找到初始化生成的root默认密码
初始化使用`--initialize`会自己生成密码，查看`log-error`日志可以得到：
2020-09-28T01:17:31.046045Z 1 [Note] A temporary password is generated for root@localhost: aQdu6?5u?.,!
所以初始化密码aQdu6?5u?.,! 就是初始化生成的root密码。



6、启动mysql
~~~
support-files/mysql.server start 
~~~
当然我们还可以使用其它方式启动，/mysqld_safe 等。具体看这里 https://www.jianshu.com/p/a5f24d0f736e。


7、用root身份登录mysql

~~~
mysql -P3306 -uroot -paQdu6?5u?.,!
~~~
这只是使用TPC/IP连接方式，我们还可以使用sock方式，具体见 https://www.jianshu.com/p/0b1f88a6c359。


###mysql8.0安装
8.0和5.7安装步骤差不多。https://dev.mysql.com/doc/refman/8.0/en/binary-installation.html
~~~
shell> groupadd mysql
shell> useradd -r -g mysql -s /bin/false mysql
shell> cd /usr/local
shell> tar xvf /path/to/mysql-VERSION-OS.tar.xz
shell> ln -s full-path-to-mysql-VERSION-OS mysql
shell> cd mysql
shell> mkdir mysql-files
shell> chown mysql:mysql mysql-files
shell> chmod 750 mysql-files
shell> bin/mysqld --initialize --user=mysql
shell> bin/mysql_ssl_rsa_setup
shell> bin/mysqld_safe --user=mysql &
# Next command is optional
shell> cp support-files/mysql.server /etc/init.d/mysql.server
~~~

###mysql5.6安装

https://dev.mysql.com/doc/refman/5.6/en/binary-installation.html
~~~
shell> groupadd mysql
shell> useradd -r -g mysql -s /bin/false mysql
shell> cd /usr/local
shell> tar zxvf /path/to/mysql-VERSION-OS.tar.gz
shell> ln -s full-path-to-mysql-VERSION-OS mysql
shell> cd mysql
shell> scripts/mysql_install_db --user=mysql
shell> bin/mysqld_safe --user=mysql &
# Next command is optional
shell> cp support-files/mysql.server /etc/init.d/mysql.server
~~~

5.6和5.7/8.0版本安装主要不同在于初始化元数据文件那个步骤。5.6使用命令：
~~~
./scripts/mysql_install_db --user=mysql --datadir=/mdata/mysql56-3309
~~~


###后续操作

1、在root下修改密码可以这样指定具体用户设置相应密码：
~~~
mysql> flush privileges;
Query OK, 0 rows affected (0.01 sec)
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';
Query OK, 0 rows affected (0.00 sec)
mysql> flush privileges;
Query OK, 0 rows affected (0.01 sec)
~~~

在当前用户下修改密码就更简单了：
~~~
set password = '123456';
~~~
5.6需要加password函数
~~~
(root@localhost) [(none)]>set password= password('1111aaA_');
~~~

2、将mysql注册为服务
~~~
cd support-files/
cp mysql.server /etc/init.d/mysqld
chkconfig --add mysqld
~~~

随后就可以这样开启或固关闭mysql服务：
~~~
service mysqld stop
service mysqld start
~~~

3、将mysql服务设置为开机启动
~~~
chkconfig --level 345 mysqld on
~~~


4、开启远程访问
~~~
 update user set host='%' where user='root';
 flush privileges;
~~~

5、忽略密码登录
要是忘记密码了，或者初始化使用了`--initialize-insecure`而不是`--initialize`导致生成了空密码。则我们可以这样操作：my.cnf添加如下
~~~
[mysqld]
skip-grant-tables
~~~
重启mysql后便可以直接登录了。

6、安装完启动后且建立各种表、导入各种数据。project运行可能报各种表、列找不到。极大可能是因为linux下文件名区分大小写，这导致mysql的表名、列名都是区分大小写的。所以我们加上以下配置后重启mysql就可以解决。
~~~
[mysqld]
lower_case_table_names=1
~~~

7、bash: mysql: 未找到命令，要使用mysql命令，需要先创建bin下的mysql程序软链：

~~~
ln -fs /soft/mysql-5.7.31-linux-glibc2.12-x86_64/bin/mysql /usr/bin
~~~
>注意：这里需要使用绝对路径！

8、pid报错，这个问题按照我的经验，是因为没有chmod授权data目录的原因。
~~~
[root@localhost mysql-5.7.31-linux-glibc2.12-x86_64]# support-files/mysql.server start
Starting MySQL.Logging to '/soft/mysql-5.7.31-linux-glibc2.12-x86_6/data/localhost.localdomain.err'.
 ERROR! The server quit without updating PID file (/soft/mysql-5.7.31-linux-glibc2.12-x86_6/data/localhost.localdomain.pid).

chmod 777 -R mysql
~~~


9、强制要求使用ssl加密连接和X509认证
详见 https://www.jianshu.com/p/0b1f88a6c359

10、使用密码插件让mysql强制规范mysql密码
详见 https://www.jianshu.com/p/9df7cb085a21

11、mysql怎么快速升级？

12、8.0使用navicat连接不了报错Authentication plugin 'caching_sha2_password' cannot be loaded。解决：
修改密码规则，还是使用老版本的。或者升级navicat驱动
~~~
mysql> update user set host ='%' where user = 'root'
    -> ;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> flush privileges;
Query OK, 0 rows affected (0.01 sec)

mysql>  ALTER USER 'root'@'%' IDENTIFIED BY '123456' PASSWORD EXPIRE NEVER;
Query OK, 0 rows affected (0.01 sec)

mysql> ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
Query OK, 0 rows affected (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)


~~~


###5.6、5.7、8.0的安装的其它差异

1、mysql5.6有的root用户空密码，还有没有用户名的用户
mysql
~~~(root@localhost) [(none)]>select user,host ,Password from mysql.user;
+------+-----------------------+-------------------------------------------+
| user | host                  | Password                                  |
+------+-----------------------+-------------------------------------------+
| root | localhost             | *EA62E958B9341EBAC96A56A6AA6D47637ED3DFD3 |
| root | localhost.localdomain |                                           |
| root | 127.0.0.1             |                                           |
| root | ::1                   |                                           |
|      | localhost             |                                           |
|      | localhost.localdomain |                                           |
+------+-----------------------+-------------------------------------------+
~~~
这些用户要删除；
@localhost、@localhost.localdomain
~~~
delete from mysql.user where user='';
~~~

空密码的root用户要修改密码。
root@localhost、root@localhost.localdomain、root@127.0.0.1、root@::1
~~~
UPDATE user SET password=PASSWORD("*****") WHERE user='root'; #修改root密码。
~~~



2、5.6 root用户密码是空的。密码要改掉。
2、5.6有test库，5.7以后test已经删除
