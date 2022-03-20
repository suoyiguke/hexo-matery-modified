---
title: mysql-避免索引失效.md
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
title: mysql-避免索引失效.md
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
###准备数据
~~~
create table staffs(
    id int primary key auto_increment,
    name varchar(24) not null default '' comment '姓名',
    age int not null default 0 comment '年龄',
    pos varchar(20) not null default '' comment '职位',
    add_time timestamp not null default current_timestamp comment '入职时间'
)charset utf8 comment '员工记录表';

insert into staffs(name,age,pos,add_time) values('z3',22,'manager',now());
insert into staffs(name,age,pos,add_time) values('July',23,'dev',now());
insert into staffs(name,age,pos,add_time) values('2000',23,'dev',now());

select * from staffs;

alter table staffs add index idx_staffs_nameAgePos(name,age,pos);
~~~
###最佳左前缀法则
where条件==>order by 条件==>group by 条件 按顺序遵守`最佳左前缀法则`

假设创建了复合索引：a,b,c
- a
~~~
EXPLAIN select * from staffs where name='July';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-20bbfaddd8c775f7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- a,b
~~~
EXPLAIN select * from staffs where name='July' AND age=25;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f8eee6629de06bd7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- a,b,c
~~~
EXPLAIN select * from staffs where name='July' AND age=25 and pos='dev';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3ab88261b776dac0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###违背最佳左前缀法则的写法
#### 没有a的写法，索引完全失效
- b,c
~~~
EXPLAIN SELECT * FROM staffs WHERE age=23 AND pos='dev';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-77f87c1799594f5b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- b
~~~
EXPLAIN SELECT * FROM staffs WHERE age=23;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a48605417b426a17.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- c
~~~
EXPLAIN SELECT * FROM staffs WHERE pos='dev';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-16d1c8f2754ac87f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 没有b的写法，索引部分失效
- a,c
~~~
EXPLAIN select * from staffs where name='July' and pos='dev';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-25922cebd8135198.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###索引列上的操作导致索引失效
不在索引列上做任何的操作（计算、函数、显式或隐式的类型转换），否则会导致索引失效而转向全表扫描
#### 函数
~~~
EXPLAIN select * from staffs where left(name,4)='July';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-efd798757832fa9c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 类型转换
 1、字符不加单引号会导致索引失效
   
name字段为varchar类型
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0d696cced2a04cf0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
EXPLAIN select * from staffs where name = '2000';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1807771c21edb76b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这条sql发生了隐式的类型转换：数值==>字符串。所以导致了全表扫描，索引失效
~~~
EXPLAIN select * from staffs where name = 2000;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-07d648462929246f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####计算
应尽量避免在 where 子句中对字段进行表达式操作，这将导致引擎放弃使用索引而进行全表扫描。如：
~~~
select id from t where num/2=100
应改为:select id from t where num=100*2
~~~
###范围条件后面的所有索引会失效
mysql中的范围条件有：in/not in、 like、 <> 、BETWEEN AND ；
#### < 和 >
<>后面的索引失效
~~~
EXPLAIN select * from staffs where name='July' AND age>25 and pos='dev';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bcb68f2a88e08b0c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
#### in 和 not in
`in会导致索引全部失效！！！`
~~~
EXPLAIN select * from staffs where name='July' AND age>25 and pos='dev';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d8e9f4a5d4686ed9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
####BETWEEN AND
`BETWEEN AND 范围条件不会导致索引失效！！！`
~~~
EXPLAIN select * from staffs where name='July' AND age BETWEEN 22 AND 23 and pos='dev';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-29a06ca62dec8e18.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###尽量使用索引覆盖
尽量让索引列和查询列一致；减少select * 的使用

1、查询表结构
~~~
desc staffs
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f49c2ddeddd4f2f8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、查询表的索引结构
联合索引：name,age,post；说明add_time字段没有添加索引
~~~
SHOW INDEX FROM staffs;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1c1a0c9f5af3a947.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、查看select * 的执行计划
~~~
EXPLAIN select * from staffs where name='July' AND age=25 and pos='dev';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-756c1f6467f6fdcb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、查看 select name,age,pos的执行计划
~~~
EXPLAIN select name,age,pos from staffs where name='July' AND age=25 and pos='dev';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-16b56052391286c7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

