---
title: spring事务失效的12种场景-总结.md
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
title: spring事务失效的12种场景-总结.md
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

事务不生效
1.方法访问权限问题，只支持public
2.方法用final修饰，动态代理不能代理final方法
3.方法内部调用，同一对象内调用没有使用代理，未被aop事务管理器控制
4.未被spring管理
5.多线程调用，事务管理内部使用threadLocal，不同线程间不在同一个SqlSession(更不在同一个事务事务)
6.表不支持事务
7.未配置事务
事务不回滚
8.错误的传播属性
9.自己吞了异常
10.手动抛了别的异常
11.自定义了回滚异常与事务回滚异常不一致
12.嵌套事务回滚多了，需要局部回滚的地方未做异常控制
