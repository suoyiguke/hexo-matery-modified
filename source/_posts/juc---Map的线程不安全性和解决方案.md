---
title: juc---Map的线程不安全性和解决方案.md
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
title: juc---Map的线程不安全性和解决方案.md
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
######1、多线程对HashMap进行put操作
~~~
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

class TestLock {

    public static void main(String[] args) {
        Map<String,String> map = new HashMap();

        for (int i = 0; i <20 ; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    map.put(UUID.randomUUID().toString().substring(0,4),UUID.randomUUID().toString().substring(0,4));
                    System.out.println(map);
                }
            }).start();
        }
    }
}
~~~
报出 java.util.ConcurrentModificationException 并发修改异常，证明HashMap不是线程安全的

######2、使用java.util.Collections的synchronizedMap方法包装下HashMap。
将HashMap变为线程安全的

~~~
Map<String,String> map = Collections.synchronizedMap(new HashMap<>());

~~~
~~~
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

class TestLock {

    public static void main(String[] args) {
        Map<String,String> map = Collections.synchronizedMap(new HashMap<>());

        for (int i = 0; i <20 ; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    map.put(UUID.randomUUID().toString().substring(0,4),UUID.randomUUID().toString().substring(0,4));
                    System.out.println(map);
                }
            }).start();
        }
    }
}
~~~
######3、使用juc下的ConcurrentHashMap
~~~
Map<String,String> map = new ConcurrentHashMap<>();
~~~
~~~
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

class TestLock {

    public static void main(String[] args) {
        Map<String,String> map = new ConcurrentHashMap<>();
        for (int i = 0; i <20 ; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    map.put(UUID.randomUUID().toString().substring(0,4),UUID.randomUUID().toString().substring(0,4));
                    System.out.println(map);
                }
            }).start();
        }
    }
}
~~~
