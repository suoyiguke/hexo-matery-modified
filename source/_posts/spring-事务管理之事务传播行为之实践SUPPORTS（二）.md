---
title: spring-事务管理之事务传播行为之实践SUPPORTS（二）.md
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
title: spring-事务管理之事务传播行为之实践SUPPORTS（二）.md
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

继续验证，这次的主角是 
@Transactional(propagation= Propagation.SUPPORTS)
它总是使用调用者事务，若调用者没事务则以无事务状态执行

######1、InsertUser 使用supports ，InsertCuser 不加注解

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7c13d2b481ee2e2e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均以无事务的状态运行

######2、InsertUser 不加注解，InsertCuser 使用supports 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0d18fa049e0ed6e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均以无事务的状态运行

######3、InsertUser 使用supports ，InsertCuser 使用supports 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7efb658dffd89e6d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均以无事务的状态运行

######4、InsertUser 使用supports ，InsertCuser 使用mandatory
报异常
> org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'


######5、InsertUser 使用mandatory，InsertCuser 使用supports
报异常
> org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'

######6、InsertUser 使用supports，InsertCuser 使用requires_new
![image.png](https://upload-images.jianshu.io/upload_images/13965490-379eaf6629a4d96d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

InsertUser 非事务方式执行，InsertCuser 创建了事务

######7、InsertUser 使用requires_new ，InsertCuser 使用supports
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d933ce460bc8f734.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 将事务传播给InsertCuser ，两者使用同一事务

######8、InsertUser 使用supports，InsertCuser 使用not_supported
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e4ee059d34f3f711.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两者均以无事务的状态运行


######9、InsertUser 使用not_supported ，InsertCuser 使用supports
两者均以无事务的状态运行

######10、InsertUser 使用supports，InsertCuser 使用never
两者均以无事务的状态运行

######11、InsertUser 使用never ，InsertCuser 使用supports
两者均以无事务的状态运行


######12、InsertUser 使用supports，InsertCuser 使用nested
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aa2e0c500985db08.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 非事务方式执行，InsertCuser 创建了事务

######13、InsertUser 使用nested ，InsertCuser 使用supports
![image.png](https://upload-images.jianshu.io/upload_images/13965490-303c37cf35de8413.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 将事务传播给InsertCuser ，两者使用同一事务



###大总结

实验|InsertUser `调用者 `|InsertCuser `被调用者`|结果|
 -----------| ----------- | ----------- | ------------ |
1|supports|不加| 两者均以无事务的状态运行 |
2|不加|supports| 两者均以无事务的状态运行 |
3|supports|supports| 两者均以无事务的状态运行 |
4|supports|mandatory | 报异常 IllegalTransactionStateException|
5|mandatory |supports| 报异常 IllegalTransactionStateException |
6|supports|requires_new| InsertUser 非事务方式执行，InsertCuser 创建了事务 |
7|requires_new|supports| InsertUser 将事务传播给InsertCuser ，两者使用同一事务|
8|supports|not_supported|两者均以无事务的状态运行|
9|not_supported|supports| 两者均以无事务的状态运行|
10|supports|never| 两者均以无事务的状态运行|
11|never|supports| 两者均以无事务的状态运行|
12|supports|nested| InsertUser 非事务方式执行，InsertCuser 创建了事务|
13|nested|supports| InsertUser 将事务传播给InsertCuser ，两者使用同一事务|

继续第三篇
https://www.jianshu.com/p/2156a6eb7038
