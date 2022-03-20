---
title: mysql操作积累.md
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
title: mysql操作积累.md
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
**join的update 将表a的一个字段赋值到表b，且表a和表b需要关联下**

把biz_user表的user_id字段，赋值到biz_cert_info这张表的user_id字段，当身份证字段相同

~~~
update biz_cert_info join biz_user on  biz_user.identity_number=biz_cert_info.identity_number
set biz_cert_info.user_id=biz_user.user_id
~~~

**mysql 常用sql之查询A表中有B表中没有的数据**
A、B两表，找出ID字段中，存在A表，但是不存在B表的数据。A表总共13w数据，去重后大约3W条数据，B表有2W条数据，且B表的ID字段有索引。

方法一
使用 not in ,容易理解,效率低 执行时间为：1.395秒
~~~
 select distinct A.ID from  A where A.ID not in (select ID from B)
~~~
方法二
使用 left join…on… , “B.ID isnull” 表示左连接之后在B.ID 字段为 null的记录 执行时间：0.739秒
~~~
 select A.ID from A left join B on A.ID=B.ID where B.ID is null
~~~

方法三
逻辑相对复杂,但是速度最快 ~执行时间: 0.570秒~（感觉这种方式挺好）
~~~
select * from  A where (select count(1) from B where A.ID=B.ID) = 0 
~~~



**批量修改id为uuid 需要分步进行。不然生成的uuid重复**
~~~
UPDATE  video  set video_id = UUID()
UPDATE video set video_id = REPLACE (video_id, '-', '')
~~~

**生成随机数**
~~~
SELECT  FLOOR(5323 + (RAND() * 20222))
~~~

**删除重复记录，只保留一条**

①、删除video_url 重复的记录，保留大id的
~~~
delete from video
where video_id not in(
select * from (select max(video_id) from video group by video_url
) as tmp);
~~~

②、删除数据库中重复的数据(多字段判断重复)
~~~
DELETE FROM tb_pregnancy_preparation_bak WHERE id NOT IN (
SELECT
id
FROM
(
SELECT
MIN(id) AS id,
count(period) AS count
FROM
tb_pregnancy_preparation_bak

GROUP BY period,day
HAVING
count(period) >= 1
) m
);
~~~
其中 not in 里面的数据是要保留的数据!网上有的sql的HAVING后面跟的count>1(此处是大坑),注意这样是不对的,如果是count>1这样的话会将原本只有一条的记录删除!!!还有要注意如果表中的数据有时间限制,要删除某一时间段内的重复数据,一定要在每个范围内加上时间的区间!!!一般删除操作还是相对危险的,一不小心就会跑路,一定要记得备份!!!写好的SQL最好在本地模拟数据去删除的试一试!!!

**删除重复记录，只保留一条**

  select category_name,count(*) as count from cb_category group by category_name having count>1;	


**清空表，可以使得自增量重置**

truncate table 表名; 

**使用select的值当做 insert into的值**


**手动批量修改 id为自增 并且从1开始**

update tb_article,(select @i:=0) as it set  new_id =  @i:=@
查询时添加列序号
SELECT  (@i:=@i+1) id ,new_id FROM tb_article,(select @i:=0) as it


**按日期分组统计**

SELECT DATE_FORMAT( video_date, "%Y-%m-%d %H" ) , COUNT( * ) 
FROM video
GROUP BY DATE_FORMAT( video_date, "%Y-%m-%d %H" ) 

查询某天：
deteline, "%Y-%m-%d"
某时：
deteline, "%Y-%m-%d %H"


**避免插入重复数据**

MySQL 提供了Ignore 用来避免数据的重复插入.

IGNORE :
若有导致unique key 冲突的记录，则该条记录不会被插入到数据库中.

示例:
INSERT IGNORE INTO `table_name` (`email`, `phone`, `user_id`) VALUES ('test9@163.com', '99999', '9999');
这样当有重复记录就会忽略,执行后返回数字0
还有个应用就是复制表,避免重复记录：
INSERT IGNORE INTO `table_1` (`name`) SELECT `name` FROM `table_2`;


**逗号分隔转in查询**
select * from sys_depart where FIND_IN_SET(depart_name,  '企业管理员,企业用户2')

**逗号转in查询并select使用逗号拼接**
select  GROUP_CONCAT(org_code) from sys_depart where FIND_IN_SET(depart_name,  '企业用户2-企业管理员,企业用户2')

适合是用是用在 逗号分隔的字符串转化 


**where条件中使用逗号分隔的id查询**
~~~
 SELECT * FROM tb_box WHERE FIND_IN_SET(id, '1249602002032267265,1249627442268606466,1249601566097281025' )  

~~~ 



**指定字符分隔返回值列表**

使用GROUP_CONCAT函数可以实现没如果不指定特定字符，则默认使用逗号分隔
>SELECT GROUP_CONCAT(depart_name SEPARATOR  '-')  from sys_depart WHERE org_code  in (left('A06A01',3),'A06A01')


**注意where条件中 与、或和括号的关系。**

如下在这里的where条件中  a.sys_org_code = 'A01' 是强制条件，因为 b.number='A3213123' OR a.NAME LIKE concat( '%', '投放点', '%' ) 被括号包裹了
>WHERE  a.sys_org_code = 'A01' AND ( b.number='A3213123' OR  a.NAME LIKE concat( '%', '投放点', '%' ) )

如果是这样，b.number='A3213123' OR a.NAME LIKE concat( '%', '投放点', '%' )  没有被括号包括，那么会查询到a.sys_org_code != 'A01' 的记录

>WHERE  a.sys_org_code = 'A01' AND b.number='A3213123' OR  a.NAME LIKE concat( '%', '投放点', '%' ) 
