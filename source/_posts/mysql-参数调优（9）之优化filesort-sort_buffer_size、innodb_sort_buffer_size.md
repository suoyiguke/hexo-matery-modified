---
title: mysql-参数调优（9）之优化filesort-sort_buffer_size、innodb_sort_buffer_size.md
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
title: mysql-参数调优（9）之优化filesort-sort_buffer_size、innodb_sort_buffer_size.md
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
~~~
SHOW VARIABLES LIKE '%sort_buffer_size%'
SHOW VARIABLES LIKE '%innodb_sort_buffer_size%'
SHOW VARIABLES LIKE '%read_rnd_buffer_size%'
SHOW VARIABLES LIKE '%max_length_for_sort_data%' 
SHOW VARIABLES LIKE '%max_sort_length%'

~~~

有时我们使用EXPLAIN工具，可以看到查询计划的输出中的Extra列有filesort。filesort往往意味着你没有利用到索引进行排序。filesort的字面意思可能会导致混淆，它和文件排序没有任何关系，可以理解为不能利用索引实现排序。


###filesort的两种算法：single-pass和two-pass
single-pass新算法，two-pass旧算法
single-pass适合列数量少的查询，two-pass相反


###参数调整优化filesort

为了提高排序速度，请检查您是否可以让MySQL使用索引，而不是额外的排序阶段。如果不可能，请尝试以下策略:


1、调整max_length_for_sort_data以控制何时使用two-pass 或 single-pass
如果各列长度之和（包括选择列、排序列）超过了max_length_for_sort_data字节，那么就使用two- pass算法。如果排序BLOB、TEXT字段，使用的也是two-pass算法，那么这个值设置得太高会更加容易地使用single-pass。导致系统I/O上升，CPU下降，建议不要将max_length_for_sort_data设置得太高。

对于不使用 two-pass  的慢速ORDER BY查询，请尝试将max_length_for_sort_data系统变量降低到适合触发 two-pass  的值。(将该变量的值设置得太高的一个症状是高磁盘活动和低CPU活动的组合。)
~~~
SHOW VARIABLES LIKE '%max_length_for_sort_data%' -- 1024Bytes 1KBB
~~~
2、调整max_sort_length，优化two-pass读取的BLOB、TEXT大字段
如果排序BLOB、TEXT字段，则仅排序前max_sort_length个字节。请考虑存储在排序缓冲区中的列值的大小受max_sort_length系统变量值的影响。例如，如果元组存储长字符串列的值，并且您增加了max_sort_length的值，则排序缓冲区元组的大小也会增加，并且可能需要您增加sort_buffer_size。对于作为字符串表达式结果计算的列值(例如调用字符串值函数的列值)，文件排序算法无法判断表达式值的最大长度，因此它必须为每个元组分配max_sort_length字节。
~~~
SHOW VARIABLES LIKE '%max_sort_length%' -- 1024Bytes 1KB
~~~
3、加大sort_buffer_size优化single-pass
 一般情况下使用默认的single-pass新算法即可。可以考虑加大sort_buffer_size以减少磁盘I/O。 需要留意的是字段长度之和不要超过max_length_for_sort_data，只查询所需要的列，注意列的类型、长度（因为超过max_length_for_sort_data就会去使用旧排序算法two-pass ）。MySQL目前读取和计算列的长度是按照定义的最大的度进行的，所以在设计表结构的时候，不要将VARCHAR类型的字段设置得过大，虽然对于VARCHAR类型来说，在物理磁盘中的实际存储可以做到紧凑，但在排序的时候，是会分配最大定义的长度的，有时排序阶段所产生的临时文件甚至比原始表还要大。



~~~
SHOW VARIABLES LIKE '%sort_buffer_size%' -- 262144字节 256KB
~~~
4、加大read_rnd_buffer_size优化 two-pass 
对于two-pass旧算法，可以考虑增大read_rnd_buffer_size，但由于这个全局变量是对所有连接都生效的，因此建议只在会话级别进行设置，以加速一些特殊的大操作。增加read_rnd_buffer_size变量值，以便一次读取更多行。
~~~
SHOW VARIABLES LIKE '%read_rnd_buffer_size%' -- 262144Bytes 256KB
~~~


5、要监视合并过程的次数(合并临时文件)，请检查排序_合并_过程状态变量。


6、将tmpdir系统变量更改为指向具有大量可用空间的专用文件系统。变量值可以列出以循环方式使用的几个路径；您可以使用此功能将负载分散到几个目录中。在Unix上用冒号(:)和分号(；)分隔路径。)在Windows上。路径应该命名位于不同物理磁盘上的文件系统中的目录，而不是同一磁盘上的不同分区。



###实践
下面的查询的排序没有走索引
~~~
(root@localhost) [dbt3]>explain select * from lineitem order by l_discount desc limit 10000;
+----+-------------+----------+------------+------+---------------+------+---------+------+---------+----------+----------------+
| id | select_type | table    | partitions | type | possible_keys | key  | key_len | ref  | rows    | filtered | Extra          |
+----+-------------+----------+------------+------+---------------+------+---------+------+---------+----------+----------------+
|  1 | SIMPLE      | lineitem | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 5393375 |   100.00 | Using filesort |
+----+-------------+----------+------------+------+---------------+------+---------+------+---------+----------+----------------+
1 row in set, 1 warning (0.01 sec)

~~~


下面查询执行时间14.03 秒
~~~
select * from lineitem order by l_discount desc limit 10000;
10000 rows in set (14.03 sec)
~~~

查看当前排序的状态，Sort_merge_passes 次数是488
~~~
(root@localhost) [dbt3]>show status like 'sort%';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Sort_merge_passes | 488   |
| Sort_range        | 0     |
| Sort_rows         | 10000 |
| Sort_scan         | 1     |
+-------------------+-------+
4 rows in set (0.01 sec)

~~~

刷新状态重新统计
~~~
flush sattus;
~~~

设置会话级别的sort_buffer_size参数为256M
~~~
set session sort_buffer_size=256*1024*256;
~~~

重新执行排序sql，这次执行了9.82秒
~~~
select * from lineitem order by l_discount desc limit 10000;
10000 rows in set (9.82 sec)
~~~

再次查看排序状态，Sort_merge_passes变成了0
~~~
(root@localhost) [dbt3]>show status like 'sort%';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Sort_merge_passes | 0     |
| Sort_range        | 0     |
| Sort_rows         | 10000 |
| Sort_scan         | 1     |
+-------------------+-------+
~~~



###配置
>调大这个参数可以加快不走索引的using filesort 排序速度

sort_buffer_size 默认256K，会话级别参数，每个会话都会去申请这个内存。若全局设置为1G，假设有100个会话一起执行这个排序sql那么将申请100G的内存！所以这个参数全局设置不宜过大。

~~~
[mysqld]
sort_buffer_size=32M/256M/132M
~~~
调整完后记得重启，如果不想重启，只能每个会话一一执行set session sort_buffer_size=32M



###我们在生产环境下怎么知道当前的sort_buffer_size设置的是否ok？

查看全局的排序状态，若Sort_merge_passes特别大。就要考虑要不要调大全局的sort_buffer_size。
~~~
(root@localhost) [dbt3]>show global status like 'sort%';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Sort_merge_passes | 976   |
| Sort_range        | 0     |
| Sort_rows         | 30000 |
| Sort_scan         | 3     |
+-------------------+-------+
4 rows in set (0.01 sec)
~~~



###虚拟列优化同升同低
或者函数索引
