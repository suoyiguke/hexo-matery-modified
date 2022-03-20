---
title: mysql-安装问题.md
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
title: mysql-安装问题.md
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
###为什么推荐使用压缩包安装而不是自己编译安装或者使用yum、apt命令安装？

1、
老师：
不必纠结于这个问题，不相信编译后有什么性能提升，官方的指定的参数是最好的；
有这心思还不如去想想怎么优化一条业务sql。

反方：
指定一些参数，那些不用的功能可以不编译进来。
全内存场景，编译安装出来性能更好。



2、yum安装和apt在线安装都会导致安装目录在哪不清楚的问题


3、推荐安装使用 
MySQL Community Server Linux generic（通用）
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2921f5fe5de9b13c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
使用Compressed 压缩版本
Linux - Generic (glibc 2.12) (x86, 64-bit), Compressed TAR Archive	



###为什么推荐使用centos7来作为mysql服务器
red hat 和cerntos 最多
centos7 对一些软件支持比较好，比如mysql rotuter
centos6.6以上就行
mysql5.7.9有很多bug，复制跑着跑着出错，就看你用得到
用不到那个场景了。最新版本是mysql5.7.32


###安装哪个mysql版本？
mysql版本大小变化如下，容量逐渐增大。mysql的功能逐渐在完善中
5.6 300M 
5.7 600M  
8.0 1000M




###压缩包安装

1、指定配置文件安装服务
~~~
D:\ca\MySQL\mysql-5.7.19-winx64\bin\mysqld.exe install 3305 --defaults-file="D:\ca\MySQL\my.ini"
~~~
2、先初始化数据库
~~~
D:\ca\MySQL\mysql-5.7.19-winx64\bin>mysqld --initialize --datadir=D://ca//MySQL//mysql-5.7.19-winx64//data
~~~
3、然后执行
~~~
D:\ca\MySQL\mysql-5.7.19-winx64\bin>net start 3305
~~~
3305 服务正在启动 .
3305 服务已经启动成功。

###查看mysql自身的错误日志
~~~
mysql\data\xxxx.err
~~~

### Unknown error没有报出详细错误的问题 
需要指定errmsg.sys所在文件夹
~~~
[mysqld]
lc-messages-dir=D:\\ca\\MySQL\\mysql-5.7.19-winx64\\share\\english
~~~



###安装完毕后需要使用默认密码登录，然后修改密码

mysql> use mysql;
ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.
修改密码
~~~
alter user user() identified by "Sgl20@14";
刷新权限：flush privileges;
~~~

###另一种修改密码

~~~
选择数据库：use mysql;

更新root的密码：update user set authentication_string=password('Sgl20@14') where user='root' and Host='localhost';

刷新权限：flush privileges;
~~~


###记住：mysql的server_id不可以随便修改
否则容易启动不了mysql服务。我遇到过将server_id从2修改为ip，然后启动不了服务。总是报: mysqld.pid的错误


###skip-grant-tables
skip-grant-tables

###mysql8安装

~~~
G:\mysql\mysql-8.0.22-winx64\bin>G:\mysql\mysql-8.0.22-winx64\bin\mysqld.exe install 666 --defaults-file="G:\mysql\mysql
-8.0.22-winx64\my.ini"
Service successfully installed.

G:\mysql\mysql-8.0.22-winx64\bin>G:\mysql\mysql-8.0.22-winx64\bin\mysqld.exe --initialize

G:\mysql\mysql-8.0.22-winx64\bin>net start 666
666 服务正在启动 .....
~~~






MySql 从8.0开始修改密码有了变化，在user表加了字段authentication_string，修改密码前先检查authentication_string是否为空

1、如果不为空
~~~
use mysql; 
 -- 将字段置为空
update user set authentication_string='' where user='root';
 -- 修改密码
ALTER user 'root'@'localhost' IDENTIFIED BY 'Sgl20@14';
~~~
2、如果为空，直接修改
~~~
ALTER user 'root'@'localhost' IDENTIFIED BY 'root';--修改密码为root
如果出现如下错误

ERROR 1290 (HY000): The MySQL server is running with the --skip-grant-tables option so it cannot execute this statement
mysql> GRANT ALL PRIVILEGES ON *.* TO IDENTIFIED BY '123' WITH GRANT OPTION;
 

需要执行

flush privileges;
然后再执行

ALTER user 'root'@'localhost' IDENTIFIED BY 'root';--修改密码为root
~~~

###命令方式连接
~~~
mysql  -P 666 -u root
~~~


~~~
use mysql;
flush privileges;
-- mysql8 以后认证插件是caching_sha2_password，如果还像继续使用之前的就需要配置  default_authentication_plugin=mysql_native_password
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'Sgl20@14';
flush privileges;
~~~
