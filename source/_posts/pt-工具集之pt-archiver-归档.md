---
title: pt-工具集之pt-archiver-归档.md
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
title: pt-工具集之pt-archiver-归档.md
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
pt-archiver 归档 

@北京-青牛-王寒 可以用下归档工具，nohup pt-archiver \
--source h=192.168.32.78,P=3306,u=root,p='123456',D=db1,t=tb1 \
--charset=UTF8 --where 'create_time between '2021-01-01 00:00:00' and '2021-01-31 23:59:59' and data_source=0;' --progress 10000 --limit=10000 --txn-size 10000 --statistics --purge &
