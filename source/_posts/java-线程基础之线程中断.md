---
title: java-线程基础之线程中断.md
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
title: java-线程基础之线程中断.md
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
线程终止有两种情况：
1、线程的任务执行完成
2、线程在执行任务过程中发生异常
这两者属于线程自行终止，如何让线程 A 把线程 B 终止呢？
即线程A对线程B发出一个信号，让线程B终止执行

所以java给我们提供了一些方法

- 线程中断类方法stop()，resume(),suspend()已不建议使用，stop()会导致线程不会正确释放资源，suspend()容易导致死锁；

- 推荐使用interrupt() 方法发出中断信号，设置`中断标志位`。然后在被中断线程中对InterruptedException异常进行捕获。在finally中做一下退出之前的操作，该释放资源就释放资源



###中断相关的线程方法
######thread.interrupt()实例方法
调用一个线程的interrupt() 方法中断一个线程，并不是强行关闭这个线程，只是跟这个线程打个招呼，设置`中断标志位`，`线程是否中断，由线程本身决定`。

######thread.isInterrupted()实例方法
判断线程实例是否处于中断状态，`中断标志位`不会被清除。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-01c7af94dc428883.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######Thread.interrupted()静态方法
判定当前线程是否处于中断状态。同时清除`中断标志位`。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4ca8352e45d4e217.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###中断标志位
- 如果目标线程设置了中断标志位，则目标线程执行wait()、join()、sleep() 阻塞等方法会抛出InterruptedException异常
- 当抛出InterruptedException时候，会清除中断标志位；


###调用thread.interrupt()实例方法和线程状态的关系
不同的线程线程状态对线程中断的反应不同

1、NEW和TERMINATED对于中断操作几乎是屏蔽的(没有影响，对中断标志位也没有影响。还是false)

2、RUNNABLE和BLOCKED类似，仅仅是线程的中断标记被设置为true。并没有强制终止线程，对于线程的终止权利依然在程序手中。 

- RUNNABLE正在运行的线程，`中断操作和业务逻辑直接有非常精密的联系`。所以线程要在适当的位置通过调用isInterrupted方法来查看自己是否被中断，并做退出操作。 对于不同的工作线程，最好不要强制中断线程。在业务逻辑中退出会更好。
 比如：在死循环(RUNNABLE)中配判断当前线程中断标志符是否为true，break退出循环。程序执行完毕，也就是退出了线程
~~~
Thread thread = new Thread(new Runnable() {
    @Override
    public void run() {
        while (true) {
            System.out.println("继续监听A线程的中断标志位，如果为true。退出");
            if (Thread.currentThread().isInterrupted()) {
                System.out.println("A线程退出");
                break;
            }
        }

    }
}, "A");

thread.start();
Thread.sleep(1000*2);
thread.interrupt();
~~~


3、如果此线程处于等待（WAITING/TIMED_WAITING）状态(比如调用了join、wait、sleep方法，io等待)。如果调用了thread.interrupt()实例方法则会立马退出等待。`并抛出InterruptedException异常，清除中断标志位。`线程就可以通过捕获InterruptedException来做一定的处理，然后让线程退出。

- 如果线程的interrupt方法先被调用，然后调用等待方法进入等待状态，InterruptedException异常依旧会抛出。(无论等待在前还是在后，中断标志位是true遇到等待会抛出异常)

- 如果线程捕获InterruptedException异常后，继续调用等待方法，将不再触发InterruptedException异常(因为抛出InterruptedException异常后中断标记位被改为false，false遇到等待不会有异常)

###对于sleep()、wait()、join、IO 导致的阻塞分使用interrupt()方法验证

1、sleep()方法
~~~
public static void main(String[] args) throws InterruptedException {

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(1000*3);
                    System.out.println("下面其他的一些业务，没有得到执行...");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }finally {
                    System.out.println("线程A退出");
                }
            }
        }, "A");

        thread.start();
        Thread.sleep(1000*1);
        thread.interrupt();
    }
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-909b7a117445f5d0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、wait()
~~~
 public static void main(String[] args) throws InterruptedException {

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    synchronized (TestA.class){
                        TestA.class.wait();
                    }
                    System.out.println("下面其他的一些业务，没有得到执行...");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }finally {
                    System.out.println("线程A退出");
                }

            }
        }, "A");

        thread.start();
        Thread.sleep(1000*1);
        thread.interrupt();
    }

~~~

3、join()
~~~
 public static void main(String[] args) throws InterruptedException {
        Thread mainThread = Thread.currentThread();

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    //等待main线程执行完毕再继续执行
                    mainThread.join();
                    System.out.println("下面其他的一些业务，没有得到执行...");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }finally {
                    System.out.println("线程A退出");
                }

            }
        }, "A");

        thread.start();
        Thread.sleep(1000*1);
        thread.interrupt();
    }
~~~

4、调用interrupt()中断 io 的例子尚未找到

###对于线程中断的一些感悟
调用interrupt()方法并不会立马中断线程，还是要考虑释放资源和释放监视器锁，所以很难去把握中断线程的时机，而线程中断后就是一个不可以重复利用的资源。如果使用`线程池`就能把中断线程这个问题转化为中断任务，因为线程池中线程总是复用的。我们根本不需要去关系线程什么时候开启，什么时候终止。

最终还是推荐使用`线程池`的方式来使用线程。线程池配合Future接口提供了cancel()方法，看做是对interrupt()的一个封装。更方便达到中断线程的目的。
我的这篇文章有对FutureTask和线程池使用的示例
https://www.jianshu.com/p/f24b347bb956
