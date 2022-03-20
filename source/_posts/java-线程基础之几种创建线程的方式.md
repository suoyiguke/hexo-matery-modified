---
title: java-线程基础之几种创建线程的方式.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
---
title: java-线程基础之几种创建线程的方式.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
###创建线程的几种方式
1、使用Thread类，重写run方法
~~~
 Thread thread = new Thread() {
            @Override
            public void run() {
                System.out.println("继承Thread");
                super.run();
          }
 };
 thread.start();
~~~

2、使用Thread，实现runable接口、实现run方法
~~~
  Thread thread1 = new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("实现runable接口");
            }
   },"线程名");
  thread1.start();
~~~

在jdk1.8中的新写法，可以这样
~~~
  new Thread(()-> {
        System.out.println("hello world");

    },"线程名").start();
~~~

3、使用 FutureTask类、Callable接口来创建线程
在我的这篇文章有提到具体用法
https://www.jianshu.com/p/f24b347bb956
###Java能否两次启动同一线程？
~~~
class TestThreadTwice1 extends Thread {
    @Override
    public void run() {
        System.out.println("Start running...");
    }

    public static void main(String args[]) {
        TestThreadTwice1 t1 = new TestThreadTwice1();
        t1.start();
        t1.start();
    }
}
~~~
不能，如果一个线程被start两次则报错如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0daf36e15c3c8682.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
说来也惭愧，工作两年的我..现在才知道。因此如果需要再次运行同一个任务请再次new一个线程

###线程直接调用run()方法而不是start()方法
线程对象有start方法和run方法，那两者有什么区别呢？
~~~
class TestCallRun2 extends Thread {
    @Override
    public void run() {
        for (int i = 1; i < 5; i++) {
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                System.out.println(e);
            }
            System.out.println(i);
        }
    }

    public static void main(String args[]) {
        TestCallRun2 t1 = new TestCallRun2();
        TestCallRun2 t2 = new TestCallRun2();

        t1.start();
        t2.run();

    }
}
~~~
 发现使用run来运行，并没有创建子线程来运行run中的代码
而使用start的输出是交替输出的

结论：start的每个线程在一个单独的线程栈中启动。run方法的程序执行并没有上下文切换，因为这里t2将被视为普通对象而不是线程对象；如果需要子线程执行任务请用start

###给线程命名
Thread类提供了更改和获取线程名称的方法。默认情况下，每个线程都有一个名称，即thread-0，thread-1, ...等。 可以使用setName()方法更改线程的名称。 setName()和getName()方法的语法如下：
~~~
public String getName() : 用于返回线程的名称。
public void setName(String name): 用于更改线程的名称。
~~~

~~~
class TestMultiNaming1 extends Thread {
    @Override
    public void run() {
        System.out.println("running...");
    }

    public static void main(String args[]) {
        TestMultiNaming1 t1 = new TestMultiNaming1();
        TestMultiNaming1 t2 = new TestMultiNaming1();
        System.out.println("Name of t1:" + t1.getName());
        System.out.println("Name of t2:" + t2.getName());

        t1.start();
        t2.start();

        t1.setName("计算线程");
        System.out.println("自定义线程名称：" + t1.getName());
    }
}
~~~
###获得当前线程
~~~
Thread thread = Thread.currentThread();
~~~

###设置线程优先级
每个线程都有一个优先级。优先级是由1到10之间的数字表示。在大多数情况下，线程调度程序根据线程的优先级(称为抢占式调度)来调度线程。 但它不能保证，因为它依赖于JVM规范，它选择哪种调度。
- Thread类中定义的3个常量：
~~~
public static int MIN_PRIORITY
public static int NORM_PRIORITY
public static int MAX_PRIORITY
~~~
- 线程的默认优先级为5(NORM_PRIORITY)。 MIN_PRIORITY的值为1，MAX_PRIORITY的值为10。

~~~

class TestMultiPriority1 extends Thread {
    @Override
    public void run() {
        System.out.println("running thread name is:" + Thread.currentThread().getName());
        //获得优先级
        System.out.println("running thread priority is:" + Thread.currentThread().getPriority());

    }

