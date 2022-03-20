---
title: jvm-关于String字符串的问题大总结.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: jvm-关于String字符串的问题大总结.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
1、String str = new String("abc");  创建了几个字符串对象？

1个或者2个。

>若字符串常量池中未找到"abc"这个对象，那么分别在堆和字符串常量池中创建一个对象，则共创建2个对象;
若字符串常量池中已经存在了"abc"这个对象，那么将在堆中创建一个字符串对象。

但是，若是这样问的： 创建了几个对象？
那么还是 1个或2个，str 是对象的引用而不是对象。

2、
String str="abc";  
毫无疑问，这行代码创建了一个String对象。  
String a="abc";  
String b="abc";   那这里呢？
答案还是一个。  
String a="ab"+"cd";   再看看这里呢？
答案是三个。



