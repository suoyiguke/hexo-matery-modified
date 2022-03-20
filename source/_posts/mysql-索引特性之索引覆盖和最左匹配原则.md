---
title: mysql-索引特性之索引覆盖和最左匹配原则.md
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
title: mysql-索引特性之索引覆盖和最左匹配原则.md
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
###索引覆盖
如果要查询的字段都建立过索引，那么引擎会直接在索引表中查询而不会访问原始数据（否则只要有一个字段没有建立索引就会做全表扫描），这叫索引覆盖。因此我们需要尽可能的在select后`只写必要的查询字段`，以增加索引覆盖的几率。

比如，我建立了联合索引 index(a,b,c) ；那么select a、select b、select c、select a,b、select b,c、select a,c、select a,b,c 都是索引覆盖了（索引覆盖的执行计划type字段为 index，extra字段为Using index）；如果出现了其他未建立索引的字段d，如select a,b,c,d 那么就必须回表查询，全表扫描了。（此时执行计划的type字段会是ALL，extra字段会是null）。

> 索引覆盖针对于select条件；索引覆盖不像索引最左匹配那么严格要求，索引覆盖认定的字段上只要存在索引就行。


###索引的最左匹配原则

建立联合索引 index(a,b,c)，那么就相当于同时建立了a、ab、abc 三个索引

建立测试表
~~~
CREATE TABLE `iam`.`test`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `a` char(1) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `b` char(1) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `c` char(1) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `d` char(1) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_a_b_c`(`a`, `b`, `c`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
~~~

联合索引的最左匹配原则
~~~
# 正常使用索引
EXPLAIN SELECT *  FROM test WHERE a = '1' -- key_len=1
EXPLAIN SELECT *  FROM test WHERE a = '1' AND b = '1' -- key_len=2
EXPLAIN SELECT *  FROM test WHERE a = '1' AND b = '1' AND c = '1' -- key_len=3


# 存在索引失效
EXPLAIN SELECT *  FROM test WHERE a = '1' AND c = '1' -- key_len=1
EXPLAIN SELECT *  FROM test WHERE b = '1' AND c = '1' -- key_len=NULL
EXPLAIN SELECT *  FROM test WHERE b = '1' -- key_len=NULL
EXPLAIN SELECT *  FROM test WHERE c = '1' -- key_len=NULL


~~~

> 最左匹配针对于where、order by 条件 。而且需注意，范围条件对应用索引有影响
