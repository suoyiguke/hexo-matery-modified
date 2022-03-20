---
title: java-线程基础之线程方法join、wait、sleep.md
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
title: java-线程基础之线程方法join、wait、sleep.md
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
###join()

1、在A线程中调用了B线程的join()方法时，表示只有当B线程执行完毕时，A线程才能继续执行


2、带时间参数的join：
如果A线程中调用B线程的join(10)，则表示A线程会等待B线程执行10毫秒，10毫秒过后，A、B线程并发执行。需要注意的是，jdk规定，join(0)的意思不是A线程等待B线程0秒，而是A线程等待B线程无限时间，直到B线程执行完毕，`即join(0)等价于join()`。
可以看看join的源码，join()最终调用的是join(0)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1b798d64dcf3f5fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



3、Join 是使用wait-nodify机制实现的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e45a4c02c83e1e8e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、使用示例

使用join()方式实现 main线程等待所有子线程执行完毕
~~~
   public static void main(String[] args) throws InterruptedException {


        List<Thread> list = new ArrayList<>();
        for (int i = 0; i <10 ; i++) {
            int finalI = i;
            Thread thread = new Thread(new Runnable() {
                @SneakyThrows
                @Override
                public void run() {
                    Thread.sleep(1000*(finalI +1));
                    System.out.println(Thread.currentThread().getName()+"执行！");

                }
            },"thread-"+(i +1));

            thread.start();
            list.add(thread);

        }

        for (Thread thread : list) {
            thread.join();
        }
        System.out.println("所有线程都执行完毕。。。");


    }
~~~

###wait()
可以看看我的这篇文章<<java 线程编程-wait-notify机制>>
https://www.jianshu.com/p/36b57330531c

需要注意的是：
wait() 方法的调用会释放出当前线程所持有的监视器锁


###sleep()

####带参数 sleep(n) 

假设现在是 2019-10-1 12:00:00.000，如果我调用一下 Thread.Sleep(1000) ，在 2019-10-1 12:00:01.000 的时候，这个线程会不会被唤醒？

`结果不确定`

因为sleep(1000)只是告诉操作系统：在未来的1秒内我不想再参与到CPU竞争。那么1000毫秒过去之后
- 这时候也许另外一个线程正在使用CPU，那么这时候操作系统是不会重新分配CPU的，直到那个线程挂起或结束；
- 况且，即使这个时候恰巧轮到操作系统进行CPU 分配，那么当前线程也不一定就是总优先级最高的那个，CPU还是可能被其他线程抢占去。与此相似的，Thread有个Resume函数，是用来唤醒挂起的线程的。好像上面所说的一样，这个函数只是“告诉操作系统我从现在起开始参与CPU竞争了”，这个函数的调用并不能马上使得这个线程获得CPU控制权。

说明sleep结束之后线程可能不会立即继续执行,sleep(n) 方法会导致线程状改变：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cdb6f9238412d38e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


####sleep(0)的意义

在线程中，调用sleep（0）可以释放cpu时间，让线程马上从等待队列中出来到就绪队列，sleep(0)释放当前线程所剩余的时间片（如果有剩余的话），这样可以让操作系统切换其他线程来执行，提升效率。
~~~
 public static void main(String[] args) throws InterruptedException {

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {

                try {
                    while (true) {
                        Thread.sleep(0);
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        thread.start();

        while (true){
            System.out.println(thread.getState());
        }

    }
~~~
运行结果：
TIMED_WAITING
TIMED_WAITING
RUNNABLE
TIMED_WAITING
TIMED_WAITING

![image.png](https://upload-images.jianshu.io/upload_images/13965490-160ec8e5157dfaa9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###yield()

这是一个静态方法，一旦执行，它会使当前线程让出CPU。另外，`让出的时间片只会分配给当前线程相同优先级的线程`。但如果系统中没有相同优先级的线程，那么本线程又会重新占用cup继续运行（让出的CPU并不是代表当前线程不再运行了。如果在下一次竞争中，又获得了CPU时间片当前线程依然会继续运行）

~~~
 public static void main(String[] args)   {

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    Thread.yield();
                }
            }
        });
        thread.start();

        while (true){
            System.out.println(thread.getState());
        }

    }
~~~
执行结果
RUNNABLE
RUNNABLE
RUNNABLE
RUNNABLE
RUNNABLE
RUNNABLE

![image.png](https://upload-images.jianshu.io/upload_images/13965490-65d6009e70ce9e0c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)






###wait()和sleep()的区别     

- sleep()方法是Thread的静态方法，而wait是Object实例方法

- wait()方法必须要在同步方法或者同步块中调用，也就是必须已经获得`监视器锁`。而sleep()方法没有这个限制可以在任何地方种使用。另外，wait()方法会使当前线程释放占有的`监视器锁`，使得该线程进入等待池中，等待下一次获取资源。而sleep()方法只是会让出CPU并不会释放掉对象锁；
- sleep()方法在休眠时间达到后如果再次获得CPU时间片就会继续执行，而wait()方法必须等待Object.notift/Object.notifyAll通知后，才会离开等待池。再次获得CPU时间片才会继续执行。

**两者的相同点**
wait()和sleep()都可以通过interrupt()方法打断线程的暂停状态、将线程中断标志位设为true，从而使线程立刻抛出InterruptedException。如果线程A希望立即结束线程B，则可以对线程B对应的Thread实例调用interrupt方法。如果此刻线程B正在wait/sleep/join，则线程B会立刻抛出InterruptedException，在catch() {} 中直接return即可安全地结束线程。        
	
