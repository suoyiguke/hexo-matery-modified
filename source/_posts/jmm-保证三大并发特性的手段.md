---
title: jmm-保证三大并发特性的手段.md
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
title: jmm-保证三大并发特性的手段.md
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
###解决可见性问题
######使用Atomic类解决
~~~
import java.util.concurrent.atomic.AtomicBoolean;
class Test{
    static AtomicBoolean flag = new AtomicBoolean(false);
    public static void main(String[] args) throws InterruptedException {
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (!flag.get());
            }
        },"A").start();

        Thread.sleep(500);
        flag.set(true);
    }
}
~~~

######使用volatile解决
~~~
class Test{
    volatile static  Boolean flag = false;
    public static void main(String[] args) throws InterruptedException {
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (!flag);
            }
        },"A").start();

        Thread.sleep(500);
        flag = true;
    }
}
~~~

######使用synchronized解决

~~~
class Test {
    static Boolean flag = false;
    public static void main(String[] args) throws InterruptedException {
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (!flag) {
                    synchronized (Test.class) {
                    }
                }
            }
        }, "A").start();

        Thread.sleep(500);
        set();
    }

    public static void set() {
        flag = true;
    }
}
~~~



######使用lock解决
~~~
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class Test {
    static Lock lock = new ReentrantLock();
    static Boolean flag = false;

    public static void main(String[] args) throws InterruptedException {
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (!flag) {
                    try {
                        lock.lock();
                    }finally {
                        lock.unlock();
                    }

                }
            }
        }, "A").start();

        Thread.sleep(500);
        set();
    }

    public static void set() {
        flag = true;
    }
}
~~~

###解决原子性问题
######使用Atomic解决
~~~
import java.util.ArrayList;
import java.util.concurrent.atomic.AtomicInteger;

class Test{

    static AtomicInteger num = new AtomicInteger(0);
    public static void main(String[] args) throws InterruptedException {


        ArrayList<Thread> list = new ArrayList<>(2000);

        for (int i = 0; i <2000 ; i++) {
            Thread thread = new Thread(new Runnable() {
                @Override
                public void run() {
                    num.incrementAndGet();
                }
            });
            thread.start();
            list.add(thread);

        }

        for (Thread thread : list) {
            thread.join();
        }

        System.out.println(num);
    }

}
~~~

######使用synchronized解决
~~~
import java.util.ArrayList;

class Test{

    static Integer num = 0;
    public static void main(String[] args) throws InterruptedException {


        ArrayList<Thread> list = new ArrayList<>(2000);

        for (int i = 0; i <2000 ; i++) {
            Thread thread = new Thread(new Runnable() {
                @Override
                public void run() {
                    synchronized(Test.class){
                        num++;
                    }

                }
            });
            thread.start();
            list.add(thread);

        }

        for (Thread thread : list) {
            thread.join();
        }

        System.out.println(num);
    }

}
~~~
######使用lock解决
~~~
import java.util.ArrayList;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class Test{

    static Integer num = 0;
    static Lock lock = new ReentrantLock();
    public static void main(String[] args) throws InterruptedException {


        ArrayList<Thread> list = new ArrayList<>(2000);

        for (int i = 0; i <2000 ; i++) {
            Thread thread = new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        lock.lock();
                        num++;
                    }finally {
                        lock.unlock();
                    }

                }
            });
            thread.start();
            list.add(thread);

        }

        for (Thread thread : list) {
            thread.join();
        }

        System.out.println(num);
    }

}
~~~

######`重要` volatile关键字无法解决原子性问题
~~~
import java.util.ArrayList;

class Test{

