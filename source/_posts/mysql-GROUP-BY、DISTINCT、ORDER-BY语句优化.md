---
title: mysql-GROUP-BY、DISTINCT、ORDER-BY语句优化.md
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
title: mysql-GROUP-BY、DISTINCT、ORDER-BY语句优化.md
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
GROUP BY、DISTINCT、ORDERBY这几类子句比较类似，GROUP BY默认也是要进行ORDERBY排序的，笔者在本书中 把它们归为一类，优化的思路也是类似的。

可以考虑的优化方式如下。 

1、尽量对较少的行进行排序。 
2、如果连接了多张表，ORDERBY的列应该属于连接顺序的第一张表。
3、利用索引排序，如果不能利用索引排序，那么EXPLAIN查询语句将会看到有filesort。

4、GROUP BY、ORDERBY语句参考的列应该尽量在一个表中，如果不在同一个表中，那么可以考虑冗余一些列，或者合并表。

5、需要保证索引列和ORDERBY的列相同，且各列均按相同的方向进行排序。

6、增加sort_buffer_size。 sort_buffer_size是为每个排序线程分配的缓冲区的大小。增加该值可以加快ORDERBY或GROUP BY操作。但是，这是为每 个客户端分配的缓冲区，因此不要将全局变量设置为较大的值，因为每个需要排序的连接都会分配sort_buffer_size大小的内存。 

7、增加read_rnd_buffer_size。 当按照排序后的顺序读取行时，通过该缓冲区读取行，从而避免搜索硬盘。将该变量设置为较大的值可以大大改进ORDER BY的性能。但是，这是为每个客户端分配的缓冲区，因此你不应将全局变量设置为较大的值。相反，只用为需要运行大查询 的客户端更改会话变量即可。
~~~
SHOW VARIABLES LIKE '%sort_buffer_size%'
SHOW VARIABLES LIKE '%innodb_sort_buffer_size%'
SHOW VARIABLES LIKE '%read_rnd_buffer_size%'
~~~

8、改变tmpdir变量指向基于内存的文件系统或其他更快的磁盘。 如果MySQL服务器正作为复制从服务器被使用，那么不应将“--tmpdir”设置为指向基于内存的文件系统的目录，或者当服务 器主机重启时将要被清空的目录。因为，对于复制从服务器，需要在机器重启时仍然保留一些临时文件，以便能够复制临时表 或执行LOADDATAINFILE操作。如果在服务器重启时丢失了临时文件目录下的文件，那么复制将会失败。

 9、指定ORDERBY NULL。 默认情况下，MySQL将排序所有GROUP BY的查询，如果想要避免排序结果所产生的消耗，可以指定ORDERBY NULL。 例如：SELECT count(*) cnt, cluster_id FROM stat GROUP BY cluster_id ORDER BY NULL LIMIT 10; ·

10、优化GROUP BY WITHROLLUP。 GROUP BY WITHROLLUP可以方便地获得整体分组的聚合信息（superaggregation），但如果存在性能问题，可以考虑在应用层实现这个功能，这样往往会更高效，伸缩性也更佳。 

11、使用非GROUP BY的列来代替GROUP BY的列。 比如，原来是“GROUP BYxx_name,yy_name”，如果GROUP BYxx_id可以得到一样的结果，那么使用GROUP BYxx_id也是可 行的。

12、可以考虑使用Sphinx等产品来优化GROUP BY语句，一般来说，它可以有更好的可扩展性和更佳的性能。
