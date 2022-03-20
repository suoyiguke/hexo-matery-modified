---
title: mybatis的xml文件坑.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: mybatis的xml文件坑.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
尹凯 7-6 18:24:29
JSR-330 'javax.inject.Inject' annotation found and supported for autowiring
2021-07-06 18:23:50,980 [// -  - ] INFO  com.alibaba.druid.pool.DruidDataSource - {dataSource-1} inited
2021-07-06 18:23:53,871 [// -  - ] INFO  com.alibaba.druid.pool.DruidDataSource - {dataSource-2} inited

尹凯 7-6 18:24:47
家飞哥，我期待service总是卡在这

尹凯 7-6 18:24:55
不知道为什么

尹凯 7-6 18:25:25
clean也不行，删除编译文件也试过了

尹凯 7-6 18:33:06
[图片上传失败...(image-40a2e9-1625567862738)]

彭家飞 7-6 18:33:52
mybatis文件估计写错了

彭家飞 7-6 18:34:08
检查一下你修改过的mybatis

尹凯 7-6 18:34:14
好的


### 1、parameterType取值
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6724f48789385511.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-61fb625f13864e4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>没有set，还写set不然卡死你！





**而且，parameterType可以不写！**

resultMap或resultType是必写的
