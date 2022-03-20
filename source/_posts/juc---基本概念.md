---
title: juc---基本概念.md
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
title: juc---基本概念.md
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

juc指的是java 并发工具类
- 并发包 java.util.concurrent
- 并发原子包 java.util.concurrent.atomic
- 并发锁包 java.util.concurrent.locks

在jdk文档上可以看到
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d5900e3478a74165.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###出现线程安全问题示例程序


这段代码模拟的是3个售货员卖30张票，每人10张。3个售货员对应3个线程，对number 、n 实例属性进行操作。运行结果出现线程安全问题
~~~

public class MpCust{

    private int number = 30;

    private int n = 0;

    public void mp(){

        if(number>0){
            number--;
            n++;
            System.out.println(Thread.currentThread().getName()+"==>卖出"+n+"还剩"+number);
        }

    }
    public static void main(String[] args) {

        MpCust mpCust = new MpCust();
        for (int i = 0; i <3 ; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {

                    for (int j = 0; j < 10; j++) {
                            mpCust.mp();
                    }


                }
            },"线程"+(i+1)).start();

        }



    }

}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f9d70d34b74e1029.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###使用synchronized解决

###使用ReentrantLock 解决
~~~
import java.util.concurrent.locks.ReentrantLock;

public class MpCust {

    private int number = 30;
    private int n = 0;
    private final ReentrantLock lock = new ReentrantLock();

    public void mp() {

        if (number > 0) {

            lock.lock();
            try {
                number--;
                n++;
            } finally {
                lock.unlock();
            }
        }

        System.out.println(Thread.currentThread().getName() + "==>卖出" + n + "还剩" + number);
    }


    public static void main(String[] args) {

        MpCust mpCust = new MpCust();
        for (int i = 0; i < 3; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {

                    for (int j = 0; j < 10; j++) {
                        mpCust.mp();
                    }


                }
            }, "线程" + (i + 1)).start();

        }


    }

}
~~~
