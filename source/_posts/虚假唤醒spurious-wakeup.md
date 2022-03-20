---
title: 虚假唤醒spurious-wakeup.md
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
title: 虚假唤醒spurious-wakeup.md
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
线程基础之使用while循环代替if条件防止虚假唤醒
######先来看看下面的程序
A、C两个线程做number的增1，B、D 两个线程做number的减1
~~~
class MpCust {

    private int number = 0;
    public synchronized void increment() throws InterruptedException {
        if (number != 0){
            this.wait();
        }
        number++;
        System.out.println(Thread.currentThread().getName()+"\n"+number);
        this.notifyAll();
    }

    public synchronized void decrement() throws InterruptedException {
        if (number==0){
            this.wait();
        }
        number--;
        System.out.println(Thread.currentThread().getName()+"\n"+number);
        this.notifyAll();
    }

    public static void main(String[] args) {
        MpCust mpCust = new MpCust();

        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(300);
                        mpCust.increment();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"A").start();


        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(400);
                        mpCust.decrement();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"B").start();




        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(300);
                        mpCust.increment();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"C").start();


        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(400);
                        mpCust.decrement();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"D").start();


    }

}
~~~
运行结果中有值打印为2，这是不正常的！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-df7b2f28645a9a5d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
因为increment()方法执行到这里，number 的值不为0的话就会执行Object.wait()方法，当前线程会进入等待。
~~~
    if (number != 0){
            this.wait();
    }
~~~
因为这段代码是在多线程下执行的，线程执行到 this.wait();等待，苏醒后继续执行。这时候如果别的线程已经将number的值改为1，那么就不会再去判断一次number 是否等于0，就直接往下执行number++，导致number的值为2。这种想象我们称之为`虚假唤醒`

所以需要一种机制让线程苏醒之后`再次判断`number的值是否等于0。这时候java中的while循环正好排上用场。

######使用while循环代替if条件
~~~
    while(number != 0){
            this.wait();
    }
~~~
~~~
class MpCust {

    private int number = 0;
    public synchronized void increment() throws InterruptedException {
        while (number != 0){
            this.wait();
        }
        number++;
        System.out.println(Thread.currentThread().getName()+"\n"+number);
        this.notifyAll();
    }

    public synchronized void decrement() throws InterruptedException {
        while (number==0){
            this.wait();
        }
        number--;
        System.out.println(Thread.currentThread().getName()+"\n"+number);
        this.notifyAll();
    }

    public static void main(String[] args) {
        MpCust mpCust = new MpCust();

        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(300);
                        mpCust.increment();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"A").start();


        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(400);
                        mpCust.decrement();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"B").start();




        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(300);
                        mpCust.increment();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"C").start();


        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(400);
                        mpCust.decrement();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"D").start();


    }

}
~~~
完美~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1441677c82c202d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