    volatile static Integer num = 0;
    public  static void main(String[] args) throws InterruptedException {
        ArrayList<Thread> list = new ArrayList<>(2000);

        for (int i = 0; i <2000 ; i++) {
            Thread thread = new Thread(new Runnable() {
                @Override
                public void run() {
                    num++;
                }
            });
            thread.start();
            list.add(thread);
        }

        for (Thread thread : list) {
            thread.join();
        }
        System.out.println(num);
    }
}
~~~
仍然出现线程安全问题，结果小于2000
![image.png](https://upload-images.jianshu.io/upload_images/13965490-dd0b7e0e34881b0f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###解决有序性问题

######使用volatile解决
使用volatile修饰的变量不会参与到`指令重排序`中
~~~
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class Test {

   volatile static int x;
   volatile static int y;

    public static void main(String[] args) throws InterruptedException {
        Set<String> hashSet = new HashSet<String>();
        Map<String, Integer> concurrentHashMap = new ConcurrentHashMap<>();

        for (int i = 0; i <10000000; i++) {
            x = 0;
            y = 0;
            //清除之前记录的结果
            hashSet.clear();
            concurrentHashMap.clear();

            Thread t1 = new Thread(() -> {
                int v1 = y;// Step1
                x = 1; //Step2
                concurrentHashMap.put("v1", v1);//Step3
            },"A") ;

            Thread t2 = new Thread(() -> {
                int v2 = x;//Step4
                y = 1;//Step5
                concurrentHashMap.put("v2", v2);//Step6
            },"B");

            t1.start();
            t2.start();
            //等待线程 t1 t2 执行完成
            t1.join();
            t2.join();


            if(concurrentHashMap.get("v1") == 1 && concurrentHashMap.get("v2") == 1){
                hashSet.add("(v1=" + concurrentHashMap.get("v1") + ",v2=" + concurrentHashMap.get("v2") + ")");
                System.out.println(hashSet);
            }

        }
    }

}
~~~
######使用synchronized解决
synchronized内存的代码不允许重排序
~~~
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class Test {

    static int x;
    static int y;

    public static void main(String[] args) throws InterruptedException {
        Set<String> hashSet = new HashSet<String>();
        Map<String, Integer> concurrentHashMap = new ConcurrentHashMap<>();

        for (int i = 0; i < 10000000; i++) {
            x = 0;
            y = 0;
            //清除之前记录的结果
            hashSet.clear();
            concurrentHashMap.clear();

            Thread t1 = new Thread(() -> {
                synchronized (Thread.currentThread()) {
                    int v1 = y;// Step1
                    x = 1; //Step2
                    concurrentHashMap.put("v1", v1);//Step3
                }

            }, "A");

            Thread t2 = new Thread(() -> {
                synchronized (Thread.currentThread()) {
                    int v2 = x;//Step4
                    y = 1;//Step5
                    concurrentHashMap.put("v2", v2);//Step6
                }
            }, "B");

            t1.start();
            t2.start();
            //等待线程 t1 t2 执行完成
            t1.join();
            t2.join();


            if (concurrentHashMap.get("v1") == 1 && concurrentHashMap.get("v2") == 1) {
                hashSet.add("(v1=" + concurrentHashMap.get("v1") + ",v2=" + concurrentHashMap.get("v2") + ")");
                System.out.println(hashSet);
            }

        }
    }

}
~~~

######使用lock解决
请使用一个ReentrantLock，不存在锁的竞争关系的话无法保证有序性
~~~
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Test {

    static int x;
    static int y;
    static Lock lock1 = new ReentrantLock();
    public static void main(String[] args) throws InterruptedException {
        Set<String> hashSet = new HashSet<String>();
        Map<String, Integer> concurrentHashMap = new ConcurrentHashMap<>();

        for (int i = 0; i < 10000000; i++) {
            x = 0;
            y = 0;
            //清除之前记录的结果
            hashSet.clear();
            concurrentHashMap.clear();

            Thread t1 = new Thread(() -> {
                try {
                    lock1.lock();
                    int v1 = y;// Step1
                    x = 1; //Step2
                    concurrentHashMap.put("v1", v1);//Step3
                } finally {
                    lock1.unlock();
                }


            }, "A");

            Thread t2 = new Thread(() -> {
                try {
                    lock1.lock();
                    int v2 = x;//Step4
                    y = 1;//Step5
                    concurrentHashMap.put("v2", v2);//Step6
                } finally {
                    lock1.unlock();
                }
            }, "B");

            t1.start();
            t2.start();
            //等待线程 t1 t2 执行完成
            t1.join();
            t2.join();


            if (concurrentHashMap.get("v1") == 1 && concurrentHashMap.get("v2") == 1) {
                hashSet.add("(v1=" + concurrentHashMap.get("v1") + ",v2=" + concurrentHashMap.get("v2") + ")");
                System.out.println(hashSet);
            }

        }
    }



}
~~~

######`重要`使用Atomic类无法保证有序性
下面的实例程序无法得到 v1 = 1 ， v2 =1 的值。很奇怪
~~~
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class Test {

    static AtomicInteger x;
    static AtomicInteger y;

    public static void main(String[] args) throws InterruptedException {
        Set<String> hashSet = new HashSet<String>();
        Map<String, AtomicInteger> concurrentHashMap = new ConcurrentHashMap<>();

        for (int i = 0; i < 10000000; i++) {
            x = new AtomicInteger(0);
            y = new AtomicInteger(0);
            //清除之前记录的结果
            hashSet.clear();
            concurrentHashMap.clear();

            Thread t1 = new Thread(() -> {
                AtomicInteger v1 = y;// Step1
                x = new AtomicInteger(1); //Step2
                concurrentHashMap.put("v1", v1);//Step3

            }, "A");

            Thread t2 = new Thread(() -> {
                AtomicInteger v2 = x;//Step4
                y = new AtomicInteger(1);//Step5
                concurrentHashMap.put("v2", v2);//Step6

            }, "B");

            t1.start();
            t2.start();
            //等待线程 t1 t2 执行完成
            t1.join();
            t2.join();


            if (concurrentHashMap.get("v1").get() == 1 && concurrentHashMap.get("v2").get() == 1) {
                hashSet.add("(v1=" + concurrentHashMap.get("v1").get() + ",v2=" + concurrentHashMap.get("v2").get() + ")");
                System.out.println(hashSet);
            }

        }
    }


}
~~~
