---
title: mysql-典型sql之按课程分组显示分数前3名（一）.md
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
title: mysql-典型sql之按课程分组显示分数前3名（一）.md
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
> 蚓无爪牙之利，上食埃土，下饮黄泉，用心一也

有一张分数表如下，记录了三个字段
> 用户id,课程id，分数

~~~
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for score
-- ----------------------------
DROP TABLE IF EXISTS `score`;
CREATE TABLE `score`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NULL DEFAULT NULL,
  `subject_id` bigint(20) NULL DEFAULT NULL,
  `score` double(5, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of score
-- ----------------------------
INSERT INTO `score` VALUES (1, 1, 1, 9.00);
INSERT INTO `score` VALUES (2, 1, 2, 9.00);
INSERT INTO `score` VALUES (3, 1, 3, 8.00);
INSERT INTO `score` VALUES (4, 2, 1, 6.00);
INSERT INTO `score` VALUES (5, 2, 2, 10.00);
INSERT INTO `score` VALUES (6, 2, 3, 7.00);
INSERT INTO `score` VALUES (7, 3, 1, 10.00);
INSERT INTO `score` VALUES (8, 3, 2, 6.00);
INSERT INTO `score` VALUES (9, 3, 3, 9.00);
INSERT INTO `score` VALUES (10, 4, 1, 5.00);
INSERT INTO `score` VALUES (11, 4, 2, 5.00);
INSERT INTO `score` VALUES (12, 4, 3, 5.00);

SET FOREIGN_KEY_CHECKS = 1;

~~~


分组统计各个科目前三名的分数，最终sql如下

~~~
SELECT
	a.* 
FROM
	score a
	LEFT JOIN score b ON a.subject_id = b.subject_id 
	AND a.score < b.score
GROUP BY a.id,a.score,a.subject_id,a.user_id
HAVING COUNT(a.id) < 3
ORDER BY a.subject_id,a.score DESC
~~~

###分析

1、首先使用left join按subject_id课程id进行分数表score的自关联（a.subject_id = b.subject_id ）且 a.score < b.score ；表示相同课程，且test a 分数小于 test b 的所有记录。select条件只查test a.*

>SELECT
	a.* 
FROM
	score a
	LEFT JOIN score b ON a.subject_id = b.subject_id 
	AND a.score < b.score

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f7037fafe4f3ed44.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

执行查询，可以发现结果集存在重复记录。自关联都会如此


2、在1步骤的基础上，按test  a.id,a.score,a.subject_id,a.user_id 分组，这里的GROUP BY分组目的就是去重

>SELECT
	>a.* 
>FROM
	score a
	LEFT JOIN score b ON a.subject_id = b.subject_id 
	AND a.score < b.score
`GROUP BY a.id,a.score,a.subject_id,a.user_id`

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1994436cabe696c2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可见，去重之后是按user_id分组显示的，而我们需要按课程sybject_id分组显示


3、在第2步的基础上加上按`课程`和`分数`倒序排列（DESC），注意ORDER BY 先作用于 subject_id，再作用于score 这样才能保证相同的课程subject_id被分组到一起；还需要注意的是倒序的DESC，因为我们需要取前3名

>SELECT
	a.* 
FROM
	score a
	LEFT JOIN score b ON a.subject_id = b.subject_id 
	AND a.score < b.score
GROUP BY a.id,a.score,a.subject_id,a.user_id
`ORDER BY a.subject_id,a.score DESC`

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c6b244937e8cef12.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 有些时候我们甚至可以使用ORDER BY来达到分组的目的

4、在GROUP BY后面，ORDER BY 前面 再添加 HAVING语句，只取前3条信息
>SELECT
	a.* 
FROM
	score a
	LEFT JOIN score b ON a.subject_id = b.subject_id 
	AND a.score < b.score
GROUP BY a.id,a.score,a.subject_id,a.user_id
`HAVING COUNT(a.id)<3`
ORDER BY a.subject_id,a.score DESC

![image.png](https://upload-images.jianshu.io/upload_images/13965490-8a946a7e6d78013a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


