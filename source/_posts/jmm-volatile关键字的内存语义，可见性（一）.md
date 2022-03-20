---
title: jmm-volatile关键字的内存语义，可见性（一）.md
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
title: jmm-volatile关键字的内存语义，可见性（一）.md
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
读音  [ˈvɒlətaɪl]

volatile是java虚拟机提供的最轻量级的同步机制

######happens-before规则和volatile的关系
happens-before规则中有一条是：
> volatile变量规则，对一个volatile域的写，happens-before于任意后续对这个volatile域的读

关于happens-before规则可以看看这篇https://www.jianshu.com/p/bb894b1fe2e6

换句话说就是：
> 被volatile修饰的变量能够保证每个线程能够获取该变量的最新值。


######volatile的内存语义
从JSR-133开始（即从JDK5开始），volatile的内存语义得到了增强

`volatile写`的内存语义
>当写一个volatile变量时，JMM会把该线程对应的本地内存中的共享变量值刷新到主内存。

`volatile读`的内存语义
>当读一个volatile变量时，JMM会把该线程对应的本地内存置为无效。线程接下来将从主内存中读取共享变量。


######volatile可以看做是一种线程通信的手段
如果我们把volatile写和volatile读两个步骤综合起来看的话，在读线程B读一个volatile变量后，写线程A在写这个volatile变量之前所有可见的共享变量的值都将立即变得对读线程B可见。下面对volatile写和volatile读的内存语义做个总结。

>线程A写一个volatile变量，实质上是线程A向接下来将要读这个volatile变量的某个线程发出了（其对共享变量所做修改的）消息。*通知工作内存中的volatile变量已经失效，请重新从主内存中获取最新值。*
线程B读一个volatile变量，实质上是线程B接收了之前某个线程发出的（在写这个volatile变量之前对共享变量所做修改的）消息。
`线程A写一个volatile变量，随后线程B读这个volatile变量，这个过程实质上是线程A通过主内存向线程B发送消息。`

![image.png](https://upload-images.jianshu.io/upload_images/13965490-82a261effd0e211f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######volatile的特性
- 保证可见性：保证了不同线程对这个变量进行操作时的可见性，即一个线程修改了某个变量的值，这新值对其他线程来说是立即可见的。
- 保证有序性： 禁止进行指令重排序。
- 一定程度上保证原子性：volatile 只能保证对单次读/写的原子性，i++ 这种操作不能保证原子性。

######volatile内存语义实现的原理
volatile通过插入`内存屏障`的方式禁止指令重排序优化


######volatile使用示例
案例1：不加volatile关键字，执行下面的程序，程序一直得不到退出
~~~
package test;

public class VolatileDemo {
    private static boolean isOver = false;

    public static void main(String[] args) {
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (!isOver) ;
            }
        },"thread-A");
        thread.start();
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        isOver = true;
    }
}
~~~

加上volatile关键字，执行下面的程序
~~~
package test;

public class VolatileDemo {
    private static volatile boolean isOver = false;

    public static void main(String[] args) {
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (!isOver) ;
            }
        },"thread-A");
        thread.start();
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        isOver = true;//thread-A"线程马上执行完毕
    }
}
~~~

注意不同点，现在已经将isOver设置成了volatile变量，这样在main线程中将isOver改为了true后，thread的工作内存该变量值就会失效，从而需要再次从主内存中读取该值，现在能够读出isOver最新值为true从而能够结束在thread里的死循环，从而能够顺利停止掉thread线程。

没有加volatile，如果在while这行打个断点，发现isOver设置成true生效。程序退出,原因有待研究
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3aa8bc9549fa622c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


案例2：
在编写单例模式中懒汉加载的`双重检测锁`实现时使用到了volatile关键字；这里volatile的作用是禁止指令重排序；

~~~
package test;

class A {

    private volatile static A a;

    public static A newInstance() {
        if (a == null) {
            synchronized (A.class) {
                if (a == null) {
                    a = new A();
                }
            }

        }
        return  a;
    }

