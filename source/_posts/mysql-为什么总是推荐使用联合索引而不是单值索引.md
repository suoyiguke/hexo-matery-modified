---
title: mysql-为什么总是推荐使用联合索引而不是单值索引.md
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
title: mysql-为什么总是推荐使用联合索引而不是单值索引.md
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
有一句话是有谬误的： 在where条件中使用到的字段都加上索引。这个结论似乎成为了好多人的习惯性结论。

事实上我们只需要添加一个联合索引包括这些字段，而不是为每个字段分别添加索引！ 这不仅仅是对空间的浪费，而且真正起作用的只是其中一个！

可以做出实验在验证下：

tb_box 表有100万条数据
~~~
SELECT count(*) FROM tb_box -- 1045408
~~~

查询语句如下：
~~~
EXPLAIN SELECT * FROM tb_box   WHERE sb_number like 'g%' AND create_time >= '2020-04-20 20:33:08' 

~~~

1、先为tb_box的sb_number、create_time字段分别建立a、b索引
![image.png](https://upload-images.jianshu.io/upload_images/13965490-520cb871834475c8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

执行计划如下，key的值为a 表示只是使用到a索引，b索引未使用！而且extra中出现了using where，表明有字段参与where而不是索引直接参与where
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5c48ddf4884d8f19.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

执行时间 0.442秒


2、重新建立索引，为tb_box添加一个联合索引包含sb_number、create_time字段
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a6b9d4984bc08c04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

查看执行计划，a索引被直接使用。索引长度是137比单独创建的131大，说明有更多索引生效。rows=76969比80910小，表明扫描更少的行就能找到结果了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-175f4a0c00d79378.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

执行时间 0.181秒，快了接近4倍

