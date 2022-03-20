---
title: mysql-基于docker的安装和配置.md
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
title: mysql-基于docker的安装和配置.md
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
######docker-compose安装mysql
~~~
version: "2"
services:
  mysql:
   image: "docker.io/mysql:5.7"
   environment:
     - "MYSQL_ROOT_PASSWORD=rUK9GDkzmdP9gFa4mysql"
     - "MYSQL_DATABASE=test"
   volumes:
     - "./data:/var/lib/mysql"
     - "./my.cnf:/etc/mysql/my.cnf"
   ports:
     - "3307:3306"
   restart: always

~~~

######my.cnf
~~~
[client]
port=3306
default-character-set = utf8mb4
[mysql]
default-character-set=utf8mb4
[mysqld]
port=3306
character_set_filesystem = utf8mb4
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
init_connect='SET NAMES utf8mb4'
lower_case_table_names=1
sql_mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER"
~~~

###修改root密码和授权生效
- 修改密码
将root的密码设为root
~~~
update mysql.user set authentication_string=password('root') where user='root' ;
~~~
- 授权远程访问
~~~
grant all privileges on *.* to 'root'@'%' identified by 'root' with grant option;
~~~
- 刷新生效
~~~
flush privileges;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-73ed625d702314f0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######windows中mysql配置 my.ini

~~~
[client]
port=3306
default-character-set = utf8mb4

[mysql]
default-character-set=utf8mb4

[mysqld]

port=3306

#匿名登录，需要修改密码时可以打开
#skip-grant-tables


character_set_filesystem = utf8mb4
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
init_connect='SET NAMES utf8mb4'


#解压目录

basedir=G:\mysql\mysql-5.7.22-winx64

#解压目录下data目录

datadir=G:\mysql\mysql-5.7.22-winx64\data

 

sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES

#全部sql语句都查询到
general_log=ON
general_log_file=G:\mysql\mysql-5.7.22-winx64\data\mysql.log


#开启二进制日志
server_id=1918
log_bin = mysql-bin
binlog_format = ROW
~~~
