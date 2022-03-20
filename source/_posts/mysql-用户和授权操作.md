---
title: mysql-用户和授权操作.md
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
title: mysql-用户和授权操作.md
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
###修改用户的host
mysql安装后默认的root的host是locahost，因此不允许远程访问。所以可以将host改为%允许所有ip。线上服务器为了安全可以将root的host改为应用服务器的ip。
~~~
UPDATE mysql.USER SET HOST = '%' WHERE USER = 'root';
FLUSH PRIVILEGES;
~~~

如果要让本局域网都可以登录，那么可以这样设置
~~~
UPDATE mysql.USER SET HOST = '192.168.0.*' WHERE USER = 'root';
FLUSH PRIVILEGES;
~~~


###mysql5.7修改用户密码
~~~
UPDATE mysql.USER SET authentication_string = PASSWORD ( 'yk123' ) WHERE USER = 'kaikai';
FLUSH PRIVILEGES;
~~~



###创建用户和授权步骤
请使用具有超级管理员权限的root用户进行创建操作。
1、创建用户
~~~
CREATE USER 'yinkai'@'%' IDENTIFIED BY '123456';
~~~
 - yinkai 用户名
- % 允许用户连接的IP地址，%表示运行所有
- 123456 就是密码了


2、给用户授权特定库和特定表

~~~
GRANT ALL ON sp.* TO 'yinkai'@'%';

~~~
 - ALL 权限标识 ; 可以取值ALL，CREATE，DROP，INSERT，UPDATE，SELECT
-  sp.*  库名.表名; 可以取值 *.* 表示所有库所有表
-   'yinkai'@'%'; 用户名和访问host


###给用户授权为超级管理员
该操作需要root用户才能完成，执行完后这个ggg用户就有root用户一样的权限了！可以使用这个ggg用户再去创建用户、授权、甚至再去设置超级管理员
~~~
GRANT ALL PRIVILEGES ON *.* TO 'ggg'@'%' WITH GRANT OPTION
~~~


###查看用户的授权记录
~~~
show grants for 'root'
~~~
> root 用户默认是这个
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION

###免密码登录
mysqld下
~~~
skip-grant-tables
~~~

mysql -u -p

net start mysql
net stop mysql


###mysql连接命令
~~~
mysql -u root -P 3305 -h localhost -p
~~~