5、如果select只用一部分索引
- 查看select name、select age、select pos、select name,age、select name,pos、select age,pos的执行计划
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8c32077cf4bbba30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
`ps: 看来select中索引的顺序和个数都不影响索引覆盖呀~因为Extra字段的值都为 Using index；影响的是“是否使用索引”，影响key字段，使用到索引的话key字段的值就不为NULL。`

###使用不等于（!=或者<>）的时候会导致全表扫描
~~~
EXPLAIN select * from staffs where name != 'July';
EXPLAIN select * from staffs where name <> 'July';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-830e072780ecd941.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
`ps：在业务上必须使用这个不等于的话也得使用，不能为了优化而不去写`

###is null,is not null 也无法使用索引
~~~
EXPLAIN select * from staffs where name is null;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0c53d703203ef135.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
~~~
EXPLAIN select * from staffs where name is not null;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-87ab65d9becf58ba.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
`ps：因为is null,is not null 无法使用到索引查询，所以在设计数据表时指定字段的默认值，不能指定为null，一定要给出特定的值。比如0，-1，空字符串“” 等等`

###like以通配符开头（’%abc…’）mysql索引失效

like以通配符开头（’%abc…’）mysql索引失效会变成全表扫描的操作。
- 两个%
~~~
EXPLAIN select * from staffs where name like '%July%';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5a3f1efcd0385a9e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- %在前面
~~~
EXPLAIN select * from staffs where name like '%July';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-295a8486ffa012c4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- %在后面
~~~
EXPLAIN select * from staffs where name like 'July%';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-826e062ab9283549.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### 问题：解决like‘%字符串%’时索引不被使用的方法？
 解决：可以使用`覆盖索引`来解决这个问题！
1、先查看表上的索引
id、name、age、pos 四个字段上都有索引；`注意：name是联合索引中的第一个，带头大哥！`
~~~
SHOW INDEX FROM staffs;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9df24a98cb54e5ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、查看表结构
有个add_time字段没有用到索引
~~~
desc staffs;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0f4d82257ac7765f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、查看执行计划

- 失效写法：不符合索引覆盖，多出了add_time字段！
 全表扫描，且没有用到索引
~~~
EXPLAIN select * from staffs where name like '%July%';
EXPLAIN select id,name,age,pos,add_time from staffs where name like '%July%';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cb826167f42d6a67.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 索引生效写法：符合索引覆盖
~~~
EXPLAIN select id,name,age,pos from staffs where name like '%July%';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f77cb44ba593a637.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 联合索引：a,c,b,c 的索引覆盖写法的所有情况
~~~
-- id开头
EXPLAIN select id from staffs where name like '%July%';
EXPLAIN select id,name from staffs where name like '%July%';
EXPLAIN select id,age from staffs where name like '%July%';
EXPLAIN select id,pos from staffs where name like '%July%';
EXPLAIN select id,name,age from staffs where name like '%July%';
EXPLAIN select id,name,pos from staffs where name like '%July%';
EXPLAIN select id,age,pos from staffs where name like '%July%';
EXPLAIN select id,name,age,pos from staffs where name like '%July%';

-- name开头
EXPLAIN select name from staffs where name like '%July%';
EXPLAIN select name,age from staffs where name like '%July%';
EXPLAIN select name,pos from staffs where name like '%July%';
EXPLAIN select name,age,pos from staffs where name like '%July%';
-- age开头
EXPLAIN select age from staffs where name like '%July%';
EXPLAIN select age,pos from staffs where name like '%July%';

-- pos开头
EXPLAIN select pos from staffs where name like '%July%';

~~~

- 如果name like '%July%' 中的name字段不是联合索引中第一个字段的话，索引会全部生效吗？？
1、查看索引情况，发现name是联合索引的第2层！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b7495c8d5b5860fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
2、执行查询计划
只是age索引生效，特别注意这个情况
~~~
EXPLAIN select age,name,pos from staffs_copy1 where  age = 22  AND  name like '%July%'  AND pos='dev' ;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2b93e5df97ab2dcc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####如果需要让like '%%' 索引完全生效就需要满足下面条件
- select中符合索引覆盖
- 需要like的字段必须是联合索引的带头大哥，第一个索引！

###少用or，用它来连接时会导致索引失效
~~~
SHOW INDEX FROM staffs;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-16ca6f56d190d667.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
EXPLAIN select * from staffs where name = 'July' or name = 'z3';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-784120d3ceef773e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
####怎么达到or的效果又不导致索引失效？
使用UNION ALL
~~~
EXPLAIN
select * from staffs where name = 'July'
UNION ALL
select * from staffs where name = 'z3'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-83974170d48744f9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##练习
假设创建了联合索引 x(a,b,c)

