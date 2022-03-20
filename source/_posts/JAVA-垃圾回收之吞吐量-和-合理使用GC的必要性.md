---
title: JAVA-垃圾回收之吞吐量-和-合理使用GC的必要性.md
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
title: JAVA-垃圾回收之吞吐量-和-合理使用GC的必要性.md
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
###吞吐量 （ Throughput )
吞吐量主要关注一个特定时间段内应用系统的最大工作量。衡量吞吐量的指标包括以下内容。
>- 给定时间内完成的事务数。
>- 每小时批处理系统能完成的作业（ job s ）数量。
>-  每小时能完成多少次数据库查询。

在吞吐量方面优化的系统，停顿时间长（ High Pause Times ）也是可以接受的。由于高吞吐量应用运行时间长，所以此时更关心的是如何尽可能快地完成整个任务，而不考虑快速响应。
大家都知道 GC 暂停很容易造成性能瓶颈。现代 NM 在发布的时候都自带了高级的垃圾回收器，不过从我的使用经验来看，要找出某个应用最优的配置真是难上加难 l 。手动调优是必需的，但是你得了解 GC 算法的确切机制才行。用来演示 GC 对吞吐量产生影响的应用只是一个简单的程序，它包含以下两个线程 。

• PigEater ： 它会模仿巨鳞不停吞食大肥猪的过程。代码是通过往 Java.util.List 中添加321在B 字节来实现这点的，每次吞食完后会睡眠 lOOms 。
• P igDigester： 它模拟异步消化的过程 。 实现消化的代码只是将猪的列表置为空。 由于这是个很累的过程，因此每次清除完引用后这个线程都会睡眠 2000ms 。

两个线程都会在一个 while 循环中运行，不停地吃了再消化直到蛇吃饱为止 。 这大概得吃掉 5000 头猪 。

~~~
package com.company;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;

import static com.company.PiginThePython.PigDigester.takeANap;

public class PiginThePython {
    static volatile List pigs = new ArrayList();
    static volatile int pigsEaten = 0;
    static final int ENOUGH_PIGS = 5000;

    public static void main(String[] args) throws InterruptedException {

        String arch = System.getProperty("sun.arch.data.model");
        System.out.println(arch);
        new PigEater().start();
        new PigDigester().start();
    }


    static class PigEater extends Thread {
        @Override
        public void run() {
            while (true) {
                pigs.add(new byte[32 * 1024 * 1024]); //32MB per pig
                if (pigsEaten > ENOUGH_PIGS) {
                    return;
                }
                takeANap(100);
            }
        }
    }


    static class PigDigester extends Thread {
        @Override
        public void run() {
            long start = System.currentTimeMillis();
            while (true) {
                takeANap(2000);
                pigsEaten += pigs.size();
                pigs = new ArrayList();
                if (pigsEaten > ENOUGH_PIGS) {
                    PrintStream format = System.out.format("Digested %d pigs in %d ms .%n ", pigsEaten, System.currentTimeMillis() - start);
                    System.out.println(format.toString());
                    return;
                }
            }

        }

        static void takeANap(int ms) {
            try {
                Thread.sleep(ms);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
~~~

实例一，以如下参数运行
>-Xms4g -Xmx4g -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -Xmn512m 

实例二：以如下参数运行，此次堆内存减半
>-Xms2g -Xmx2g -XX:+UseParallelGC -Xmn1536m



哪个配置的表现会更好一些（就是每秒能吃多少猪〉，来看一下结果 。
· 第一个配置（大堆，大的老年代， CMSGC ）每秒能吞食 8.2 头猪 。
· 第二个配置（小堆，大的新生代， Pare llel GC ）每秒可以吞食 9 . 2 头猪 。
现在来客观地看待一下这个结果 。 分配的资源少了 112 但吞吐量提升了 12% 。 这和常识正
好相反，因此有必要进一步分析下到底发生了什么 。 选择的不同结果也会对吞吐盐和容量规划产生很大的影响。
