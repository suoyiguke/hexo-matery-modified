---
title: mysql-查询索引使用情况分析补充.md
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
title: mysql-查询索引使用情况分析补充.md
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
###我的mysql版本
~~~
SELECT VERSION()
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1a873c5d8136c709.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###准备数据
~~~
/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : localhost:3306
 Source Schema         : test

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 07/01/2020 17:49:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for test03
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `a` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `b` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `c` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `d` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `e` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_test_aBCD`(`a`, `b`, `c`, `d`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of test03
-- ----------------------------
INSERT INTO `test` VALUES (1, 'a1', 'a2', 'a3', 'a4', 'a5');
INSERT INTO `test` VALUES (2, 'b1', 'b2', 'b3', 'b4', 'b5');
INSERT INTO `test` VALUES (3, 'c1', 'c2', 'c3', 'c4', 'c5');
INSERT INTO `test` VALUES (4, 'd1', 'd2', 'd3', 'd4', 'd5');
INSERT INTO `test` VALUES (5, 'e1', 'e2', 'e3', 'e4', 'e5');

SET FOREIGN_KEY_CHECKS = 1;

~~~
###这个表结构的key_len
key_len表示所有参与查找的索引长度之和；不统计参与排序和分组的
43(a)=>86(a+b)=>129(a+b+c)=>172(a+b+c+d)，e字段上没有添加索引

###联合索引的顺序写法改变
由于mysql底层有sql优化机制，无论程序员提供什么样的where条件索引顺序。mysql都会按索引顺序进行优化；如下三种情况效果是一样的；都使用到了a+b+c+d索引

~~~
EXPLAIN SELECT * FROM test where a='a1' and b = 'b1' and c = 'c1' and d = 'd1'
EXPLAIN SELECT * FROM test where a='a1' and b = 'b1' and d = 'c1' and c = 'd1'
EXPLAIN SELECT * FROM test where d='a1' and c = 'b1' and b = 'c1' and a = 'd1'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7de956da25579b28.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###where条件中间出现范围条件
~~~
EXPLAIN SELECT * FROM test where a='a1' and b = 'b1' and c > 'c1' and d = 'd1'
~~~
生效索引：a、b、c 均做查找
![image.png](https://upload-images.jianshu.io/upload_images/13965490-09d2197d49cbb202.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###顺序和范围结合
~~~
EXPLAIN SELECT * FROM test where a='a1' and b = 'b1' and d > 'd1' and c = 'c1'
~~~
使用到了a+b+c+d 4个索引做查找；
![image.png](https://upload-images.jianshu.io/upload_images/13965490-70c46f8295491443.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

因为sql最终被优化为：
SELECT * FROM test where a='a1' and b = 'b1' and c = 'c1' and d > 'd1' 
而d是最后一个索引，d后面没有索引了。因此都会被使用到

### order by  情况
1、a、b、d 字段用作where条件；c字段用作排序条件
~~~
EXPLAIN SELECT * FROM test where a='a1' and b = 'b1' and d = 'd1' ORDER BY c;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2df008da7f6dd42e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看出a、b、c三个索引都被用到；a+b索引做查找，c索引做排序；d索引失效，因为没按索引创建顺序排列,违背了`最佳左前缀法则`

去掉d的条件再试一次，发现结果和上面一致
~~~
EXPLAIN SELECT * FROM test where a='a1' and b = 'b1' ORDER BY c;
~~~

2、a、b字段用做where条件，d字段做排序条件
~~~
EXPLAIN SELECT * FROM test where a='a1' and b = 'b1' ORDER BY d;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8abce55ee96056f7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在这里少了c，出现了`断层`。因此直接排序d字段，d字段上的索引就失效了;a+b参与筛选
出现了filesort文件内排序，性能大大降低


3、a、e字段做where条件，b、c字段做排序字段
~~~
EXPLAIN SELECT * FROM test where a='a1' and e = 'e1' ORDER BY b,c;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aa1bf1b3b4c7261a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

只使用a索引查找，b、c索引用作排序，e索引失效。无filesort


`结论：order by 子句和where条件一样，都参与最佳左前缀法则`

4、这个和上面的差不多，只是c、b字段做排序字段
~~~
EXPLAIN SELECT * FROM test where a='a1' and e = 'e1' ORDER BY c,b;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-90d0643efbc1322b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

调换了下排序字段的位置，因为和联合索性顺序相反，出现了filesort！
只使用a索引查找，c、b索引均失效

5、b字段在where中使用又在order by中使用

~~~
EXPLAIN SELECT * FROM test where a='a1' and b = 'b1' ORDER BY b,c;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4d54be29710ed241.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


`注意：test表的字符集排序规则是utf8_general_ci 
如果排序规则是：utf8mb4_unicode_ci的话就会出现Using filesort`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3f02951241773576.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

同样，在上面的基础上加个 e='e1' 条件结果也是同样的
~~~
EXPLAIN SELECT * FROM test where a='a1' and b = 'b1' and e='e1' ORDER BY b,c;
~~~

6、`重要` 常量字段的排序
与排序的例子4可以比较一下：虽然下列sql的排序字段顺序也是c,b。但是b这里在where条件中已经赋值 b = 'b1'，说明b字段现在是个常量。相当于:
ORDER BY c,'b1' 因此没有出现Using fileSort
~~~
EXPLAIN SELECT * FROM test where a='a1' and b = 'b1' and e='e1' ORDER BY c,b;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-67fc246c5dffb6aa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###GROUP BY 情况
1、a、d字段做筛选条件；b，c做分组条件
~~~
EXPLAIN SELECT * FROM test where a='a1' and d = 'd1' GROUP BY b,c
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8e415c2520bf97b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
a索引做where条件优化，d索引失效；b、c做group by的条件优化

2、相比上面，调换一下分组字段顺序
~~~
EXPLAIN SELECT * FROM test where a='a1' and d = 'd1' GROUP BY d,c
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3f6e9723d185c193.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

GROUP BY d,c 违背了索引的最佳左前缀法则,d、c索引失效；
好家伙！Using temporay 使用中间表 和Using filesort 文件内排序同时出现！这下有的玩了~

注意：GROUP BY和ORDER BY 一样，索引生效必须遵守`最佳左前缀法则`


###总结

- 定值、范围还是排序三种情况要记住，一般order by是给个范围
- group by 之前必排序，不然会有临时表产生
- 对于单键索引，尽量选择针对当前query过滤性更好的索引
- 在选择组合索引的时候，当前Query中过滤性最好的字段在索引字段顺序中，位置越靠前越好。
- 在选择组合索引的时候，尽量选择可以能包含当前query中的where子句中更多字段的索引
- 尽可能通过分析统计信息和调整query的写法来达到选择合适索引的目的
