---
title: mysql-感知-mysql的where条件和join-on条件的区别.md
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
title: mysql-感知-mysql的where条件和join-on条件的区别.md
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
###数据和表结构
~~~
/*
 Navicat Premium Data Transfer

 Source Server         : 经理 eas
 Source Server Type    : MySQL
 Source Server Version : 50719
 Source Host           : 192.168.1.55:3306
 Source Schema         : iam

 Target Server Type    : MySQL
 Target Server Version : 50719
 File Encoding         : 65001

 Date: 07/01/2021 15:14:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for biz_cert_apply_record
-- ----------------------------
DROP TABLE IF EXISTS `biz_cert_apply_record`;
CREATE TABLE `biz_cert_apply_record`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_num` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `dept_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `identity_number` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `mobile` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `cert_type` tinyint(4) NOT NULL,
  `status` tinyint(4) NOT NULL,
  `note` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user_id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `created_at` datetime(0) NOT NULL,
  `updated_at` datetime(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of biz_cert_apply_record
-- ----------------------------
INSERT INTO `biz_cert_apply_record` VALUES (1, '4466', '', '杨耀绥', '445222199004240316', '18922834466', 1, 22, '申请成功', 'a01e50a91450bff803a275b403c1015c', '2020-04-20 00:58:50', '2020-04-20 00:59:03');

-- ----------------------------
-- Table structure for biz_department
-- ----------------------------
DROP TABLE IF EXISTS `biz_department`;
CREATE TABLE `biz_department`  (
  `dept_id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_dept_id` int(11) NULL DEFAULT NULL,
  `dept_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `dept_code` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `seq` int(11) NOT NULL,
  `created_at` datetime(0) NOT NULL,
  `updated_at` datetime(0) NOT NULL,
  PRIMARY KEY (`dept_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of biz_department
-- ----------------------------
INSERT INTO `biz_department` VALUES (1, 0, '测试部门', '1', 1, '2021-01-05 17:47:50', '2021-01-21 17:47:52');

-- ----------------------------
-- Table structure for biz_user
-- ----------------------------
DROP TABLE IF EXISTS `biz_user`;
CREATE TABLE `biz_user`  (
  `user_id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户Id',
  `user_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `employee_num` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '工号',
  `gender` tinyint(4) NOT NULL COMMENT '性别：0表示女，1表示男',
  `dept_id` int(11) NULL DEFAULT NULL COMMENT '科室Id',
  `identity_type` tinyint(4) NOT NULL COMMENT '证件类型',
  `identity_number` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '证件号码',
  `mobile` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '手机号',
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `postal_address` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '通讯地址',
  `post_code` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '邮编',
  `status` tinyint(4) NOT NULL COMMENT '在职状态',
  `job_posts` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '职称',
  `qualification` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '职业资格证类别',
  `license` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '职业资格证号码',
  `note` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `ttp_user_oid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `authentication_mark` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户唯一标识',
  `enabled` tinyint(4) NOT NULL COMMENT '是否启用',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `mobile`(`mobile`) USING BTREE,
  UNIQUE INDEX `authentication_mark`(`authentication_mark`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of biz_user
-- ----------------------------
INSERT INTO `biz_user` VALUES ('277e718384ea97f8a315c0fefb3c7f32', '谢植超', '8742', 1, 1, 1, '441900199112164310', '18899777409', '', '', '', 0, '', '', '', '', '', 'SF441900199112164310', 1, '2020-04-19 15:58:50', '2020-04-19 15:58:50');
INSERT INTO `biz_user` VALUES ('3bfc7edf758b679d1ba2beef8075d5a9', '彭照明', '8758', 1, 1, 1, '420983197605260017', '13510959799', '', '', '', 0, '', '', '', '', '', 'SF420983197605260017', 1, '2020-04-19 15:58:50', '2020-04-19 15:58:50');
INSERT INTO `biz_user` VALUES ('68b80f75cf2f80d06d979fa8350ed68f', '高抚刚', '9999', 1, 1, 1, '362502198103292414', '15889456732', '', '', '', 0, '', '', '', '', '', 'SF362502198103292414', 1, '2020-04-20 03:37:47', '2020-04-20 03:37:47');
INSERT INTO `biz_user` VALUES ('68dcc0700b5ce0e371a391509e62e169', '彭峰', '8734', 1, 1, 1, '422302198010070017', '13699873478', '', '', '', 0, '', '', '', '', '', 'SF422302198010070017', 1, '2020-04-19 15:58:50', '2020-04-19 15:58:50');
INSERT INTO `biz_user` VALUES ('6d971ae49872ae51ad4e6e672df71398', '王辰', '8888', 0, 1, 1, '370923199110162229', '18650371936', '', '', '', 0, '', '', '', '', '', 'SF370923199110162229', 1, '2020-04-20 00:38:34', '2020-04-20 00:58:32');
INSERT INTO `biz_user` VALUES ('738b02ef4e4145dde6461e24f5cceaa8', '粘铭轩', '8056', 1, NULL, 5, '05631029', '15807555698', '', '', '', 0, '', '', '', '', '', 'HX056310293026', 1, '2020-04-26 15:23:52', '2020-04-26 15:23:52');
INSERT INTO `biz_user` VALUES ('76da8ed95a9e0f083d0dd995584895dd', '李国强', '8595', 1, 1, 1, '130402198908122412', '13824356916', '', '', '', 0, '', '', '', '', '', 'SF130402198908122412', 1, '2020-04-19 15:58:50', '2020-04-19 15:58:50');
INSERT INTO `biz_user` VALUES ('89dd8ec140180d8e50e37b3c79f1e690', '李新', '1754', 0, 1, 1, '230121197908090029', '15907555767', '', '', '', 0, '', '', '', '', '', 'SF230121197908090029', 1, '2020-04-19 15:58:50', '2020-04-19 15:58:50');
INSERT INTO `biz_user` VALUES ('983d45ccbd35849edda503dea1e00eb8', '冯涛', '1234', 0, NULL, 1, '431021199412178613', '19925278191', '', '', '', 0, '', '', '', '', '', 'SF431021199412178613', 1, '2020-05-21 02:50:45', '2020-05-21 02:50:45');
INSERT INTO `biz_user` VALUES ('9b669046a2cb308839fe7984f8a00650', '李旭', '1217', 0, NULL, 1, '431021199612178613', '19925278190', '', '', '', 0, '', '', '', '测试', '', 'SF431021199612178613', 1, '2020-06-15 15:21:03', '2020-06-15 15:21:03');
INSERT INTO `biz_user` VALUES ('a01e50a91450bff803a275b403c1015c', '杨耀绥', '4466', 1, 1, 1, '445222199004240316', '18922834466', '', '', '', 0, '', '', '', '', '', 'SF445222199004240316', 1, '2020-04-20 00:58:20', '2020-04-20 00:58:40');
INSERT INTO `biz_user` VALUES ('ef8f1fdbdc591ae94f8a89379e812b9b', '刘雅洁', '1677', 0, 1, 1, '230107196607270227', '13823394075', '', '', '', 0, '', '', '', '', '', 'SF230107196607270227', 1, '2020-04-19 15:58:50', '2020-04-19 15:58:50');

SET FOREIGN_KEY_CHECKS = 1;

~~~

###加在join on后面
是在join的同时进行过滤的，这样可以查出多条。
LEFT JOIN biz_cert_apply_record T2 ON T2.`employee_num` = T0.`employee_num` AND T2.`status` IN (0,-21,-22,22)
~~~
SELECT
	T0.`user_id`,
	T0.`user_name`,
	T0.`employee_num`,
	T0.`gender`,
	T0.`dept_id`,
	T0.`identity_type`,
	T0.`identity_number`,
	T0.`qualification`,
	T0.`job_posts`,
	T0.`license`,
	T0.`email`,
	T0.`mobile`,
	T0.`status`,
	T0.`note`,
	T0.`postal_address`,
	T0.`post_code`,
	T0.`authentication_mark`,
	T0.`enabled`,
	T0.`created_at`,
	T0.`updated_at`,
	T2.*
FROM
	`biz_user` T0
LEFT JOIN biz_department T1 ON T1.`dept_id` = T0.`dept_id`
LEFT JOIN biz_cert_apply_record T2 ON T2.`employee_num` = T0.`employee_num` AND T2.`status` IN (0,-21,-22,22)
WHERE

 T0.`employee_num` LIKE '%%'
AND T0.`user_name` LIKE '%%'
AND (
	T0.`enabled` = 1
	OR T0.`enabled` = 0
)
ORDER BY
	T0.`updated_at` DESC
LIMIT 15
~~~


###加在where

是在join之后过滤的，这样会只会查出1条 WHERE T2.`status` IN (0,-21,-22,22) AND
~~~
SELECT
	T0.`user_id`,
	T0.`user_name`,
	T0.`employee_num`,
	T0.`gender`,
	T0.`dept_id`,
	T0.`identity_type`,
	T0.`identity_number`,
	T0.`qualification`,
	T0.`job_posts`,
	T0.`license`,
	T0.`email`,
	T0.`mobile`,
	T0.`status`,
	T0.`note`,
	T0.`postal_address`,
	T0.`post_code`,
	T0.`authentication_mark`,
	T0.`enabled`,
	T0.`created_at`,
	T0.`updated_at`,
	T2.*
FROM
	`biz_user` T0
LEFT JOIN biz_department T1 ON T1.`dept_id` = T0.`dept_id`
LEFT JOIN biz_cert_apply_record T2 ON T2.`employee_num` = T0.`employee_num`
WHERE
	T2.`status` IN (0,-21,-22,22) AND
 T0.`employee_num` LIKE '%%'
AND T0.`user_name` LIKE '%%'
AND (
	T0.`enabled` = 1
	OR T0.`enabled` = 0
)
ORDER BY
	T0.`updated_at` DESC
LIMIT 15
~~~
