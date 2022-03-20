---
title: java-基础之错误和异常.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---

![image.png](https://upload-images.jianshu.io/upload_images/13965490-768cbbd2ccc997ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
`异常和错误有一个共同的基类java.lang.Throwable`

###错误
error 表示恢复不是不可能但很困难的情况下的一种严重问题。比如说内存溢出。不可能指望程序能处理这样的情况。
比如 栈内存溢出错误(java.lang.StackOverflowError)


###异常
exception 表示一种设计或实现问题。也就是说，它表示如果程序运行正常，从不会发生的情况。
异常(java.lang.Exception)可以分为
######非受检异常
也叫`运行时异常` ，它继承了java.lang.RuntimeException类;虽然不是一定要使用try-catch捕获，但是也可以使用之捕获
> 常见的受检异常有 空指针异常（java.lang.NullPointerException）、除0异常（java.lang.ArithmeticException）、数组越界异常（java.lang.ArrayIndexOutOfBoundsException）、类型强转异常（java.lang.ClassCastException）

######常见运行时异常测试
java.lang.NullPointerException
~~~
Object a = null;
a.equals("1");
~~~
 java.lang.ArithmeticException: / by zero
~~~
int i = 1/0;
~~~
java.lang.ArrayIndexOutOfBoundsException
~~~
int[] arr = new int[1];
arr[2] = 1;
~~~

java.lang.ClassCastException
~~~
 String str = (String) new Object();
~~~



###### 受检异常
受检异常必须被try-catch捕获或throws抛出处理，否则idea将报错
> 常见的受检异常有 反射异常（java.lang.ReflectiveOperationException）、类文件未找到异常（java.lang.ClassNotFoundException）、数据库sql异常（java.sql.SQLException）、文件IO异常（java.io.IOException）

###### 受检异常测试
我们在写jdbc代码时会遇到这种情况，idea提示异常，需要显式的对异常进行try/catch或者在方法的尾巴上  throws SQLException 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c8bcbd1e3e1af11e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


使用try/catch
![image.png](https://upload-images.jianshu.io/upload_images/13965490-be05fdef79dcf70d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在方法尾巴上抛出
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c0522d7bcf4f78f1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
