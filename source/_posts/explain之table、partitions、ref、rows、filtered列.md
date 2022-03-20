---
title: explain之table、partitions、ref、rows、filtered列.md
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
title: explain之table、partitions、ref、rows、filtered列.md
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
###table列
该列的值表示输出行所引用的表的名称，比如前面的：test1、test2等。

但也可以是以下值之一：

<unionM,N>：具有和id值的行的M并集N。
<derivedN>：用于与该行的派生表结果id的值N。派生表可能来自（例如）FROM子句中的子查询 。
<subqueryN>：子查询的结果，其id值为N

###partitions列
该列的值表示查询将从中匹配记录的分区



### ref列

该列表示索引命中的列或者常量。

执行sql如下：

```
explain select *  from test1 t1 inner join test1 t2 on t1.id=t2.id where t1.code='001';
```

结果：

![图片](https://upload-images.jianshu.io/upload_images/13965490-6583ee758a766341?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们看到表t1命中的索引是const(常量)，而t2命中的索引是列sue库的t1表的id字段。

### rows列

该列表示MySQL认为执行查询必须检查的行数。

![图片](https://upload-images.jianshu.io/upload_images/13965490-8ee9ad58be58c704?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

对于InnoDB表，此数字是估计值，可能并不总是准确的。

### filtered列

该列表示按表条件过滤的表行的估计百分比。最大值为100，这表示未过滤行。值从100减小表示过滤量增加。

![图片](https://upload-images.jianshu.io/upload_images/13965490-bdb738ed4bf545bb?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

rows显示了检查的估计行数，rows× filtered显示了与下表连接的行数。例如，如果 rows为1000且 filtered为50.00（50％），则与下表连接的行数为1000×50％= 500。

