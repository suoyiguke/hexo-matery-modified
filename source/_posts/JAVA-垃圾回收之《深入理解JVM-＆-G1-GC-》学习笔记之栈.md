---
title: JAVA-垃圾回收之《深入理解JVM-＆-G1-GC-》学习笔记之栈.md
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
title: JAVA-垃圾回收之《深入理解JVM-＆-G1-GC-》学习笔记之栈.md
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
与程序计数器一样， Java虚拟机栈（Java Virtual Machine Stack） 也是`线程私有的`， 它的生命周期与线程相同。 虚拟机栈描述的是Java方法执行的线程内存模型： 每个方法被执行的时候， Java虚拟机都会同步创建一个`栈帧`[1]（Stack Frame） 用于`存储局部变量表`、 `操作数栈`、 `动态连接`、 `方法出口`等信息。 每一个方法被调用直至执行完毕的过程， 就对应着一个栈帧在虚拟机栈中从入栈到出栈的过程。

栈管运行，堆管存储

######局部变量表
局部变量表存放了编译期可知的各种Java虚拟机基本数据类型（boolean、 byte、 char、 short、 int、float、 long、 double） 、 对象引用（reference类型， 它并不等同于对象本身， 可能是一个指向对象起始地址的引用指针， 也可能是指向一个代表对象的句柄或者其他与此对象相关的位置） 和returnAddress类型（指向了一条字节码指令的地址） 。

这些数据类型在局部变量表中的存储空间以 `局部变量槽（Slot）` 来表示， 其中64位长度的long和double类型的数据会占用两个变量槽， 其余的数据类型只占用一个。 局部变量表所需的内存空间在编
译期间完成分配， 当进入一个方法时， 这个方法需要在栈帧中分配多大的局部变量空间是完全确定的， 在方法运行期间不会改变局部变量表的大小。 请读者注意， 这里说的“大小”是指变量槽的数量，
虚拟机真正使用多大的内存空间（譬如按照1个变量槽占用32个比特、 64个比特， 或者更多） 来实现一个变量槽， 这是完全由具体的虚拟机实现自行决定的事情。


######总结
- 栈也叫栈内存
- 主管java程序的运行，在线程创建时创建，它的生命周期跟随线程的生命周期。线程结束栈内存也就释放
- 栈内存中不存在垃圾回收
- 是线程私有的；线程之前是隔离的
- 8种基本类型变量+对象引用的变量+实例方法都是在栈内存中

###什么是 栈帧
栈帧：jvm虚拟机中的方法就叫做“栈帧”

在jvm下，栈帧就是方法，方法就是栈帧


###栈帧主要保存3类数据：

1、本地变量(Local Variables)
    输入参数和输出参数 和方法内的变量

2、栈操作(Operand Stack)
  记录出栈、入栈的操作

3、栈帧数据(Frame Data)
  包括类文件、方法等等

###栈的运行原理：
- 栈中的数据都是以栈帧（Stack Frame）的格式存在，栈帧是一个内存区块，是一个数据集，是一个有关方法 (Method) 和运行期数据的数据集，当一个方法A被调用时就产生了一个栈帧 F1，并被压入到栈中，

- A方法又调用了 B 方法，于是产生栈帧 F2 也被压入栈，B方法又-调用了 C方法，于是产生栈帧 F3 也被压入栈，

- ……执行完毕后，先弹出 F3 栈帧，再弹出 F2 栈帧，再弹出 F1 栈帧……

- 遵循“先进后出”/“后进先出”原则

- `每个方法执行的同时都会创建一个栈帧`，用于 `存储局部变量表`、`操作数栈`、`动态链接`、`方法出口`等信息，每一个方法从调用直至执行完毕的过程，就对应着一个栈帧在虚拟机中入栈到出栈的过程。栈的大小和具体 JVM 的实现有关，通常在256K~756K之间


![image.png](https://upload-images.jianshu.io/upload_images/13965490-f52cceb74543f716.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###java中方法递归调用导致的错误
- 这是个错误而不是异常
- 在jvm运行时的数据区域中有一个java虚拟机栈，当执行java方法时会进行压栈弹栈的操作。
- 在栈中会保存局部变量，操作数栈，方法出口等等。
- jvm规定了栈的最大深度，当执行时栈的深度大于了规定的深度，就会抛出StackOverflowError错误


Exception in thread "main" java.lang.StackOverflowError
~~~
public class zz {
    public static void gg(){
        gg();
    }
    public static void main(String[] args) {
        gg();
    }
}
~~~
