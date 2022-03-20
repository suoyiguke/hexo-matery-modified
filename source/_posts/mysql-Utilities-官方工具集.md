---
title: mysql-Utilities-官方工具集.md
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
title: mysql-Utilities-官方工具集.md
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
现在主流使用procona tools ，官方的用的少了。

###安装mysql Utilities
1、下载
https://downloads.mysql.com/archives/utilities/
2、安装 python setup.py install
~~~
-rw-r--r--. 1 root root  668241 5月   9 18:35 mysql-utilities-1.6.5.tar.gz
[root@localhost home]# cd mysql-utilities-1.6.5
[root@localhost mysql-utilities-1.6.5]# ll
总用量 132
-rw-r--r--. 1 7161 31415 37814 1月  18 2017 CHANGES.txt
drwxr-xr-x. 3 7161 31415    17 1月  18 2017 docs
-rw-r--r--. 1 7161 31415  6680 1月  18 2017 info.py
-rw-r--r--. 1 7161 31415 17987 1月  18 2017 LICENSE.txt
drwxr-xr-x. 4 7161 31415    59 1月  18 2017 mysql
-rw-r--r--. 1 7161 31415   928 1月  18 2017 PKG-INFO
-rw-r--r--. 1 7161 31415 34819 1月  18 2017 README.txt
drwxr-xr-x. 2 7161 31415  4096 1月  18 2017 scripts
-rw-r--r--. 1 7161 31415 14232 1月  18 2017 setup.py
drwxr-xr-x. 2 7161 31415  4096 1月  18 2017 unit_tests
[root@localhost mysql-utilities-1.6.5]# python setup.py install
~~~

3、查看工具集合
~~~
copying build/scripts-2.7/mysqldbimport -> /usr/bin
copying build/scripts-2.7/mysqlbinlogpurge -> /usr/bin
copying build/scripts-2.7/mysqlfrm -> /usr/bin
copying build/scripts-2.7/mysqlserverclone -> /usr/bin
copying build/scripts-2.7/mysqlindexcheck -> /usr/bin
copying build/scripts-2.7/mysqldiff -> /usr/bin
copying build/scripts-2.7/mysqlbinlogrotate -> /usr/bin
copying build/scripts-2.7/mysqlrpladmin -> /usr/bin
copying build/scripts-2.7/mysqlgrants -> /usr/bin
copying build/scripts-2.7/mysqlrplcheck -> /usr/bin
copying build/scripts-2.7/mysqlprocgrep -> /usr/bin
copying build/scripts-2.7/mysqlauditgrep -> /usr/bin
copying build/scripts-2.7/mysqlrplms -> /usr/bin
copying build/scripts-2.7/mysqlslavetrx -> /usr/bin
copying build/scripts-2.7/mysqlreplicate -> /usr/bin
copying build/scripts-2.7/mysqldbexport -> /usr/bin
copying build/scripts-2.7/mysqlrplshow -> /usr/bin
copying build/scripts-2.7/mysqluc -> /usr/bin
copying build/scripts-2.7/mysqlserverinfo -> /usr/bin
copying build/scripts-2.7/mysqlauditadmin -> /usr/bin
copying build/scripts-2.7/mysqlrplsync -> /usr/bin
copying build/scripts-2.7/mysqldbcompare -> /usr/bin
copying build/scripts-2.7/mysqldiskusage -> /usr/bin
copying build/scripts-2.7/mysqlfailover -> /usr/bin
copying build/scripts-2.7/mysqluserclone -> /usr/bin
copying build/scripts-2.7/mysqlbinlogmove -> /usr/bin
copying build/scripts-2.7/mysqlmetagrep -> /usr/bin
copying build/scripts-2.7/mysqldbcopy -> /usr/bin
~~~
