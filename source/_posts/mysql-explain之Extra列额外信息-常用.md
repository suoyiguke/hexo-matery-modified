---
title: mysql-explain之Extra列额外信息-常用.md
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
title: mysql-explain之Extra列额外信息-常用.md
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
mysql的sql执行计划中Extra字段是一个优化非常关键的参数

![image.png](https://upload-images.jianshu.io/upload_images/13965490-9d886f397053f72c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Using MRR  read_cache _size
Using temopory temopory_size
Using filesort sort_buffer_size
Using join buffer  join_buffer_size

### Using filesort
文件内排序，出现这个就要优化orderby排序条件。说明mysql会对数据使用文件内排序，而不是按照表内的索引顺序进行读取。也就是说mysql中无法利用索引完成的排序操作称为“文件排序”。

Using filesort出现条件：
1、order by 字段没有创建索引
2、order by 上字段索引失效
3、order by 多字段时没有同升同降
4、order by


因为联合索引的范围条件导致的后面列的索引失效案例，从而出现Using filesort；
解决方式：
- 不使用 order by，可以在应用代码中进行排序
- ORDER BY  sb_number,create_time 重新从第一个索引开始。不过这样的order by 在业务上是没有意义的
- 调整联合索引字段的顺序
- Using filesort 可能因为业务的关系是不可避免的，但是我们可以通过调整mysql参数来对它进行优化


### Using temporary 
（产生中间表，非常需要优化！）使用了临时表保存中间结果，mysql在对查询结果排序的时候使用临时表。常见于order by 和分组查询group by


`ps： 要么不建索引，要建索引，group by 字段一定要和索引的数量和顺序一致 ，否则容易产生文件内排序和产生临时表`

### Using index
表示相应的select操作中使用了`覆盖索引（Covering Index）`，避免访问了表的数据行，效率不错！
- 如果同时出现了Using where ，用到了范围查询

- 如果没有同时出现Using where，用到了等值查询

### Using index condition
 说明查询的字段,其中有字段不存在或全部字段都没有被索引, 所以需要回表查询；效率低于Using where Using index和Using index

###Using where 
存在这个说明有where条件没用到索引

###Using join buffer 
使用了连接缓存，配置文件里的join buffer可以调大

###impossible where  
表示where条件冲突

###select tables optimized away
 在没有group by子句的情况下，基于索引优化min/max操作或者对于MyISAM引擎优化count(*)
直接读取数据

### distinct 
优化distinct，找到第一个匹配的就停止查询

###NULL
用到了索引，但是没用到索引覆盖
