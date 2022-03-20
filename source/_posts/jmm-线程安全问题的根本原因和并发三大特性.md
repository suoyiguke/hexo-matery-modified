---
title: jmm-线程安全问题的根本原因和并发三大特性.md
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
title: jmm-线程安全问题的根本原因和并发三大特性.md
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
###导致出现并发问题的根本原因
- CPU、内存、IO 设备的读写速度差异巨大，表现为 CPU 的速度 > 内存的速度 > IO 设备的速度。
- 为了更好地利用 CPU 的高性能，计算机体系结构，给 CPU 增加了`缓存`（可以理解为jmm中的`工作内存`），均衡 CPU 和内存的速度差异。操作系统，增加了进程与线程，分时复用 CPU，均衡 CPU 和 IO 设备的速度差异
编译器，`增加了指令执行重排序`，`更好地利用缓存`，`提高程序的执行速度`

因为上面的优化策略，给并发编程带来了三大问题。


###并发三大特性

######可见性问题
可见性：一个线程对共享变量的修改，另一个线程能够立刻看到修改

由于`工作内存与主内存同步延迟`，带来了可见性问题


下例程序有可见性问题:  
A线程中的while读取的是flag。在main线程中有设置成true，但是A线程的while 循环迟迟不退出，证明A线程读取的flag的值为flase，并没有读到最新的值。但是堆内存是不存在这种问题的 换成Map就不存在这个问题了
~~~
    private static final HashMap<Object, Boolean> zz = new HashMap<>();
    static {
        JgOriginalOrderServiceImpl.zz.put("flag", false);
    }
~~~

~~~
class Test{
    static Boolean flag = false;
    public static void main(String[] args) throws InterruptedException {
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (!flag);
            }
        },"A").start();

        Thread.sleep(500);
        flag = true;
    }
}
~~~
**解决可见性问题的手段**
可以通过 volatile、synchronized、Lock接口、Atomic 类型保障可见性。

######原子性问题
原子性：一个操作是不可中断的，要么全部执行成功要么全部执行失败，有着“同生共死”的感觉。
操作系统对当前执行线程的切换，带来了原子性问题

下面的例子中，我创建了2000个线程去执行num++，最后的值小于2000。
这个就是因为线程切换导致的原子性问题。

Java 代码中 的 num++ 就不符合原子性 。它至少需要三条 CPU 指令：
~~~
指令 1：把变量 num从内存加载到 CPU 的寄存器
指令 2：在寄存器中执行 num + 1 操作
指令 3：+1 后的结果写入 CPU 缓存 或 内存
~~~
即使是单核的 CPU，当线程 1 执行到指令 1 时发生线程切换，线程 2 从内存中读取 num 变量，此时线程 1 和线程 2 中的 num 变量值是相等，都执行完指令 2 和指令 3，写入的 num 的值是相同的。从结果上看，两个线程都进行了 num++，但是 num 的值只增加了 1。

~~~
import java.util.ArrayList;

class Test{

    static Integer num = 0;
    public static void main(String[] args) throws InterruptedException {


        ArrayList<Thread> list = new ArrayList<>(2000);

        for (int i = 0; i <2000 ; i++) {
            Thread thread = new Thread(new Runnable() {
                @Override
                public void run() {
                    num++;
                }
            });
            thread.start();
            list.add(thread);

        }

        for (Thread thread : list) {
            thread.join();
        }

        System.out.println(num);



    }

}
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-3927148d79dfdc88.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**解决原子性问题的手段**
可以通过 synchronized、Lock接口、Atomic 类型保障原子性。`volatile关键字无法保证原子性`
######有序性问题
有序性：即程序执行的顺序按照代码的先后顺序执行。
因为`指令重排序优化` ，带来了有序性问题

可以看到下面的代码：
~~~
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class Test {

    static int x;
    static int y;

    public static void main(String[] args) throws InterruptedException {
        Set<String> hashSet = new HashSet<String>();
        Map<String, Integer> concurrentHashMap = new ConcurrentHashMap<>();

        for (int i = 0; i <10000000; i++) {
            x = 0;
            y = 0;
            //清除之前记录的结果
            hashSet.clear();
            concurrentHashMap.clear();

            Thread t1 = new Thread(() -> {
                int v1 = y;// Step1
                x = 1; //Step2
                concurrentHashMap.put("v1", v1);//Step3
            },"A") ;

            Thread t2 = new Thread(() -> {
                int v2 = x;//Step4
                y = 1;//Step5
                concurrentHashMap.put("v2", v2);//Step6
            },"B");

            t1.start();
            t2.start();
            //等待线程 t1 t2 执行完成
            t1.join();
            t2.join();


           // if(concurrentHashMap.get("v1") == 1 && concurrentHashMap.get("v2") == 1){
                hashSet.add("(v1=" + concurrentHashMap.get("v1") + ",v2=" + concurrentHashMap.get("v2") + ")");
                System.out.println(hashSet);
           // }

        }
    }

}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-118167e84125cf0c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[(v1=0,v2=0)]  的执行顺序是 Step1 和 Step 4 并行执行；
[(v1=0,v2=1)] 的执行顺序是 Step2 先于 Step4 执行。线程A比线程B先执行；
[(v1=1,v2=0)] 的执行顺序是 Step5 先于 Step1 执行。线程B比线程A先执行；
[(v1=1,v2=1)] 出现的概率极低，就是因为 `指令重排序优化`造成的。指令重排，可能会发生在两个没有相互依赖关系之间的指令，step1和step2、step4和step5都可能发生。Step2 被优化到 Step1 前，Step5 被优化到 Step4 前，至少需要成立一个。

关于指令重排序优化，我的这篇文章有讲解
https://www.jianshu.com/p/40cb45484f1e

######解决有序性问题的手段
可以通过volatile关键字、 synchronized、Lock接口。`Atomic类型无法保证有序性 `

######总结
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6f512bb9647230f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
