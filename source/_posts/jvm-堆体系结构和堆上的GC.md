---
title: jvm-堆体系结构和堆上的GC.md
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
title: jvm-堆体系结构和堆上的GC.md
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
###java堆物理结构的示意图
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ef61c207c320064d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
1、Eden和Form、To的大小比值为 8:1:1
2、新生代与老年代比值为 1:2


###概念说明
`一些概念有很多个名字`
1、GC = YGC(youce GC 年轻的GC)  = 轻量级GC = Minor GC = 普通GC
2、Full GC = FGC  = MajorGC = 全局GC
3、from space = S0区 = SurvivorFrom 区 =幸存者1区 
4、to space = S1区 =  SurvivorTo区=幸存者2区
5、eden space= 伊甸园区
6、PSYoungGen = 新生区 =  新生代
7、ParOldGen = 老年区 = 老年代 
8、Metaspace = 元空间

一个JVM实例只存在一个堆内存，`堆内存的大小是可以调节的`。类加载器读取了类文件后，需要把类、方法、常变量放到堆内存中，保存所有引用类型的真实信息，以方便执行器执行，堆内存分为三部分：新生代、老年代 、永久区（1.8是元空间）
###新生代       Young/New

新生代是类的诞生、成长、消亡的区域，一个类在这里产生，应用，最后被垃圾回收器收集，结束生命。新生代又分为两部分：伊甸区（Eden Space）和幸存者区（Survivor space），`所有的类都是在伊甸区被new出来的`。

新生代可分为三块区域         
- 伊甸区     
- 幸存者0区(from区)             
- 幸存者1区(to区)  

###老年代 Old/ Tenure

经过多次Minor GC依旧存活 或 大对象 或 达到新生区内存空间达到某种阈值,对象会放置到养老区,该区域较少进行GC

###永久区 Perm

永久存储区是一个常驻内存区域，`用于存放JDK自身所携带的Class,Interface 的元数据`，**也就是说它存储的是运行环境必须的类信息**，被装载进此区域的数据是不会被垃圾回收器回收掉的，关闭 JVM 才会释放此区域所占用的内存。方法区是逻辑上定义的一个区域,永久区是方法区的具体实现,逻辑上被划分在堆区域,但实际上永久带并不属于堆

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c1be95c31186112f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- java7逻辑上划分：新生+养老+永久存储区（逻辑概念，实际不存在）
- java8逻辑上划分：新生+养老+元空间（逻辑概念，实际不存在）
- 物理上划分：新生+养老




###堆上的GC

####具体流程

1、`所有的类都是在伊甸区被new出来的`，当伊甸的空间用完时，程序又需要创建对象，JVM的垃圾回收器将对伊甸区进行垃圾回收（Minor GC），将伊甸区中的不再被其他对象所引用的对象进行销毁。然后将伊甸区中的剩余对象移动到幸存0区。若幸存0区也满了，再对该区进行垃圾回收，然后移动到1区。如果1区也满了，再移动到养老区。

2、若养老区也满了，那么这个时候将产生Major GC（Full GC），进行养老区的内存清理。若养老区执行了FUll GC之后发现依然无法进行对象的保存，就会产生OOM异常『OutOfMemoryError』。

3、如果出现java.lang.OutOfMemoryError:Java heap space异常，说明Java虚拟机的堆内存不够，原因有两点：

- Java虚拟机的堆内存设置不够，可以通过参数-Xms、-Xmx来调整。
- 代码中创建了大量大对象，并且长时间不能被垃圾收集器收集（存在被引用）。

伊甸区（new 对象） ==Minor GC（GC）=> 幸存1区====>幸存2区==Major GC(Full GC)==>养老区


####GC发生的地方
- GC（较小收集）只发生在jvm堆内存.新生代.伊甸区
- Full GC（较大收集）大部分发生在老年代
 ![image.png](https://upload-images.jianshu.io/upload_images/13965490-a34bfec2f188a6c8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
####GC和Full GC 的区别
JVM在进行GC时，并非每次都对上面三个内存区域一起回收的，大部分时候回收的都是指新生代，因此GC按照回收的区域又分为两种类型：

普通GC（Minor GC）：只针对新生代区域的GC，因为Java对象大多都具备朝生夕灭的特性，所以MiniorGC非常频繁，一般回收速度也比较快
全局GC（Major GC or Full GC）：针对老年代的GC，偶尔伴随对新生代的minor GC以及方法区的GC，`Major GC的速度一般会比Minor GC慢10倍以上`


####MinorGC的过程（复制->清空->互换）


1、  eden（伊甸园区）、SurvivorFrom （幸存者Form区）复制到 SurvivorTo（幸存者to区），年龄+1

首先，当Eden区满的时候会触发第一次GC,把还活着的对象拷贝到SurvivorFrom区，当Eden区再次触发GC的时候会扫描Eden区和From区域,对这两个区域进行垃圾回收，经过这次回收后还存活的对象,则直接复制到To区域（如果有对象的年龄已经达到了老年的标准，则赋值到老年代区），同时把这些对象的年龄+1

2、 清空 eden、SurvivorFrom

然后，清空Eden和SurvivorFrom中的对象，也即复制之后有交换，谁空谁是to

3、 SurvivorTo和 SurvivorFrom 互换

最后，SurvivorTo和SurvivorFrom互换，原SurvivorTo成为下一次GC时的SurvivorFrom区。部分对象会在From和To区域中复制来复制去,如此交换15次(由JVM参数MaxTenuringThreshold决定,这个参数默认是15),最终如果还是存活,就存入到老年代
~~~
#####幸存者区之间交换：
幸存者1和2区之间会在每次GC后交换: from区和to区，他们的位置和名分，不是固定的，每次GC后会交换。谁空了谁是to区
~~~


第一次GC： 伊甸园区满了，触发GC，将没有被干掉的变量复制到Form区

第二次GC：伊甸园区再次满了，触发GC，扫描Eden区和From区域,对这两个区域进行垃圾回收，经过这次回收后还存活的对象,则直接复制到To区域
第三次 。。。。

第十五 次GC：对象的年龄已经达到了老年的标准，则赋值到老年代区

####方法区和永久代的区别
方法区（Method Area）与Java堆一样，是各个线程共享的内存区域，它用于存储已被虚拟机加载的类信息、 常量、 静态常量、 即时编译器编译后的代码等数据。 虽然Java虚拟机规范把方法区描述为堆的一个逻辑部分，但是它却有一个别名叫做Non-Heap（非堆），目的应该是与Java堆区分开来。

- 对于HotSpot虚拟机，很多开发者习惯将方法区称之为“永久代(Parmanent Gen)” ，但严格本质上说两者不同，或者说使用永久代来实现方法区而已，永久代是方法区(相当于是一个接口interface)的一个实现
- jdk1.7的版本中，已经将原本放在永久代的字符串常量池移走。
- jdk1.8以后 。永久代被移除，转换为元空间。
- 永久代中存的是rt.jar包中常用的类，不可能被GC!

###java7和java8在jvm堆结构划分上的区别
- java7 在堆上的GC
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e0b25f7adcebcb24.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- java8 在堆上的GC
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ee30c965aad700b0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



