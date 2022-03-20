---
title: mysql-官网文档怎么看参数？.md
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
title: mysql-官网文档怎么看参数？.md
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
官网文档怎么看参数？可以举几个例子

1、innodb_buffer_pool_size
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b7b9d470844d5429.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


innodb_buffer_pool_size是
- 范围是 Global 全局参数；
- Dynamic	Yes 可以动态修改
- 类型是 Integer 数值类型



2、lower_case_table_names 控制大小写敏感；0区分1不区分
![image.png](https://upload-images.jianshu.io/upload_images/13965490-00cc53bb87bc436f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 范围是 Global 全局参数；
- Dynamic No ，重启服务修改才会生效
- 默认是0，区分大小写
- lower_case_table_names在win下默认是1；linux下默认是0


3、replicate-do-db 从机同步主机的数据库
![image.png](https://upload-images.jianshu.io/upload_images/13965490-42352b8a71b70e9b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这个参数只有一个Type属性，很特殊。。。

5.7后可以在线修改，它的修改方式和普通参数不一样。
>CHANGE REPLICATION FILTER REPLICATE_DO_DB = (d1);




4、binlog_do_db
在配置文件中想当然地配置成binlog_do_db=test,xx,jj，以为是三个库。结果无论什么操作都没有binlog产生
原因
内部将“test,xx,jj”当成一个[数据库]了，结果因为我们没有这个db，自然就啥binlog都没写入了。

处理方法
正确的配置方法应该是这样
binlog_do_db=test
binlog_do_db=xx
binlog_do_db=jj
