---
title: spring-事务管理之事务的七大传播行为之理论.md
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
title: spring-事务管理之事务的七大传播行为之理论.md
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
>譬如朝露，去日苦多

事务传播行为： Propagation [ˌprɒpə'ɡeɪʃ(ə)n]

spring 给我们提供了7大传播行为；我们打开org.springframework.transaction.annotation.Propagation类源码可以分别看到这7种：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8bbc698b06f67f1b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这里提出一个概念，方便下面的理解
- 调用者方法
- 被调用者方法

事务的传播行为指的是：当事务方法嵌套调用时， `调用者事务`和`被调用者事务`冲突的解决方案。spring为我们提供了7种解决方案

###支持调用者事务
######required  [rɪˈkwaɪərd]
（必须的）
`这是spring默认的事务传播行为`
- 申明在被调用者上，调用者没有开启事务，则被调用者开启事务；调用者有开启事务，则被调用者加入调用者事务。即`优先使用调用者事务`,此时内部出现异常回滚会使外部调用者事务方法也回滚

- 申明在调用者上，会创建新事务

就好像在公司遇到前端的样式问题一样，前端在就找前端解决，不在就自己解决

~~~
@Transactional(propagation=Propagation.REQUIRED) 
~~~


######supports 
（支持）
`本身不会创建事务`
- 申明在被调用者上，调用者没有开启事务，则被调用者方法就是一个不带事务的方法。调用者有开启事务，则被调用者加入调用者事务
- 申明在调用者上，当前方法以非事务方式运行

就像遇到前端问题，就把问题忽略。不去解决
~~~
@Transactional(propagation=Propagation.SUPPORTS) 
~~~



######mandatory   [ˈmændətɔːri] 
（强制）
`本身不会创建事务`
- 申明在被调用者上，当前方法必须使用`调用者的事务`，如果调用者有事务，就加入。如果没有就抛出IllegalTransactionStateException异常
- 申明在调用者上，报异常IllegalTransactionStateException

就像遇到了比较难以解决的前端问题。前端不在，自己也解决不了
~~~
@Transactional(propagation=Propagation.MANDATORY) 
~~~


###不支持调用者事务

######requires_new
（隔离）
- 申明在被调用者上，不管调用者是否使用事务会都创建一个新的事务，调用者中的事务挂起，等到被调用者事务执行完毕，继续执行调用者中的事务。`一般局部数据操作一致性都用此方法。`
- 申明在调用者上，会创建新事务
~~~
@Transactional(propagation=Propagation.REQUIRES_NEW) 
~~~


######not_supported
（不支持）
本身不会创建事务。
- 申明在被调用者上方法上。调用者事务方法调用此方法时，事务不会进到此方法。即把外部事务挂起，直到此方法执行完后恢复外部事务。
- 申明在调用者上，当前方法以非事务方式运行 

~~~
@Transactional(propagation=Propagation.NOT_SUPPORTED) 
~~~


######never
（强制非事务）
本身不会创建事务。
- 申明在被调用者方法上，调用者方法上使用了事务则报IllegalTransactionStateException
异常 
- 申明在调用者上，当前方法以非事务方式运行 

~~~
@Transactional(propagation=Propagation.NEVER) 
~~~

###嵌套事务
###### nested  [ˈnestɪd]
（嵌套事务）

开始一个 "嵌套的" 事务,  它是已经存在事务的一个真正的子事务。嵌套事务开始执行时,  它将取得一个 savepoint。 如果这个嵌套事务失败, 我们将回滚到此 savepoint。嵌套事务是外部事务的一部分, 只有外部事务结束后它才会被提交。

~~~
 @Transactional(propagation= Propagation.NESTED)
~~~


###我对事务传播行为的个人理解
`事务总是沿着方法的调用方向来传播的`，A方法调用B方法，A方法的事务可能会传播给B方法。不存在B方法事务传播给A方法！具体分为下面几种情况：

- A创建了事务，并将事务传播给B。两者使用同一事务
- A创建了事务，B也创建了事务。两者隔离执行
- A创建了事务，B无事务运行

- A无事务运行，B创建事务
- A无事务运行，B无事务运行

为了深入理解事务的传播行为，我对之做了实验。这篇文章有记录
https://www.jianshu.com/p/bc3cbacf9e70

