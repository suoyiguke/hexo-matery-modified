---
title: explain之select_type列.md
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
title: explain之select_type列.md
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
该列表示select的类型。具体包含了如下11种类型：

![图片](https://upload-images.jianshu.io/upload_images/13965490-dd29633f4d958cdf?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

但是常用的其实就是下面几个：

| 类型 | 含义 |
| --- | --- |
| SIMPLE | 简单SELECT查询，不包含子查询和UNION |
| PRIMARY | 复杂查询中的最外层查询，表示主要的查询 |
| SUBQUERY | SELECT或WHERE列表中包含了子查询 |
| DERIVED | FROM列表中包含的子查询，即衍生 |
| UNION | UNION关键字之后的查询 |
| UNION RESULT | 从UNION后的表获取结果集 |

下面看看这些SELECT类型具体是怎么出现的：

1.  SIMPLE

    执行sql如下：

    ```
    explain select * from test1;
    ```

    结果：

    ![图片](https://upload-images.jianshu.io/upload_images/13965490-0b95541ff861a643?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

    它只在简单SELECT查询中出现，不包含子查询和UNION，这种类型比较直观就不多说了。

2.  PRIMARY 和 SUBQUERY

    执行sql如下：

    ```
    explain select * from test1 t1 where t1.id = (select id from  test1 t2 where  t2.id=2);
    ```

    结果：

    ![图片](https://upload-images.jianshu.io/upload_images/13965490-20f0ae8f92ee5099?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

    我们看到这条嵌套查询的sql中，最外层的t1表是PRIMARY类型，而最里面的子查询t2表是SUBQUERY类型。

3.  DERIVED

    执行sql如下：

    ```
    explainselect t1.* from test1 t1inner join (select max(id) mid from test1 group by id) t2on t1.id=t2.mid
    ```

    结果：

    ![图片](https://upload-images.jianshu.io/upload_images/13965490-6f827a5cf34f3ee9?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

    最后一条记录就是衍生表，它一般是FROM列表中包含的子查询，这里是sql中的分组子查询。

4.  UNION 和 UNION RESULT

    执行sql如下：

    ```
    explainselect * from test1unionselect* from test2
    ```

    结果：

    ![图片](https://upload-images.jianshu.io/upload_images/13965490-c57fc5a7cda2e558?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

     test2表是UNION关键字之后的查询，所以被标记为UNION，test1是最主要的表，被标记为PRIMARY。而<union1,2>表示id=1和id=2的表union，其结果被标记为UNION RESULT。

UNION 和 UNION RESULT一般会成对出现。

**此外，回答上面的问题：****id列的值允许为空吗？**

如果仔细看上面那张图，会发现id列是可以允许为空的，并且是在SELECT类型为： UNION RESULT的时候。

### table列
