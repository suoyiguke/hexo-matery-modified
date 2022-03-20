---
title: juc---Set的线程不安全性和解决方案.md
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
title: juc---Set的线程不安全性和解决方案.md
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
######1、对HashSet进行并发add
~~~
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

class TestLock {

    public static void main(String[] args) {
        Set<String> set = new HashSet<>();

        for (int i = 0; i <20 ; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    set.add(UUID.randomUUID().toString().substring(0,4));
                    System.out.println(set);
                }
            }).start();
        }
    }
}
~~~

报出异常：java.util.ConcurrentModificationException。说明HashSet不是线程安全的

######2、使用java.util.Collections工具来将HashSet转化为线程安全

~~~
 Set<String> set = Collections.synchronizedSet(new HashSet<>());
~~~
~~~
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

class TestLock {

    public static void main(String[] args) {
        Set<String> set = Collections.synchronizedSet(new HashSet<>());

        for (int i = 0; i <20 ; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    set.add(UUID.randomUUID().toString().substring(0,4));
                    System.out.println(set);
                }
            }).start();
        }
    }
}
~~~

######3、使用JUC提供的CopyOnWriteArraySet
~~~
Set<String> set = new CopyOnWriteArraySet();
~~~
~~~
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.CopyOnWriteArraySet;

class TestLock {

    public static void main(String[] args) {
        Set<String> set = new CopyOnWriteArraySet();

        for (int i = 0; i <20 ; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    set.add(UUID.randomUUID().toString().substring(0,4));
                    System.out.println(set);
                }
            }).start();
        }
    }
}
~~~
