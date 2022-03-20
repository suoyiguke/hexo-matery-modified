---
title: mysql-之AND和OR操作符的计算次序导致的问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: mysql-之AND和OR操作符的计算次序导致的问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
>AND 的优先级高于 OR 。AND会被优先处理；因此会引发一些问题

WHERE可包含任意数目的AND和OR操作符。允许两者结合以进行复杂和高级的过滤。但是，组合AND和OR带来了一个有趣的问题。

为了说明这个问题，来看一个例子。假如需要列出价格为10美元（含）以上且由1002或1003制造的所有产品。下面的SELECT语句使用AND和OR操作符的组合建立了一个WHERE子句：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-977334d69021697c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



请看上面的结果。返回的行中有两行价格小于10美元，显然，
返回的行未按预期的进行过滤。为什么会这样呢？原因在于计算的次序。

 SQL（像多数语言一样）在处理OR操作符前，优先处理AND操作符。当SQL看到上述WHERE子句时，它理解为由供应商1003制造的任何价格为10美元（含）以上的产品，或者由供应商1002制造的任何产品，而不管其价格如何。换句话说，由于AND在计算次序中优先级更高，操作符被错误地组合了

![image.png](https://upload-images.jianshu.io/upload_images/13965490-2108c2ab95284d4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这条SELECT语句与前一条的唯一差别是，这条语句中，前两个条件用圆括号括了起来。因为圆括号具有较AND或OR操作符高的计算次序， DBMS首先过滤圆括号内的OR条件。这时， SQL语句变成了选择由供应商1002或1003制造的且价格都在10美元（含）以上的任何产品，这正是我们所希望的。



在WHERE子句中使用圆括号 任何时候使用具有AND和OR操作符的WHERE子句，都应该使用圆括号明确地分组操作符。`不要过分依赖默认计算次序`，即使它确实是你想要的东西也是如此。`使用圆括号没有什么坏处，它能消除歧义。`