    public static void main(String args[]) {
        TestMultiPriority1 m1 = new TestMultiPriority1();
        TestMultiPriority1 m2 = new TestMultiPriority1();
        //设置优先级
        m1.setPriority(Thread.MIN_PRIORITY);
        m2.setPriority(Thread.MAX_PRIORITY);
        m1.start();
        m2.start();

    }
}
~~~

###守护线程
java中的守护程序线程是一个服务提供程序线程，它为用户线程提供服务。 它的生命依赖于用户线程，即当所有用户线程都死掉时，JVM会自动终止该线程。有许多java守护程序线程自动运行，例如 gc，finalizer 等通过在命令提示符下键入jconsole来查看所有详细信息。 jconsole工具提供有关已加载类，内存使用情况，运行线程等的信息。

####Java中的守护程序线程的要点
- 它为用户线程提供后台支持任务的服务。它在生命中没有为服务用户线程而发挥作用。
- 它的生命取决于用户线程。
- 它是一个低优先级的线程。

####如果没有用户线程，为什么JVM会终止守护线程？
守护程序线程的唯一目的是`它为用户线程提供后台支持任务的服务`。 如果没有用户线程，为什么JVM要继续运行这个线程？这就是为什么JVM在没有用户线程的情况下终止守护进程线程的原因。
####Thread类的Java守护程序线程的方法
java.lang.Thread类为java守护程序线程提供了两种方法。
~~~
public void setDaemon(boolean status)//用于将当前线程标记为守护程序线程或用户线程。
public boolean isDaemon()//用于检查当前是守护进程。
~~~

####使用示例
~~~


class TestDaemonThread1 extends Thread {
    @Override
    public void run() {
        //判断是不是守护线程
        if (Thread.currentThread().isDaemon()) {// checking for daemon thread
            System.out.println("daemon thread work");
        } else {
            System.out.println("user thread work");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // creating thread
        TestDaemonThread1 t1 = new TestDaemonThread1();
        TestDaemonThread1 t2 = new TestDaemonThread1();
        TestDaemonThread1 t3 = new TestDaemonThread1();

        //在t1线程启动之前设置为守护线程
        t1.setDaemon(true);

        // starting threads
        t1.start();
        t2.start();
        t3.start();
        Thread.sleep(2000);
        System.out.println("t1 "+t1.getState());
        System.out.println("t2 "+t2.getState());
        System.out.println("t3 "+t3.getState());
        System.out.println("end");
    }
}
~~~
####线程在start后能不能设置为守护线程？
可以一试：
~~~
class TestDaemonThread2 extends Thread {
    @Override
    public void run() {
        System.out.println("Name: " + Thread.currentThread().getName());
        System.out.println("Daemon: " + Thread.currentThread().isDaemon());
    }

    public static void main(String[] args) {
        TestDaemonThread2 t1 = new TestDaemonThread2();
        TestDaemonThread2 t2 = new TestDaemonThread2();
        t1.start();
        t1.setDaemon(true);// will throw exception here
        t2.start();
    }
}
~~~
报错
![image.png](https://upload-images.jianshu.io/upload_images/13965490-80592a5bf9e039ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可见：线程start之后不能再设置为守护线程了！

####守护线程的子线程是不是守护线程？
写个代码试下，在线程里面再new个线程
~~~
    public static void main(String[] args)  {
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {

                new Thread(()-> {
                    System.out.println(Thread.currentThread().isDaemon());

                },"线程名").start();

            }
        });
        thread.setDaemon(true);
        thread.start();
    }
~~~
可是得不到输出，不知道为什么；知道的朋友可以在评论区赐教一下，不胜感激~

既然代码输出不了，那就再看看Thread 类源码吧；线程的daemon、priority属性都是继承于父线程的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d8bab53600ef01c0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###main方法中的线程
![image.png](https://upload-images.jianshu.io/upload_images/13965490-860d5e0bd3a9d8e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

一个java程序从main()方法开始执行，然后按照既定的代码逻辑执行，看似没有其他线程参与，但实际上java程序天生就是一个多线程程序，包含了：
~~~
（1）分发处理发送给给JVM信号的线程；
（2）调用对象的finalize方法的线程；
（3）清除Reference的线程；
（4）main线程，用户程序的入口。
~~~
