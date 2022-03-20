---
title: mysql-存储过程学习.md
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
title: mysql-存储过程学习.md
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
存储过程就是封装sql语言的一个没有返回值的函数

######查看已有存储过程
~~~
SHOW PROCEDURE STATUS;
SHOW CREATE PROCEDURE insert_100;
~~~
######执行存储过程
call insert_100();

######存储过程使用学习
1、这是一个简单的使用局部变量，字符串拼接，字符串赋值
~~~
CREATE DEFINER="root"@"%" PROCEDURE "test1"()
BEGIN
	DECLARE a int DEFAULT 0;
	DECLARE b varchar(20) DEFAULT 'yinkai';
	DECLARE c VARCHAR(30) DEFAULT '';
	
	SELECT concat('a=',a,' ','b=',b) INTO c;
	SELECT c;

END
~~~

2、简单计算
~~~
CREATE DEFINER="root"@"%" PROCEDURE "test1"()
BEGIN
	DECLARE a int DEFAULT 0;
	DECLARE b int DEFAULT 0;
	DECLARE c int DEFAULT 0;
	
	SET a = 100,b = 300;

	SET c = a + b;
	SELECT c;

END
~~~

3、传入参数，进行if-elseif-else 判断
~~~
CREATE DEFINER="root"@"%" PROCEDURE "test1"(a int)
BEGIN
    if a < 18 AND a >= 0 then
        select CONCAT(a,'岁==>未成年');
    elseif a >= 18  then
        select CONCAT(a,'岁==>已成年');
    else
        select CONCAT(a,'岁==>非法参数');
    end if;
END
~~~


######存储过程的in和out 、inout 参数
1、in  是输入类型参数
~~~
CREATE DEFINER="root"@"%" PROCEDURE "p1"(IN `num` int)
BEGIN
   
   DECLARE i INT UNSIGNED DEFAULT 0; 
   DECLARE sum INT UNSIGNED DEFAULT 0;

   WHILE i < num DO
        SET i := i + 1;
			  SET sum := sum+ i;
        
   END WHILE;
	 SELECT sum;

END
~~~

2、out类型是输出类型的参数
顾名思义out类型的参数可以从过程中传出来
~~~
CREATE DEFINER="root"@"%" PROCEDURE "p2"(IN `num` int,OUT `sum` INT )
BEGIN
   
   DECLARE i INT UNSIGNED DEFAULT 0; 
   -- 注意需要初始化，还有初始化方式，不要加@。这不是用户变量
   SET sum := 0;
	 
   WHILE i < num DO
        SET i := i + 1;
			  SET sum := sum+ i;
        
   END WHILE;
END
~~~

执行
~~~
CALL p2(10,@j);
SELECT @j;
~~~

注意事项：
1、OUT sum INT 申明的OUT类型参数需要在过程中进行初始化！ 直接使用 `SET sum := 0;` 即可，不然结果一直是NULL的
2、需要传入一个变量，之后这个变量被赋值后又可以传出来。传入参数示例`CALL p2(10,@j);` 这个@j之后就可以直接使用select查询了

3、inout类型
即是in又是out
~~~
CREATE DEFINER="root"@"%" PROCEDURE "p3"(INOUT `age` int)
BEGIN
   SET age := age + 20;
END
~~~

执行
~~~
SET @x = 10; -- in的特性
CALL p3(@x); -- out的特性
SELECT @x;
~~~
######存储过程实例
1、输出逗号分隔的 100次随机数，范围在 0- 100之间
~~~
 create procedure test_xh(a int) 
    begin
        declare sum int default 0;  -- default 是指定该变量的默认值
        declare i int default 1;
				declare str VARCHAR(16383) default '';
    while i<=a DO -- 循环开始
        set sum=sum+i;
        set i=i+1;
				set str = CONCAT_WS(',', FLOOR( 1 + RAND() * (100 - 1)),str);
    end while; -- 循环结束
    
		SELECT str; -- 打印结果
		 
    end;
		
		
    -- 执行存储过程
    call test_xh(100);
    -- 删除存储过程
    drop procedure if exists test_xh;

~~~



2、退出存储过程

>1、 使用    label:BEGIN 定义开始
2、使用LEAVE label;退出
~~~

 create procedure test_xh(a int) 
    label:BEGIN
        declare i int default 1;
    while i<=a DO -- 循环开始
        set i=i+1;
				if (FLOOR( 1 + RAND() * (100 - 1)) = 1) then
          select '包含1';
					-- 退出
					LEAVE label;
				elseif(FLOOR( 1 + RAND() * (100 - 1)) = 100) then
				  select '包含100';
					-- 退出
					LEAVE label;

        end if;
				
    end while; -- 循环结束
    
		 
    end;
			
    -- 执行存储过程
    call test_xh(10000000);
    -- 删除存储过程
    drop procedure if exists test_xh;
~~~

3、批量插入数据存储过程
~~~
CREATE DEFINER=`root`@`%` PROCEDURE `insert_hit_counter`(in start int(10),in max_num int(10))
begin
 declare i int default 0;
 /*把autocommit设置成0*/
 set autocommit= 0;
 repeat
 set i=i+1;
 INSERT INTO `test`.`hit_counter`(`slot`, `cnt`) VALUES ((start+i), 0);
 until i=max_num end repeat;
commit;
end
~~~
