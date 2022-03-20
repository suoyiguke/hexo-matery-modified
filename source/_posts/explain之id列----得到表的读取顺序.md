---
title: explain之id列----得到表的读取顺序.md
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
title: explain之id列----得到表的读取顺序.md
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
### id列

该列的值是select查询中的序号，比如：1、2、3、4等，它决定了表的执行顺序。

某条sql的执行计划中一般会出现三种情况：

1.  id相同
2.  id不同
3.  id相同和不同都有

那么这三种情况表的执行顺序是怎么样的呢？

###### 1.id相同

执行sql如下：

```
explain select * from test1 t1 inner join test1 t2 on t1.id=t2.id
```

结果：![图片](https://upload-images.jianshu.io/upload_images/13965490-dc4928efe726fd2b?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们看到执行结果中的两条数据id都是1，是相同的。

这种情况表的执行顺序是怎么样的呢？

答案：从上到下执行，先执行表t1，再执行表t2。

执行的表要怎么看呢？

答案：看table字段，这个字段后面会详细解释。

###### 2.id不同

执行sql如下：

```
explain select * from test1 t1 where t1.id = (select id from  test1 t2 where  t2.id=2);
```

结果：![图片](https://upload-images.jianshu.io/upload_images/13965490-d6ad486171e6bfe5?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们看到执行结果中两条数据的id不同，第一条数据是1，第二条数据是2。

这种情况表的执行顺序是怎么样的呢？

答案：序号大的先执行，这里会从下到上执行，先执行表t2，再执行表t1。

###### 3.id相同和不同都有

执行sql如下：

```
explainselect t1.* from test1 t1inner join (select max(id) mid from test1 group by id) t2on t1.id=t2.mid
```

结果：

![图片](https://upload-images.jianshu.io/upload_images/13965490-0c547ef916f77b7a?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们看到执行结果中三条数据，前面两条数据的的id相同，第三条数据的id跟前面的不同。

这种情况表的执行顺序又是怎么样的呢？

答案：先执行序号大的，先从下而上执行。遇到序号相同时，再从上而下执行。所以这个列子中表的顺序顺序是：test1、t1、

**也许你会在这里心生疑问：`<``derived2>` 是什么鬼？**

它表示派生表，别急后面会讲的。

**还有一个问题：id列的值允许为空吗？**

答案在后面揭晓。


###id顺序不全对

出现依赖子查询的时候会 dpendent subquery 即使是2。也是后执行
![image.png](https://upload-images.jianshu.io/upload_images/13965490-74bdc89022ab85a0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
