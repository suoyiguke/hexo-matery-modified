---
title: innodb_fill_factor--页填充因子.md
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
title: innodb_fill_factor--页填充因子.md
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
有个选项 innodb_fill_factor 用于定义InnoDB page的填充率，默认值是100，但其实最高只能填充约15KB的数据，因为InnoDB会预留1/16的空闲空间。

在InnoDB文档中，有这么一段话An innodb_ll_factor setting of 100 leaves 1/16 of the space in clustered indexpages free for future index growth.另外，文档中还有这样一段话When new records are inserted into an InnoDB clustered index, InnoDB tries toleave 1/16 of the page free for future insertions and updates of the indexrecords.   If   index   records   are   inserted   in   a   sequential   order   (ascending   ordescending),  the  resulting index pages  are about   15/16  full. If   records areinserted in a random order, the pages are from 1/2 to 15/16 full.

上面这两段话，综合起来理解，就是即便 innodb_fill_factor =100，也会预留1/16的空闲空间，用于现存记录长度扩展用在最佳的顺序写入数据模式下，page填充率有可能可以达到15/16在随机写入新数据模式下，page填充率约为 1/2 ~ 15/16预留1/16这个规则，只针对聚集索引的叶子节点有效。d

对于聚集索引的非叶子节点以及辅助索引（叶子及非叶子）节点都没有这个规则不过 innodb_fill_factor 选项对叶子节点及非叶子节点都有效，但对存储text/blob溢出列的page无效

innodb_fill_factor=100 16K  预留1/16的空间 =  1K空间
innodb_fill_factor=10 预留90%的空间 16K 预留1.6K空间

这个参数不常用，但如果更新操作比较多，或许可以调下这个参数
