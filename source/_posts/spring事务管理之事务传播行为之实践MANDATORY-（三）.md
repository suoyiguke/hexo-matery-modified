---
title: spring事务管理之事务传播行为之实践MANDATORY-（三）.md
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
title: spring事务管理之事务传播行为之实践MANDATORY-（三）.md
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

这次的主角是    @Transactional(propagation= Propagation.MANDATORY )；调用者方法必须存在事务，不然报出IllegalTransactionStateException  异常


继续验证
######1、InsertUser 使用mandatory  ，InsertCuser不加注解
InsertUser 报异常
> org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'

######2、InsertUser 不加注解 ，InsertCuser使用mandatory 
InsertUser 非事务方式执行
InsertCuser报异常
> org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'


######3、InsertUser 使用 mandatory，InsertCuser 使用requires_new
InsertUser 报异常
> org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'


######4、InsertUser 使用 requires_new，InsertCuser 使用mandatory  
![image.png](https://upload-images.jianshu.io/upload_images/13965490-16f564512bcbf162.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 将事务传播给InsertCuser ，两者使用同一事务




######5、InsertUser 使用 mandatory，InsertCuser 使用not_supported
InsertUser 报异常
> org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'
######6、InsertUser 使用not_supported ，InsertCuser 使用mandatory 

![image.png](https://upload-images.jianshu.io/upload_images/13965490-20dda2e930c663d5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 以非事务方式执行，InsertCuser 报错
>org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'

######7、InsertUser 使用 mandatory，InsertCuser 使用never
InsertUser 报异常
> org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'

######8、InsertUser 使用 never，InsertCuser 使用 mandatory

![image.png](https://upload-images.jianshu.io/upload_images/13965490-0e6febaad95734e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 非事务状态执行，InsertCuser报异常
> org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'
######9 、InsertUser 使用 mandatory，InsertCuser 使用 nested 
InsertUser 报异常
> org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'

######10、InsertUser 使用 nested  ，InsertCuser 使用 mandatory
![image.png](https://upload-images.jianshu.io/upload_images/13965490-efbe3ec384178031.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 将事务传播给InsertCuser ，两者使用同一事务


###大总结

实验|InsertUser `调用者 `|InsertCuser `被调用者`|结果|
 -----------| ----------- | ----------- | ------------ |
1|mandatory |不加| InsertUser 报异常IllegalTransactionStateException  |
2|不加|mandatory | InsertUser 非事务方式执行，InsertCuser报异常 IllegalTransactionStateException |
3|mandatory |requires_new| InsertUser 报异常IllegalTransactionStateException |
4|requires_new |mandatory|InsertUser 将事务传播给InsertCuser ，两者使用同一事务|
5|mandatory|not_supported|InsertUser 报异常IllegalTransactionStateException |
6|not_supported|mandatory|InsertUser 以非事务方式执行，InsertCuser 报错IllegalTransactionStateException |
7|mandatory|never|InsertUser 报异常IllegalTransactionStateException  |
8|never|mandatory|InsertUser 以非事务方式执行，InsertCuser 报错IllegalTransactionStateException |
9|mandatory|nested|InsertUser 报异常IllegalTransactionStateException  | 
10|nested|mandatory|InsertUser 将事务传播给InsertCuser ，两者使用同一事务 |

继续第四篇
https://www.jianshu.com/p/08e5c7d30d51
