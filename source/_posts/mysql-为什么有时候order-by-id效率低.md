---
title: mysql-为什么有时候order-by-id效率低.md
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
title: mysql-为什么有时候order-by-id效率低.md
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
数据准备，这张tb_box中有100万条数据。有id默认的聚簇索引。然后自己在字段create_time上加了一个索引
~~~
CREATE TABLE `test`.`tb_box`  (
  `id` bigint(36) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `create_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  `update_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `sys_org_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属部门',
  `status` int(10) NULL DEFAULT 0 COMMENT '状态',
  `number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '编号',
  `zi_number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '自编号',
  `house_address` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '仓库地址',
  `sb_number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备id',
  `point_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '投放点id',
  `point` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '投放点',
  `confirm` int(32) NULL DEFAULT 0 COMMENT '商户/企业用户确认入库，默认为0（未确认）1是已确认',
  `last_point` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '最近一次投放点名',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `a`(`create_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1079045 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
~~~


先来看看这个where条件中只有create_time ，没有id。然后进行 ORDER BY id desc; 出现了Using filesort。执行时间6.272秒
~~~
mysql> EXPLAIN SELECT * FROM tb_box FORCE index(a) WHERE create_time BETWEEN '2020-04-20 10:33:08' AND  '2020-04-23 20:33:08' ORDER BY id desc;
+----+-------------+--------+------------+-------+---------------+-----+---------+------+--------+----------+---------------------------------------+
| id | select_type | table  | partitions | type  | possible_keys | key | key_len | ref  | rows   | filtered | Extra                                 |
+----+-------------+--------+------------+-------+---------------+-----+---------+------+--------+----------+---------------------------------------+
|  1 | SIMPLE      | tb_box | NULL       | range | a             | a   | 6       | NULL | 515010 |   100.00 | Using index condition; Using filesort |
+----+-------------+--------+------------+-------+---------------+-----+---------+------+--------+----------+---------------------------------------+
1 row in set (0.01 sec)
~~~


再来看这个，ORDER BY create_time  desc。没有出现Using filesort。执行时间3.598 快了将近1半。

~~~
mysql> EXPLAIN SELECT * FROM tb_box FORCE index(a) WHERE create_time BETWEEN '2020-04-20 10:33:08' AND  '2020-04-23 20:33:08' ORDER BY create_time  desc;
+----+-------------+--------+------------+-------+---------------+-----+---------+------+--------+----------+-----------------------+
| id | select_type | table  | partitions | type  | possible_keys | key | key_len | ref  | rows   | filtered | Extra                 |
+----+-------------+--------+------------+-------+---------------+-----+---------+------+--------+----------+-----------------------+
|  1 | SIMPLE      | tb_box | NULL       | range | a             | a   | 6       | NULL | 515010 |   100.00 | Using index condition |
+----+-------------+--------+------------+-------+---------------+-----+---------+------+--------+----------+-----------------------+
1 row in set (0.06 sec)

~~~

思考：为什么order by id 会出现Using filesort 文件内排序呢？明明id上有索引啊？

因为id没有使用在where条件里！order by id，mysql 的优化器会选择主键索引，但是 where 条件里又没有主键条件，导致全表的id都进行排序。

而 order by create_time ，结合 where 条件里 create_time ，mysq 优化器会选择 create_time 索引，扫描的记录数少，效果更好。
