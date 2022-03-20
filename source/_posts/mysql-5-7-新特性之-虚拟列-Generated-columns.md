---
title: mysql-5-7-新特性之-虚拟列-Generated-columns.md
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
title: mysql-5-7-新特性之-虚拟列-Generated-columns.md
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
有时候需要对字段上加函数然后进行GROUP BY。使用执行分析，发现出现  Using temporary， 分组条件并没有走索引。因为mysql 5.7 的函数会导致索引失效。我们可以通过添加一个冗余字段来保存函数的计算结果，然后添加索引，这时候的GROUP BY就会走索引了。其实mysql 5.7 提供了一个新特性：虚拟列 Generated columns，我们可以使用虚拟列来方便的达到这个目的。

###虚拟列
MySQL的表生成列通常又叫做虚拟列或计算列。这个生成列的值是在列定义时包含了一个计算表达式计算得到的，有两种类型的生成列：

Virtual（虚拟）：这个类型的列会在读取表记录时自动计算此列的结果并返回。
Stored（存储）：这个类型的列会在表中插入一条数据时自动计算对应的值，并插入到这个列中，那么这个列会作为一个常规列存在表中。虚拟生成列有时候比存储生成列更有用，因为它不会占用存储空间。

1、衍生列的定义可以修改，但virtual和stored之间不能相互转换，必要时需要删除重建
2、虚拟列字段只读，不支持 INSRET 和 UPDATE。
3、只能引用本表的非 generated column 字段，不可以引用其它表的字段。
4、使用的表达式和操作符必须是 Immutable 属性。
5、支持创建索引。
6、可以将已存在的普通列转化为stored类型的衍生列，但virtual类型不行；同样的，可以将stored类型的衍生列转化为普通列，但virtual类型的不行。
7、MySQL可以在衍生列上面创建索引。对于stored类型的衍生列，跟普通列创建索引无区别。
8、对于virtual类型的衍生列，创建索引时，会将衍生列值物化到索引键里，即把衍生列的值计算出来，然后存放在索引里。如果衍生列上的索引起到了覆盖索引的作用，那么衍生列的值将直接从覆盖索引里读取，而不再依据衍生定义去计算。

9、针对virtual类型的衍生列索引，在insert和update操作时会消耗额外的写负载，因为更新衍生列索引时需要将衍生列值计算出来，并物化到索引里。`但即使这样，virtual类型也比stored类型的衍生列好`，有索引就避免了每次读取数据行时都需要进行一次衍生计算，同时stored类型衍生列实际存储数据，使得聚簇索引更大更占空间。

10、virtual类型的衍生列索引使用 MVCC日志，避免在事务rollback或者purge操作时重新进行不必要的衍生计算。

>注意，出于性能的考虑，选择Virtual 而不是 Stored



