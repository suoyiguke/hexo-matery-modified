---
title: jvm-static-静态块特征.md
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
title: jvm-static-静态块特征.md
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
1、在类被初始化时执行
2、只会执行一次，即使被多次new。那也是在第一次new的时候执行，后面几次new都不会执行
> static 一般只在第一次new时执行，而new这个动作时可以控制的


实际运用：
我们可以在一个类的静态块里注入实例的service/dao 对象。
之前的那句结论：“静态块里不能访问实例属性实例方法”不全对。应该改为：

同一个类的静态块不能访问自己的实例属性和实例方法，但是可以访问别的类的实例属性和实例方法。
