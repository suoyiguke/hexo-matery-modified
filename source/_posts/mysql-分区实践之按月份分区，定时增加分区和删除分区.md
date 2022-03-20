---
title: mysql-分区实践之按月份分区，定时增加分区和删除分区.md
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
title: mysql-分区实践之按月份分区，定时增加分区和删除分区.md
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

按月份分区，这样再使用分区字段时间来查询数据将会很快，因为这样只需要扫描指定的分区。

1、创建表，并使用RANGE COLUMNS分区。按创建时间create_time字段分区;分区名使用p0、p1、p2、p3 .. 的形式；create_time字段小于2019-01-01的数据将进入p0 分区，依次类推。。
~~~
CREATE TABLE "box_fenqu" (
  "id" bigint(36) NOT NULL AUTO_INCREMENT COMMENT '主键',
  "create_by" varchar(50) DEFAULT NULL COMMENT '创建人',
  "create_time" datetime NOT NULL COMMENT '创建日期',
  "update_by" varchar(50) DEFAULT NULL COMMENT '更新人',
  "update_time" datetime DEFAULT NULL COMMENT '更新日期',
  "sys_org_code" varchar(64) DEFAULT NULL COMMENT '所属部门',
  "status" int(10) DEFAULT '0' COMMENT '状态',
  "number" varchar(32) DEFAULT NULL COMMENT '编号',
  "zi_number" varchar(32) DEFAULT NULL COMMENT '自编号',
  "house_address" varchar(32) DEFAULT NULL COMMENT '仓库地址',
  "sb_number" varchar(32) DEFAULT NULL COMMENT '设备id',
  "point_id" varchar(32) DEFAULT NULL COMMENT '投放点id',
  "point" varchar(32) DEFAULT NULL COMMENT '投放点',
  "confirm" int(32) DEFAULT '0' COMMENT '商户/企业用户确认入库，默认为0（未确认）1是已确认',
  "last_point" varchar(32) DEFAULT NULL COMMENT '最近一次投放点名',
  PRIMARY KEY ("id","create_time") USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2120001 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC
 PARTITION BY RANGE  COLUMNS(create_time)
(PARTITION p0 VALUES LESS THAN ('2019-01-01') ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN ('2019-02-01') ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN ('2019-03-01') ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN ('2019-04-01') ENGINE = InnoDB,
 PARTITION p4 VALUES LESS THAN ('2019-05-01') ENGINE = InnoDB,
 PARTITION p5 VALUES LESS THAN ('2019-06-01') ENGINE = InnoDB,
 PARTITION p6 VALUES LESS THAN ('2019-07-01') ENGINE = InnoDB,
 PARTITION p7 VALUES LESS THAN ('2019-08-01') ENGINE = InnoDB,
 PARTITION p8 VALUES LESS THAN ('2019-09-01') ENGINE = InnoDB,
 PARTITION p9 VALUES LESS THAN ('2019-10-01') ENGINE = InnoDB,
 PARTITION p10 VALUES LESS THAN ('2019-11-01') ENGINE = InnoDB,
 PARTITION p11 VALUES LESS THAN ('2019-12-01') ENGINE = InnoDB,
 PARTITION p12 VALUES LESS THAN ('2020-01-01') ENGINE = InnoDB,
 PARTITION p13 VALUES LESS THAN ('2020-02-01') ENGINE = InnoDB,
 PARTITION p14 VALUES LESS THAN ('2020-03-01') ENGINE = InnoDB,
 PARTITION p15 VALUES LESS THAN ('2020-04-01') ENGINE = InnoDB,
 PARTITION p16 VALUES LESS THAN ('2020-05-01') ENGINE = InnoDB,
 PARTITION p17 VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) 
~~~

2、创建存储过程proc_create_partition，用它来直接对box_fenqu表进行分区。其实就是将分区名加1，如p2加1就是p3;指定的日期范围就是往后面进一个月，保证最新的分区总是`MAXVALUES`的 ,如20200401就变成20200401和20200501，其中20200401指定范围，20200501为`MAXVALUES`
~~~
CREATE DEFINER="root"@"%" PROCEDURE "proc_create_partition"(in_tbname VARCHAR(64))
BEGIN

SELECT DATABASE() INTO @dbname;

SET @tbname = in_tbname;

#查询表的最近一次分区的名字，这里按自然数递增的。比如0,1,2,4。去掉 p
SELECT
	REPLACE (partition_name, 'p', '') INTO @PMAX
FROM
	INFORMATION_SCHEMA.PARTITIONS
WHERE
	TABLE_SCHEMA = @dbname
AND table_name = @tbname
ORDER BY
	partition_ordinal_position DESC
LIMIT 1;

#查询表的最近一次分区的指定时间,比如最近时间的分区时 2020.04.01
SELECT
REPLACE(partition_description, '\'', '') INTO @DNAME
FROM
	INFORMATION_SCHEMA.PARTITIONS
WHERE
	TABLE_SCHEMA = @dbname
AND table_name = @tbname
ORDER BY
	partition_ordinal_position DESC
LIMIT 1, 1;


SET @t=CONCAT('alter table `',@dbname,'`.',@tbname,' reorganize partition p',@PMAX,
						  ' into(partition p',@PMAX,' values less than (''',date(DATE_ADD(@DNAME,INTERVAL 1 MONTH)),'''),',
							'partition p',@PMAX+1,' values less than MAXVALUE)');

SELECT @t;
PREPARE stmt FROM @t;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

COMMIT;
END
~~~

>这样传入box_fenqu表名即可进行增加分区了： CALL proc_create_partition('box_fenqu');

3、创建mysql事件，定时调度分区；下面的事件到的意思就是从2020-05-03 00:00:00开始，每过一个月就执行下` CALL proc_create_partition('box_fenqu')`
~~~
CREATE DEFINER=`root`@`%` EVENT `e_create_partition` 
ON SCHEDULE EVERY 1 MONTH STARTS '2020-05-03 00:00:00' 
ON COMPLETION PRESERVE DISABLE 
DO CALL proc_create_partition('box_fenqu')
~~~

4、如果有多个表需要都需要定时的动态增加分区的话，就可以再写个存储如下，这个存储过程将对当前库下所有分区表都进行遍历，然后增加分区
~~~
CREATE DEFINER="root"@"%" PROCEDURE "proc_create_partition_all"()
BEGIN

  DECLARE tbname varchar(32);
  DECLARE tmpSql varchar(256);
  DECLARE done INT DEFAULT FALSE ;

#查询已手动分区的表
	DECLARE part_cursor CURSOR FOR (SELECT DISTINCT table_name FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_SCHEMA = DATABASE() AND partition_expression IS NOT NULL AND table_name NOT LIKE '%bak');
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

#循环对表添加分区
	OPEN part_cursor;
		myLoop: LOOP
			FETCH part_cursor INTO tbname;
			IF done THEN 
				LEAVE myLoop;
			END IF;
			#调用分区存储过程
			CALL proc_create_partition(tbname);

			COMMIT;
		END LOOP myLoop;
	CLOSE part_cursor;
	
END
~~~


5、mysql允许创建的分区数量有限，因此我们可以根据业务的情况。定期删除已经不需要的分区


6、查询有数据的最新日期/月份

~~~
select REPLACE(partition_description, '\'', '') date from INFORMATION_SCHEMA.PARTITIONS where TABLE_SCHEMA=SCHEMA() AND TABLE_NAME='box_fenqu' AND table_rows != 0
ORDER BY REPLACE(partition_description, '\'', '') desc limit 1
~~~

查询有数据的数据条数
~~~
select table_rows from INFORMATION_SCHEMA.PARTITIONS where TABLE_SCHEMA=SCHEMA() AND TABLE_NAME='box_fenqu' AND table_rows != 0
ORDER BY REPLACE(partition_description, '\'', '') desc limit 1

~~~

7、插入数据测试，编写存储过程如下
~~~
CREATE DEFINER="root"@"localhost" PROCEDURE "insert_box_fq"(in max_num int(10),in sDate datetime,in eDate datetime)
begin
 declare i int default 0;
 /*把autocommit设置成0*/
 set autocommit= 0;
 repeat
 set i=i+1;
  INSERT INTO `test`.`box_fenqu`(`create_by`, `create_time`, `update_by`, `update_time`, `sys_org_code`, `status`, `number`, `zi_number`, `house_address`, `sb_number`, `point_id`, `point`, `confirm`, `last_point`) VALUES (rand_string(3), getDateTime(sDate,eDate), rand_string(3), now(), 'A03', 0, rand_string(3), 'A001', '仓库1', rand_string(3), rand_string(3), NULL, 1, rand_string(3));


 until i=max_num end repeat;
commit;
end
~~~
> 插入10万条 call insert_box_fq(100000,'2019-01-01 00:00:00',now())

8、查询各个分区数据情况
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

###思考分区结合分页

既然是按日期分区，那么我们在分页查询时就可以使用日期。如下我查询最新的10条数据。效率非常低，因为需要扫描所有的分区。但是事实上我们只需要10条而已，只需要在最新的分区中查找。若最新的分区记录数大于等于10那么就需要前移动一个月份，另外扫描一个分区。依次类推。我想这样应该查询效率很快了吧
~~~
SELECT *  FROM box_fenqu ORDER BY create_time DESC LIMIT 10
~~~

这样需要写一个存储过程来查询，将limit 扫描的分区只锁定在需要的分区里
