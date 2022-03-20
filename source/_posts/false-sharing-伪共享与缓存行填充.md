---
title: false-sharing-伪共享与缓存行填充.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
---
title: false-sharing-伪共享与缓存行填充.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
Move false-sharing padding to be in bytes rather than long to fit with JDK 15 memory layout changes. see: https://shipilev.net/jvm/objects-inside-out/#_observation_hierarchy_tower_padding_trick_collapse_in_jdk_15 alanger 2021/2/1 22:45



在Cell类的定义中，用了一个独特的注解@sun.misc.Contended， 这是JDK 8之后才有的，背后涉及一个很重要的优化原理：伪共享与缓存行填充。

>CPU缓存失效最小单位是Cache Line

在讲 CPU 架构的时候提到过，每个 CPU 都有自己的缓存。缓存 与主内存进行数据交换的基本单位叫Cache Line（缓存行）。在64位x86架构中，缓存行是64字节，也就是8个Long型的大小。这也意味着当缓存失效，要刷新到主内存的时候，最少要刷新64字节。如图2-4所示，主内存中有变量X、Y、Z（假设每个变量都是一个Long型），被CPU1和CPU2分别读入自己的缓存，放在了同一行Cache Line里面。当CPU1修改了X变量，它要失效整行Cache Line，也就是往总 线上发消息，通知CPU 2对应的Cache Line失效。由于Cache Line是数据交换的基本单位，无法只失效X，要失效就会失效整行的Cache Line，这会导致Y、Z变量的缓存也失效。
据交换的基本单位，无法只失效X，要失效就会失效整行的Cache Line，这会导致Y、Z变量的缓存也失效。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-50903496f244dd54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

虽然只修改了X变量，本应该只失效X变量的缓存，但Y、Z变量也 随之失效。Y、Z变量的数据没有修改，本应该很好地被 CPU1 和 CPU2共享，却没做到，这就是所谓的“伪共享问题”。问题的原因是，Y、Z和X变量处在了同一行Cache Line里面。要解 决这个问题，需要用到所谓的“缓存行填充”，分别在X、Y、Z后面加 上7个无用的Long型，填充整个缓存行，让X、Y、Z处在三行不同的缓
存行中，如图2-5所示。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7766b1c3078bd82c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
下面的代码来自JDK 7的Exchanger类，为了安全，它填充了15（8+7）个long型。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-130211796bec8d0f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在著名的开源无锁并发框架Disruptor中，也有类似的代码：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-de359245fa4eff30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

而在JDK 8中，就不需要写这种晦涩的代码了，只需声明一个@sun.misc.Contended即可。下面的代码摘自JDK 8里面Exchanger中Node的定义，相较于JDK 7有了明显变化。

回到上面的例子，之所以这个地方要用缓存行填充，是为了不让Cell[]数组中相邻的元素落到同一个缓存行里。







![image.png](https://upload-images.jianshu.io/upload_images/13965490-d2f4d649a4484a43.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
