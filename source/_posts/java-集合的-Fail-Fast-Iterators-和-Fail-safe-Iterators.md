---
title: java-集合的-Fail-Fast-Iterators-和-Fail-safe-Iterators.md
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
引用 https://www.codejava.net/java-core/collections/understanding-collections-and-thread-safety-in-java

### Fail-Fast Iterators
-  迭代器遍历集合，过程中对集合对象的内容进行了修改( add、remove、update），则会抛出ConcurrentModificationException
  
- java.util 包下的集合类都是快速失败的，不能在多线程下发生并发修改，迭代过程中被修改


###测试代码
~~~
import java.util.*;

/**
 * This test program illustrates how a collection's iterator fails fast
 * and throw ConcurrentModificationException
 * @author www.codejava.net
 *
 */
public class IteratorFailFastTest {

    private List<Integer> list = new Vector<>();

    public IteratorFailFastTest() {
        for (int i = 0; i < 10_000; i++) {
            list.add(i);
        }
    }

    public void runUpdateThread() {
        Thread thread1 = new Thread(new Runnable() {

            @Override
            public void run() {
                for (int i = 10_000; i < 20_000; i++) {
                    list.add(i);
                }
            }
        });

        thread1.start();
    }


    public void runIteratorThread() {
        Thread thread2 = new Thread(new Runnable() {

            @Override
            public void run() {
                ListIterator<Integer> iterator = list.listIterator();
                while (iterator.hasNext()) {
                    Integer number = iterator.next();
                    System.out.println(number);
                }
            }
        });

        thread2.start();
    }

    public static void main(String[] args) {
        IteratorFailFastTest tester = new IteratorFailFastTest();

        tester.runIteratorThread();
        tester.runUpdateThread();
    }
}
~~~
抛出ConcurrentModificationException异常
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bae5b7a19cfa283d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###Fail-safe Iterators 

- 先copy原有集合内容，在copy的集合上进行遍历
- 迭代器并不能访问到修改后的内容
- java.util.concurrent 包下的容器都是安全失败，可以在多线程下并发使用，并发修改

### 测试代码
- java.util.concurrent.CopyOnWriteArrayList代替原来的java.utils.Vector
~~~
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * This test program illustrates how a collection's iterator fails fast
 * and throw ConcurrentModificationException
 * @author www.codejava.net
 *
 */
public class IteratorFailFastTest {

    private List<Integer> list = new CopyOnWriteArrayList<Integer>();

    public IteratorFailFastTest() {
        for (int i = 0; i < 10_000; i++) {
            list.add(i);
        }
    }

    public void runUpdateThread() {
        Thread thread1 = new Thread(new Runnable() {

            @Override
            public void run() {
                for (int i = 10_000; i < 20_000; i++) {
                    list.add(i);
                }
            }
        });

        thread1.start();
    }


    public void runIteratorThread() {
        Thread thread2 = new Thread(new Runnable() {

            @Override
            public void run() {
                ListIterator<Integer> iterator = list.listIterator();
                while (iterator.hasNext()) {
                    Integer number = iterator.next();
                    System.out.println(number);
                }
            }
        });

        thread2.start();
    }

    public static void main(String[] args) {
        IteratorFailFastTest tester = new IteratorFailFastTest();

        tester.runIteratorThread();
        tester.runUpdateThread();
    }
}
~~~
- 正常执行
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c7299ea60ffe9b88.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
