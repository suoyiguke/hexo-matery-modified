---
title: juc---CyclicBarrier-使用方法.md
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
title: juc---CyclicBarrier-使用方法.md
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
CyclicBarrier拥有CountDownLatch的功能，任何一个线程在没有完成时，所有线程都在等待。当最后一个线程进入wait，到达屏障点。构造器中的Runnable接口的run方法会得到执行。 CyclicBarrie 可以翻译为 `循环屏障`，所谓循环就是可以循环使用，这点区别于CountDownLatch

######CyclicBarrier 与 CountDownLatch 区别

- CountDownLatch 一次性，CyclicBarrier 可循环使用
- CountDownLatch 使用`减计数方式`，等于0则释放；CyclicBarrier 使用`加计数方式`，到达指定值时释放，而且`自动重置为0`
- CyclicBarrier 有一个所有线程都到达屏障时的回调

![image.png](https://upload-images.jianshu.io/upload_images/13965490-db36fd76a734f95e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######CyclicBarrier 的构造器

有两种构造器
![image.png](https://upload-images.jianshu.io/upload_images/13965490-66e2c27ec67349d5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- int parties参数为达`到线程屏障的线程数量` 
- Runnable  barrierAction参数实现run方法，在parties个线程全部达到屏障点时回调执行


######CyclicBarrier的实例方法



- cyclicBarrier.await() 在此方法处线程阻塞，parties个线程都执行await()后回调Runnable里的逻辑；`由执行await()的线程其中之一来执行cyclicBarrier中Runnable接口的run()方法，可能是最后到达屏障的线程`
- cyclicBarrier.getParties() 获取初始化屏障的数量：parties
- cyclicBarrier.getNumberWaiting() 获得到达await()（屏障）的线程的数量，这个数量从0增加到barrier后就表示全部线程都已经达到屏障点了

- cyclicBarrier.reset() 将屏障重置为其初始状态。如果所有参与者目前都在屏障处等待，则将他们唤醒，同时抛出一个BrokenBarrierException异常

- cyclicBarrier.isBroken(); 当前线程的屏障是否出现损坏，例如终止线程的时候

######CyclicBarrier 的可重复使用验证
~~~
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.TimeUnit;

public class CyclicBarrierTest {
    public static void main(String[] args) throws InterruptedException {


        CyclicBarrier cyclicBarrier = new CyclicBarrier(3, new Runnable() {
            @Override
            public void run() {
                System.out.println("回调！");
            }
        });

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "A").start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "B").start();


        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "C").start();

        TimeUnit.SECONDS.sleep(3);

        for (int i = 0; i < 3; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    System.out.println(Thread.currentThread().getName());
                    try {
                        cyclicBarrier.await();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } catch (BrokenBarrierException e) {
                        e.printStackTrace();
                    }
                }
            }).start();

        }



    }
}
~~~
CyclicBarrier可以自动的重置，使用多少次都没关系
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c1a5349fccb1b770.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######BrokenBarrierException异常
在上面的源代码中，我们可能需要注意Generation 对象，在上述代码中我们总是可以看到抛出BrokenBarrierException异常，那么什么时候抛出异常呢？

- 如果一个线程处于等待状态时，如果其他线程调用reset()，或者调用的barrier原本就是被损坏的，则抛出BrokenBarrierException异常。
~~~
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

public class CyclicBarrierTest {
    public static void main(String[] args) throws InterruptedException {

        CyclicBarrier cyclicBarrier = new CyclicBarrier(3, new Runnable() {
            @Override
            public void run() {
                System.out.println("3个线程均到达屏障点，回调线程的run方法");
            }
        });

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "A").start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "B").start();


       new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    cyclicBarrier.reset();
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "C").start();
    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6ec91f76e57b8c08.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- 同时，任何线程在等待时被中断了，被中断的线程抛出InterruptedException。则其他所有线程都将抛出BrokenBarrierException异常，并将barrier置于损坏状态。
~~~
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

public class CyclicBarrierTest {
    public static void main(String[] args) throws InterruptedException {

        CyclicBarrier cyclicBarrier = new CyclicBarrier(3, new Runnable() {
            @Override
            public void run() {
                System.out.println("3个线程均到达屏障点，回调线程的run方法");
            }
        });

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "A").start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "B").start();


        Thread c = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "C");
        c.start();

        c.interrupt();


    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6be5ff237d40cbef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######执行回调Runnable 接口的run()方法是哪一个线程？
~~~
import java.util.concurrent.BrokenBarrierException;
        import java.util.concurrent.CyclicBarrier;

public class CyclicBarrierTest {
    public static void main(String[] args) throws InterruptedException {

        CyclicBarrier cyclicBarrier = new CyclicBarrier(3, new Runnable() {
            @Override
            public void run() {
                System.out.println(Thread.currentThread().getName());
            }
        });

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "A").start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "B").start();


        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    System.out.println(Thread.currentThread().getName() + "线程到达屏障点");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }
        }, "C").start();



    }
}
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-fcc541ff930f73ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

根据多次的运行结果来看，`由最后到达屏障点的线程来执行回调Runnable接口中的run方法`
也可以去看看CyclicBarrier 的源码，这样更加可信。我的这篇文章对CyclicBarrier 源码有一些解读
https://www.jianshu.com/p/c6fa925540c2

