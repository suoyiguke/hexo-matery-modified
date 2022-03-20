---
title: mysql-用户自定义变量.md
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
title: mysql-用户自定义变量.md
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
> 或为出师表，鬼神泣壮烈。

1、使用自定义变量的查询，无法使用查询缓存。
2、不能在使用常量或者标识符的地方使用自定义变量，例如表名、列名和LIMIT子句中。
3、用户自定义变量的生命周期是在一个连接中有效，所以不能用它们来做连接间的通信！
> 经过我的实践，打开一个连接，申明赋值一个变量。然后重新打开另一个连接，新的连接访问变量为NULL; 所以一般只将自定义变量用户在 一个事务上下文中

4、如果使用连接池或者持久化连接，自定义变量可能让看起来毫无关系的代码发生交互。`因为连接可能被重用`

5、不能显式地申明自定义变量的类型。确认未定义变量的具体类型的时机在不同mysql版本中可能不一样。如果你希望是整数类型那么最好是在申明时同时赋值为0、字符串类型赋值为`''`、浮点类型就赋值为0.0。用户自定义变量的类型在赋值的时候会改变。mysql的用户自定义变量是一个动态类型。

> 所以使用SET定义变量请这样使用
~~~
SET @a := 0;
SELECT @a;

SET @b := 0.0;
SELECT @b;

SET @c := '';
SELECT @c;
~~~


6、mysql优化器在某些场景下可能会将这些变量优化掉，这可能导致代码不按预想的方式运行。


7、也可使用 = 赋值，但是为了避免歧义、请始终使用:=赋值

8、用户自定义变量具有`左值`特性；在对一个变量赋值的同时可以使用这个变量。（有点像链式操作，lombox的setXxx()具有返回值一样的功能）

~~~
SELECT  @age:= 22;
~~~
9、也可以在select语句中使用 INTO 对变量进行赋值

~~~
SELECT 'abc' INTO @x;
SELECT @x;
~~~
> 如果使用@x形式的用户变量，需要注意给变量赋值的两种方式的区别： `INTO` 和 `:=`的区别， 在`触发器`中需要使用`INTO`而不是 `:=`，因为 `:=` 会返回结果集，触发器中不允许返回结果集！报错 `Not allowd to return  a result set from trigger`
###mysql用户自定义变量赋值和读取的细节
使用用户自定义变量的一个最常见的问题就是没有注意到在赋值和读取变量的时候可能是在查询的不同阶段。例如下面的查询在where条件中过滤行号变量小于等于的记录：

~~~
-- 1 返回二条记录
SET @rownum := 0;
SELECT id,@rownum := @rownum + 1 AS cnt
FROM tb_box
WHERE @rownum <=1;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-68b71514cecf83a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
> 查询就居然返回了cnt字段为2的记录。很奇怪吧？对此只能做出假设：WHERE @rownum <=1; 操作在 @rownum := @rownum + 1 之后执行。

对此，我们可以这样解决，让变量的赋值和取值发生在执行查询的同一阶段：将变量和赋值操作都写如where条件中

~~~
-- 3 返回一条记录
SET @rownum := 0;
SELECT id,@rownum  AS cnt
FROM tb_box
WHERE (@rownum:= @rownum+1)<=1;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f200211b7bb56424.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###mysql用户自定义变量的应用
######使用变量来实现行号的功能
~~~
SET @rownum := 0;
SELECT  id,@rownum:= @rownum+ 1 AS rownum from tb_box  LIMIT 10
~~~


######分组统计类型之间的数据数量排名，相同数量视为同级

~~~
SET @curr := 0,@prev := 0,@rank :=0;
SELECT
	point_id,
	@curr := COUNT( * ) AS  curr,
	@rank := IF(@curr <> @curr,@rank+1,@rank) AS rank,
	@prev := @curr AS prev
FROM
	tb_box 
GROUP BY
	point_id 
ORDER BY curr DESC
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c05e196eec29fb7b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 这里出现了一个诡异的现象，rank和prev列均为0；有可能是变量名写错了（mysql用户变量使用错误并不会报错，这一点不友好）；这里并不是这个原因，可能是由于变量赋值的时间和我们预料的不同。解决方案是在FROM中还有子查询生成一个中间的临时表
~~~

SET @curr := 0,@prev := 0,@rank :=0;
SELECT
	point_id,
	@curr := ct AS ct,
	@rank := IF(@prev <> @curr,@rank+1,@rank) AS rank,
	@prev := @curr AS prev
FROM(
SELECT point_id ,COUNT( * ) AS ct
FROM
	tb_box 
GROUP BY
	point_id 
ORDER BY ct DESC
) TB
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fac1018ad9d4ba3d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######更新的同时获取更新后的数据
~~~
update tb_box set house_address = '测试地址2' WHERE id = 10 AND @house_address := '测试地址2';
SELECT @house_address;

~~~

######ON DUPLICATE KEY UPDATE批量插入语句中，分别统计
表结构
~~~
CREATE TABLE `test`.`test_update_num`  (
  `id` tinyint(100) NOT NULL,
  `num` int(255) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
~~~
插入和更新的数量
~~~
set @x := 0;
INSERT INTO `test`.`test_update_num`(`id`, `num`) VALUES (1,1 ), (2,1 ), (3,1), (4,1 ), (5,1), (6,1),(7,1),(8,1)  ON DUPLICATE KEY UPDATE num =  VALUES(num) + (0 * (@x := @x + 1));
SELECT @x '更新数量';
~~~
我们最终也是查询这个  @x 变量来得到更新的数量。至于插入的数量我们可以通过 ` 批量INSERT语句的影响行数 - @x` 得到，若 ` 批量INSERT语句的影响行数` 为0 则插入数量为0,此时全为更新。

######编写偷懒的 UNION
假设需要编写一个UNION查询，其第一个子查询作为分支条件先执行，如果找到匹配的行，则跳过第二个分支。

在某些业务场景中确实会有这样的需求，比如先在一个频繁访问的表中查找“热”数据，找不到再去另外一个较少访问的表查找“冷”数据；

下面的查询先到 tb_box中查找id='1999999'的记录，若找到了则不去执行查询tb_box_cp；若没找到再去tb_box_cp中找。
~~~
SELECT GREATEST(@found := -1,id) AS id,'tb_box' AS which_tbl FROM tb_box WHERE id ='1999999' 
UNION ALL
SELECT id, 'tb_box_cp'
FROM tb_box_cp WHERE id ='1999999' AND @found IS NULL
UNION ALL
SELECT 1,'reset' FROM DUAL WHERE (@found := NULL ) IS NOT NULL;
~~~

