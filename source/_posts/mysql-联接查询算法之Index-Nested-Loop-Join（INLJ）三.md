---
title: mysql-联接查询算法之Index-Nested-Loop-Join（INLJ）三.md
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
title: mysql-联接查询算法之Index-Nested-Loop-Join（INLJ）三.md
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
>Index Nested-Loop Join：INLJ，索引嵌套循环连接

在Join的优化时候，通常都会建议在内表建立索引，以此降低 Simple  Nested-Loop Join算法的开销，减少内表扫描次数，MySQL数据库中使用较多的就是这种算法，以下称为INLJ。来看这种算法的伪代码：
~~~
For each row r in R do                     -- 扫描R表
    lookup s in S index                    -- 查询S表的索引（固定3~4次IO，B+树高度）
        If find s == r                     -- 如果r匹配了索引s
            Then output the tuple <r, s>   -- 返回结果集
~~~
由于内表上有索引，所以比较的时候不再需要一条条记录进行比较，而可以通过索引来减少比较，从而加速查询。可以看到外表中的每条记录通过内表的索引进行访问，就是读取外部表一行数据，然后去内部表索引进行二分查找匹配；而一般B+树的高度为3\~4层，也就是说匹配一次的io消耗也就3~4次，因此索引查询的成本是比较固定的，故优化器都倾向于使用记录数少的表作为外表。故INLJ的算法成本如下表所示：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7cfd85a085f68d39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


上表Smatch表示通过索引找到匹配的记录数量。同时可以发现，通过索引可以大幅降低内表的Join的比较次数，每次比较1条外表的记录，其实就是一次indexlookup（索引查找），而每次index lookup的成本就是树的高度，即IndexHeight。INLJ的算法并不复杂，也算简单易懂。但是效率是否能达到用户的预期呢？其实如果是通过表的主键索引进行Join，即使是大数据量的情况下，INLJ的效率亦是相当不错的。因为索引查找的开销非常小，并且访问模式也是顺序的（假设大多数聚集索引的访问都是比较顺序的）。大部分人诟病MySQL的INLJ慢，主要是因为在进行Join的时候可能用到的索引并不是主键的聚集索引，而是辅助索引，这时INLJ的过程又需要多一步Fetch的过程，而且这个过程开销会相当的大：

 ![image](https://upload-images.jianshu.io/upload_images/13965490-7414e029ace1d7ef?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
由于访问的是辅助索引，如果查询需要访问聚集索引上的列，那么必要需要进行回表取数据，看似每条记录只是多了一次回表操作，但这才是INLJ算法最大的弊端。首先，辅助索引的index lookup是比较随机I/O访问操作。其次，根据index lookup再进行回表又是一个随机的I/O操作。所以说，INLJ最大的弊端是其可能需要大量的离散操作，这在SSD出现之前是最大的瓶颈。而即使SSD的出现大幅提升了随机的访问性能，但是对比顺序I/O，其还是慢了很多，依然不在一个数量级上。




###总结下
1、 索引嵌套循环连接是基于索引进行连接的算法，索引是基于内层表的，通过外层表匹配条件直接与内层表索引进行匹配，避免和内层表的每条记录进行比较， 从而利用索引的查询减少了对内层表的匹配次数，优势极大的提升了 join的性能：

> 原来的匹配次数 = 外层表行数 * 内层表行数
> 优化后的匹配次数= 外层表的行数 * 内层表索引的高度（3~4）

2、  使用场景：只有内层表join的列有索引时，才能用到Index Nested-LoopJoin进行连接。
> 所以 left join 加索引到右表；right join 加索引到左表。

3、 由于用到索引，如果索引是辅助索引而且返回的数据还包括内层表的其他数据，则会回内层表查询数据，多了一些IO操作。回表查询会导致INLJ变慢。
>所以尽量不要查内表的其它数据
   

