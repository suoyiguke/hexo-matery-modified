---
title: spring事务传播行为之应用.md
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
title: spring事务传播行为之应用.md
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
业务操作中记录日志。如果业务异常失败，将回滚，但日志继续记录异常(不回滚)

1、使用事务的传播行为来实现
业务上加 requetd ， 日志上加 no_suupurs
业务上加 requetd , 日志上加reuerds_new

但是这种方法有问题： 业务方法在调用日志记录方法之前出现异常，那么日志方法根本得不到执行！



2、建议用一个全局拦截器，在其中 try catch 所有异常，然后做下日志即可，业务层事务有异常回滚事务以后，仍然会向外抛出异常



3、当然最好的方法是,异步处理(mq,线程池,kafka等等),这才是合理解决方案


4、使用aop的异常通知实现记录日志
