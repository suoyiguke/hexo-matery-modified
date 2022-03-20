---
title: mysql-分区PARTITIONS之基本使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: mysql-分区PARTITIONS之基本使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---

###分区的使用
当数据表中的数据量很大时，分区带来的效率提升才会显现出来。
只有检索字段为分区字段时，分区带来的效率提升才会比较明显。因此，  `分区字段的选择很重要`，并且`业务逻辑要尽可能地根据分区字段做相应调整`（尽量使用分区字段作为查询条件）。

######分区优点
1、分区表对业务透明，只需要维护一个表的数据结构。
2、DML操作加锁仅影响操作的分区，不会影响未访问分区。
3、通过分区交换快速将数据换入和换出分区表。
4、通过TRUNCATE操作快速清理特定分区数据。
5、通过强制分区仅访问特定分区数据，减少操作影响。
6、通过大数据量分区能有效降低索引层数，提高查询性能。

> 我的理解是，分区就类似于水平分表。将记录按一定规则划分到一些区域
######mysql 5.7中查看分区功能
~~~
SHOW PLUGINS
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8d1c8b3d24ee1d73.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###分区使用

1、创建表时指定分区
~~~

CREATE TABLE `test`.`test_pa`(
  `id` int(11) NOT NULL,
  `t` date NOT NULL,
  PRIMARY KEY (`id`, `t`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic PARTITION BY RANGE (to_days(t))
PARTITIONS 3
(PARTITION `p737899` VALUES LESS THAN (737899) ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p737999` VALUES LESS THAN (737999) ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p738000` VALUES LESS THAN (738000) ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 )
;
 
~~~
物理文件：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-388f4ce8fc1e467a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、插入数据
~~~
insert into test_pa values (1,"2010-07-22"),(2,"2010-08-22"),(3,"2010-08-23"),(4,"2010-08-24");
~~~

3、查询 `information_schema.partitions` 表得到该表的分区信息
~~~
SELECT
    PARTITION_NAME AS '分区名',
    TABLE_ROWS AS '记录数' ,
		PARTITION_DESCRIPTION '范围'
FROM
    information_schema.PARTITIONS 
WHERE
    table_schema = 'test' 
    AND table_name = 'box_fenqu';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0c1b5d75c91cbbe8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


4、查询计划分析
~~~
EXPLAIN SELECT * FROM test_pa
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f6601abdc18c50e7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

5、添加分区
~~~
alter table test_pa add partition (PARTITION pmax VALUES LESS THAN maxvalue ENGINE = InnoDB  )
~~~
若报错：
> 1481 - MAXVALUE can only be used in last partition definition;表示这里不能再定义到MAXVALUE 分区之后了

6、修改/覆盖/合并分区
~~~
alter table test_pa REORGANIZE PARTITION p100,p200,pmax into (
 PARTITION p100 VALUES LESS THAN (100) ENGINE = InnoDB,
 PARTITION p200 VALUES LESS THAN (200) ENGINE = InnoDB
)
~~~
报错
> 1520 - Reorganize of range partitions cannot change total ranges except for last partition where it can extend the range；
重新分区时，如果原分区里面存在maxvalue则新的分区里面也必须包含maxvalue否则就错误。

所以需要添加pmax 分区，一同修改
~~~
alter table test_pa REORGANIZE PARTITION p737899,p737999,p738000,pmax into (
 PARTITION p837899 VALUES LESS THAN (837899) ENGINE = InnoDB,
 PARTITION p837999 VALUES LESS THAN (837999) ENGINE = InnoDB,
 PARTITION p838000 VALUES LESS THAN (838000) ENGINE = InnoDB,
 PARTITION pmax VALUES LESS THAN maxvalue ENGINE = InnoDB
)
~~~

7、删除分区
>注意：删除分区时，数据也同样会被删除；如果希望从所有分区删除所有的数据，但是又保留表的定义和表的分区模式，请使用TRUNCATE TABLE命令。
~~~
alter table test_pa drop partition pmax;
~~~


8、查询具体分区的下数据
> p737899是分区名
~~~
select * FROM  test_pa partition(p737899)
~~~

###分区的限制
MySQL分区的限制

-   最大分区数目不能超过1024
-   如果含有唯一索引或者主键，则分区列必须包含在所有的唯一索引或者主键在内
-   不支持外键
-   不支持全文索引（fulltext）
- 不支持查询缓存query cache

###重新命名/划分分区
~~~
alter table box_fq REORGANIZE PARTITION  p201901,p201902,p201903,p201904,p201905,p201906,p201907,p201908,p201909,p201910,p201911,p201912,p202001,p202002,p202003,p202004,p202005 into (
PARTITION `p0` VALUES LESS THAN ('2019-01-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p1` VALUES LESS THAN ('2019-02-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p2` VALUES LESS THAN ('2019-03-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p3` VALUES LESS THAN ('2019-04-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p4` VALUES LESS THAN ('2019-05-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p5` VALUES LESS THAN ('2019-06-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p6` VALUES LESS THAN ('2019-07-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p7` VALUES LESS THAN ('2019-08-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p8` VALUES LESS THAN ('2019-09-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p9` VALUES LESS THAN ('2019-10-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p10` VALUES LESS THAN ('2019-11-01')ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p11` VALUES LESS THAN ('2019-12-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p12` VALUES LESS THAN ('2020-01-01') ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p13` VALUES LESS THAN ('2020-02-01')  ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p14` VALUES LESS THAN ('2020-03-01')  ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p15` VALUES LESS THAN ('2020-04-01')  ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 ,
PARTITION `p16` VALUES LESS THAN MAXVALUE  ENGINE = InnoDB MAX_ROWS = 0 MIN_ROWS = 0 
)

~~~
