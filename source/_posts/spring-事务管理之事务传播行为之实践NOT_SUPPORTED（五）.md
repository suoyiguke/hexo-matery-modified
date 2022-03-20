---
title: spring-事务管理之事务传播行为之实践NOT_SUPPORTED（五）.md
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
title: spring-事务管理之事务传播行为之实践NOT_SUPPORTED（五）.md
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


这次的主角是@Transactional(propagation= Propagation.NOT_SUPPORTED)
调用者事务方法调用使用该注解的申明方法时，事务不会进到此方法。即把外部事务挂起，直到此方法执行完后恢复外部事务。


######1、InsertUser 加上not_supported ，InsertCuser 不加事务
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a1149d1a4f243f1e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均不使用事务
######2、InsertUser 不加事务 ，InsertCuser 加上not_supported 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-165d32059dd8ef55.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均不使用事务
######3、InsertUser 加上 not_supported，InsertCuser 加上not_supported
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3abcd15dea2505a5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均不使用事务
######4、InsertUser 加上 not_supported，InsertCuser 加上never
![image.png](https://upload-images.jianshu.io/upload_images/13965490-158d352d0424ad67.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均不使用事务
######5、InsertUser 加上never ，InsertCuser 加上not_supported
![image.png](https://upload-images.jianshu.io/upload_images/13965490-447f58346c062430.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均不使用事务


######6、InsertUser 加上not_supported，InsertCuser 加上nested
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ddcbac42952e91b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 非事务状态执行，InsertCuser 开启事务
######7、InsertUser 加上nested，InsertCuser 加上not_supported
![image.png](https://upload-images.jianshu.io/upload_images/13965490-628840c6045ae680.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser  开启事务，InsertCuser 非事务状态执行


###大总结
实验|InsertUser `调用者 `|InsertCuser `被调用者`|结果|
 -----------| ----------- | ----------- | ------------ |
1|not_supported |不加|两者均不使用事务 |
2|不加|not_supported |两者均不使用事务 |
3|not_supported |not_supported |两者均不使用事务|
4|not_supported|never|两者均不使用事务|
5|never |not_supported|两者均不使用事务|
6|not_supported|nested|InsertUser 非事务状态执行，InsertCuser 开启事务|
7|nested|not_supported|InsertUser 开启事务，InsertCuser 非事务状态执行|

继续第六篇
https://www.jianshu.com/p/067ab40f3637
