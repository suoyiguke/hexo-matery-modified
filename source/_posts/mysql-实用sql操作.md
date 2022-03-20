---
title: mysql-实用sql操作.md
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
title: mysql-实用sql操作.md
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
# 1、**批量修改id为uuid 需要分步进行。不然生成的uuid重复**

UPDATE  video  set video_id = UUID()

UPDATE video set video_id = REPLACE (video_id, '-', '')

# 2、**随机数**

SELECT  FLOOR(5323 + (RAND() * 20222))

# 3、**删除重复记录，只保留一条**

1、删除video_url 重复的记录，保留大id的

delete from video

where video_id not in(

select * from (select max(video_id) from video group by video_url

) as tmp);

2、删除数据库中重复的数据(多字段判断重复)

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

其中 not in 里面的数据是要保留的数据!

网上有的sql的HAVING后面跟的count>1(此处是大坑),注意这样是不对的,如果是count>1这样的话会将原本只有一条的记录删除!!!

还有要注意如果表中的数据有时间限制,要删除某一时间段内的重复数据,一定要在每个范围内加上时间的区间!!!

一般删除操作还是相对危险的,一不小心就会跑路,一定要记得备份!!!

写好的SQL最好在本地模拟数据去删除的试一试!!!

# **4、查詢 表中的重复数据**

  select category_name,count(*) as count from cb_category group by category_name having count>1;

[图片上传失败...(image-b815ec-1591839326818)]

# **5、清空表，可以使得增重置**

truncate table 表名; 

alter table <table name>  auto_increment=2 <u>这个好像没用</u>

# 6、**使用select的值当做 insert into的值**

INSERT INTO `tb_article`(`new_id`, `category_id`, `title`, `bigpic_url`, `source_url`, `images`, `time`, `click`, `origin`, `origin_url`, `is_delete`)

SELECT MAX(new_id)+1, 1905081058472190000, 'adsdasdsasd', 'https://img.pcbaby.com.cn/images/upload/upc/tx/baby_baike/1411/04/c0/40537121_1415074010253_295x220.jpg', 'www.www.www', '', '2019-05-08 10:58:49', 8448, NULL, 'www.www.www', 0 FROM tb_article

批量

INSERT INTO `tb_article`(`new_id`, `category_id`, `title`, `bigpic_url`, `source_url`, `images`, `time`, `click`, `origin`, `origin_url`, `is_delete`)

(SELECT MAX(new_id)+1, 1905081058472190000, 'adsdasdsasd', 'https://img.pcbaby.com.cn/images/upload/upc/tx/baby_baike/1411/04/c0/40537121_1415074010253_295x220.jpg', 'www.www.www', '', '2019-05-08 10:58:49', 8448, NULL, 'www.www.www', 0 FROM tb_article)

UNION ALL

(SELECT MAX(new_id)+2, 1905081058472190000, 'adsdasdsasd', 'https://img.pcbaby.com.cn/images/upload/upc/tx/baby_baike/1411/04/c0/40537121_1415074010253_295x220.jpg', 'www.www.www', '', '2019-05-08 10:58:49', 8448, NULL, 'www.www.www', 0 FROM tb_article)

# 7、**手动批量修改 id为自增 并且从1开始**

update tb_article,(select @i:=0) as it set  new_id =  @i:=@i+1

查询时添加列序号

SELECT  (@i:=@i+1) id ,new_id FROM tb_article,(select @i:=0) as it

# **8、mysql 在某个列里去掉指定字符**

UPDATE cb_category  SET category_name=REPLACE(category_name,'大全','')

# **9、按日期分组统计**

SELECT DATE_FORMAT( video_date, "%Y-%m-%d %H" ) , COUNT( * )

FROM video

GROUP BY DATE_FORMAT( video_date, "%Y-%m-%d %H" )

查询某天：

deteline, "%Y-%m-%d"

某时：

deteline, "%Y-%m-%d %H"

# 10、**分组和排序同时需要**

# 11、**避免插入重复数据**

MySQL 提供了Ignore 用来避免数据的重复插入.

IGNORE :

若有导致unique key 冲突的记录，则该条记录不会被插入到数据库中.

示例:

INSERT IGNORE INTO `table_name` (`email`, `phone`, `user_id`) VALUES ('test9@163.com', '99999', '9999');

这样当有重复记录就会忽略,执行后返回数字0

还有个应用就是复制表,避免重复记录：

INSERT IGNORE INTO `table_1` (`name`) SELECT `name` FROM `table_2`;
