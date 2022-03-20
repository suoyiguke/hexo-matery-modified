---
title: java-基础之finally是否一定会执行-.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
事实上finally区域代码在很多情况下都不会执行
######没有进入try区域
 
1、程序在进入try区域之前抛出异常，那么整个try-catch -finally都不会执行
~~~
class TestThreadLocal {

    public static Integer test() {
        int a = 1 / 0;

        try {
            int b = 1 / 0;// 不会执行
        } catch (Exception e) {
            System.out.println(e);// 不会执行
        } finally {
            System.out.println("执行finally！");// 不会执行
            return 1;// 不会执行
        }

    }

    public static void main(String[] args) {
        Integer test = test();
        System.out.println(test);

    }
}
~~~

2、程序在进入try区域之前return，那么整个try-catch -finally都不会执行
~~~
class TestThreadLocal {

    public static Integer test() {

        if (true) {
            return 0;
        }

        try {
            int b = 1 / 0;// 不会执行
        } catch (Exception e) {
            System.out.println(e);// 不会执行
        } finally {
            System.out.println("执行finally！");// 不会执行
            return 1;// 不会执行
        }

    }

    public static void main(String[] args) {
        Integer test = test();
        System.out.println(test);

    }
}
~~~

######进入了try区域
 如果当一个线程在执行 try 语句块或者 catch 语句块时被打断（interrupted）或者被终止（killed），与其相对应的 finally 语句块可能不会执行。还有更极端的情况，就是在线程运行 try 语句块或者 catch 语句块时，突然死机或者断电，finally 语句块肯定不会执行了。

1、守护线程随着用户线程退出而退出，finally 不会执行
~~~
class DaemonDemo {

    public static void main(String[] args) {
        Thread daemonThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        System.out.println("i am alive");
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } finally {
                        System.out.println("finally block");
                    }
                }
            }
        });
        daemonThread.setDaemon(true);
        daemonThread.start();
        try {
            //确保main线程结束前能给daemonThread能够分到时间片
            Thread.sleep(800);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2ac9520341c45633.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
第二次没有执行finally

######退出程序
1、执行了System.exit(0); 退出java虚拟机
~~~
class TestFinally{

    public static Integer test() {

        System.exit(0);

        try {
            int b = 1 / 0;// 不会执行
        } catch (Exception e) {
            System.out.println(e);// 不会执行
        } finally {
            System.out.println("执行finally！");// 不会执行
            return 1;// 不会执行
        }

    }

    public static void main(String[] args) {
        Integer test = test();
        System.out.println(test);

    }
}
~~~
