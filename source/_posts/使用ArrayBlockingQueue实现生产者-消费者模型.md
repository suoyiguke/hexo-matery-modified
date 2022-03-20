---
title: 使用ArrayBlockingQueue实现生产者-消费者模型.md
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
title: 使用ArrayBlockingQueue实现生产者-消费者模型.md
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
* CountDownLatch 确保生产者消费者线程同时执行
* BlockingQueue.put() 和 BlockingQueue.take()  会引发阻塞

~~~
package 线程池;
import java.util.concurrent.*;
/**
 * @author 蓑衣孤客
 * @date 2019/9/2710:09
 */
public class ArrayBlockingQueueTest {

    static BlockingQueue<Integer> arrayBlockingQueue = new ArrayBlockingQueue(10);

    public static void main(String[] args) throws InterruptedException {
        final ExecutorService executorService = Executors.newCachedThreadPool();
        final CountDownLatch countDownLatch = new CountDownLatch(1);

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    countDownLatch.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("生产者开始");

                for (int i = 0; i < 1000; i++) {
                    executorService.execute(new shengchangzhe(i));

                }
            }
        },"生产者线程").start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    countDownLatch.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("消费者开始");
                for (int i = 0; i < 1000; i++) {
                    executorService.execute(new xiaofeizhe());
                }
            }
        },"消费者线程").start();

        countDownLatch.countDown();

    }


    static class xiaofeizhe implements Runnable {

        @Override
        public void run() {
            try {
                Integer take = arrayBlockingQueue.take();
                System.out.println("消费者====>" + take);

            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    static class shengchangzhe implements Runnable {
        private Integer number;

        public shengchangzhe(Integer number) {
            this.number = number;
        }

        @Override
        public void run() {
            try {
                arrayBlockingQueue.put(this.number);
                System.out.println("生产着===>" + this.number);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
    }
}

~~~
