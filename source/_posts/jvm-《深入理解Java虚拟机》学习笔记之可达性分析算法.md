---
title: jvm-《深入理解Java虚拟机》学习笔记之可达性分析算法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: JAVA-GC
categories: JAVA-GC
---
---
title: jvm-《深入理解Java虚拟机》学习笔记之可达性分析算法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: JAVA-GC
categories: JAVA-GC
---
>驽马十驾，功在不舍

######可达性分析算法的应用
当前主流的商用程序语言（Java、 C#， 上溯至前面提到的古老的Lisp） 的内存管理子系统， 都是通过可达性分析（Reachability Analysis） 算法来判定对象是否存活的。 

######具体内容
这个算法的基本思路就是通过一系列称为`GC Roots`的根对象作为起始节点集， 从这些节点开始， 根据引用关系向下搜索， 搜索过程所走过的路径称为`引用链`（Reference Chain） ， 如果某个对象到GC Roots间没有任何引用链相连，或者用图论的话来说就是从GC Roots到这个对象不可达时， 则证明此对象是不可能再被使用的。


如下图， 对象object 5、 object 6、 object 7虽然互有关联， 但是它们到GC Roots是不可达的，因此它们将会被判定为可回收的对象。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7feca4d91a90e7e7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

简单来说：
> 没有被GC roots  引用链引用的对象就是不可达的，不可达的对象会被GC回收


######java中哪些对象是GC Roots根对象？
在Java技术体系里面， 固定可作为GC Roots的对象包括以下几种：

>1、在虚拟机栈（栈帧中的本地变量表） 中引用的对象， 譬如各个线程被调用的方法堆栈中使用到的参数、 局部变量、 临时变量等。
>2、在方法区中类静态属性引用的对象， 譬如Java类的引用类型静态变量。
>3、在方法区中常量引用的对象， 譬如字符串常量池（String Table） 里的引用。
>4、在本地方法栈中JNI（即通常所说的Native方法） 引用的对象。


>5、Java虚拟机内部的引用， 如基本数据类型对应的包装对象， 一些常驻的异常对象（比如NullPointExcepiton、OutOfMemoryError） 等， 还有系统类加载器。
>6、所有被同步锁（synchronized关键字） 持有的对象。
>7、反映Java虚拟机内部情况的JMXBean、 JVMTI中注册的回调、 本地代码缓存等。
>8、除了这些固定的GC Roots集合以外， 根据用户所选用的垃圾收集器以及当前回收的内存区域不同， 还可以有其他对象“临时性”地加入， 共同构成完整GC Roots集合。 譬如  `分代收集`和`局部回收`（Partial GC） ， 如果只针对Java堆中某一块区域发起垃圾收集时（如最典型的只针对新生代的垃圾收集） ， 必须考虑到内存区域是虚拟机自己的实现细节（在用户视角里任何内存区域都是不可见的） ， 更不是孤立封闭的， 所以某个区域里的对象完全有可能被位于堆中其他区域的对象所引用， 这时候就需要将这些关联区域的对象也一并加入GC Roots集合中去， 才能保证可达性分析的正确性。
