---
title: mysql-索引填充因子.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
---
title: mysql-索引填充因子.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
InnoDB indexes are B-tree data structures. Index records are stored in the leaf pages of their B-tree data structure. The default size of an index page is 16KB.

当一条新记录被插入到InnoDB clustered index中时，InnoDB预留page（页）的1/16的空间以备将来插入或者更新索引记录。

如果索引记录是顺序插入的（升序或者降序），那么填满这一页就是剩下的那15/16的空间；
如果记录是按照随机顺序插入的，那么填满这一条就是1/2 ~ 15/16 页。

配置项 innodb_fill_factor 定义每个B-tree page 百分之多少的空间用于存储有序的索引记录，剩下的空间是为以后索引增长而预留的。5.7默认值是100，但其实最高只能填充约15KB的数据，因为InnoDB会预留1/16的空闲空间
~~~
show variables like '%innodb_fill_factor%';
~~~

你可以通过innodb_page_size设置InnoDB表空间的page size。支持64KB, 32KB, 16KB (default), 8KB, and 4KB.


https://blog.csdn.net/n88Lpo/article/details/100179043
