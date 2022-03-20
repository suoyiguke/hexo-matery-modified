---
title: mysql--EXPLAIN-的key_len的长度是如何计算出来的？.md
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
title: mysql--EXPLAIN-的key_len的长度是如何计算出来的？.md
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
key_len的长度在联合索引中的查询分析特别有意义，可以通过它来判断查询的索引使用情况。可以清晰的分析出没有良好使用索引的查询。

###key_len的长度计算公式：
>varchr 比 char 需要多使用1个字节存储长度;允许NULL 的字段需要多使用1个字节存储NULL

varchr(10)变长字段且允许NULL    =  10 * ( character set：utf8=3,gbk=2,latin1=1)+1(NULL)+2(变长字段)
varchr(10)变长字段且不允许NULL =  10 *( character set：utf8=3,gbk=2,latin1=1)+2(变长字段)

char(10)固定字段且允许NULL        =  10 * ( character set：utf8=3,gbk=2,latin1=1)+1(NULL)
char(10)固定字段且不允许NULL        =  10 * ( character set：utf8=3,gbk=2,latin1=1)



###举个例子
建表
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

查询分析
~~~
EXPLAIN SELECT *  FROM test WHERE a = '1' AND b > '1' AND c = '1'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2d552d85bd505dfb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这里的key_len=2，而索引若全部使用key_len=3 ：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ce0689e70206eecb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这就说明b>'1' 让索引部分失效了！再进一步分析：
~~~
EXPLAIN SELECT *  FROM test WHERE a = '1' AND b > '1' 
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9cfc5f59c1d06c9b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以看出，联合索引的c字段部分没有生效。这样就可以得出结论，b>'1' 范围条件会导致后面的索引失效

###key_len大小不只是和where条件有关，我可以举个反例

~~~
EXPLAIN SELECT id  FROM test force index(PRI)
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4dc98e2fdb6f591d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
EXPLAIN SELECT id  FROM test force index(index_a_b_c)   
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-51e82c2037f06b7e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
