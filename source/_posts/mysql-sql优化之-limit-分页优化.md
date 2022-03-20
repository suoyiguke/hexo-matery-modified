---
title: mysql-sql优化之-limit-分页优化.md
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
title: mysql-sql优化之-limit-分页优化.md
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
> 在秦张良椎，在汉苏武节

**LIMIT 分页性能问题**
![上图出自《高性能MYSQL](https://upload-images.jianshu.io/upload_images/13965490-b9fce6bad6aa1b21.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


问题sql： 普通limit
~~~
EXPLAIN SELECT *  FROM emp ORDER BY id LIMIT 5000000,10 
~~~
> 问题sql执行时间 8.231秒，存在性能问题。

**业务层面上的优化**
1、限制用户分页，不允许进行过大的分页。比如说百度的分页，它最多只能跳转到一定页数，用户再往下翻页也只显示最后一页。

2、禁用count(*)，不去查询总条数，不计算总页数，不设计跳页的功能



###下面介绍几种优化思路和手段
**sql层面优化方式**

1、增加冗余的列 “页码” 来定位记录
对条件值可以进行估算，对于几百上千页的检索，往往不需要很精确。也可以专门增加冗余的列来定位记录，比如如下的 查询，有一个page列，指定记录所在的页，代价是在修改数据的时候需要维护这个列的数据，如下面的查询。
~~~
 SELECT * FROM emp WHERE page = 100 ORDER BY name;
~~~
**2、索引覆盖，延时关联**

使用 `索引覆盖，延时关联` 的方式，将大大提高查询效率，它让mysql扫描尽可能少的页面，获取需要访问的记录后再根据关联列回原表查询需要所有的列。这个技术可以用于优化关联查询中的LIMIT字句。

> 我们可以使用  `SELECT id FROM emp ORDER BY id LIMIT 5000000,10` 充当子查询，这样就只在索引中查询id，而不用回表查；然后根据子查询得出来的id集合再去查对应的select * 数据即可;


~~~
EXPLAIN SELECT  * FROM emp INNER JOIN (SELECT id FROM emp ORDER BY id LIMIT 5000000,10 )AS tb USING(id)
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a43cbd8bdc62e580.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 最后查询时间是 5.4 秒，效果在这里并不理想。但是`索引覆盖，延时关联` 的优化思想是非常好的！它不仅是可以用在这里。


> 还有注意一点： 能用 `INNER JOIN` 就不要使用`IN`。比如在这个limit优化中，我使用的是`INNER JOIN` 自关联查询。如果我使用IN呢？情况会如何？

~~~
EXPLAIN SELECT * FROM emp WHERE id IN ( SELECT id from (  SELECT id FROM emp ORDER BY id LIMIT 5000010, 10)tb )  
~~~


> 首先，使用IN 的话最终的查询时间是15.7秒，是使用JOIN的三倍！再来看它的查询计划： 直接多了一个查询！

![image.png](https://upload-images.jianshu.io/upload_images/13965490-bb3fa50ebe203bb3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**4、计算出边界值，直接 BETWEEN AND**

可以将limit查询转换为已知位置的查询，让mysql通过范围扫描获得到对应的结果。
~~~
EXPLAIN SELECT *  FROM emp WHERE id BETWEEN 5000001 AND 5000010 ORDER BY id 
~~~
> 使用BETWEEN .. AND 最终的时间是 0.063秒，少去了大量的扫描操作；使用这种方式的前提是必须要知道id的边界值！同样id必须是连续单调递增的；如果之间有数据被删除掉，或者因为where条件过滤掉，那么最终得到的页数不会是10了吧；所以这种方式局限性太大了




**5、得到上页最后一条记录的id，然后limit**

假设查询返回的是 5000001  到 5000011 的记录，那么下一页查询就可以从这个5000011 开始拿10条数据。这样做无论翻多少也性能都会很好！
~~~
EXPLAIN SELECT *  FROM emp WHERE id >= 5000001 ORDER BY id  LIMIT 10
~~~
> 这种方式查询时间为 0.067。是limit优化的首选。不过它不能实现当前页（无法实现点击页码跳转），只能上一页，下一页的翻页。适合app端分页优化；它要求id是递增的（不能使用uuid等字符串充当id），但id可以不连续（可以使用where过滤、删除数据，都不会影响分页）；我们来看看它的查询计划如下：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-4fca8c011226b648.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###结合索引优化
最终是推荐使用第3个方法：得到上页最后一条记录的id，然后limit；但是若需要同时进行where条件检索、 order by排序的话就必须参加合适的联合索引了！

比如下面的语句，使用ename 进行like的模糊查询， 排序的时候指定id DESC,ename DESC
~~~
EXPLAIN SELECT
	* 
FROM
	emp 
WHERE
	id >= 5000001 
	AND ename LIKE '%a%' 
ORDER BY
	id DESC,
	ename DESC 
	LIMIT 10

~~~
那么先看看查询计划：出现了 Using filesort
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b36a4a92ac3ce38f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后执行下，执行时间为 4.6秒。需要优化！

所以，需要创建联合索引如下 index(id,ename)
~~~
SHOW INDEX  FROM emp
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-49948e24e2b9a32d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

最终查询时间为：0.089 秒，优化成功。再看看它的查询计划：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b7099897055ca850.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
很好，已经没有 Using filesort 了
###其他方法

1、在网上看到有人这样做
~~~
EXPLAIN SELECT
	* 
FROM
	emp 
WHERE
	id >= ( SELECT id FROM emp ORDER BY id LIMIT 5000001, 1 ) 
	LIMIT 10;
~~~
这个方法和上面讲的`索引覆盖` 是一样的，先从索引中找到id，然后通过id查数据。只不过上面是使用JOIN这里使用 >=。这样就必须让id是连续的了。最终查询时间是 4-5 秒。和`索引覆盖`差不多![image.png](https://upload-images.jianshu.io/upload_images/13965490-d82800bf20a7f1f2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、使用Sphinx等搜索引擎来完成分页查询
