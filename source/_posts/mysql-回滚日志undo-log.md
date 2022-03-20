---
title: mysql-回滚日志undo-log.md
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
title: mysql-回滚日志undo-log.md
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
### 浅析如何将undo log从tablespace分离

从MySQL5.6.3之后，MySQL支持将undo日志从tablespace（ibdataN 共享表空间）中独立开来放到单独的磁盘上。MySQL官方建议将undo放到ssd（固态硬盘）上，而把ibdata放在hd（机械硬盘）。（这里似乎有争论，国内某些大牛建议将顺序读写的log日志放在hdd）

比较重要的一个概念：

虽然undo log被分离出去了，但是其io处理还是在system tablespace内完成，所以定义上来讲还是算tablespace的。文档中原文如下：

*“Because these files handle**I/O operations formerly done inside the  system tablespace**, we broaden the definition of system tablespace to include these new files. ”*

undo logs 存放在rollback segment内

###如何回收undo log

undo log回滚日志物理文件空间回收
MySQL5.6之前
undo log在ibdata1文件里，ibdata1文件会越来越大，想要回收，必须全库导出，删除data目录，再重新初始化数据库，最后把全库导入，才可实现ibdata1回收。
MySQL5.6
可以把undo log回滚分离到一个单独的表空间里，但不能回收空间大小。
MySQL5.7
支持在线回收
undo log从共享表空间里ibdata1拆分出去，在安装MySQL时，需要在my.cnf里指定，
数据库启动再指定，会报错。

配置文件里指定如下参数，如创建数据以后再指定会报错。

~~~
show VARIABLES like '%innodb_undo_tablespaces%'
~~~
用于设定创建的undo表空间的个数，在Install db时初始化后，就再也不能被改动了；
默认值为0，表示不独立设置undo的tablespace，默认记录到ibdata中；否则，则在undo目录下创建这么多个undo文件，例如假定设置 该值为16，那么就会创建命名为undo001~undo016的undo tablespace文件，每个文件的默认大小为10M；
innodb_undo_tablespaces参数必须大于或等于2，即回收一个undolog日志时，要保证另一个undo可以使用。


~~~
show VARIABLES like '%innodb_undo_directory%'
~~~
undolog物理文件存放位置
~~~
show VARIABLES like '%innodb_undo_logs%'
~~~

定义多少个回滚段的数量，至少大于等于35，默认值和最大值都是128，每个undolog能保存最多1024个事务，这个参数可以用来性能调优，官方建议先将这个参数设小然后逐步增大来观察性能变化。（因为如果一下子分配过多也可能用不到）

~~~
SHOW VARIABLES LIKE '%innodb_undo_log_truncate%'
~~~
innodb_undo_log_truncate参数设置为1，即开启在线回收undo日志文件，支持动态设置。


~~~
SHOW VARIABLES LIKE '%innodb_max_undo_log_size%'
~~~
innodb_max_undo_log_size(1073741824 默认1GB)当超过阈值时，会触发truncate回收动作，truncate后空间缩小到10MB

~~~
SHOW VARIABLES LIKE '%innodb_purge_rseg_truncate_frequency%'
~~~
innodb_purge_rseg_truncate_frequency 控制回收undo log的频率。undo log空间在它的回滚段没有得到释放之前不会收缩，想要增加释放回滚的频率，需要降低innodb_purge_rseg_truncate_frequency的设定值。



