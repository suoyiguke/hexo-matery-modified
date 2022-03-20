---
title: mysql-8-新特性二DDL操作的原子化.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: mysql-8-新特性二DDL操作的原子化.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
https://dev.mysql.com/doc/refman/8.0/en/atomic-ddl.html

MySQL 8.0支持原子数据定义语言(DDL)语句。这个特性被称为原子DDL。原子DDL语句将数据字典更新、存储引擎操作和与DDL操作相关联的二进制日志写入组合成单个原子操作。即使服务器在操作过程中停止运行，操作也可以提交，将适用的更改保存到数据字典、存储引擎和二进制日志中，或者回滚。

>注意，原子DDL不是事务性DDL。DDL语句，无论是原子的还是其他的，都会隐式地结束当前会话中任何活动的事务，就好像在执行语句之前您已经完成了一个COMMIT一样。这意味着DDL语句不能在另一个事务中执行，不能在事务控制语句(如开始事务)中执行...提交，或者与同一事务中的其他语句结合使用。

MySQL 8.0中MySQL数据字典的引入使原子DDL成为可能。在早期的MySQL版本中，元数据存储在元数据文件、非事务表和存储引擎特定的字典中，这需要中间提交。MySQL数据字典提供的集中式事务性元数据存储消除了这一障碍，使得将DDL语句操作重构为原子操作成为可能。

mysql5.7中就是遇到错误也是会部分成功的
~~~
CREATE TABLE t1 (c1 INT);
DROP TABLE t1, t2;
ERROR 1051 (42S02): Unknown table 'test.t2'
SHOW TABLES;
Empty set (0.00 sec)
~~~

mysql8中，DDL操作遇到错误会回滚
~~~
CREATE TABLE t1 (c1 INT);
DROP TABLE t1, t2;
ERROR 1051 (42S02): Unknown table 'test.t2'
SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
~~~


说白了就是：原子DDL，一个ddl语句要么成功，要么失败。不会出现像mysql5.7中出现异常的情况，生成一个异常文件

特别的，原子化的DDL操作若在执行一半时，mysql服务突然停止也不会像5.7那样生成一个报错文件。它只会回滚。



**支持的ddl语句：**
原子ddl特性支持表ddl语句和非表ddl语句。与表相关的ddl操作需要存储引擎的支持，非表相关的ddl操作不需要存储引擎的支持。
1、支持表ddl的语句包含对数据库、表空间、表和索引的create、alter、drop操作，以及对表的truncate操作
2、支持非表ddl的语句包含：create，drop语句，以及对存储函数、触发器、视图和用户定义的函数的alter语句；
3、账号管理语句如create、alter、drop以及对角色和用户的rename语句，grant、revoke语句

 

**原子ddl特性不支持以下语句：**
表相关的ddl语句涉及到非innodb存储引擎
1、install plugin、uninstall plugin语句
2、install component、uninstall component语句
3、create server、alter server、drop server语句

 

 
**存储引擎的支持**
目前，只有innodb存储引擎支持原子ddl。


**查看DDL日志**
另外就是我们可以通过设置innodb_print_ddl_logs=1和log_error_verbosity=3在 MySQL 的 系统日志里面查看 DDL log，比如我运行的 MySQL 8.0 是在 docker 中 ，使用docker logs mysql8.0 。
~~~
SET GLOBAL innodb_print_ddl_logs=1
SET GLOBAL log_error_verbosity=3
~~~

那么就会记录到xxx.error中了，贴下DDL信息如下

>2021-01-11T09:40:58.117786Z 9 [Note] [MY-012473] [InnoDB] DDL log insert : [DDL record: DELETE SPACE, id=336, thread_id=9, space_id=51, old_file_path=.\test\t1.ibd]
2021-01-11T09:40:58.118260Z 9 [Note] [MY-012478] [InnoDB] DDL log delete : 336
2021-01-11T09:40:58.240853Z 9 [Note] [MY-012477] [InnoDB] DDL log insert : [DDL record: REMOVE CACHE, id=337, thread_id=9, table_id=1109, new_file_path=test/t1]
2021-01-11T09:40:58.241357Z 9 [Note] [MY-012478] [InnoDB] DDL log delete : 337
2021-01-11T09:40:58.265496Z 9 [Note] [MY-012472] [InnoDB] DDL log insert : [DDL record: FREE, id=338, thread_id=9, space_id=51, index_id=214, page_no=4]
2021-01-11T09:40:58.265902Z 9 [Note] [MY-012478] [InnoDB] DDL log delete : 338
2021-01-11T09:40:58.462472Z 9 [Note] [MY-012485] [InnoDB] DDL log post ddl : begin for thread id : 9
2021-01-11T09:40:58.462877Z 9 [Note] [MY-012486] [InnoDB] DDL log post ddl : end for thread id : 9
