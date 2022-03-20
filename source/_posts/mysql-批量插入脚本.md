---
title: mysql-批量插入脚本.md
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
title: mysql-批量插入脚本.md
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
https://www.cnblogs.com/phpper/p/7361841.html
1、
~~~
create table dept(
  id int unsigned primary key auto_increment,
  deptno mediumint unsigned not null default 0,
  dname varchar(20) not null default "",
  loc varchar(13) not null default ""
)engine=innodb default charset=utf8;
create table emp(
  id int unsigned primary key auto_increment,
  empno mediumint unsigned not null default 0,/*编号*/
  ename varchar(20) not null default "",/*姓名*/
  job varchar(9) not null default "",/*工作*/
  mgr mediumint unsigned not null default 0,/*上级编号*/
  hiredate date not null,/*入职时间*/
  sal decimal(7,2) not null, /*薪水*/
  comm decimal(7,2) not null,/*红利*/
  deptno mediumint unsigned not null default 0/*部门编号*/
)engine=innodb default charset=utf8;
~~~

~~~
delimiter $$
 create function rand_string(n int) returns varchar(255)
 begin
   declare chars_str varchar(100) default 'qwertyuiopasdfghjklzxcvbnm';
   declare return_str varchar(255) default '';
   declare i int default 0;
   while i<n do
   set return_str=concat(return_str,substring(chars_str,floor(1+rand()*52),1));
   set i=i+1;
   end while;
   return return_str;
 end $$
~~~

~~~
delimiter $$
 create function rand_num() returns int(5)
 begin
   declare i int default 0;
   set i=floor(100+rand()*10);
 return i;
 end $$
~~~

~~~
delimiter $$
create procedure insert_emp(in start int(10),in max_num int(10))
begin
 declare i int default 0;
 /*把autocommit设置成0*/
 set autocommit= 0;
 repeat
 set i=i+1;
 insert into emp(empno,ename,job,mgr,hiredate,sal,comm,deptno)
 values((start+i),rand_string(6),'SALESMAN',0001,curdate(),2000,400,rand_num());
 until i=max_num end repeat;
commit;
end $$
~~~
~~~
delimiter $$
create procedure insert_dept(in start int(10),in max_num int(10))
begin
declare i int default 0;
 set autocommit=0;
 repeat
 set i=i+1;
 insert into dept(deptno,dname,loc) values((start+i),rand_string(10),rand_string(8));
 until i=max_num end repeat;
 commit;
 end $$
~~~

~~~
call insert_dept(1,100);//从deptno为1起插入100条随机生成数据
call insert_emp(1,100);//从deptno为1起插入100条随机生成数据
~~~
