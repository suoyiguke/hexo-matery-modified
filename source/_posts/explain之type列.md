---
title: explain之type列.md
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
title: explain之type列.md
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
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6fb3fedd5256cd84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


该列的值表示连接类型，是查看索引执行情况的一个重要指标。包含如下类型：

![图片](https://upload-images.jianshu.io/upload_images/13965490-0937d7f01d114033?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

执行结果从最好到最坏的的顺序是从上到下。

我们需要重点掌握的是下面几种类型：

system > const > eq_ref > ref > range > index > ALL

在演示之前，先说明一下test2表中只有一条数据：

![图片](https://upload-images.jianshu.io/upload_images/13965490-18e213f29d287728?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

并且code字段上面建了一个普通索引：

![图片](https://upload-images.jianshu.io/upload_images/13965490-7741099ae006694d?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下面逐一看看常见的几个连接类型是怎么出现的：

1.  system

    这种类型要求** 数据库表中只有一条数据** ，是const类型的一个特例，一般情况下是不会出现的。

2.  const

    ** 通过一次索引就能找到数据** ，一般用于主键或唯一索引作为条件的查询sql中，执行sql如下：

    ```
    explain select * from test2 where id=1;
    ```

    结果：

    ![图片](https://upload-images.jianshu.io/upload_images/13965490-cfa1d0c87c47947f?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3.  eq_ref  

   ** 常用于主键或唯一索引扫描** 。执行sql如下：

    ```
    explain select * from test2 t1 inner join test2 t2 on t1.id=t2.id;
    ```

    结果：

    ![图片](https://upload-images.jianshu.io/upload_images/13965490-ac514675a53da97a?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

    此时，有人可能感到不解，const和eq_ref都是对主键或唯一索引的扫描，有什么区别？

     答：const只索引一次，而eq_ref主键和主键匹配，**由于表中有多条数据，一般情况下要索引多次，才能全部匹配上。** 

4.  ref

    常用于** 非主键和唯一索引扫描** 。执行sql如下：

    ```
    explain select * from test2 where code = '001';
    ```

    结果：

    ![图片](https://upload-images.jianshu.io/upload_images/13965490-694f822198bf979f?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

5.  range

    常用于范围查询，比如：between ... and 或 In 等操作，执行sql如下：

    ```
    explain select * from test2 where id between 1 and 2;
    ```

    结果：

    ![图片](https://upload-images.jianshu.io/upload_images/13965490-f0e76f2f06d165c0?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

6.  index

    全索引扫描。执行sql如下：

    ```
    explain select code from test2;
    ```

    结果：

    ![图片](https://upload-images.jianshu.io/upload_images/13965490-d0d1ed9f3f55204e?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

7.  ALL

    全表扫描。执行sql如下：

    ```
    explain select *  from test2;
    ```

    结果：

    ![图片](https://upload-images.jianshu.io/upload_images/13965490-fc2075f2c2bd87e5?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
