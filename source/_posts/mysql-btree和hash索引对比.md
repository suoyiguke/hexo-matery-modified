---
title: mysql-btree和hash索引对比.md
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
title: mysql-btree和hash索引对比.md
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
>莫等闲、白了少年头，空悲切

只有 `MEMORY` 存储引擎的表才可以选择使用 BTREE 索引或者 HASH 索引，像我们`常用的innodb只支持btree索引`。两种不同类型的索引各有其不同的适用范围。

######HASH 索引的优势
Hash索引只能用于对等比较，例如=,<=>（相当于=）操作符。时间复杂度是O(1)，一次查找便能定位数据，不像BTree索引需要从根节点到枝节点，最后才能访问到页节点这样多次IO访问，所以Hash在`单值查询`下检索效率远高于BTree索引。 

但是，事实上我们更多情况是使用btree而不是hash


######既然hash索引的查找那么高效，为什么 不都使用hash索引？
HASH 索引有一些重要的特征需要在使用的时候特别注意，如下所示。
>1、只用于使用 `=` 或 `<=>`  操作符的等式比较，当然还有`in`这种范围条件（因为IN可以看做是多个等值比较）。
 2、HASH 索引不能用来排序。优化器不能使用 HASH 索引来加速 ORDER BY 操作。
3、HASH 索引不能用来分组。优化器不能使用 HASH 索引来加速 GROUP BY 操作。
4、hash索引计算后的结果，是随机的，如果是在磁盘上安置数据。以主键为id为例，那么随着id的增长，id对应的行在磁盘上随机放置。查的时候虽然快，但是取的话也慢
5、必须回行，就是说通过索引拿到数据位置，必须回表中取数据
6、无法使用前缀索引，hash('helloword')和hash('hello')两者的关系仍为随机





下面我们可以进行验证：

######实验准备
创建一个city_memory表，其中 country_id字段上加了 `HASH索引`
~~~
CREATE TABLE `test`.`Untitled`  (
  `city_id` smallint(5) UNSIGNED NOT NULL AUTO_INCREMENT,
  `city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `country_id` smallint(5) UNSIGNED NOT NULL,
  `last_update` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`city_id`) USING HASH,
  INDEX `idx_fk_country_id`(`country_id`) USING HASH
) ENGINE = MEMORY AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Fixed STORAGE MEMORY;
~~~

插入数据
~~~
INSERT INTO `test`.`city_memory`(`city_id`, `city`, `country_id`, `last_update`) VALUES (1, '广州', 1, '2020-04-04 16:17:52');
INSERT INTO `test`.`city_memory`(`city_id`, `city`, `country_id`, `last_update`) VALUES (2, '深圳', 2, '2020-04-04 16:34:49');
INSERT INTO `test`.`city_memory`(`city_id`, `city`, `country_id`, `last_update`) VALUES (3, '上海', 3, '2020-04-04 16:35:15');
INSERT INTO `test`.`city_memory`(`city_id`, `city`, `country_id`, `last_update`) VALUES (4, '北京', 4, '2020-04-04 16:35:23');
INSERT INTO `test`.`city_memory`(`city_id`, `city`, `country_id`, `last_update`) VALUES (5, '杭州', 5, '2020-04-04 16:35:35');

~~~

######查询计划分析where条件

1、先开看这条等值条件sql
~~~
 explain SELECT * FROM city_memory WHERE country_id =  1
 explain SELECT * FROM city_memory WHERE country_id <=>  1
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d4aede94367ea9c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可见使用 `=` 和 `<=>`这种确定条件是能够用上hash索引的。

2、那么再来看 大于和小于条件sql
~~~
 explain SELECT * FROM city_memory WHERE country_id  > 1
 explain SELECT * FROM city_memory WHERE country_id  < 1
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-45c4323bf47a9779.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
对于 `>` 和　`<` 这种范围条件不能用到hash索引。而 btree是能用到的，只是说之后的查询条件无法用到索引。证明如下：
~~~
 show INDEX FROM city_memory
 explain SELECT * FROM city_memory WHERE country_id  > 1
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-20965bbaecb5e4cb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


3、那么in这种范围条件呢？
~~~
show INDEX FROM city_memory
explain SELECT * FROM city_memory WHERE country_id in (1,2)
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-663393235eb54bb8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
in 条件对于hash来说是支持的，同样btree当然也支持。而且btree索引在使用in条件找数据时相对于hash性能更好，因为rows由4变为2（说明使用btree扫描2行即可找到）证明如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-668d6d60757b442d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、 BETWEEN  ..  AND .. 条件呢？
![image.png](https://upload-images.jianshu.io/upload_images/13965490-633e4e840e9cf5d8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 BETWEEN  ..  AND .. 条件在 不会用到hash索引！再来看看 btree的情况：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3fd6f0295193556b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
BETWEEN  ..  AND .. 条件能够使用到btree索引。


5、like 条件呢？
为了使用like条件，我们先将country_id类型改为 varchar
~~~
ALTER TABLE `test`.`city_memory` 
MODIFY COLUMN `country_id` varchar(5) NOT NULL AFTER `city`
~~~

我们再来执行：
~~~
show INDEX FROM city_memory
explain SELECT * FROM city_memory WHERE country_id  like '1%'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-da2f9ab926c2cb74.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
like条件会让hash索引失效。我们再来看btree下的like怎样：

好的，btree下也支持 like的不带开头%的访问查询
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a76d29fdcf379d42.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######查询计划分析排序和分组

1、先来看hash索引支不支持排序
![image.png](https://upload-images.jianshu.io/upload_images/13965490-894eab5fed1e4136.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
hash索引果然不能用在排序中，这多么致命呀！产生了 Using filesort文件内排序。性能上是个大坑。

2、同样，我们知道分组是要基于排序的。排序不使用索引，分组当然也不使用索引了。验证如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0fd0059a0619ef42.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

最终不仅没使用到索引，还产生了文件内排序和使用临时表。

###总结

当使用 MEMORY 引擎表的时候，如果是默认创建的 HASH索引，就要注意 SQL 语句的编写，确保可以使用上索引，如果索引字段需要 范围查询、排序、分组 就请使用btree索引；
