---
title: oracle-创建用户并授权.md
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
title: oracle-创建用户并授权.md
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


###1、创建用户并赋予权限和默认数据库

>创建用户：创建一个名为 ORCL的用户，密码为123456，指定默认表空间为KMS ，临时表空间为KMS_TEMP
~~~
create user ORCL identified by 123456 default tablespace KMS temporary tablespace KMS_TEMP;
~~~           



###2、给用户授权：
>给ORCL用户授权  connect,resource,dba,sysdba
~~~
grant connect,resource,dba,sysdba to ORLC;
~~~
