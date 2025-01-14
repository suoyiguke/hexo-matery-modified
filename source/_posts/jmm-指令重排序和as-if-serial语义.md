---
title: jmm-指令重排序和as-if-serial语义.md
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
title: jmm-指令重排序和as-if-serial语义.md
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


###三种重排序类型
在执行程序时为了提高性能，编译器和处理器常常会对指令做重排序。重排序分三种类型：

1、编译器优化的重排序。编译器在不改变单线程程序语义的前提下，可以重新安排语句的执行顺序。

2、指令级并行的重排序。现代处理器采用了指令级并行技术（Instruction-LevelParallelism， ILP）来将多条指令重叠执行。如果不存在`数据依赖性`，处理器可以改变语句对应机器指令的执行顺序。

3、内存系统的重排序。由于处理器使用缓存和读/写缓冲区，这使得加载和存储操作看上去可能是在乱序执行。从 java 源代码到最终实际执行的指令序列，会分别经历下面三种重排序：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b9128044d7159e0c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 上述的 1 属于编译器重排序，2 和 3 属于处理器重排序。这些重排序都可能会多线程程序出现内存可见性问题。 
- 对于编译器，JMM 的编译器重排序规则会特定类型的编译器重排序（不是所有的编译器重排序都要禁止）。 
- 对于处理器重排排序，JMM 的处理器重排序规则会要求 java 编译器在生成指令序列时，插入特定类型的`内存屏障`（memory barriers，intel 称之为 memory fence）指令，通过内存屏障指令来禁止特定类型的处理器重排序（不是所有的处理器重排序都要禁止）。JMM 属于语言级的内存模型，它确保在不同的编译器和不同的处理器平台之上，通过禁止特定类型的编译器重排序和处理器重排序，为程序员提供一致的内存可见
性保证

###数据依赖性
如果两个操作访问同一个变量，且这两个操作中有一个为写操作，此时这两个操作之间就存在数据依赖性。数据依赖分下列三种类型：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1a58061350b55bc0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 上面三种情况，只要重排序两个操作的执行顺序，程序的执行结果将会被改变。

- 前面提到过，编译器和处理器可能会对操作做重排序。编译器和处理器在重排序时，会遵守数据依赖性，编译器和处理器不会改变存在数据依赖关系的两个操作的执行。

- 注意，这里所说的数据依赖性仅针对单个处理器中执行的指令序列和单个线程中执行的操作，不同处理器之间和不同线程之间的数据依赖性不被编译器和处理器考虑。


###as-if-serial 语义

- as-if-serial 语义的意思指：不管怎么重排序（编译器和处理器为了提高并行度），（单线程）程序的执行结果不能被改变。

- 编译器，runtime 和处理器都必须遵守as-if-serial 语义。为了遵守 as-if-serial 语义，编译器和处理器不会对存在数据依赖关系的操作做重排序，因为这种重排序会改变执行结果。

- 但是，如果操作之间不存在数据依赖关系，这些操作就可能被编译器和处理器重排序。 为了具体说明，请看下面计算圆面积的代码示例：
~~~
double pi = 3.14; //A
double r = 1.0; //B
double area = pi * r * r; //C
System.out.println(area);
~~~
上面三个操作的数据依赖关系如下图所示：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b28ba9af53028cb8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
如上图所示，A 和 C 之间存在数据依赖关系，同时 B 和 C 之间也存在数据依赖关系。因此在最终执行的指令序列中，C 不能被重排序到 A 和 B 的前面（C 排到 AB 的前面，程序的结果将会被改变）。但 A 和 B 之间没有数据依赖关系，编译器处理器可以重排序 A 和 B 之间的执行顺序。下图是该程序的两种执行顺序：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-eee484c3f29b8c38.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
as-if-serial 语义把单线程程序保护了起来，遵守 as-if-serial 语义的编译器，`runtime 和处理器共同为编写单线程程序的程序员创建了一个幻觉：单线程程序是按程序的顺序来执行的。` as-if-serial 语义使单线程程序员无需担心重排序会干扰他们，也无需担心内存可见性问题。

