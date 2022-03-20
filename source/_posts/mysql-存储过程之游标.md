---
title: mysql-存储过程之游标.md
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
title: mysql-存储过程之游标.md
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
游标按我的理解就是用在sql编程中对查询结果集的解析，类比jdbc中的resultset对象。FETCH 一行游标指针就往下面移动一行，直到所有行被遍历完成。

游标的使用分为4步：
1、定义游标，指定游标名和查询sql语句
2、打开游标
3、fetch 获取数据，赋值给变量
4、关闭游标


######基本使用

1、数据准备
~~~
CREATE TABLE `goods`  (
  `gid` int(11) NOT NULL COMMENT '主键',
  `name` char(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '商品',
  `num` int(11) NULL DEFAULT NULL COMMENT '库存',
  PRIMARY KEY (`gid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of goods
-- ----------------------------
INSERT INTO `goods` VALUES (1, 'cat', 34);
INSERT INTO `goods` VALUES (2, 'dog', 0);
INSERT INTO `goods` VALUES (3, 'pig', 12);
~~~

2、定义存储过程，简单使用下游标
~~~
CREATE DEFINER="root"@"%" PROCEDURE "p5"()
BEGIN

  # 定义接受sql数据的变量
	DECLARE row_gid int;
  DECLARE row_name varchar(20);
	DECLARE row_num int;

   
  # 定义游标
	DECLARE getgoods CURSOR FOR
	select gid, name, num from goods;
	
	# 打开游标
	OPEN getgoods;
	
	# 获取数据,使用一次FETCH就是获取一行
	# 注意需要按列顺序的顺序赋值
	FETCH getgoods INTO row_gid, row_name, row_num;
	select  row_gid, row_name, row_num;
	
	FETCH getgoods INTO row_gid, row_name, row_num;
	select  row_gid, row_name, row_num;
	
	
	FETCH getgoods INTO row_gid, row_name, row_num;
	select  row_gid, row_name, row_num;
	
	FETCH getgoods INTO row_gid, row_name, row_num;
	select  row_gid, row_name, row_num;
	
	
	# 关闭游标
	CLOSE getgoods;

	 
END
~~~

执行下 CALL p5(); 可以看到有三个结果集
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1a87e555a949d46e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然而我FETCH 了4次，只有3行。那么产生了游标越界错误。
> 1329 - No data - zero rows fetched, selected, or processed


######使用REPEAT循环去FETCH 数据
使用循环去遍历游标，将查询sql所有的数据取出。使用count(*)总记录数去做循环的判断条件。若循环计数器大于等于总记录数则停止循环。
~~~
CREATE DEFINER="root"@"%" PROCEDURE "p6"()
BEGIN

  # 定义接受sql数据的变量
	DECLARE row_gid int;
  DECLARE row_name varchar(20);
	DECLARE row_num int;
	
	# 总行数
	DECLARE cnt INT DEFAULT 0;
	# 循环变量i
	DECLARE i INT DEFAULT 0;
	
	

	
 
  # 定义游标
	DECLARE getgoods CURSOR FOR select gid, name, num from goods;
	
		
	# 查询总行数并赋值给 cnt
	# 注意这句话一定要放到定义游标的下面，否则报错创建存储过程失败！
	SELECT COUNT(*) INTO cnt FROM goods;
	
	# 打开游标
	OPEN getgoods;
	

  # 开始循环
  REPEAT
    SET i := i+1;
	  FETCH getgoods INTO row_gid, row_name, row_num;
	  select  row_gid, row_name, row_num;
  UNTIL i>=cnt END REPEAT;
	# 循环结束
	
	# 关闭游标
	CLOSE getgoods;
	
	 
END
~~~

######使用游标监听器 continue handler 和 exit handler 来完善游标的遍历

上面遍历游标，防止越界读取。使用的是count(*) 额外的去发出一条查询，有着额外的性能损耗。事实上不需要这样，mysql游标有提供它的方式。

我们可以使用 handler 监听器，在该监听器中定义sql。等到游标被遍历完便会自动执行这个sql。那么我们可以使用一个变量，初始化为0，默认未遍历完。在监听器sql中写入设置变量值为1。然后在循环中使用该变量判断即可

>  定义监听器
    DECLARE CONTINUE HANDLER FOR NOT FOUND set flag :=1;
~~~
CREATE DEFINER="root"@"%" PROCEDURE "p7"()
BEGIN
	DECLARE row_gid int;
        DECLARE row_name varchar(20);
	DECLARE row_num int;

	# 定义循环退出标志符变量
	DECLARE flag INT DEFAULT 0;
	DECLARE getgoods CURSOR FOR select gid, name, num from goods;
  # 定义监听器
	DECLARE CONTINUE HANDLER FOR NOT FOUND set flag :=1;
	OPEN getgoods;
  REPEAT
	  FETCH getgoods INTO row_gid, row_name, row_num;
	  select  row_gid, row_name, row_num;
  UNTIL flag=1 END REPEAT;
	CLOSE getgoods; 
END
~~~

执行下 call p7();发现只有3行记录却放回4个结果集。而且第3个和第4个结果集是相同的。这是一个问题。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d6cc48fa192de072.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
第4次执行fetch时是没数据的，那么触发not found set flag:=1 ，然后continue一下继续执行后面的sql语句，那么` select  row_gid, row_name, row_num;`又被执行一次，最后一行就被执行了2次。

> 若not found set flag:=1 触发后，后面的select不再执行即可。那么我们可以使用 exit代替continute，exit和continute的区别是：exit触发后后面的语句不再执行！

那么使用exit可以完美解决如下：
~~~
CREATE DEFINER="root"@"%" PROCEDURE "p7"()
BEGIN
	DECLARE row_gid int;
  DECLARE row_name varchar(20);
	DECLARE row_num int;

	# 定义循环退出标志符变量
	DECLARE flag INT DEFAULT 0;
	
	DECLARE getgoods CURSOR FOR select gid, name, num from goods;
  # 定义EXIT 监听器
	DECLARE EXIT HANDLER FOR NOT FOUND set flag :=1;

	OPEN getgoods;
	
  REPEAT
	  FETCH getgoods INTO row_gid, row_name, row_num;
	  select  row_gid, row_name, row_num;
  UNTIL flag=1 END REPEAT;
	CLOSE getgoods;
END
~~~
执行如下，3个返回集没问题
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4938f7ce97227dda.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


> 除了continue 和exit还有一种undo handler 。undo的功能是触发后，前面的语句撤销，目前mysql不支持



除了使用exit解决，continue 基础上也是可以的。让如果一定要使用continue 的话就需要修改下逻辑，提前FETCH 下了。为了避免查询结果为空而导致返回空结果集，就需要使用while循环代替pepeat循环。因为pepeat循环类似do while，它总是先执行一次循环体再判断的。


那么，while加上continue handler 的正确遍历方式如下：
~~~
CREATE DEFINER="root"@"%" PROCEDURE "p7"()
BEGIN
	DECLARE row_gid int;
  DECLARE row_name varchar(20);
	DECLARE row_num int;
	# 定义循环退出标志符变量
	DECLARE flag INT DEFAULT 0;

	DECLARE getgoods CURSOR FOR select gid, name, num from goods;
  # 定义监听器
	DECLARE CONTINUE HANDLER FOR NOT FOUND set flag :=1;

	OPEN getgoods;
	# 提前FETCH下
	FETCH getgoods INTO row_gid, row_name, row_num;
	
  # 换成while循环，就不会当返回集为null时查出数据为空的了
	# 注意while循环的循环条件为true时才进入循环
  WHILE flag=0 DO
	  select  row_gid, row_name, row_num;
		FETCH getgoods INTO row_gid, row_name, row_num;
  END WHILE;
	CLOSE getgoods;	 
END
~~~