- where a=3	
使用到a
- where a=3 and b=5	
使用到a和b
- where a=3 and b=5 and c=4	
使用到a,b,c
- where b=3 或者 where b=3 and c=4 或者where c=4
因为有or导致索引失效！没有使用到索引
- where a=3 and c=5	
使用到a，但是c不可以，b中间断了
- where a=3 and b>4 and c=5	
使用到a和b，c不能用在范围之后

###like做中间条件有所不同
- where a=3 and b like ‘kk%’ and c=4	
使用到a和b和c
- where a=3 and b like ‘%kk’ and c=4	
使用到a
- where a=3 and b like ‘%kk%’ and c=4	
使用到a
- where a=3 and b like ‘k%kk%’ and c=4	
使用到a和b和c

`ps：like虽然也是范围查询但是区别于>、<，%用在最前面就只用到索引a了；%用在最后面可以用到a+b+c！`
###可以试验一下结果是否正确
~~~
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test`  (
  `id` int(11) NOT NULL,
  `a` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `c` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `d` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_test_aBC`(`a`, `b`, `c`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of test
-- ----------------------------
INSERT INTO `test` VALUES (1, 'a1', 'b1', 'c1', 'd1');
INSERT INTO `test` VALUES (2, 'a2', 'b2', 'c2', 'd2');
INSERT INTO `test` VALUES (3, 'a3', 'b3', 'c3', 'd3');
INSERT INTO `test` VALUES (4, 'a4', 'b4', 'c4', 'd4');
INSERT INTO `test` VALUES (5, 'a5', 'b5', 'c5', 'd5');

SET FOREIGN_KEY_CHECKS = 1;

~~~
~~~
EXPLAIN SELECT * FROM test where a='a1' and b like 'b%' and c = 'c1'
EXPLAIN SELECT * FROM test where a='a1' and b like '%b' and c = 'c1'
EXPLAIN SELECT * FROM test where a='a1' and b like '%b%' and c = 'c1'
EXPLAIN SELECT * FROM test where a='a1' and b like 'b%1%' and c = 'c1'
~~~
###大总结
####索引全部失效：
   -  where条件违反最左匹配原则，没有第带头大哥第一位索引： b=2 and c=3、c=3
   -  where条件使用OR
   -  where条件使用 不等于 !=、<>
   -  where条件使用 is null 
   -  where条件使用 in（多个）
   -  where条件使用 is not null，在第一位索引
   -  where条件 ‘=’左边使用函数，在第一位索引
   -  where条件出现类型转换，在第一位索引
   -  like 中使用% 开头，在第一位索引；select不符合索引覆盖
 

####部分失效
   -  不符合索引的最左匹配原则，中间的b断了：a=1 and c=3；此时只有a索引生效
   -  where条件 > 在中间，那么后面的索引失效；生效的索引包括自己，使用>的索引是生效的
   -  where条件 ‘=’左边出现计算，不是在第一位索引；生效的索引不包括自己
   -  where条件 ‘=’左边使用函数，不是在第一位索引；生效的索引不包括自己
   -  where条件出现类型转换，不是在第一位索引 ；生效的索引不包括自己
   -  where 条件使用 is not null，不是第一位索引；生效的索引不包括自己
   -  like 中使用% 开头，不是第一位索引；生效的索引不包括自己


####全部生效
   -  符合索引的最左匹配原则： a=1、a=1 and b=2、a=1 and b=2 and c=3；
   -  where 条件中使用 BETWEEN AND
   -  where条件 > 在末尾，后面没有索引了，全部生效！
   -  where条件使用 in（一个），相当于 = 
   -  like 中使用% 结尾，全部生效！
   -  a like '%aa%'，select中形成索引覆盖；a字段为联合索引的第一个！此时索引全部生效
    
#####如果达到了索引覆盖，那么索引总是生效的！！
下面的sql几乎违背了上面的所有原则，索引依然全部生效。因为select是索引覆盖的，select里不包含没有建立索引的字段。因此总是用到索引的。可以看出来索引覆盖在sql优化中的作用性
~~~
EXPLAIN select age,name,pos from staffs_copy1 where  age is null AND name is not null OR  age*2 = 11  OR  name in ('July','213','dasda')  OR pos!=213 OR name LIKE '%HAHA' OR left(name,4) = 'July'   ;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-96d91d660a7408d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-22da98b9afd83e4d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
