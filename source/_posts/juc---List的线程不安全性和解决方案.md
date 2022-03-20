---
title: juc---List的线程不安全性和解决方案.md
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
title: juc---List的线程不安全性和解决方案.md
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
######1、启动20个线程对ArrayList做add剿操作
~~~
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

class TestLock {

    public static void main(String[] args) {

        List<String> list = new ArrayList<>();

        for (int i = 0; i <20 ; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    list.add(UUID.randomUUID().toString().substring(0,4));
                    System.out.println(list);
                }
            }).start();
        }
    }
}
~~~
不仅打印了null元素，出现线程不安全。而且还报出异常：
java.util.ConcurrentModificationException 并发修改异常。说明ArrayList是线程不安全的

######2、使用Vector代替ArrayList
~~~
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.Vector;

class TestLock {

    public static void main(String[] args) {

        List<String> list = new Vector<>();

        for (int i = 0; i <20 ; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    list.add(UUID.randomUUID().toString().substring(0,4));
                    System.out.println(list);
                }
            }).start();
        }
    }
}
~~~


Vector表现为线程安全，查看Vector源码，发现是使用synchronized同步锁机制来实现线程安全的！效率会有问题。因此不推荐使用
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4ad1f2efdde91ce2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######3、使用java.util.Collections工具类来实现ArrayList的线程安全
用这种方式可以把线程不安全的ArrayList转换为线程安全，`这种方式在小数量下完全可行！`
~~~
List<String> list = Collections.synchronizedList( new ArrayList<>());
~~~

~~~
import java.util.*;

class TestLock {

    public static void main(String[] args) {
        List<String> list = Collections.synchronizedList( new ArrayList<>());

        for (int i = 0; i <20 ; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    list.add(UUID.randomUUID().toString().substring(0,4));
                    System.out.println(list);
                }
            }).start();
        }
    }
}
~~~

######4、使用JUC下的 CopyOnWriteArrayList 来实现list线程安全

CopyOnWriteArrayList使用了一种 `写时复制`机制也是`读写分离`思想的一种。`多线程下推荐使用`
~~~
List<String> list = new CopyOnWriteArrayList();
~~~
~~~
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

class TestLock {

    public static void main(String[] args) {
        List<String> list = new CopyOnWriteArrayList();

        for (int i = 0; i <20 ; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    list.add(UUID.randomUUID().toString().substring(0,4));
                    System.out.println(list);
                }
            }).start();
        }
    }
}
~~~
