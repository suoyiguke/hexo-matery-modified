---
title: mysql-DDL与DML的并发关系.md
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
title: mysql-DDL与DML的并发关系.md
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
###概念

一、修改列
1、修改列数据类型，还包括修改长度如varchar(10)==>varchar(20) 是不允许dml并发的

2、修改列名并且同时设置它为外键的时候是不允许dml并发的，若只是单纯修改列名就可以

3、添加是自增列的时候不允许和dml并发，若只是添加列则可以！

4、指定字符集/修改列的字符编码时不允许和dml并发

5、设置null、not null；设置、删除列默认值 都是允许dml并发的！

二、修改表


表的话注意下字符集就行了。修改表名是可以和dml并发的！


三、主键操作
1、删除主键而不新增主键不允许dml并发。注意，新增主键、和修改主键（更换主键作用的字段）是可以与dml并发的！


四、索引操作
1、添加全文索引 fulltext index不允许dml并发
2、添加空间索引 spatial index 不允许dml并发

五、虚拟列操作
1、Adding a STORED column	添加STORED虚拟列阻塞dml
2、Modifying STORED column order	 修改STORED虚拟列顺序阻塞dml
3、Modifying VIRTUAL column order	 修改VIRTUAL虚拟列顺序阻塞dml

六、分区操作

PARTITION BY 分区依据

ADD PARTITION  添加分区
DROP PARTITION 删除分区
DISCARD PARTITION 禁用分区
IMPORT PARTITION 导入分区
COALESCE PARTITION  聚结分区
REORGANIZE PARTITION  重组分区
OPTIMIZE PARTITION    优化分区
REBUILD PARTITION     重建分区
REMOVE PARTITIONING 移除分区


###总结

######我们ddl常用操作中，会阻塞dml的ddl有：
1、修改列数据类型，数据长度，如varchar(10) 改为varchar(20)
2、修改列字符编码
3、添加自增列
4、修改列名并指定外键
5、删除主键索引而不新增主键索引
6、添加全文索引 fulltext index
7、添加空间索引 spatial index 
8、常见分区操作都会导致阻塞dml！
######允许和dml并发的有：
1、修改列名不添加外键
2、添加一个非自增的列、删除列、移动列顺序
3、设置null、not null
4、添加、删除、修改 列默认值
5、添加主键索引、变更主键索引作用的字段
6、添加、删除、修改普通索引
7、添加、删除外键


###参考资料
https://dev.mysql.com/doc/refman/5.7/en/innodb-online-ddl-operations.html#online-ddl-partitioning

###对实践的指导
像一些常用DDL操作如修改字段字符编码、修改字段数据类型都会导致锁住修改的表，出现 Waiting for table metadata lock。所以需要一些可以在线DDL的手段，可以手动覆盖 frm https://www.jianshu.com/p/0cdc671adfcf 。或者使用pt-online-schema-change 工具

###参数
~~~
(root@localhost) [dbt3]>show variables like 'innodb_online_alter_log_max_size';
+----------------------------------+-----------+
| Variable_name                    | Value     |
+----------------------------------+-----------+
| innodb_online_alter_log_max_size | 134217728 |
+----------------------------------+-----------+
~~~

默认128M，若更新操作比较多，导致产生了大量的日志的话就会报错。
请调整为1G

~~~
[mysqld]
innodb_online_alter_log_max_size=1G
~~~

###在线索引添加造成的主从演示
若主库执行添加索引，5分钟才完成。那么从库也执行到这个DDL时就会延迟5分钟

pt toolkit percona
延时会非常小，而且不阻塞读写

![image.png](https://upload-images.jianshu.io/upload_images/13965490-3ebedf32bd478c2e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
