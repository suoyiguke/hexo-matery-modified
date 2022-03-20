---
title: mysql-索引优化特性之索引下推.md
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
title: mysql-索引优化特性之索引下推.md
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

>索引下推优化默认开启，索引下推 和联合索引有密切的关系，它让组合索引里的范围条件变得有意义

查询开启状态
~~~
SHOW VARIABLES LIKE '%optimizer_switch%'
~~~

我们可以通过修改系统变量optimizer_switch的index_condition_pushdown标志来控制
~~~
SET optimizer_switch = 'index_condition_pushdown=off'; 
SET optimizer_switch = 'index_condition_pushdown=on';
~~~

对于 test 表，我们现在有（a,b）联合索引，如果现在有一个需求，查出a='k'且b以“l”开头的记录，如下：
~~~
EXPLAIN SELECT * FROM test WHERE a = 'k' AND  b LIKE 'l%'  
~~~
有两种执行可能：
1、根据（a,b）联合索引查询所有满足a = 'k'的记录，然后回表查询出相应的全行数据，然后再筛选出满足b LIKE 'l%' 的记录。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b85cc5bab67293ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、根据（a,b）联合索引查询所有满足a = 'k'的记录，直接筛选出满足b LIKE 'l%' 的索引，之后再回表查询全行数据。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f2abc08dd573f0d6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>当使用explan进行分析时，如果使用了索引条件下推，Extra会显示Using index condition。并不是Using index因为并不能确定利用索引条件下推查询出的数据就是符合要求的数据，还需要通过其他的查询条件来判断。

明显的，第二种方式需要回表查询的全行数据比较少、减少了磁盘IO，这就是mysql的索引下推。

