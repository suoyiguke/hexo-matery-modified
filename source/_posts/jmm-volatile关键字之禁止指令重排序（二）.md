---
title: jmm-volatile关键字之禁止指令重排序（二）.md
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
title: jmm-volatile关键字之禁止指令重排序（二）.md
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
> 不积跬步，无以至千里

volatile禁止指令重排序情景模式

在一个线程中对两个没有`数据依赖性`的变量进行两个操作，原本是可能发生指令重排序的。但是如果某个变量上使用了volatile关键字，那么情况就会不同了。具体分为3中情况：
>1、对普通变量的读和写
2、对volatile变量的读
3、对vlolatile变量的写

那么对这三种情况进行拍列组合就有 3*3 = 9 种组合方式。具体如下：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-fef6281d42df1bdc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1、坐标（1,3） 当第一个操作为普通的读或写时，若第二个操作为volatile写，则编译器不能重排序这两个操作

2、坐标（2,1）、（2,2）、（2,3）即第二行。 当第一个操作是volatile读时，不管第二个操作是什么，都不能重排序。这个规则确保volatile读之后的操作不会被编译器重排序到volatile读之前

3、坐标(3,2) 当第一个操作是volatile写，第二个操作是volatile读时，不能重排序

4、坐标（1,3）、（2,3）、（3,3）即第3列。当第二个操作是volatile写时，不管第一个操作是什么，都不能重排序

总结：

>1、当第一个操作是volatile读时，不管第二个操作是什么，都不能进行重排序；
2、当第二个操作是voaltile写时，无论第一个操作是什么，都不能进行重排序；
3、当第一个操作是volatile写时，第二个操作是volatile读时，不能进行重排序。


