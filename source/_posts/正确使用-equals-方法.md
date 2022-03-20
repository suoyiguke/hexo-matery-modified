---
title: 正确使用-equals-方法.md
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
正确使用 equals 方法 Object的equals方法容易抛空指针异常，应使用常量或确定有值的对象来调用 equals。  举个例子：

  // 不能使用一个值为null的引用类型变量来调用非静态方法，否则会抛出异常 
String str = null; if (str.equals("SnailClimb")) {   ... } else {   .. } 
运行上面的程序会抛出空指针异常，但是我们把第二行的条件判断语句改为下面这样的话，就不会抛出空指针异常，else 语句块得到执行。：

  "SnailClimb".equals(str);// false  


不过更推荐使用 java.util.Objects#equals(JDK7 引入的工具类)。 
~~~
 Objects.equals(null,"SnailClimb");
~~~
// false 我们看一下java.util.Objects#equals的源码就知道原因了。 
 public static boolean equals(Object a, Object b) {   
  // 可以避免空指针异常。如果a=null的话此时a.equals(b)就不会得到执行，避免出现空指针异常。    
 return (a == b) || (a != null && a.equals(b));
 } 


**注意：**

Reference:[Java中equals方法造成空指针异常的原因及解决方案](https://blog.csdn.net/tick_tock97/article/details/72824894)

*   每种原始类型都有默认值一样，如int默认值为 0，boolean 的默认值为 false，null 是任何引用类型的默认值，不严格的说是所有 Object 类型的默认值。
*   可以使用 == 或者 != 操作来比较null值，但是不能使用其他算法或者逻辑操作。在Java中`null == null`将返回true。
*   不能使用一个值为null的引用类型变量来调用非静态方法，否则会抛出异常
