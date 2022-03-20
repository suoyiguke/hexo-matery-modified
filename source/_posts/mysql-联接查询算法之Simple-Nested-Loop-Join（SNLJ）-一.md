---
title: mysql-联接查询算法之Simple-Nested-Loop-Join（SNLJ）-一.md
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
title: mysql-联接查询算法之Simple-Nested-Loop-Join（SNLJ）-一.md
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
>Simple Nested-Loop Join：SNLJ，简单嵌套循环连接

Simple Nested-Loops Join算法相当简单、直接。即外表（驱动表）中的每一条记录与内表（被驱动表）中的记录进行比较判断（就是个笛卡尔积）。对于两表联接来说，驱动表只会被访问一遍，`但被驱动表却要被访问到好多遍`，被驱动表的具体访问次数取决于对驱动表执行单表查询后的结果集中的记录条数。

用伪代码表示一下这个过程就是这样：
~~~
For each row r in R do                         -- 扫描R表（驱动表）
    For each row s in S do                     -- 扫描S表（被驱动表）
        If r and s satisfy the join condition  -- 如果r和s满足join条件
            Then output the tuple <r, s>       -- 返回结果集
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1ecb939431e4acd5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


其中R表为外部表（Outer Table），S表为内部表（Inner Table）。这是一个最简单的算法，这个算法的开销其实非常大。假设在两张表R和S上进行联接的列都不含有索引，外表的记录数为RN，内表的记录数位SN。根据上一节对于Join算法的评判标准来看，SNLJ的开销如下表所示：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f9aa6f729922bb97.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看到读取记录数的成本和比较次数的成本都是SN*RN。假设外表内表都是1万条记录，那么其读取的记录数量和Join的比较次数都需要上亿。实际上数据库并不会使用到SNLJ算法，而是会去使用BNJL算法，因为SNLJ实在是太慢！

**mysql 什么时候会去使用SMLJ？**

其实mysql
~~~
SET optimizer_switch = 'block_nested_loop=off'; 
~~~
