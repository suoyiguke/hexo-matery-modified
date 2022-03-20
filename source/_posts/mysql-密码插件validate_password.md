---
title: mysql-密码插件validate_password.md
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
title: mysql-密码插件validate_password.md
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
防止使用过于简单的密码，mysql提供了validate_password密码插件来强制规范密码复杂度。用了这个插件再去创建123456这种密码时操作会报错。

https://dev.mysql.com/doc/refman/5.7/en/validate-password-installation.html

在线安装：
~~~
INSTALL PLUGIN validate_password SONAME 'validate_password.so';
~~~
或者增加配置然后重启
~~~
[mysqld]
plugin-load-add=validate_password.so
~~~

show plugins;查看下刚刚安装的validate_password插件
~~~
(root@localhost) [(none)]>show plugins;
+----------------------------+----------+--------------------+----------------------+---------+
| Name                       | Status   | Type               | Library              | License |
+----------------------------+----------+--------------------+----------------------+---------+
| binlog                     | ACTIVE   | STORAGE ENGINE     | NULL                 | GPL     |
| mysql_native_password      | ACTIVE   | AUTHENTICATION     | NULL                 | GPL     |
| sha256_password            | ACTIVE   | AUTHENTICATION     | NULL                 | GPL     |
| CSV                        | ACTIVE   | STORAGE ENGINE     | NULL                 | GPL     |
| MEMORY                     | ACTIVE   | STORAGE ENGINE     | NULL                 | GPL     |
| InnoDB                     | ACTIVE   | STORAGE ENGINE     | NULL                 | GPL     |
| INNODB_TRX                 | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_LOCKS               | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_LOCK_WAITS          | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_CMP                 | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_CMP_RESET           | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_CMPMEM              | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_CMPMEM_RESET        | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_CMP_PER_INDEX       | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_CMP_PER_INDEX_RESET | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_BUFFER_PAGE         | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_BUFFER_PAGE_LRU     | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_BUFFER_POOL_STATS   | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_TEMP_TABLE_INFO     | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_METRICS             | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_FT_DEFAULT_STOPWORD | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_FT_DELETED          | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_FT_BEING_DELETED    | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_FT_CONFIG           | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_FT_INDEX_CACHE      | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_FT_INDEX_TABLE      | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_SYS_TABLES          | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_SYS_TABLESTATS      | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_SYS_INDEXES         | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_SYS_COLUMNS         | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_SYS_FIELDS          | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_SYS_FOREIGN         | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_SYS_FOREIGN_COLS    | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_SYS_TABLESPACES     | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_SYS_DATAFILES       | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| INNODB_SYS_VIRTUAL         | ACTIVE   | INFORMATION SCHEMA | NULL                 | GPL     |
| MyISAM                     | ACTIVE   | STORAGE ENGINE     | NULL                 | GPL     |
| MRG_MYISAM                 | ACTIVE   | STORAGE ENGINE     | NULL                 | GPL     |
| PERFORMANCE_SCHEMA         | ACTIVE   | STORAGE ENGINE     | NULL                 | GPL     |
| ARCHIVE                    | ACTIVE   | STORAGE ENGINE     | NULL                 | GPL     |
| BLACKHOLE                  | ACTIVE   | STORAGE ENGINE     | NULL                 | GPL     |
| FEDERATED                  | DISABLED | STORAGE ENGINE     | NULL                 | GPL     |
| partition                  | ACTIVE   | STORAGE ENGINE     | NULL                 | GPL     |
| ngram                      | ACTIVE   | FTPARSER           | NULL                 | GPL     |
| validate_password          | ACTIVE   | VALIDATE PASSWORD  | validate_password.so | GPL     |
+----------------------------+----------+--------------------+----------------------+---------+
45 rows in set (0.00 sec)
~~~

查看参数 show variables like 'validate%';

~~~
(root@localhost) [(none)]>show variables like 'validate%';
+--------------------------------------+--------+
| Variable_name                        | Value  |
+--------------------------------------+--------+
| validate_password_check_user_name    | OFF    |
| validate_password_dictionary_file    |        |
| validate_password_length             | 8      |
| validate_password_mixed_case_count   | 1      |
| validate_password_number_count       | 1      |
| validate_password_policy             | MEDIUM |
| validate_password_special_char_count | 1      |
+--------------------------------------+--------+
7 rows in set (0.01 sec)
~~~
>1、validate_password_length 8 密码长度为8位
2、validate_password_mixed_case_count 1   包含一个大写字母
3、validate_password_number_count 1 包含一个数字
4、validate_password_special_char_count  包含一个特殊字符


完了之后修改密码为123，报错如下。密码不安全，不符合validate_password插件的约束。
~~~
(root@localhost) [(none)]>alter user david@'%' identified by '123';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
~~~

那么我们设置一个符合规范的密码，设置成功
~~~
(root@localhost) [(none)]>alter user david@'%' identified by '1111aaA_';
Query OK, 0 rows affected (0.00 sec)
~~~



**validate_password_dictionary_file 密码字典表**
启用这个`密码字典表`可以做到限制密码不能包含字典中指定的字符串。

创建一个包含admin字符串的文件：
 echo 'admin'> dic.file
指定validate_password_dictionary_file和validate_password_policy 值
~~~
(root@localhost) [(none)]>set global validate_password_dictionary_file = '/mdata/mysql57/dic.file';
Query OK, 0 rows affected (0.00 sec)

(root@localhost) [(none)]>set global validate_password_policy = STRONG;
Query OK, 0 rows affected (0.00 sec)
~~~

现在设置密码为1111adminDD_提示修改失败。去掉admin使用kk代替就成功了。
~~~
(root@localhost) [(none)]>alter user david@'%' identified by '1111adminDD_';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
(root@localhost) [(none)]>alter user david@'%' identified by '1111kkDD_';
Query OK, 0 rows affected (0.00 sec)
~~~


**validate_password_check_user_name**
设置ON，约束密码不能直接设置为用户名
~~~
set global validate_password_check_user_name= ON;
(root@localhost) [(none)]>alter user david@'%' identified by 'root';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
~~~

