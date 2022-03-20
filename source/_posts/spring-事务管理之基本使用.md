---
title: spring-事务管理之基本使用.md
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
title: spring-事务管理之基本使用.md
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
我们知道spring事务可以分为`申明式事务`和`编程式事务`

>- 编程式事务 在代码中显式调用begin Transaction() commit(). rollback() 等事务管理相关的方法
>- 申明式事务 则是基于AOP面向切面编程思想的优秀用法；在ssm框架的工程中直接也使用配置xml的方式配置事务；现在springboot中推荐使用注解的方式


springboot中使用事务的核心就是@Transactional注解，这个注解在tx包中
![image.png](https://upload-images.jianshu.io/upload_images/13965490-40e37be5f9351e4c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
我使用的mybatis_plus依赖也是依赖了这个rx包。所以不需要添加maven配置了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-55be938241379f5d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





###@Transactional有十大参数
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bc9d20539b0ba6a1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>- value 指定事务管理器
>-  transactionManager 和value一样配置了多个事务管理器时，可以使用该属性指定选择哪个事务管理器
>- isolation 事务隔离级别
>- noRollbackFor 设置不需要进行回滚的异常类数组
> - noRollbackForClassName 设置不需要回滚的异常类名称数组
> - propagation 事务传播行为
> - readOnly 是否为只读事务
> - rollbackFor 指定回滚的异常类数组
>- rollbackForClassName 指定回滚的异常类名称数组
>- timeout 设置事务的超时秒数


######isolation 
我们可以在@Transactional中使用isolation参数设置当前事务的隔离级别

> @Transactional(isolation = Isolation.READ_UNCOMMITTED)：读取未提交数据(会出现脏读, 不可重复读) 基本不使用
@Transactional(isolation = Isolation.READ_COMMITTED)：读取已提交数据(会出现不可重复读和幻读)
@Transactional(isolation = Isolation.REPEATABLE_READ)：可重复读(会出现幻读) `mysql中默认级别`
@Transactional(isolation = Isolation.SERIALIZABLE)：串行化

关于mysql的事务隔离级别可以看看我的这篇文章https://www.jianshu.com/p/653e6eec3acb
######propagation
设置事务的传播行为
https://www.jianshu.com/p/437538a5e5c2

######noRollbackFor 
设置不需要进行回滚的`异常类数组`
~~~
@Transactional(noRollbackFor = {RuntimeException.class, Exception.class})
~~~
######noRollbackForClassName 
设置不需要回滚的`异常类名称数组`
~~~
@Transactional(noRollbackForClassName= {"RuntimeException","Exception"})
~~~
######rollbackFor 
设置回滚的`异常类数组`
~~~
@Transactional(rollbackFor = {RuntimeException.class, Exception.class})
~~~
######rollbackForClassName
设置回滚的`异常类名称数组`
~~~
@Transactional(rollbackForClassName= {"RuntimeException","Exception"})
~~~

######readOnly 
设置当前事务是否为只读事务，设置为true表示只读，false则表示可读写，`默认值为false`；这个属性是非常有必要的！具体的解释我的这篇文章有提到 https://www.jianshu.com/p/f2ab7aee4e95

######timeout 
设置事务的超时秒数，`默认值为-1表示永不超时`




###@Transactional注解的使用注意
1、@Transactional可以使用类或接口和方法上，推荐使用在service的实现类上(一般不建议在接口上上添加@Transactional)，可以将整个类纳入spring事务管理，在每个业务方法执行时都会开启一个事务，不过这些事务采用相同的管理方式。若同时在类和方法上使用，方法上注解的优先级大于类上。

2、@Transactional 注解只能应用到 public 可见度的方法上。 如果应用在protected、private或者 package可见度的方法上，也不会报错，不过事务设置不会起作用。

3、默认情况下，Spring会对`运行时异常/非受检异常 unchecked`进行事务回滚；如果是`受检异常checked`则不回滚。 使用@Transactional(rollbackFor=Exception.class)就能够回滚受检异常，而且方法需要显式的`抛出异常`，这样事务就会回滚。若受检异常自行使用try-catch处理不抛出则不会回滚

4、其实可以使用api手动进行回滚。如下
~~~
TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
~~~
但是这种方式不推荐使用，既然都使用注解的aop形式解耦了。就不要再反其道而行之了。不然这代码可就是四不像了


关于运行时异常和检查类异常可以看看我这篇文章https://www.jianshu.com/p/590a7f5c340b




####spring的事务到底在什么时候回滚？
出现异常，并且没有被处理的时候
