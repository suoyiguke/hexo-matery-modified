---
title: spring-事务管理之事务传播行为之实践REQUIRES_NEW（四）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: spring-事务管理之事务传播行为之实践REQUIRES_NEW（四）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
> 纸上得来终觉浅，绝知此事要躬行


这次的主角是    @Transactional(propagation= Propagation.REQUIRES_NEW)；它总是自己创建事务，给人一种另起炉灶，自力更生的感觉


######1、InsertUser 加上requires_new，InsertCuser 不加事务
 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-517e41ff637d01d8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 将事务传播给InsertCuser ，两者使用同一事务

######2、InsertUser 不加事务，InsertCuser  加上requires_new

![image.png](https://upload-images.jianshu.io/upload_images/13965490-913611d39e489e68.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 以非事务状态执行，InsertCuser  创建事务

######3、InsertUser加上requires_new，InsertCuser  加上requires_new
![image.png](https://upload-images.jianshu.io/upload_images/13965490-96f72d1e99e25204.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者各自创建了事务，相互隔离。互不影响

######4、InsertUser加上requires_new，InsertCuser  加上not_supported
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3f0e6c0c641aed16.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser创建了事务，InsertCuser  以非事务的方式执行

######5、InsertUser加上not_supported，InsertCuser  加上requires_new
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aa82b9b0b64056a1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 以非事务的方式执行，InsertCuser  创建了事务

######6、InsertUser加上requires_new，InsertCuser 加上never

![image.png](https://upload-images.jianshu.io/upload_images/13965490-e87eba3e9596361b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser创建事务，InsertCuser 遇到事务报异常
> org.springframework.transaction.IllegalTransactionStateException: Existing transaction found for transaction marked with propagation 'never'


######7、InsertUser加上never ，InsertCuser 加上requires_new
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7dddfd3c4bd8b9b1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser非事务方式执行，InsertCuser 创建事务

######8、InsertUser加上requires_new，InsertCuser 加上nested
 ![image.png](https://upload-images.jianshu.io/upload_images/13965490-8c0c82ee44370161.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 将事务传播给InsertCuser ，两者使用同一事务


######9、InsertUser加上nested ，InsertCuser 加上requires_new
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b7f55ed62f8738cf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者各自创建了事务，相互隔离。互不影响




###大总结
实验|InsertUser `调用者 `|InsertCuser `被调用者`|结果|
 -----------| ----------- | ----------- | ------------ |
1|requires_new|不加|InsertUser 将事务传播给InsertCuser ，两者使用同一事务 |
2|不加|requires_new|InsertUser 以非事务状态执行，InsertCuser 创建事务|
3|requires_new|requires_new|两者各自创建了事务，相互隔离。互不影响|
4|requires_new|not_supported|InsertUser创建了事务，InsertCuser 以非事务的方式执行|
5|not_supported|requires_new|InsertUser 以非事务的方式执行，InsertCuser 创建了事务|
6|requires_new|never|InsertUser创建事务，InsertCuser 遇到事务报IllegalTransactionStateException异常|
7|never|requires_new|InsertUser非事务方式执行，InsertCuser 创建事务|
8|requires_new|nested|InsertUser 将事务传播给InsertCuser ，两者使用同一事务|
9|nested|requires_new|两者各自创建了事务，相互隔离。互不影响|

继续第五篇https://www.jianshu.com/p/6d6e8c563b72
