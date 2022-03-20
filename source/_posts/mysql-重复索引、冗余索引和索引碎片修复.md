---
title: mysql-重复索引、冗余索引和索引碎片修复.md
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
title: mysql-重复索引、冗余索引和索引碎片修复.md
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
###重复索引和冗余索引
重复索引：在同一个列建立的多个单值索引，或者在顺序相同的多个列上建立了多个复合索引。这种重复索引没有任何帮助只会增大索引文件，拖慢更新速度，需要去掉！

冗余索引：
2个索引说覆盖的列有重叠。
比如 index x(x)和index xm(x,m)。这连两个索引的x列重叠了，这种情况称为冗余索引。
甚至有 xm(x,m) 和 mx(m,x) ，这两和复合索引的索引顺序不同，也是看做冗余索引的。像在这种情况在特定业务下也有它的用处！

###索引碎片修复
在长期的数据更改过程中，索引文件和数据文件，都将产生空洞，形成碎片（页分裂页移动）。时间一久时间会查询效率会变慢。

若表的引擎是innodb，可以使用
~~~
ALTER TABLE tb_box ENGINE INNODB
~~~

可以使用
~~~
OPTIMIZE TABLE tb_box;
~~~

注意：
修复表的数据和索引碎片，就会把所有的数据文件重新整理一遍，使之对齐。这个过程如果表的行数比较大，也是非常耗费资源的操作。所以不能频繁修复。

若表的update操作很频繁，可以按 周/月来修复。若update的不多，可以更长周期来做修复
