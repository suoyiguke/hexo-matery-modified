---
title: mysql-按日期查询统计sql记录.md
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
title: mysql-按日期查询统计sql记录.md
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
### 统计当前月份内，按天数的登录信息

数据准备
~~~
CREATE TABLE `biz_cloudsign_login`  (
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
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of biz_cloudsign_login
-- ----------------------------
INSERT INTO `biz_cloudsign_login` VALUES (1, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '192.168.0.103', '0EAC3AB538B27B9EBE781323FAC4C7B2427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8MEVBQzNBQjUzOEIyN0I5RUJFNzgxMzIzRkFDNEM3QjI0Mjc=', '2020-06-06 18:57:31');
INSERT INTO `biz_cloudsign_login` VALUES (2, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '192.168.0.103', '3515D6E6DC3CC3FCE465E98255091B22427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8MzUxNUQ2RTZEQzNDQzNGQ0U0NjVFOTgyNTUwOTFCMjI0Mjc=', '2020-06-06 18:59:37');
INSERT INTO `biz_cloudsign_login` VALUES (3, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '192.168.0.103', '9AB3CFF98536934830A1AFDE8D1FEC25427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8OUFCM0NGRjk4NTM2OTM0ODMwQTFBRkRFOEQxRkVDMjU0Mjc=', '2020-06-06 19:00:53');
INSERT INTO `biz_cloudsign_login` VALUES (4, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '192.168.0.103', '1FAD736B41D1ABDAA7547560D5254465427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8MUZBRDczNkI0MUQxQUJEQUE3NTQ3NTYwRDUyNTQ0NjU0Mjc=', '2020-06-06 19:25:23');
INSERT INTO `biz_cloudsign_login` VALUES (5, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '192.168.0.103', 'C756FF55630C9BAA4F24754DB7FBF1B3427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8Qzc1NkZGNTU2MzBDOUJBQTRGMjQ3NTREQjdGQkYxQjM0Mjc=', '2020-06-06 19:35:15');
INSERT INTO `biz_cloudsign_login` VALUES (6, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '0:0:0:0:0:0:0:1', '8FC54CB7AEE20EFA1C92154A35364D85427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8OEZDNTRDQjdBRUUyMEVGQTFDOTIxNTRBMzUzNjREODU0Mjc=', '2020-06-08 09:58:31');
INSERT INTO `biz_cloudsign_login` VALUES (7, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '0:0:0:0:0:0:0:1', '9E87AF67CFF9548B970D84B507CBCA0D427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8OUU4N0FGNjdDRkY5NTQ4Qjk3MEQ4NEI1MDdDQkNBMEQ0Mjc=', '2020-06-08 09:59:34');
INSERT INTO `biz_cloudsign_login` VALUES (8, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '0:0:0:0:0:0:0:1', 'F06F02F679C7183B0B63F46CADF1A076427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8RjA2RjAyRjY3OUM3MTgzQjBCNjNGNDZDQURGMUEwNzY0Mjc=', '2020-06-08 10:28:18');
INSERT INTO `biz_cloudsign_login` VALUES (9, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '0:0:0:0:0:0:0:1', '76EAAD9AD860823894492F94C40D378B427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8NzZFQUFEOUFEODYwODIzODk0NDkyRjk0QzQwRDM3OEI0Mjc=', '2020-06-08 11:02:54');
INSERT INTO `biz_cloudsign_login` VALUES (10, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '0:0:0:0:0:0:0:1', '1BD1A3AABDC927CED28C42C662884D29427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8MUJEMUEzQUFCREM5MjdDRUQyOEM0MkM2NjI4ODREMjk0Mjc=', '2020-06-08 18:27:55');
INSERT INTO `biz_cloudsign_login` VALUES (11, 9998, '信息科', '11', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '0:0:0:0:0:0:0:1', '7B0196C434242D186D55673A50AC680F427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8N0IwMTk2QzQzNDI0MkQxODZENTU2NzNBNTBBQzY4MEY0Mjc=', '2020-06-08 18:28:45');
INSERT INTO `biz_cloudsign_login` VALUES (12, 9998, '信息科', '4466', '杨耀绥', '445222199004240316', 'AFCAE751-6868-4A53-85BA-36BF7C5BF14E', '0:0:0:0:0:0:0:1', '7B0196C434242D186D55673A50AC680F427', '0199ce84-0b5c-401a-9d21-9205846b6a74', 'MTA4QzRGREIwOUU4RDIzQjVCRjQzNXx8fG51bGx8fHwyfHx8U0Y0NDUyMjIxOTkwMDQyNDAzMTZ8fHw0NDY2fHx8N0IwMTk2QzQzNDI0MkQxODZENTU2NzNBNTBBQzY4MEY0Mjc=', '2020-05-08 18:28:45');

~~~

~~~
SELECT
	count(*) y ,DATE_FORMAT(updated_at,   '%m-%d') x
FROM
	biz_cloudsign_login 
       -- 筛选出当前月份内
	WHERE DATE_FORMAT( updated_at, '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' )
GROUP BY
        -- 按天数做分组
	DATE_FORMAT(updated_at,   '%m-%d')
	
	
~~~
