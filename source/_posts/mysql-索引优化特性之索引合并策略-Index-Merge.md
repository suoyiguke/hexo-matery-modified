---
title: mysql-索引优化特性之索引合并策略-Index-Merge.md
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
title: mysql-索引优化特性之索引合并策略-Index-Merge.md
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
 https://dev.mysql.com/doc/refman/8.0/en/index-merge-optimization.html

####什么是Index Merge？Index Merge的限制有哪些？

如果查询中使用到了不同的索引，可以对不同索引的条件分别进行范围扫描，然后将扫描结果合并得到最终的结果，这就是Index Merge。
限制：只能合并同一个表的索引扫描结果，不能跨表合并。
此外，无法对fulltext索引进行合并

###如何查看语句是否使用了Index Merge？
EXPLAIN中type列的值为index_merge表示使用了索引合并。根据索引合并算法的不同，会在Extra列中显示- 
- Using intersect
- union
-  sort_union

###Index Merge有哪几种？分别适用于那些情景？
3种：Intersection,Union,Sort_union

- Intersection：使用AND结合的关于不同索引的条件（普通索引的等值表达式或者主键索引的范围表达式）
- Union
- Sort Union：使用OR结合的关于不同索引的范围条件


### 对于Index Merge的态度
持悲观心态，出现这个就说明索引创建的不够优秀；

>索引合并策略有时候是一种优化的结果，**但实际上更多时候说明了表上的索引建得很糟糕:**

1、当出现服务器对多个索引做相交操作时（通常有多个AND条件)，**通常意味着需要一个包含所有相关列的多列索引，而不是多个独立的单列索引。**

2、当服务器需要对多个索引做联合操作时（通常有多个OR条件)，通常需要耗费大量CPU和内存资源在算法的缓存、排序和合并操作上。特别是当其中有些索引的选择性不高,需要合并扫描返回的大量数据的时候。

3、**更重要的是，优化器不会把这些计算到“查询成本”(cost)中，优化器只关心随机页面读取。这会使得查询的成本被“低估”,导致该执行计划还不如直接走全表扫描。（索引倾斜）**这样做不但会消耗更多的CPU和内存资源，还可能会影响查询的并发性，但如果是单独运行这样的查询则往往会忽略对并发性的影响。通常来说，还不如像在MySQL4.1或者更早的时代一样，将查询改写成UNION的方式往往更好。


如果在EXPLAIN中看到有索引合并，应该好好检查一下查询和表的结构，看是不是已经是最优的。也可以通过参数optimizer_switch来关闭索引合并功能。也可以使用IGNORE INDEX提示让优化器忽略掉某些索引。



###关闭索引合并
因为mysql优化器索引倾斜。 有时候关闭索引合并，让mysql优化器走其它的执行计划效率会更好。

在optimizer_swith中有4个关于Index Merge的变量：
index_merge,index_merge_intersection,index_merge_union,index_merge_sort_union
默认情况下都是启用的。要单独启用某个算法，设置index_merge=off，并将相应的标志设置为on

~~~
SET GLOBAL optimizer_switch = 'index_merge=OFF,index_merge_union=OFF,index_merge_sort_union=OFF,index_merge_intersection=OFF';
SELECT @@optimizer_switch;
~~~



###遇到的相关问题
1、大佬们有碰到过， index merge 导致的全表扫描吗 
黄建:
跑出执行计划是这样的
黄建:把 index_merge 关了就正常走了
~~~

*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: m
   partitions: NULL
         type: ref
possible_keys: idx_code,idx_goods_no,idx_yn,idx_route,idx_goodsno_yn_code
          key: idx_goodsno_yn_code
      key_len: 95
          ref: const,const
         rows: 2
     filtered: 2.50
        Extra: Using where
*************************** 2. row ***************************
           id: 1
  select_type: SIMPLE
        table: d
   partitions: NULL
         type: ALL
possible_keys: idx_code,idx_goods_no,idx_yn,idx_route_yn
          key: NULL
      key_len: NULL
          ref: NULL
         rows: 1418982
     filtered: 0.00
        Extra: Using where
2 rows in set, 1 warning (0.03 sec)     
~~~

      
