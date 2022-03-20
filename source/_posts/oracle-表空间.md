---
title: oracle-表空间.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: oracle
categories: oracle
---
---
title: oracle-表空间.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: oracle
categories: oracle
---
###创建表空间
~~~
CREATE  
TABLESPACE KMS
DATAFILE 'D:\app\Administrator\oradata\orcl\KMS.DBF' 
SIZE 1024M 
REUSE 
AUTOEXTEND 
ON NEXT 100M
MAXSIZE unlimited 
EXTENT MANAGEMENT LOCAL UNIFORM SIZE 1024K;
~~~

###指定用户的默认表空间
指定用户BSOFT  的默认表空间为 HISDB
~~~
alter user BSOFT  
default tablespace HISDB
~~~

###查看当前用户及默认表空间
~~~
select username,default_tablespace from user_users
~~~
