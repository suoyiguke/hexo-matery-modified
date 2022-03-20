---
title: jvm-字符串常量池-interned-strings(一).md
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
title: jvm-字符串常量池-interned-strings(一).md
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
###何为字符串常量池？
在 Java 语言中有 8 种基本类型和一种比较特殊的类型 String。这些类型为了使它们在运行过程中速度更快、更节省内存，都提供了一种`常量池`的概念。
常量池就类似一个 Java 系统级别提供的缓存。 8 种基本类型的常量池都是系统协调的， String 类型的常量池比较特殊 。 

>它的主要使用方法有两种。
1、直接使用双引号声明出来的 String 对象会直接存储在常量池中。
2、如果不是用双引号声明的 String 对象，可以使用 String 提供的 intern 方法。 intern 方法会从字符串常量池中查询当前字符串是否存在，若不存在就会将当前字符串放入常量池中。


###字符串常量池在各个JDK版本中有很大变化



######JDK6中的字符串常量池



>JDK6中的字符串常量池存在于PermGen 永久代。

PermGen 区是一个类静态的区域，主要存储一些加载类的信息、常量池、方法片段等内容，默认大小只有 4MB，一旦常量池中大量使用 intern 是会直接产生Java.lang.OutOtMemoryError: PermGen space 错误的。所以在 JDK7 的版本中，字符串常量池己经从 PermGen 区移到正常的 Java Heap 区域了。为什么要移动， PermGen  区域太小就是其中一个主要原因。





######JDK7中的字符串常量池

>JDK7时，字符串常量池已经从 PermGen 代移到了堆中。

JDK7 中 Oracle 的工程师对字符串池的逻辑做了很大的改变，`即将字符串池的位置调整到 Java 堆内`，这个改动意味着你再也不会被固定的内存空间限制了。所有的字符串都保存在堆(Heap ）中，和其他普通对象一样，这样可以让你在进行调优应用时仅需要调整堆大小就可以了。字符串池概念原本使用得比较多，但是这个改动使得我们有足够的理由让我们重新考虑在JDK7中使用 String.intem()。


######JDK8中的字符串常量池

>JDK8时虽然完全干掉了永久代，并使用元空间取而代之。但是字符串常量池 interned strings 仍然存在于堆中，并没有再次调整




关于永久代PermGen 和元空间 Metaspace可以看看这篇文章：
https://www.jianshu.com/p/22b6501a041c



###我们可以做实验来验证各个JDK版本下的字符串常量池
如下代码，打印当前JDK版本号。循环调用intern方法将拼接后的字符串放到常量池。这样常量池中的字符串对象会越来越多。直到发生OOM。我们可以通过观察各个版本的OOM出错位置来判断字符串常量池在JVM中哪个区域。
~~~
package com.company;
import java.util.ArrayList;
import java.util.List;
class Main{
    static String  base = "string";
    public static void main(String[] args) {
        System.out.println(System.getProperty("java.version"));
        List<String> list = new ArrayList<String>();
        for (int i=0;i< Integer.MAX_VALUE;i++){
            base = base.concat(base);
            list.add(base.intern());//插入到字符常量池中
        }
    }
}

~~~

######JDK1.6
方法区（即JDK 6的HotSpot虚拟机中的PermGen space 永久代）
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2458103456a4be09.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######JDK1.7
Java heap space  堆
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e0bae852c091cd80.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######JDK1.8
Java heap space 堆

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b97d374c8fc205bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###指定常量池大小

>Error: Could not create the Java Virtual Machine.
Error: A fatal exception has occurred. Program will exit.
StringTable size of 100 is invalid; must be between 1009 and 2305843009213693951
~~~
-XX:StringTableSize=1009 
~~~



###字符串常量池能被GC
是的，JVM字符串常量池中所有的字符串都能被垃圾回收掉，前提条件是那些不再被GC Roots引用的字符串 -- 这个结论适用于我们正在讨论的JDK6，7，8三个版本。这就意味着，如果你通过String.intern()池化的字符串超过了范围，并且不再被引用，那么它们是可以被GC掉的。

字符串常量池中的字符串能够被GC，也能保留在Java堆中。这样看来，对所有字符串来说，字符串常量池似乎是一个很合适的地方，理论上是这样的 -- 没有使用的字符串会在常量池中被GC掉，使用的字符串允许你保存在内存中，这样当然取等值的字符串时就能直接从常量池中取出来。听起来似乎是一个完美的保存策略，但是在下结论之前，你需要先了解字符串常量池实现的细节。
