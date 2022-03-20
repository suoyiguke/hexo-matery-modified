---
title: jmm-synchronized关键字之基本用法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jmm
categories: jmm
---
---
title: jmm-synchronized关键字之基本用法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jmm
categories: jmm
---


synchronized 通过`排他锁、互斥锁`的方式保证了同一时间内，被synchronized 修饰的代码是`单线程`执行的。它可以通过对java中的对象加锁，并且它是一种可重入的锁。所以，当线程执行到一段被synchronized 修饰的代码之前，会先进行加锁，执行完之后再进行解锁。在加锁之后，解锁之前的`临界区`之内其它线程试无法再次获得锁的，只有这条加锁线程可以重复获得该锁


###基本用法
synchronized关键字主要有以下这3种用法：

- 修饰实例方法，作用于当前实例（this） 加锁，进入同步代码前要获得当前实例的锁

- 修饰静态方法，作用于当前类对象（Object.class）加锁，进入同步代码前要获得当前类对象的锁

- 修饰代码块，指定加锁对象，对给定对象加锁，进入同步代码库前要获得给定对象的锁。


![image.png](https://upload-images.jianshu.io/upload_images/13965490-216aa65b99aae85d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######synchronized使用在实例方法之上
~~~
public class Test {
    static int i = 0;

    public synchronized void increase() {
        i++;
    }

    public static void main(String[] args) throws InterruptedException {
        Test test = new Test();
        Thread t1 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int j = 0; j < 1000000; j++) {
                    test.increase();
                }
            }
        });
        Thread t2 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int j = 0; j < 1000000; j++) {
                    test.increase();
                }
            }
        });
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println(i);
    }
}
~~~

######synchronized使用在静态方法之上
~~~
public class Test {
    static int i = 0;

    public static synchronized void increase() {
        i++;
    }

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int j = 0; j < 1000000; j++) {
                    Test.increase();
                }
            }
        });
        Thread t2 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int j = 0; j < 1000000; j++) {
                    Test.increase();
                }
            }
        });
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println(i);
    }
}
~~~

######synchronized修饰静态代码块，给当前的类.class加锁
相当于直接把synchronized关键字加在静态方法上了
~~~
  public static  void increase() {
        synchronized(Test.class){
            i++;
        }
    }

~~~

######synchronized修饰实例代码块，给当前实例this加锁
相当于直接把synchronized关键字在实例方法上了
~~~
    public void increase() {
        synchronized(this){
            i++;
        }
    }

~~~

######synchronized加在普通对象上
~~~
    static Object lock  = new Object();

    public void increase() {
        synchronized(lock){
            i++;
        }
    }

~~~


###特点

- 阻塞未获取到锁的线程
- 获取锁无法设置超时
- 无法实现公平锁
- 控制等待和唤醒需要结合加锁对象的 wait() 和 notify()、notifyAll()
- 锁的功能是 JVM 层面实现的
- 在加锁代码块执行完（退出`临界区`）或者出现异常，自动释放锁
- synchronized方法，一定要显示标明，它是不能隐式标明的。在继承关系中如果子类并没有重写父类的synchronized方法，那么调用的是父类的同步方法。子类重写了就看有没有使用synchronized了
- synchronized是可重入的。可以重复获取同一个对象的锁
- 两个synchronized代码块可以嵌套，同时持有多个锁
- synchronized关键字具有方法之间的传递性，一个synchronized方法去调用另一个非同步的方法。仍然线程安全

###synchronized的特征实验
1、一个synchronized方法去调用另一个非同步的方法。仍然线程安全
~~~

class SynchTest2 {
    static int i = 0;

    //加了synchronized
    public synchronized static void method1() throws InterruptedException {
        method2();
    }
    //没有加synchronized
    public  static void method2() {
        for (int j = 0; j < 100000; j++) {
            i++;
        }

    }

    //加了synchronized
    public synchronized static void method3(){
        for (int j = 0; j < 100000; j++) {
            i++;
        }
    }

    public static void main(String[] args) throws InterruptedException {


        Thread thread1 = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    method1();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        Thread thread2 = new Thread(new Runnable() {
            @Override
            public void run() {
                method3();
            }
        });

        thread1.start();
        thread2.start();

        thread1.join();
        thread2.join();

        System.out.println(i);



    }

}
~~~


###使用注意


1、不能使用int、double等基本数据类型和null做对象锁；

2、最好不要使用String、Integer等基本数据对象类型做对象锁，因为如果基本数据对象类型的值发生改变的话，原先加的锁可能会丢失；

3、synchronized关键字修饰对象时，如果对象的属性值发生改变（对象的引用发生改变例外）不会影响锁的稳定；

4、尽量缩小`临界区`范围


