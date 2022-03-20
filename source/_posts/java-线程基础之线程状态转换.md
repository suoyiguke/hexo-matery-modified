---
title: java-线程基础之线程状态转换.md
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
title: java-线程基础之线程状态转换.md
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
###java中的线程状态
  线程一共6种状态，分别是NEW，RUNNABLE，BLOCKED，WAITING，TIMED_WAITING，TERMINATED

Thread类源码中有下面的代码
~~~
    public enum State {
        /**
         * Thread state for a thread which has not yet started.
         */
        NEW,

        /**
         * Thread state for a runnable thread.  A thread in the runnable
         * state is executing in the Java virtual machine but it may
         * be waiting for other resources from the operating system
         * such as processor.
         */
        RUNNABLE,

        /**
         * Thread state for a thread blocked waiting for a monitor lock.
         * A thread in the blocked state is waiting for a monitor lock
         * to enter a synchronized block/method or
         * reenter a synchronized block/method after calling
         * {@link Object#wait() Object.wait}.
         */
        BLOCKED,

        /**
         * Thread state for a waiting thread.
         * A thread is in the waiting state due to calling one of the
         * following methods:
         * <ul>
         *   <li>{@link Object#wait() Object.wait} with no timeout</li>
         *   <li>{@link #join() Thread.join} with no timeout</li>
         *   <li>{@link LockSupport#park() LockSupport.park}</li>
         * </ul>
         *
         * <p>A thread in the waiting state is waiting for another thread to
         * perform a particular action.
         *
         * For example, a thread that has called <tt>Object.wait()</tt>
         * on an object is waiting for another thread to call
         * <tt>Object.notify()</tt> or <tt>Object.notifyAll()</tt> on
         * that object. A thread that has called <tt>Thread.join()</tt>
         * is waiting for a specified thread to terminate.
         */
        WAITING,

        /**
         * Thread state for a waiting thread with a specified waiting time.
         * A thread is in the timed waiting state due to calling one of
         * the following methods with a specified positive waiting time:
         * <ul>
         *   <li>{@link #sleep Thread.sleep}</li>
         *   <li>{@link Object#wait(long) Object.wait} with timeout</li>
         *   <li>{@link #join(long) Thread.join} with timeout</li>
         *   <li>{@link LockSupport#parkNanos LockSupport.parkNanos}</li>
         *   <li>{@link LockSupport#parkUntil LockSupport.parkUntil}</li>
         * </ul>
         */
        TIMED_WAITING,

        /**
         * Thread state for a terminated thread.
         * The thread has completed execution.
         */
        TERMINATED;
    }

~~~

####NEW 
- 尚未启动的线程的线程状态。new完之后还没有start的线程
- 在进行thread.start()后线程是否会马上执行？
    答案是不确定，线程是否运行是由操作系统进行cpu执行时间片调度后才能决定的
####RUNNABLE 
可运行线程的线程状态。处于可运行状态的线程正在Java虚拟机中执行，但也可能正在等待来自操作系统的其他资源，例如处理器；所以java中的RUNNABLE其实包含两个子状态：
- runnable(running)  获得cpu执行时间片，正在执行的线程
- runnable(ready)   尚未获得cpu执行时间片，就绪的线程
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f9bd157fd15131ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
1、就绪状态 runnabel(ready) 的线程需要获得cup时间片才能真正运行 runnabel(running)
2、操作系统使用`线程调度`的手段来分配cpu时间片；  因为：一个单核CUP同一时刻只能执行一个线程而且 不同的操作系统线程调度的方法也不一样，windows线程调度方式是`抢占`
3、java中可以直接调用 yield()、sleep(0) 方法来让当前线程做出`线程让步`,让出CPU的执行时间片,转态由runnabel(running)变为 runnabel(ready)


####BLOCKED
等待监视器锁定的线程被阻塞的线程状态；`处于BLOCKED状态下的线程会参与监视器锁的竞争！`下面的方法会导致Runnabel变为BLOCKED
- 等待进入synchronized块的线程会进入BLOCKED状态
- Object.notify() / Object.notifyAll() 会导致因为Object.wait()方法作用的waiting状态变为BLOCKED，重新参与监视器锁的竞争

####WAITING
等待线程的线程状态；下面的方法会让Runnabel(Running)线程进入WAITING 状态
- Object.wait()
- thread.join()
- LockSupport.park()

下面的方法会唤醒因为Object.wait()而成的WAITING状态，变成BLOCKED，参与监视锁竞争
- Object.notify()
- Object.notifyAll()


####TIMED_WAITING
具有指定等待时间的等待线程的线程状态。 由于以指定的正等待时间调用以下方法之一，因此线程处于定时等待状态
- sleep(n)
- Object.wait(n)
- thread.join(n)
- LockSupport.parkNanos(n)
- LockSupport.parkUntil(n)
####TERMINATED  
终止线程的线程状态。 线程已完成执行


###线程状态转换的示意图
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fbe6bca2cd244dfd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8bc1ec57f945faca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###各种状态实例
t1==>NEW
~~~
Thread t1 = new Thread("t1");
System.out.println(t1.getName()+"==>"+t1.getState());
~~~
t2==>RUNNABLE
~~~
new Thread(new Runnable() {
   @Override
   public void run() {
            System.out.println(Thread.currentThread().getName()+"==>"+Thread.currentThread().getState());
   }
},"t2").start();
~~~

t3==>TIMED_WAITING
t4==>BLOCKED

~~~
class TestThread extends Thread{
    public TestThread(String name) {
        super(name);
    }

    @SneakyThrows
    @Override
    public void run() {
        synchronized (TestThread.class){
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
    }

    public static void main(String[] args) throws InterruptedException {

        TestThread t3 = new TestThread("t3");
        t3.start();
        TestThread t4 = new TestThread("t4");
        t4.start();
        Thread.sleep(1000);

        System.out.println(t3.getName()+"==>"+t3.getState());
        System.out.println(t4.getName()+"==>"+t4.getState());
    }
}
~~~
t5==>TERMINATED
~~~
Thread t5 = new Thread(new Runnable() {
    @SneakyThrows
    @Override
    public void run() {
        Thread.sleep(10);
    }
},"t5");

t5.start();
Thread.sleep(1000);
System.out.println(t5.getName()+"==>"+t5.getState());
~~~

###线程各个状态与对象锁的竞争的关系
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a27a2b4cc72404b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- runnable(running)  获得监视器锁和CPU执行时间片，正在运行的线程

- runnable(ready)  尚未获得CPU执行时间片

- waiting/timed_waiting 不参与锁的竞争

- blocked  下的线程们直接参与对锁的竞争！
