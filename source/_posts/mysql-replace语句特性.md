---
title: mysql-replace语句特性.md
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
title: mysql-replace语句特性.md
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
> 是故弟子不必不如师,师不必贤于弟子


replace语句 要么插入，要么删除并插入。
replace语句和insert语句都能够用来插入数据，前提是在没有主键冲突或唯一索引冲突的情况下。


######replace 和  ON DUPLICATE KEY UPDATE 的区别 ?

- 没有主键和唯一索引冲突下，replace into 和ON DUPLICATE KEY UPDATE 都是插入操作。
- 在出现冲突的情况下，使用replace into只是先delete掉原来的数据，再执行insert操作，如果新的insert语句不完成，会将其余字段设置为默认值。而ON DUPLICATE KEY UPDATE 则是在原来的基础上发出update语句


实验如下，准备数据
~~~
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `a` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `b` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `c` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `d` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX ` index_a_b_c(a,b,c)`(`a`, `b`, `c`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of test
-- ----------------------------
INSERT INTO `test` VALUES (1, 'a2', 'b2', 'c2', 'd2');

SET FOREIGN_KEY_CHECKS = 1;
~~~
test表需建立联合的唯一索引
![image.png](https://upload-images.jianshu.io/upload_images/13965490-571fb66fde935aea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

开始演示replace into语句，下面再次查询时发现id自动递增了，说明进行了insert。因为没有指定d值，所以d值被insert为它的默认值NULLL
![image.png](https://upload-images.jianshu.io/upload_images/13965490-05d3800bc34c5a22.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

再来演示 ON DUPLICATE KEY UPDATE 。第二次查询结果只有a字段改了，id和bcd字段都没有变化。说明只是执行了update操作

![image.png](https://upload-images.jianshu.io/upload_images/13965490-13db3051bac61ba9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