###一个使用虚拟列的优化案例
####1、时间格式化
表结构如下
~~~
CREATE TABLE `iam`.`biz_cloudsign_login`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `business_system_code` int(11) NOT NULL,
  `user_department` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `employee_num` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `identity_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `client_id` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `client_ip` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `random_num` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cert_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `encrypted_token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `updated_at` datetime(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 302 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
~~~

查询语句
~~~
SELECT
	DATE_FORMAT(v.updated_at,   '%Y-%m-%d'),
	count(DATE_FORMAT(v.updated_at,   '%Y-%m-%d'))
FROM
	biz_cloudsign_login v
	INNER JOIN ( SELECT MAX( id ) 'id' FROM biz_cloudsign_login GROUP BY employee_num,DATE_FORMAT(updated_at, '%Y-%m-%d') ORDER BY NULL ) c ON v.id = c.id
	GROUP BY DATE_FORMAT(v.updated_at,   '%Y-%m-%d') ORDER BY NULL
~~~
执行分析，出现Using temporary;  并且有两个步骤中key为空
![image.png](https://upload-images.jianshu.io/upload_images/13965490-030af8d9216ce889.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

分别给updated_at 、 employee_num,updated_at 加上索引
~~~
ALTER TABLE `iam`.`biz_cloudsign_login` 
ADD INDEX `idx_updated_at`(`updated_at`),
ADD INDEX `idx_employee_num_updated_at`(`employee_num`, `updated_at`);
~~~
再次进行查询分析看看效果，extra出现 using index，key也多出了索引名。但是 Using temporary 仍然存在， GROUP BY仍然没走索引！其实也不难理解，因为这个查询语句的GROUP BY条件包含了函数。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-ba78424a9b63f191.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在mysql5.7版本之前可以增加一个冗余字段，为了不修改代码，可以使用触发器，维护这个字段的默认值为DATE_FORMAT(updated_at,   '%Y-%m-%d') ，然后在这个字段上group by。
5.7版本则可以使用虚拟列 Generated columns 虚拟列来实现，添加一个Virtual  类型的 虚拟列，指定表达式为date_format(`updated_at`,'%Y-%m-%d') ：
~~~
ALTER TABLE `iam`.`biz_cloudsign_login` 
ADD COLUMN `update_at_date` date GENERATED ALWAYS AS (date_format(`updated_at`,'%Y-%m-%d')) Virtual NULL AFTER `updated_at`;

~~~

将之前的索引干掉后重新添加索引
~~~
ALTER TABLE `iam`.`biz_cloudsign_login` 
ADD INDEX `idx_updated_at`(`update_at_date`),
ADD INDEX `idx_employee_num_updated_at`(`employee_num`, `update_at_date`);
~~~


查询的sql修改如下
~~~
EXPLAIN
SELECT
    update_at_date,
    count(update_at_date)
FROM
    biz_cloudsign_login v force index(idx_updated_at) 
    INNER JOIN ( SELECT MAX( id ) 'id' FROM biz_cloudsign_login force index(idx_employee_num_updated_at) GROUP BY employee_num,update_at_date ORDER BY NULL ) c ON v.id = c.id
    GROUP BY v.update_at_date ORDER BY NULL
~~~

执行分析，终于 Using temporary消失了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-dd59dada79f92894.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####2、使用虚拟列优化using filesort
5.7中并没有倒排索引的支持，那么我们应该如何优化 非同升同降的order by？
~~~
CREATE TABLE `t` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `a` int(255) DEFAULT NULL,
  `b` int(255) DEFAULT NULL,
  `c` int(255) DEFAULT NULL,
  `sort_b` int(255) GENERATED ALWAYS AS (-(`b`)) VIRTUAL,
  PRIMARY KEY (`id`),
  KEY `idx1` (`a`,`b`,`c`),
  KEY `idx2` (`a`,`sort_b`,`c`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4
~~~
ORDER BY a ASC,B DESC,CASC
按普通列查询出现filesort
~~~
mysql> EXPLAIN SELECT * from t force index(idx1) order by a,b desc,c;
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+----------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra          |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+----------------+
|  1 | SIMPLE      | t     | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    3 |   100.00 | Using filesort |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+----------------+
1 row in set (0.02 sec)
~~~
建立虚拟列 `sort_b` int(255) GENERATED ALWAYS AS (-(`b`)) VIRTUAL, 
和索引后：
~~~
mysql> EXPLAIN SELECT * from t force index(idx2) order by a,sort_b,c ;
+----+-------------+-------+------------+-------+---------------+------+---------+------+------+----------+-------+
| id | select_type | table | partitions | type  | possible_keys | key  | key_len | ref  | rows | filtered | Extra |
+----+-------------+-------+------------+-------+---------------+------+---------+------+------+----------+-------+
|  1 | SIMPLE      | t     | NULL       | index | NULL          | idx2 | 15      | NULL |    3 |   100.00 | NULL  |
+----+-------------+-------+------------+-------+---------------+------+---------+------+------+----------+-------+
1 row in set (0.02 sec)
~~~

####3、结合JSON字段加虚拟列、索引


###mysql 8 支持函数索引，直接使用函数会走索引的

这个有时间使用mysql8验证下