###程序顺序规则
根据 happens- before 的程序顺序规则，上面计算圆的面积的示例代码存在三个happens- before 关系：
~~~
1. A happens- before B；
2. B happens- before C；
3. A happens- before C；
~~~
这里的第 3 个 happens- before 关系，是根据 happens- before 的传递性推导出来的。

这里 A happens- before B，但实际执行时 B 却可以排在 A 之前执行（看上面的重排序后的执行顺序）。`happens- before规则里有说过，如果 A happens- before B，JMM 并不要求 A 一定要在 B 之前执行。 JMM 仅仅要求前一个操作（执行的结果）对后一个操作可见，且前一个操作按顺序排在第二个操作之前。`这里操作 A 的执行结果不需要对操作 B 可见；而且重排序操作 A 和操作 B 后的执行结果，与操作 A 和操作B 按 happens- before 顺序执行的结果一致。在这种情况下，JMM 会认为这种重排序并不非法（not illegal），JMM 允许这种重排序。

在计算机中，软件技术和硬件技术有一个共同的目标：在不改变程序执行结果的前提下，尽可能的开发并行度。编译器和处理器遵从这一目标，从 happens- before的定义我们可以看出，JMM 同样遵从这一目标。

###重排序对多线程的影响
现在让我们来看看，重排序是否会改变多线程程序的执行结果。请看下面的示例代码：
~~~
package test;

class ReorderExample {
    int a = 0;
    boolean flag = false;
    public void writer() {
        a = 1; //1
        flag = true; //2
    }
    public void reader() {
        if (flag) { //3
            int i = a * a; //4
        }
    }
}
~~~
flag 变量是个标记，用来标识变量 a 是否已被写入。 这里假设有两个线程 A 和 A 首先执行 writer()方法，随后 B 线程接着执行 reader()方法。线程 B 在执行4 时，能否看到线程 A 在操作 1 对共享变量 a 的写入？
答案是：不一定能看到。
由于操作 1 和操作 2 没有数据依赖关系，编译器和处理器可以对这两个操作重排序；同样，操作 3 和操作 4 没有数据依赖关系，编译器和处理器也可以对这两个操作重排序。 让我们先来看看，当操作 1 和操作 2 重排序时，可能会产生什么效果？
请看下面的程序执行时序图：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c01aeee6c14c70cd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如上图所示，操作 1 和操作 2 做了重排序。程序执行时，线程 A 首先写标记变量flag，随后线程 B 读这个变量。由于条件判断为真，线程 B 将读取变量 a。此时，变量 a 还根本没有被线程 A 写入，在这里多线程程序的语义被重排序破坏了！
※注：本文统一用红色的虚箭线标识错误的读操作，用绿色的虚箭线标识正确的读操作。下面再让我们看看，当操作 3 和操作 4 重排序时会产生什么效果（借助这个重排序，可以顺便说明`控制依赖性`）。 下面是操作 3 和操作 4 重排序后，程序的执行时序图：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5798aa17a0c8988e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
在程序中，操作 3 和操作 4 存在`控制依赖关系`。 当代码中存在控制依赖性时，会影响指令序列执行的并行度。 为此，编译器和处理器会采用`猜测（Speculation）执行`来克服控制相关性对并行度的影响。 以处理器的猜测执行为例，执行线程 B 的处理器可以提前读取并计算 a*a，然后把计算结果临时保存到一个名为`重排序缓冲（reorder buffer ROB）`的硬件缓存中。当接下来操作 3 的条件判断为真时，就把该计算结果写入变量 i 中。
从图中我们可以看出，猜测执行实质上对操作 3 和 4 做了重排序。重排序在这里破坏了多线程程序的语义！在单线程程序中，对存在控制依赖的操作重排序，不会改变执行结果（这也是 asif-serial 语义允许对存在控制依赖的操作做重排序的原因）；`但在多线程程序中，对存在控制依赖的操作重排序，可能会改变程序的执行结果。`
