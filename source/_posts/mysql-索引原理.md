---
title: mysql-索引原理.md
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
title: mysql-索引原理.md
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
https://www.cs.usfca.edu/~galles/visualization/Algorithms.html


B+ 树： 
> 通过多叉来减少树的深度，提高查询效率

多叉平衡树
1、非叶子节点不存储data，只存储索引字段（冗余）。这样16K可以放更多的索引。
2、叶子节点包含所有索引字段data
3、叶子节点用指针连接，提高区间访问的性能。指针6字节

###聚簇索引和辅助索引
1、mysql总会有一个聚簇索引
2、自己建立的叫辅助索引
3、
3、辅助索引叶子节点保存：key键值和主键值。所以select中如果有id主键那么也不需要回表查询！

3、使用辅助索引效率要比直接使用聚簇索引低
3、仅仅通过扫描辅助索引就能找到所有的select字段叫做：索引覆盖 using index；通过扫描辅助索引得不到，还必须到聚簇索引中找就叫：回表


####结论：
1、order by id 要比createDate要快。因为直接走聚簇索引
2、延迟加载思想。有大量where条件。先查id，再通过id查其它字段



