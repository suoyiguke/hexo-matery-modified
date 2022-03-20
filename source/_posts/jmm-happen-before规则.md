---
title: jmm-happen-before规则.md
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
title: jmm-happen-before规则.md
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
从 JDK5 开始，java 使用新的 JSR -133 内存模型。 JSR-133 使用 happens-before 的概念来阐述操作之间的内存可见性。 在 JMM 中，如果一个操作执行的结果需要对另一个操作可见，那么这两个操作之间必须要存在 happens-before 关系。 这里提到的两个操作既可以是在一个线程之内，也可以是在不同线程之间。

与程序员密切相关的 happens-before 规则如下：

- 程序顺序规则：一个线程中的每个操作，happens-before于该线程中的任意后续操作。

- 监视器锁规则：对一个锁的解锁，happens-before于随后对这个锁的加锁。

- volatile变量规则：对一个volatile域的写，happens-before于任意后续对这个volatile域的读。

- 传递性：如果A happens-before B，且B happens-before C，那么A happens-before C。

-  start()规则：如果线程A执行操作ThreadB.start()（启动线程B），那么A线程的ThreadB.start()操作happens-before于线程B中的任意操作。

- join()规则：如果线程A执行操作ThreadB.join()并成功返回，那么线程B中的任意操作happens-before于线程A从ThreadB.join()操作成功返回。

- 程序中断规则：对线程interrupted()方法的调用先行于被中断线程的代码检测到中断时间的发生。

- 对象finalize规则：一个对象的初始化完成（构造函数执行结束）先行于发生它的finalize()方法的开始。


`重要` 注意，两个操作之间具有 happens-before 关系，并不意味着前一个操作必须要在后一个操作之前执行！happens-before 仅仅要求前一个操作（执行的结果）对后一个操作可见，且前一个操作按顺序排在第二个操作之前（the first is visible toand ordered before the second）。
~~~
A happens- before B 不是说A在B之前执行，而是说A的操作对B可见。真正的程序执行顺序将由JMM根据A和B的`数据依赖性`、遵循`as-if-serial 语义`来进行`重排序`的
~~~

 happens- before 的定义很微妙，后文会具体说明 happens-before 为什么要这么定义。happens-before 与 JMM 的关系如下图所示

![image.png](https://upload-images.jianshu.io/upload_images/13965490-dd59c993a01d4180.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
如上图所示，一个 happens-before 规则对应于一个或多个编译器和处理器重排序规则。 对于 java 程序员来说，happens-before 规则简单易懂，它避免 java 程序员为了理解 JMM 提供的内存可见性保证而去学习复杂的重排序规则以及这些规则的具体实现。