    public static void main(String[] args) {

        for (int i = 0; i < 1000; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    System.out.println(A.newInstance());
                }
            },"线程"+i).start();

        }



    }

}
~~~

######在volatile和synchronized做出抉择
volatile看起来简单，但是要想理解它还是比较难的，这里只是对其进行基本的了解。volatile相对于synchronized稍微轻量些，在某些场合它可以替代synchronized，但是又不能完全取代synchronized，只有在某些场合才能够使用volatile。

使用它必须满足如下两个条件：
>对变量的写操作不依赖当前值；
该变量没有包含在具有其他变量的不变式中。

###探究jmm中工作内存和主内存的同步时机

如果不使用volatile关键字，那么到底经过什么操作之后。或者说在什么时机 工作内存会去同步主内存呢？
~~~

class MyThread extends Thread{

    public boolean flag = true;

    public void setFlag(boolean flag) {
        this.flag = flag;
    }

    @SneakyThrows
    @Override
    public void run() {
        System.out.println("线程开始");
        while (flag) {
            //System.out.println("运行中，子线程:"+Thread.currentThread().getName());
            //Thread.sleep(0);
            //Thread.yield();
        }
        System.out.println("线程结束");


    }

    public static void main(String[] args) throws InterruptedException {
        MyThread myThread = new MyThread();
        myThread.start();
        Thread.sleep(3000);
        myThread.setFlag(false);
        Thread.sleep(1000);
        System.out.println(myThread.flag);
    }

}
~~~

1、上面的程序运行后，子线程没有退出。可以得出结论：在空的while 无限循环中，循环条件的变量使用的工作内存不会同步主内存的数据

2、如果在循环体里面使用System.out.println打印字符串到控制台，while循环条件变量马山同步主内存中的true。猜测原因是System.out.println中使用到了同步锁synchronized

3、如果在循环体里面使用Thread.sleep(0)、Thread.yield()；也会马上同步

4、基本类型运算不会导致同步，可以试试在while循环里加上下面代码
~~~
int a = 1;
int b = 2;
int c = a+b;
~~~
~~~
Integer a = 1;
Integer b = 2;
Integer c = a+b;
~~~

5、字符串连接会导致同步
~~~
String a = "aaa";
String b = "ffff";
String c = a.concat(b);
~~~

6、new对象导致同步
~~~
String a = new String("123") ;
~~~



###在其它对象中
在对象中的成员属性也会有问题
把这里的bool属性的volatile去掉一样有问题
~~~
    @AllArgsConstructor
    @Data
    private static class zz {
        private volatile Boolean bool = false;
    }
    public static void main(String[] args) throws InterruptedException {
        zz zz = new zz(false);
        new Thread(() -> {
            while (!zz.getBool()) {
            }
            System.out.println("A 跳出循环");
        }, "A").start();

        new Thread(() -> {
            while (!zz.getBool()) {
            }
            System.out.println("B 跳出循环");
        }, "B").start();
        Thread.sleep(500);
        zz.setBool(true);
    }
~~~

2、Map中没有问题
~~~
       HashMap<Object, Boolean> map = new HashMap<>(1);
        map.put("bool",false);

        new Thread(() -> {
            while (!map.get("bool")) {
            }
            System.out.println("A 跳出循环");
        }, "A").start();

        new Thread(() -> {
            while (!map.get("bool")) {
            }
            System.out.println("B 跳出循环");
        }, "B").start();
        Thread.sleep(500);
        map.put("bool",true);
~~~

3、long也没有问题

~~~

    public long testLong = 0;


    public static void main(String[] args) {
        AccountingSync accountingSync = new AccountingSync();

        new Thread(new Runnable() {
            @Override
            public void run() {

                while (!Objects.equals(999999999999999999L,accountingSync.testLong)){
                }

            }
        }).start();
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        accountingSync.testLong = 999999999999999999L;


    }
~~~
