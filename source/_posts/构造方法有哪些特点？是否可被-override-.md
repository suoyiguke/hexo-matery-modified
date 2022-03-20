---
title: 构造方法有哪些特点？是否可被-override-.md
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
特点：

名字与类名相同。
没有返回值，但不能用 void 声明构造函数。
生成类的对象时自动执行，无需调用。
构造方法不能被 override（重写）,但是可以 overload（重载）,所以你可以看到一个类中有多个构造函数的情况。
