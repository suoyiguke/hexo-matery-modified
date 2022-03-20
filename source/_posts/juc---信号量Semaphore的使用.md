---
title: juc---信号量Semaphore的使用.md
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
title: juc---信号量Semaphore的使用.md
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

Semaphore 读音 [ˈseməfɔːr]
Semaphore有两个目的，第一个目的是多个共享资源互斥使用，第二目的是并发线程数的控制
######实现互斥锁
~~~

 class TestSemaphore {

    private static int count;

    private static Semaphore semaphore = new Semaphore(1);

    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {

                try {
                    semaphore.acquire();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                count++;
                semaphore.release();

                System.out.println(count);
            }).start();
        }
    }
}
~~~

######`重要`控制并发量(限流)
除了能实现互斥锁，信号量还可以做到`允许多个线程访问同一个临界区`，这是它与互斥锁一个较大的区别点。假如某公司有3台测试机，有6名工程师需要使用。一人使用一次即释放给别人使用
~~~
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;

public class CyclicBarrierTest {

    public static void main(String[] args) {
        Semaphore semaphore = new Semaphore(3);

        for (int i = 0; i < 6; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {

                    try {
                        semaphore.acquire();
                        System.out.println(Thread.currentThread().getName().concat(" 抢到了手机"));
                        TimeUnit.SECONDS.sleep(3);
                        System.out.println(Thread.currentThread().getName().concat(" 用完了手机"));

                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } finally {
                        semaphore.release();
                    }

                }
            }, String.valueOf(i + 1)).start();


        }
    }
}
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-d53aabe3c5cccca1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
