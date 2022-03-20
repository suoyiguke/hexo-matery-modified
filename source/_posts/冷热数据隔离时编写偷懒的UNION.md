---
title: 冷热数据隔离时编写偷懒的UNION.md
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
title: 冷热数据隔离时编写偷懒的UNION.md
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
先到热数据表里查，没有再查冷数据的

~~~
	SELECT logistics_username from (
	select greatest(@found:=-1,1) as x,logistics_username from client_order_ext WHERE  order_no = 'GO640070337175759'
union all select 2 AS x,logistics_username from client_order_ext_60 where  order_no = 'GO640070337175759' and @found is null 
union all select 0 AS x ,'reset' from dual where (@found:=NULL) is not null ) a
~~~





![image.png](https://upload-images.jianshu.io/upload_images/13965490-9d8c0c2288eaa211.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
