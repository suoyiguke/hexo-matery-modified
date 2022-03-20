---
title: mysql-ALGORITHM=COPY-和ALGORITHM=INPLACE.md
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
title: mysql-ALGORITHM=COPY-和ALGORITHM=INPLACE.md
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
①：Copy Table方式： 这是InnoDB最早支持的方式。顾名思义，通过临时表拷贝的方式实现的。新建一个带有新结构的临时表，将原表数据全部拷贝到临时表，然后Rename，完成创建操作。这个方式过程中，原表是可读的，不可写。但是会消耗一倍的存储空间。
若表的数据过大，可能会造成/tem 满了

②：Inplace方式：这是原生MySQL 5.5，以及innodb_plugin中提供的方式。所谓Inplace，也就是在原表上直接进行，不会拷贝临时表。相对于Copy                        Table方式，这比较高效率。原表同样可读的，但是不可写。

③：Online方式：这是MySQL 5.6以上版本中提供的方式，也是今天我们重点说明的方式。无论是Copy Table方式，还是Inplace方式，原表只能允许读取，           不可写。对应用有较大的限制，因此MySQL最新版本中，InnoDB支持了所谓的Online方式DDL。与以上两种方式相比，online方式支持DDL时不仅可以读，还可以写，对于dba来说，这是一个非常棒的改进。

 

