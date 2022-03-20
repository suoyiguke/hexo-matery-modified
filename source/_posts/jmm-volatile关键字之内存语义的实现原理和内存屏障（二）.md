---
title: jmm-volatile关键字之内存语义的实现原理和内存屏障（二）.md
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
title: jmm-volatile关键字之内存语义的实现原理和内存屏障（二）.md
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
> 不积小流，无以成江海


###java内存模型中8种原子指令

关于主内存与工作内存之间的交互协议，即一个变量如何从主内存拷贝到工作内存。如何从工作内存同步到主内存中的实现细节。java内存模型定义了8种操作来完成。这8种操作每一种都是原子操作。8种操作如下：


######主内存的操作
1、lock 锁定：主内存，将一个变量标识为某线程独有。
2、unlock 解锁：主内存，将一个锁定状态的变量解除锁定，其他变量可以占用。
######工作内存和执行引擎之间
3、use 使用：作用于工作内存，将变量传递给执行引擎。
4、assign 赋值：作用域工作内存，将执行引擎的执行结果赋值给工作内存中的变量。
主内存和工作内存的同步操作
######主内存到工作内存
5、read 读取：作用于主内存，将主内存的变量传输到工作内存中
6、load 载入：作用于工作内存，将 read 操作读取到的值放入工作内存的副本中
######工作内存到主内存
7、store 存储：作用于工作内存，将工作内存中的一个变量的值传递给主内存
8、write 写入:作用于主内存，将store传递来的值保存到主内存的一个变量中。



###原子指令的遵循规则

Java内存模型还规定了执行上述8种基本操作时必须满足如下规则:

>1、不允许read和load、store和write操作之一单独出现（即不允许一个变量从主存读取了但是工作内存不接受，或者从工作内存发起会写了但是主存不接受的情况）。
read和load、store和write 必须按顺序执行，但没有保证必须连续执行，也就是说，read与load之间、store与write之间是可插入其他指令的。

> 2、不允许一个线程丢弃它的最近的assign操作，即变量在工作内存中改变了之后必须把该变化同步回主内存。

> 3、不允许一个线程无原因地（没有发生过任何assign操作）把数据从线程的工作内存同步回主内存中。

>4、一个新的变量只能从主内存中“诞生”，不允许在工作内存中直接使用一个未被初始化（load或assign）的变量，换句话说就是对一个变量实施use和store操作之前，必须先执行过了assign和load操作。

>5、一个变量在同一个时刻只允许一条线程对其执行lock操作，但lock操作可以被同一个条线程重复执行多次，多次执行lock后，只有执行相同次数的unlock操作，变量才会被解锁。

>6、如果对一个变量执行lock操作，将会清空工作内存中此变量的值，在执行引擎使用这个变量前，需要重新执行load或assign操作初始化变量的值。

>7、如果一个变量实现没有被lock操作锁定，则不允许对它执行unlock操作，也不允许去unlock一个被其他线程锁定的变量。

>8、对一个变量执行unlock操作之前，必须先把此变量同步回主内存（执行store和write操作）。


######java中的内存屏障有4种类型
java中内存屏障分为4种，为硬件层内存屏障的组合情况：
LoadLoad,StoreStore,LoadStore,StoreLoad，借此完成一系列的屏障和数据同步：

>1、LoadLoad
load1;LoadLoad;load2;在load2及之后要读取的数据被访问之前，保证load1要读取的数据已经被读取完毕；

>2、StoreStore
store1;StoreStore;store2;在store2及之后的写操作执行之前，保证store1的写入操作对所有处理器可见；

>3、LoadStore
load1;LoadStore;store2;在store2及之后的写操作执行之前，保证load1要读取的数据已经被读取完毕；

>4、StoreLoad
store1;StoreLoad;load2;在load2及之后要读取的数据被访问之前，保证store1的写入对所有处理器可见。StoreLoad Barriers是一个“全能型”的屏障，它同时具有其他3个屏障的效果。现代的多处理器大多支持该屏障（其他类型的屏障不一定被所有处理器支持）。执行该屏障开销会很昂贵，因为当前处理器通常要把写缓冲区中的数据全部刷新到内存中（Buffer Fully Flush）。


######基于保守策略的JMM内存屏障插入策略

为了实现volatile的内存语义，编译器在生成字节码时，会在指令序列中`插入内存屏障`来禁止特定类型的处理器重排序。
对于编译器来说，发现一个最优布置来最小化插入屏障的总数几乎不可能。为此，JMM采取保守策略。下面是基于保守策略的JMM内存屏障插入策略。

 ![image.png](https://upload-images.jianshu.io/upload_images/13965490-a716fc379a9f06b7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>1、在每个volatile写操作的前面插入一个StoreStore屏障。
>2、在每个volatile写操作的后面插入一个StoreLoad屏障。
>3、在每个volatile读操作的后面插入一个LoadLoad屏障。
>4、在每个volatile读操作的后面插入一个LoadStore屏障。

上述内存屏障插入策略非常保守，但它可以保证在任意处理器平台，任意的程序中都能得到正确的volatile内存语义。

下面是保守策略下，volatile写插入内存屏障后生成的指令序列示意图
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9e9792de10d126f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

