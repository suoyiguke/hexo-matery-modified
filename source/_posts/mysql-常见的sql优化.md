---
title: mysql-常见的sql优化.md
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
title: mysql-常见的sql优化.md
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
###exists 和 in的选择使用 

按照“小表驱动大表”的优化经验，可以得出in和exists的使用经验

1、当子查询数据集大小小于父查询数据集时，使用in

2、当子查询数据集大小大于父查询数据集时，使用exists

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1078653619cda226.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####具体实验

- 数据准备
~~~

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb1_dept
-- ----------------------------
DROP TABLE IF EXISTS `tb1_dept`;
CREATE TABLE `tb1_dept`  (
  `id` int(11) NOT NULL,
  `deptName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `locAdd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb1_dept
-- ----------------------------
INSERT INTO `tb1_dept` VALUES (1, 'RD', '11');
INSERT INTO `tb1_dept` VALUES (2, 'HR', '12');
INSERT INTO `tb1_dept` VALUES (3, 'MK', '13');
INSERT INTO `tb1_dept` VALUES (4, 'MIS', '14');
INSERT INTO `tb1_dept` VALUES (5, 'FD', '15');

-- ----------------------------
-- Table structure for tb1_emp
-- ----------------------------
DROP TABLE IF EXISTS `tb1_emp`;
CREATE TABLE `tb1_emp`  (
  `id` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `deptId` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_`(`deptId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb1_emp
-- ----------------------------
INSERT INTO `tb1_emp` VALUES (1, 'z3', 1);
INSERT INTO `tb1_emp` VALUES (2, 'z4', 1);
INSERT INTO `tb1_emp` VALUES (3, 'z5', 1);
INSERT INTO `tb1_emp` VALUES (4, 's5', 2);
INSERT INTO `tb1_emp` VALUES (5, 'w6', 2);
INSERT INTO `tb1_emp` VALUES (6, 's7', 3);
INSERT INTO `tb1_emp` VALUES (7, 's8', 4);
INSERT INTO `tb1_emp` VALUES (8, 's9', 51);

SET FOREIGN_KEY_CHECKS = 1;

~~~

- 使用in查询
~~~
EXPLAIN SELECT * FROM tb1_emp e WHERE e.deptId in (SELECT id FROM tb1_dept d);
~~~

- 使用EXISTS 查询
~~~
EXPLAIN SELECT * FROM tb1_emp e WHERE EXISTS (SELECT id FROM tb1_dept d WHERE e.deptId = d.id);
~~~



###在一张表上同时进行查询和更新
![image.png](https://upload-images.jianshu.io/upload_images/13965490-93be74d841c77d45.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###避免重复查询刚刚更新的数据
更新一条记录，同时返回最新的记录
![image.png](https://upload-images.jianshu.io/upload_images/13965490-130c0f0dd422962c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
UPDATE logs1 set laddtime = NOW() WHERE id =1811 AND @now :=NOW();
SELECT @now;
~~~

###统计因为主键冲突而更新的数量
![image.png](https://upload-images.jianshu.io/upload_images/13965490-98bc36d249e94ae1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###优化COUNT()
- 统计某列的数量`（不统计NULL）`
- 统计结果集行数（可以使用count(*)、count(主键)、count(1)）
![image.png](https://upload-images.jianshu.io/upload_images/13965490-05202f785258ca8a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


1.count(1)与count(*)得到的结果一致，包含null值。
2.count(字段)不计算null值
3.count(null)结果恒为0
~~~
SELECT COUNT(1) FROM logs1  -- 9999999、0.055s
SELECT COUNT(*) FROM logs1 -- 9999999、0.050s
SELECT COUNT(id) FROM logs1 -- 9999999、0.055s
 
SELECT COUNT(lfadduser) FROM logs1 -- 9999996、5.3s

SELECT COUNT(null) FROM logs1 -- 0、5.086s
~~~
