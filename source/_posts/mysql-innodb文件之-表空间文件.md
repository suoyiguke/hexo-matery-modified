---
title: mysql-innodb文件之-表空间文件.md
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
title: mysql-innodb文件之-表空间文件.md
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
###共享表空间文件
查看innodb_data_file_path参数。
~~~
mysql> SHOW VARIABLES LIKE '%innodb_data_file_path%';
+-----------------------+------------------------+
| Variable_name         | Value                  |
+-----------------------+------------------------+
| innodb_data_file_path | ibdata1:12M:autoextend |
+-----------------------+------------------------+
1 row in set (0.01 sec)

~~~

值为 ibdata1:12M:autoextend   表示 ibdata1就是默认表空间文件，文件大小为12M。因为有autoextend，若空间不够用，该文件可以自动增长。

在/mysql/data 目录下可以查看到这个 ibdata1
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7bbb46c461466e18.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######指定多个共享表空间文件

用户可以通过多个文件组成一个表空间同时制定文件的属性,如: 
~~~
[mysqld] 
innodb_data_file_path=/db/ibdatal:2000m;/dr2/db/ibdata22:2000m:autoextend 
~~~


同时,两个 文件的文件名后都跟了属性,表示文件 idbdatal的大小为2000MB,文件 ibdata22的大小 为2000MB,如果用完了这2000MB,该文件可以自动增长(autoextend) 


设置 `innodb_data_file_path` 参数后,所有基于 InnoDB存储引擎的表的数据都会 记录到该`共享表空间`中。


修改innodb_data_file_path参数时，可能出现以下问题导致mysql服务起不来：
> [ERROR] InnoDB: The innodb_system data file '.\ibdata1' is of a different size 4864 pages (rounded down to MB) than the 768 pages specified in the .cnf file!

ibdata1和ibdata2的大小要和data目录下的这个俩文件大小相同，因此查看此时的ibdata1大小，并设置为76M
~~~
innodb_data_file_path= ibdata1:76M;ibdata2:76M:autoextend:max:500M
~~~


我们可以将 ibdatal和ibdata2两个文件用来组成表空间。若这两个文件位于不同的磁盘上,磁盘的负载可能被平均,因此可以提高数据库的整体性能。注意若要指定不同的磁盘空间，则需要添加空的innodb_data_home_dir参数才行。然后将之前的redo log 和 共享表空间文件删除。
~~~
[mysqld]
innodb_data_home_dir =
innodb_data_file_path = E:\\ibdata1:76M;D:\\ibdata2:76M:autoextend:max:500M
~~~


######使用frm和idb文件恢复数据。共享表空间文件也要进行备份恢复`重要`

备份原始文件时，在 innodb 引擎中，每个库是一个文件夹，每个表都有一个 .frm 和 .idb 文件。但是光备份这两个然后还原是不行的，因为需要 idb 文件中的 tablespace id 与 ibdata1 （共享表空间）中的一致才可以。

需要连同 ibdata1 文件一起备份。恢复时这个ibdata1（共享表空间）也要一起恢复。不然库中的表是不被识别的！


###给每张表设置独立的表空间
若设置了参数 `innodb_file_per_table`,则用户可以将每个基于 InnoDB存储引擎的表产生一个独立表空间。独立表空间的命名规则为:表名ibd。通过这样的方式,用户不用将所有数据都存放于默认的表空间中。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1f2c8c61e325857e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
mysql> SHOW VARIABLES LIKE '%innodb_file_per_table%';
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| innodb_file_per_table | ON    |
+-----------------------+-------+
1 row in set (0.02 sec)

mysql> 
~~~


###共享的表空间和表单独的表空间分别存储什么数据？

单独的表空间 文件仅存储该表的  数据、索引和插入缓冲 BITMAP等信息。

其余信息还是存放在默认的 表空间中。

