---
title: mysql-索引概念和使用建议.md
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
title: mysql-索引概念和使用建议.md
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
###什么是索引
MySQL官方对索引的定义为：索引(Index)是帮助MySQL高效获取数据的`数据结构`。
可以得到索引的本质：索引是`数据结构`
你可以简单理解为：排好序的快速查找数据结构。

###索引用处
提高`检索`速度和`排序`速度
检索+排序
###mysql索引分类
- 单值索引 即一个索引只包含单个列。一个表可以有多个单列索引（建议一张表不要建立超过5个索引）；在查询数据时只使用一个字段做where条件，比如银行系统里的银行卡号,就经常用来查询。此时可以使用单值索引

- 复合索引 即一个索引包含多个列。`如果有多个字段做where条件，那么请使用复合索引` ； 配合 `最左前缀原则` ，举个例子： 创建了一个 a,b,c 的复合索引。那么就相当于创建了 a、a,b、a,b,c 这三个索引；可见这一份索引空间就相当于三份空间。当然符合索引的效率高了

###mysql索引类型
- UNIQUE 唯一索引 索引列的值必须唯一，但允许有空值；
- SPATIAL 空间索引
- NORMAL 普通索引
- FULLTEXT 全文索引
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5989c610df96bb26.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###mysql的索引实现方法
我们平时所说的索引，如果没有特别指明，都是指B树(多路搜索树，并不一定是二叉树)结构组织的索引。其中聚集索引，次要索引，覆盖索引，复合索引，前缀索引，唯一索引`默认都是使用B+树索引`，统称索引。当然,除了B+树这种类型的索引之外，还有哈希索引(hash index)等。
- B+树索引 BTREE
- 哈希索引  HASH
![image.png](https://upload-images.jianshu.io/upload_images/13965490-547edc448630dfca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###索引优势和劣势
####优势：
- 类似大学图书馆建书目索引，提高数据检索效率，降低数据库的IO成本；
- 通过索引列对数据进行排序，降低数据排序成本，降低了CPU的消耗
####劣势：
- 实际上索引也是一张表，该表保存了主键和索引字段，并指向实体表的记录,所以索引列也是要占用空间的；
- 虽然索引大大提高了查询速度，同时却会降低更新表的速度,如果对表INSERT,UPDATE和DELETE。因为更新表时，MySQL不仅要不存数据，还要保存一下索引文件每次更新添加了索引列的字段，都会调整因为更新所带来的键值变化后的索引信息

- 索引只是提高效率的一个因素，如果你的MySQL有大数据量的表，就需要花时间研究建立优秀的索引，或优化查询语句

###那些情况应该建立索引？
- 主键自动建立唯一索引
- 频繁作为查询条件的字段应该建立索引
- 查询中与其它表关联的字段，外键关系建立索引
- 单值/复合索引怎么选择？在高并发下倾向创建组合索引
- 查询中order by 排序的字段适合创建索引，提高排序速度
- 查询中统计和分组 group by的字段适合建立索引

###那些情况不适合建立索引？ 
- 表记录太少 `mysql300万开始性能下降`
- 频繁增删改的字段不适合创建索引
- where条件里用不到的字段不要创建索引
- 数据重复且分布平均的表字段，应该只为最经常查询和最经常排序的数据列建立索引；如果某个数据列包含许多重复的内容，为它建立索引就没有太大的实际效果。比如枚举值：性别、国籍等
- 可以求出`值分布概率`来确定索引效率
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1986780b05215fc9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

