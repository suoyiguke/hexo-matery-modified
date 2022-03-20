---
title: mysql-8-新特性一-ALGORITHM=INSTANT-实现的快速DDL.md
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
title: mysql-8-新特性一-ALGORITHM=INSTANT-实现的快速DDL.md
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
参考 https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-12.html
在线DDL之 快速增加列（秒级别的），并不会造成业务抖动。该功能自 MySQL 8.0.12 版本引入，是由腾讯游戏DBA团队贡献，我国程序员还是挺厉害的嘛。注意一下，此功能只适用于 InnoDB 表。实际上MySQL 5.7就已支持 Online DDL，虽说大部分 DDL 不影响对表DML操作，但是依然会消耗非常多的时间，且占用额外的磁盘空间，并会造成主从延迟，或者影响表的查询速度。有了这个ALGORITHM=INSTANT 就可应对瞬息万变的需求了。。

**ALGORITHM=INSTANT 目前对6种ddl有效：** 

*   Adding a column. This feature is referred to as Instant Add Column . 添加列
*   Adding or dropping a virtual column. 添加或删除virtual 列
*   Adding or dropping a column default value. 添加或删除列默认值
*   Modifying the definition of an ENUM.  修改 ENUM 定义
*   Changing the index type. 修改索引类型
*   Renaming a table. 重命名表


实际试验下，使用 mysql5.7的INPLACE 算法 时间: 52s。
~~~
mysql> ALTER TABLE `test`.`book` 
ADD COLUMN `zz` varchar(255) NULL ,algorithm=INPLACE;
Query OK, 0 rows affected (52.30 sec)
Records: 0  Duplicates: 0  Warnings: 0

~~~

使用 Instant Add Column ，时间:0.39 s。 `果然是秒级别添加`
~~~
mysql> ALTER TABLE `test`.`book` 
ADD COLUMN `gg` varchar(255) NULL,algorithm=instant;
Query OK, 0 rows affected (0.39 sec)
Records: 0  Duplicates: 0  Warnings: 0
~~~

当然我们不需要显式指定algorithm=instant;mysql会优先使用INSTANT算法来进行ddl的；若显式指定algorithm=instant 同时目标ddl不支持就会报错。如下，DROP COLUMN 时指定则报错
~~~
mysql> ALTER TABLE `test`.`book` 
DROP COLUMN `gg` ,algorithm=instant; 
1845 - ALGORITHM=INSTANT is not supported for this operation. Try ALGORITHM=COPY/INPLACE.
~~~







添加或删除virtual 列
~~~
mysql> ALTER TABLE `test`.`book` 
ADD COLUMN `x` varchar(255) AS (book_name) VIRTUAL NULL AFTER `book_name`;
Query OK, 0 rows affected (0.90 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> ALTER TABLE `test`.`book` 
DROP COLUMN `x`,algorithm=INPLACE;
Query OK, 0 rows affected (0.47 sec)
Records: 0  Duplicates: 0  Warnings: 0
~~~

添加或删除列默认值
~~~
mysql> ALTER TABLE `test`.`book` 
MODIFY COLUMN `zz` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' AFTER `book_name`;
Query OK, 0 rows affected (0.88 sec)
Records: 0  Duplicates: 0  Warnings: 2

mysql> ALTER TABLE `test`.`book` 
MODIFY COLUMN `zz` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL AFTER `book_name`;
Query OK, 0 rows affected (0.16 sec)
Records: 0  Duplicates: 0  Warnings: 2

~~~

修改 ENUM 定义
~~~
mysql> ALTER TABLE `test`.`book` 
MODIFY COLUMN `mj` enum('one','two','three','4') CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `gg`;
Query OK, 0 rows affected (0.26 sec)
Records: 0  Duplicates: 0  Warnings: 2
~~~

修改索引类型

重命名表，好像和5.7的INPLACE算法也没啥时间上的区别。INPLACE的rename table已经足够快了
~~~
mysql> ALTER TABLE book1 RENAME book;
Query OK, 0 rows affected (0.55 sec)

mysql> ALTER TABLE book RENAME book1,algorithm=INPLACE;
Query OK, 0 rows affected (0.46 sec)
~~~

**还有一些特殊情况不能使用ALGORITHM=INSTANT的：** 
Instant Add Column只能将新字段添加到表的尾巴上，不能添加到中间!
~~~
mysql> ALTER TABLE `test`.`book` 
ADD COLUMN `hhh` varchar(255) NULL AFTER `book_name`,algorithm=instant;
1845 - ALGORITHM=INSTANT is not supported for this operation. Try ALGORITHM=COPY/INPLACE.
~~~

不支持压缩表，即该表行格式不能是 COMPRESSED。
~~~
mysql> show create table book;
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| book  | CREATE TABLE `book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint DEFAULT NULL,
  `book_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `zz` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `gg` varchar(255) DEFAULT NULL,
  `mj` enum('one','two','three','4') CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_user_id` (`user_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=762475 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPRESSED |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.03 sec)

mysql> ALTER TABLE `test`.`book` 
ADD COLUMN `ggg` varchar(255) NULL,algorithm=instant;
1845 - ALGORITHM=INSTANT is not supported for this operation. Try ALGORITHM=COPY/INPLACE.
~~~

不支持包含全文索引的表；不支持临时表；不支持那些在数据字典表空间中创建的表。这些就不一一验证了。平时操作时要注意下！
