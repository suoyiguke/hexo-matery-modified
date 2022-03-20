---
title: java-多线程之生产者消费者模式.md
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
title: java-多线程之生产者消费者模式.md
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
生产者消费者模式可以让生产者线程和消费者线程之间并发执行互不干扰。核心就是：
- 数据没了停止消费
- 数据满了停止生产
- 数据有了激活消费
- 数据没了激活生产，数据没了才激活生产？那不晚了吗

######使用synchronized和wait/notify机制加上Integer 类型的共享数据实现
- 如果number不等于0则唤醒消费者
- 如果number等于0则唤醒生产者
- number不能超过10，否则生产者线程进入等待状态
- number不能小于0，否则消费者线程进入等待状态
- 消费者和生产者均开4个线程工作

~~~
class Producer extends Thread implements Runnable {

    public Producer(String name) {
        super(name);
    }

    @Override
    public void run() {

        synchronized (A.class) {
            //number不能超过10，否则生产者线程进入等待状态
            //防止虚假唤醒
            while (A.number>=10){
                try {
                    A.class.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            //number小于10则再加1
            A.number++;
            System.out.println(Thread.currentThread().getName() + "==>让number加1。当前number=" + A.number);
            //唤醒其他线程，通知其他线程加入监视器锁竞争
            A.class.notifyAll();
        }

    }


}

class Consumer extends Thread implements Runnable {
    public Consumer(String name) {
        super(name);
    }

    @Override
    public void run() {
        synchronized (A.class) {

            //防止虚假唤醒
            while (A.number<=0){
                try {
                    A.class.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }


            A.number--;
            System.out.println(Thread.currentThread().getName() + "==>让number减1。当前number=" + A.number);
            //唤醒其他线程，通知其他线程加入监视器锁竞争
            A.class.notifyAll();
        }
    }
}


class A {

    //number最大值为100，最小值为0
    volatile static Integer number = 0;


    public static void main(String[] args) {

        //4个生成者线程，4个消费者线程
        for (int i = 0; i < 4; i++) {
            new Producer("生产者" + (i + 1)).start();

        }


        for (int i = 0; i < 4; i++) {
            new Consumer("消费者" + (i + 1)).start();
        }


    }
}
~~~
