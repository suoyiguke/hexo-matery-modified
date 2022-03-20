---
title: mysql-sql编程.md
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
title: mysql-sql编程.md
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
mysql的sql编程一般使用在 存储过程/触发器/事件 等sql程序中。

###DECLARE 变量申明 

1、使用DECLARE 语句申明变量，而不是使用@x 形式的用户变量。因为用户变量的作用域为当前连接，范围比较大。而DECLARE 变量只在当前的BEGIN ... END复合语句里有效。
~~~
CREATE DEFINER="root"@"%" PROCEDURE "test_1"()
begin
    
		DECLARE a INT DEFAULT 1;
		DECLARE b INT DEFAULT 100;
		DECLARE i INT DEFAULT 0;
		
		WHILE i < 1000 DO
         SET a = a + b;
				 SET i = i + 1;
    END WHILE;
		SELECT a; 
		
end
~~~

2、使用unsigned关键字将变量申明为无符号。表示范围将扩大一倍
~~~
     -- 定义变量
    DECLARE i int unsigned DEFAULT 0;
~~~

3、 变量名不能和列名一样。SELECT a INTO b  FROM
 tb 会默认将a变量赋值给b变量，即使tb表中存在名字为b的列
~~~
CREATE DEFINER="root"@"%" PROCEDURE "sp1"(x VARCHAR(5))
BEGIN
    DECLARE xname VARCHAR(5) DEFAULT 'bob';
    DECLARE newname VARCHAR(5);
    
    SELECT xname INTO newname 
      FROM (SELECT 'yinkai' newname  ) tb WHERE xname = xname;
    SELECT newname;
  END
~~~
最终SELECT newname;输出 'bob' 而不是我们希望的 'yinkai'
###变量赋值
1、手动赋值 ：使用 SET 命令

2、在select查询参数中使用查询结果集赋值：
使用 SELECT  num`字段` INTO rnum`变量`。例如下面存储过程的例子，tb表的a，b字段赋值到number1 、number2的字段当中了。而且这种`SELECT .. INTO ..`的方式不会产生结果集，适合使用在触发器里。
~~~
CREATE DEFINER="root"@"%" PROCEDURE "test_1"()
begin
    
		DECLARE number1 INT DEFAULT 0;
		DECLARE number2 INT DEFAULT 0;
		SELECT a,b INTO number1,number2 FROM (SELECT 1 a, 2 b ) tb;
		SELECT number1,number1;
		
end
~~~





###流程控制
######if-else语句
如下存储过程，展示了if-else语句的用法
~~~
create procedure p_hello_world(in v_id int)
begin
    if (v_id > 0) then
        select '> 0';
    elseif (v_id = 0) then
        select '= 0';
    else
        select '< 0';
    end if;
end;
 
call p_hello_world(-9);

drop procedure if exists p_hello_world;
~~~



######循环
1、while循环

~~~
CREATE DEFINER="root"@"%" PROCEDURE "test_1"()
begin
		DECLARE i INT DEFAULT 0;
		WHILE i < 10 DO
		 
				 SET i = i + 1;
				 SELECT CONCAT('i==>',i) ; 
    END WHILE;
		
end
~~~

2、repeat循环
类似于c语言中的 do while循环，先执行一次循环体再判断。

~~~
CREATE DEFINER="root"@"%" PROCEDURE "test_1"()
begin
    -- 定义变量
    DECLARE i int unsigned DEFAULT 0;
    REPEAT
        SET i = i+1;
        SELECT i;
    UNTIL i >= 10
    END REPEAT;
		
end
~~~

3、loop循环

~~~
CREATE DEFINER="root"@"%" PROCEDURE "test_1"()
begin
     -- 定义变量
    DECLARE i int unsigned DEFAULT 0;
    LOOP_LABEL:LOOP
        SELECT i;
        SET i = i+1;
        IF i >= 10 THEN
            LEAVE LOOP_LABEL;
        END IF;
    END LOOP;
		
end
~~~

######case语句
类似于java中的switch语句，传入一个值。根据它去执行不同的语句
~~~
CREATE DEFINER="root"@"%" PROCEDURE "p4"(IN `age` int)
BEGIN
   
	 CASE age
	 WHEN 1 THEN 
	    select '我是1';
	 WHEN 2 THEN
	    select '我是2';
	 WHEN 3 THEN
	    select '我是3';
   ELSE 
	    select '我不是任何1到3之间的数';
	END CASE ;
	 
END
~~~

执行 CALL p4(1);


