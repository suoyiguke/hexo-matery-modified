---
title: java线程基础之-yield();-和线程优先级的关系.md
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
title: java线程基础之-yield();-和线程优先级的关系.md
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
~~~
import java.util.concurrent.CountDownLatch;

public class Test1{
    static CountDownLatch countDownLatch = new CountDownLatch(1);

    public static void main(String[] args) throws InterruptedException {

        //想办法让线程B和C并行执行

        Thread B = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    countDownLatch.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("线程B执行"+System.currentTimeMillis());
                System.out.println("线程B执行完毕");

            }
        },"B");


        Thread C =  new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    countDownLatch.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                System.out.println("线程C执行"+System.currentTimeMillis());
                System.out.println("线程C执行完毕");
            }
        },"C");

        B.setPriority(1);
        B.start();

        C.setPriority(10);
        C.start();



        Thread A = new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("线程A执行");
                System.out.println("线程A调用yield()");
                Thread.yield();;
                System.out.println("线程A执行完毕");
                System.out.println("开启阀门，让线程B和C同时执行");
                countDownLatch.countDown();


            }
        }, "A");
        A.setPriority(1);
        A.start();




    }
}




~~~
###多核cpu系统下执行结果：可以看出线程B和C是并发执行的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-880d294be96fa9e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

B和C谁先打印顺序没有保证，即使C线程的优先级为10
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b70dac078e5c462d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
多运行几下甚至会出现这种情况
![image.png](https://upload-images.jianshu.io/upload_images/13965490-dd50921ddb4e5a7f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###linux下单核cpu的执行结果，B线程总是在C之前打印
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5deb31789f926d0a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/13965490-1645151f06a1b46f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

设置线程优先级对yield()没有任何影响
B.setPriority(Thread.NORM_PRIORITY);
