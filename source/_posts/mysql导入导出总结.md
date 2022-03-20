---
title: mysql导入导出总结.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: mysql导入导出总结.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
1、将 dbt3_s1_fk.sql恢复到dbt3库中

先创建一个dbt3库,然后直接使用 mysql xxx< xxx.sql 导入
~~~
create database dbt3；
exit;
mysql dbt3 < dbt3_s1_fk.sql
~~~
