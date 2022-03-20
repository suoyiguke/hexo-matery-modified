---
title: jmm--synchronized关键字之八种锁测验.md
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
title: jmm--synchronized关键字之八种锁测验.md
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
###规则
线程之前不是竞争同一个监视器锁的话可以无视synchronized 

######1、printA和printB方法均加上synchronized 关键字，A和B的打印顺序？
打印顺序是A，B 原因是同一个实例，同一把锁。由于main线程中的sleep。A线程优先获得了监视器锁先执行

~~~
class TestLock{

    public synchronized void printA(){
        System.out.println("A");
    }
    public synchronized void printB(){
        System.out.println("B");
    }


    public static void main(String[] args) throws InterruptedException {

            TestLock testLock = new TestLock();
            new Thread(new Runnable() {
                @Override
                public void run() {
                    testLock.printA();
                }
            }, "A").start();

            //让A线程先执行
            Thread.sleep(2*1000);

            new Thread(new Runnable() {
                @Override
                public void run() {
                    testLock.printB();
                }
            }, "B").start();
        }

}
~~~

######2、printA和printB方法均加上synchronized 关键字，A线程睡眠4s。
相比第一点，A线程睡眠了4秒。执行结果顺序还是A,B。因为A线程start在B线程前面，A线程会先得到监视器锁先执行

~~~
import java.util.concurrent.TimeUnit;
class TestLock{
    public synchronized void printA(){
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("A");
    }
    public synchronized void printB(){
        System.out.println("B");
    }


    public static void main(String[] args) throws InterruptedException {
            TestLock testLock = new TestLock();
            new Thread(new Runnable() {
                @Override
                public void run() {
                    testLock.printA();
                }
            }, "A").start();

            //让A线程先执行
            Thread.sleep(2*1000);
            new Thread(new Runnable() {
                @Override
                public void run() {
                    testLock.printB();
                }
            }, "B").start();
        }
}
~~~

######3、新增无锁的printC方法，B线程调用printC方法。问执行顺序？

A线程虽然加了synchronized ，但是此时并没有与之竞争监视器锁的线程。A线程一定是先执行，但是sleep4秒。所以顺序是C，A
~~~
 public void printC(){
        System.out.println("C");
    }
~~~
~~~
import java.util.concurrent.TimeUnit;

class TestLock{

    public synchronized void printA(){
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("A");
    }

    public void printC(){
        System.out.println("C");
    }

    public static void main(String[] args) throws InterruptedException {

            TestLock testLock = new TestLock();
            new Thread(new Runnable() {
                @Override
                public void run() {
                    testLock.printA();
                }
            }, "A").start();

            //让A线程先执行
            Thread.sleep(2*1000);

            new Thread(new Runnable() {
                @Override
                public void run() {
                    testLock.printC();
                }
            }, "B").start();
        }

}
~~~

######4、使用两个对象，分别为printA方法和printB方法做对象锁。此时输出顺序是？
~~~
TestLock testLock1 = new TestLock();
TestLock testLock2 = new TestLock();
~~~
printA方法和printB方法竞争的不是同一把监视器锁，因此不需要考虑锁的竞争。因为A线程与sleep的原因，所以顺序是：B,A
~~~
import java.util.concurrent.TimeUnit;

class TestLock{

    public synchronized void printA(){
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("A");
    }

    public synchronized void printB(){
        System.out.println("B");
    }

    public static void main(String[] args) throws InterruptedException {

            TestLock testLock1 = new TestLock();
            TestLock testLock2 = new TestLock();
            new Thread(new Runnable() {
                @Override
                public void run() {
                    testLock1.printA();
                }
            }, "A").start();

            //让A线程先执行
            Thread.sleep(2*1000);

            new Thread(new Runnable() {
                @Override
                public void run() {
                    testLock2.printB();
                }
            }, "B").start();
        }

}
~~~

######5、printA和printB方法是静态同步块（加上synchronized 、static关键字）
因为printA和printB方法都加上了static，所以synchronized 锁定的是TestLock.class。即是同一把锁，因为main线程的Thread.sleep(2 * 1000) A线程先竞争到对象锁先执行了。所以打印顺序是A，B

~~~
import java.util.concurrent.TimeUnit;

class TestLock {

    public synchronized static void printA() {
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("A");
    }

    public synchronized static void printB() {
        System.out.println("B");
    }

    public static void main(String[] args) throws InterruptedException {

        TestLock testLock = new TestLock();
        new Thread(new Runnable() {
            @Override
            public void run() {
                testLock.printA();
            }
        }, "A").start();

        //让A线程先执行
        Thread.sleep(2 * 1000);

        new Thread(new Runnable() {
            @Override
            public void run() {
                testLock.printB();
            }
        }, "B").start();
    }

}
~~~

######6、printA和printB方法是静态同步块，且使用两个对象
打印顺序是A,B 原因和上面的一样，即是使用两个对象。因为方法上加了static
~~~
import java.util.concurrent.TimeUnit;

class TestLock {

    public synchronized static void printA() {
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("A");
    }

    public synchronized static void printB() {
        System.out.println("B");
    }

    public static void main(String[] args) throws InterruptedException {

        TestLock testLock1 = new TestLock();
        TestLock testLock2 = new TestLock();
        new Thread(new Runnable() {
            @Override
            public void run() {
                testLock1.printA();
            }
        }, "A").start();

        //让A线程先执行
        Thread.sleep(2 * 1000);

        new Thread(new Runnable() {
            @Override
            public void run() {
                testLock2.printB();
            }
        }, "B").start();
    }

}
~~~
######7、一个静态同步块，一个实例同步块
打印顺序是B,A 因为竞争的不是同一把锁，一个是TestLock .class一个是testLock 实例。而A线程有sleep，所以B先执行

~~~
import java.util.concurrent.TimeUnit;

class TestLock {

    public synchronized static void printA() {
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("A");
    }

    public synchronized  void printB() {
        System.out.println("B");
    }

    public static void main(String[] args) throws InterruptedException {

        TestLock testLock = new TestLock();
        new Thread(new Runnable() {
            @Override
            public void run() {
                testLock.printA();
            }
        }, "A").start();

        //让A线程先执行
        Thread.sleep(2 * 1000);

        new Thread(new Runnable() {
            @Override
            public void run() {
                testLock.printB();
            }
        }, "B").start();
    }

}
~~~

######8、一个静态同步块，一个实例同步块。两个对象实例
顺序还是B,A 原因和第7点一样
~~~
import java.util.concurrent.TimeUnit;

class TestLock {

    public synchronized static void printA() {
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("A");
    }

    public synchronized void printB() {
        System.out.println("B");
    }

    public static void main(String[] args) throws InterruptedException {

        TestLock testLock1 = new TestLock();
        TestLock testLock2 = new TestLock();
        new Thread(new Runnable() {
            @Override
            public void run() {
                testLock1.printA();
            }
        }, "A").start();

        //让A线程先执行
        Thread.sleep(2 * 1000);

        new Thread(new Runnable() {
            @Override
            public void run() {
                testLock2.printB();
            }
        }, "B").start();
    }

}
~~~
