---
title: spring-事务管理之事务传播行为之实践NEVER和-NESTED（六）.md
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
title: spring-事务管理之事务传播行为之实践NEVER和-NESTED（六）.md
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

本次的主角是 @Transactional(propagation= Propagation.NEVER)
被申明的方法不会创建事务，调用者方法上使用了事务则报IllegalTransactionStateException 异常

还有@Transactional(propagation= Propagation.NESTED)
这个传播行为的作用和REQUIRED的作用差不多，如果调用者没有事务，它自己会创建事务；如果调用者有事务则加入这个事务。但是它的功能要比REQUIRED强大，它能够让被调用者`部分回滚`。具体的作用以后说


######1、InsertUser 加上never，InsertCuser 不加事务
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9575393a6b0169d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均以无事务的状态运行


######2、InsertUser 不加事务 ，InsertCuser  加上never
![image.png](https://upload-images.jianshu.io/upload_images/13965490-678bf382ab01662d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均以无事务的状态运行


######3、InsertUser 加上never ，InsertCuser  加上never
![image.png](https://upload-images.jianshu.io/upload_images/13965490-be901033f3e70999.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均以无事务的状态运行


######4、InsertUser 加上never ，InsertCuser  加上nested
![image.png](https://upload-images.jianshu.io/upload_images/13965490-371e39703407c5eb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
 InsertUser 无事务状态执行，InsertCuser 创建事务

######5、InsertUser 加上nested ，InsertCuser  加上never
![image.png](https://upload-images.jianshu.io/upload_images/13965490-845e0d123bafc26f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

InsertUser 创建事务，InsertCusr报出异常
>org.springframework.transaction.IllegalTransactionStateException: Existing transaction found for transaction marked with propagation 'never'


######6、InsertUser 加上nested，InsertCuser 不加事务
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e514455974d97b6e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 将事务传播给InsertCuser ，两者使用同一事务

######7、InsertUser 加上不加事务，InsertCuser 加上nested
![image.png](https://upload-images.jianshu.io/upload_images/13965490-249c3278c8e1ceee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 非事务状态执行，InsertCuser 创建事务

######8、InsertUser 加上nested，InsertCuser 加上nested
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1d3ea281f917a3c0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 将事务传播给InsertCuser ，两者使用同一事务

###大总结
实验|InsertUser `调用者 `|InsertCuser `被调用者`|结果|
 -----------| ----------- | ----------- | ------------ |
1|never|不加|两者均以无事务的状态运行 |
2|不加|never|两者均以无事务的状态运行 |
3|never |never|两者均以无事务的状态运行|
4|never |nested|InsertUser 无事务状态执行，InsertCuser 创建事务|
5|nested|never|InsertUser 创建事务，InsertCusr报出异常IllegalTransactionStateException|
6|nested|不加|InsertUser 将事务传播给InsertCuser ，两者使用同一事务|
7|不加|nested|InsertUser 非事务状态执行，InsertCuser 创建事务|
8|nested|nested|InsertUser 将事务传播给InsertCuser ，两者使用同一事务|


