---
title: final关键字.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jmm
categories: jmm
---
---
title: final关键字.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jmm
categories: jmm
---
答案是：a，b未必一定等于1，2。和DCL的例子类似，也就是构造
函数溢出问题。obj=new Example（）这行代码，分解成三个操作：
① 分配一块内存；
② 在内存上初始化i=1，j=2；
③ 把obj指向这块内存。
操作②和操作③可能重排序，因此线程B可能看到未正确初始化的 值。对于构造函数溢出，通俗来讲，就是一个对象的构造并不是“原 子的”，当一个线程正在构造对象时，另外一个线程却可以读到未构造好的“一半对象”。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-3cc63d630ac439ec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### final的happen-before语义
要解决这个问题，不止有一种办法。
办法1：给i，j都加上volatile关键字，禁止指令重排序。
办法2：为read/write函数都加上synchronized关键字。
如果i，j只需要初始化一次，则后续值就不会再变了，还有办法3，为其加上final关键字。
之所以能解决问题，是因为同volatile一样，final关键字也有相
应的happen-before语义：
（1）对final域的写（构造函数内部），happen-before于后续对
final域所在对象的读。
（2）对final域所在对象的读，happen-before于后续对final域
的读。
通过这种happen-before语义的限定，保证了final域的赋值，一 定在构造函数之前完成，不会出现另外一个线程读取到了对象，但对 象里面的变量却还没有初始化的情形，避免出现构造函数溢出的问
题。
关于final和volatile的特性与背后的原理，到此为止就讲完了， 在后续Concurrent包的源码分析中会反复看到这两个关键字的身影。
接下来总结常用的几个happen-before规则。
