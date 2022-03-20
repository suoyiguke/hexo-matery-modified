---
title: java-线程基础之线程本地变量ThreadLocal.md
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
title: java-线程基础之线程本地变量ThreadLocal.md
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
> 自助者天助之

想在多个方法中使用某个变量，这个变量是当前线程的状态，其它线程不依赖这个变量。可以使用两种方法达到这种目的：

- 可以把变量定义在方法内部，然后再方法之间`传递参数`来使用，这个方法能解决问题，但是有个烦人的地方就是，每个方法都需要声明形参，多处声明，多处调用。影响代码的美观和维护。

- 可以使用`线程本地变量`ThreadLocal


###基本方法
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8802a430fa58cc82.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###使用
- threadLocal.set(e) 设置隔离变量
- threadLocal.get() 获取隔离变量
~~~
class TestThreadLocal {

    /**
     * 作用：哪个线程把数据放到threadLocal,哪个线程就可以取到，别的线程不可以取到。
     * 多个线程向threadLocal存储数据都可以做到不混乱，本线程就只能取到本线程设置的值
     */
    public static ThreadLocal<String> threadLocal = new ThreadLocal<String>();



    public static void main(String[] args) throws InterruptedException {

        Thread t1 = new Thread(new Runnable() {
            @Override
            public void run() {
                threadLocal.set("我是线程"+Thread.currentThread().getName()+" 线程号"+Thread.currentThread().getId());
                String s = threadLocal.get();
                System.out.println(s);

            }
        }, "t1");

        Thread t2 = new Thread(new Runnable() {
            @Override
            public void run() {

                threadLocal.set("我是线程"+Thread.currentThread().getName()+" 线程号"+Thread.currentThread().getId());
                String s = threadLocal.get();
                System.out.println(s);
            }
        }, "t2");

        Thread t3 = new Thread(new Runnable() {
            @Override
            public void run() {
                threadLocal.set("我是线程"+Thread.currentThread().getName()+" 线程号"+Thread.currentThread().getId());
                String s = threadLocal.get();
                System.out.println(s);
            }
        },"t3");

        t1.start();
        t2.start();
        t3.start();
    }
}
~~~


######ThreadLocal的内存泄漏问题
必须回收自定义的 ThreadLocal 变量，尤其在线程池场景下，线程经常会被复用，如果不清理自定义的 ThreadLocal 变量，可能会影响后续业务逻辑和造成`内存泄露`等问题。尽量在代理中使用 try-finally 块进行回收。
~~~
objectThreadLocal.set(userInfo);
try {
// ...
} finally {
objectThreadLocal.remove();
}
~~~

问题复现，设置-Xmx30M
~~~
        //先给大家看一段代码测试下：我们先设置了JVM堆内存的大小为30M。
        ThreadLocal<Object> threadLocal = new ThreadLocal<>();
        new Thread(() -> {
            System.out.println("线程A" + Runtime.getRuntime().freeMemory());
            threadLocal.set(new byte[1024 * 1024 * 10]);
            System.out.println("线程A"  + Runtime.getRuntime().freeMemory());
//            threadLocal.remove();
            try {
                Thread.sleep(5000);
                System.out.println("线程A" + Runtime.getRuntime().freeMemory());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();

        new Thread(() -> {
            try {
                Thread.sleep(2000);
                System.gc();
                System.out.println("线程B" +  Runtime.getRuntime().freeMemory());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("线程B" + Runtime.getRuntime().freeMemory());
            threadLocal.set(new byte[1024 * 1024 * 10]);
            System.out.println("线程B" + Runtime.getRuntime().freeMemory());
//            threadLocal.remove();
            try {
                Thread.sleep(5000);
                System.out.println("线程B" +  Runtime.getRuntime().freeMemory());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
线程A25078736
线程A14424816
线程B18773464
线程B18773464
Exception in thread "Thread-1" java.lang.OutOfMemoryError: Java heap space
	at com.company.MyArrayList.lambda$main$1(MyArray.java:39)
	at com.company.MyArrayList$$Lambda$2/1057941451.run(Unknown Source)
	at java.lang.Thread.run(Thread.java:745)
线程A18492816

~~~

>remove方法存在的意义在于：当ThreadLocal中存放的数据较大，为了节省该数据在ThreadLocalMap中占用的空间我们可以通过remove()提前释放而不是等到线程结束。


####怎么理解

1. 如果整个线程执行完任务马上回收，即非线程池模式，那么线程结束后整个 ThreadLocalMap 都会被回收，自然就不存在长久性的内存泄漏，只能说从 ThreadLocal 结束（最后一次get）到线程结束（销毁）之间存在内存泄漏


2. 如果是线程池模式，那么要分两种情况（以下线程均指核心线程，而非最大线程，最大线程同非线程池模式）

- 线程池内线程会继续使用 ThreadLocal
也就是会调用 set、get 等方法，在这些方法内部会有尝试性清除部分过期 Entry（注意**不是全部**的过期 Entry）的动作，是有机会将内存泄漏控制在一个可以接收的范围的。（set 涉及到了 rehash 操作时会有一次全局清理过期Entry）


- 创建 ThreadLocal 后不再使用，ThreadLocalMap 这块内存创建后就不再访问了，而线程一直存活导致的强引用无法回收，这就是真真切切地发生了内存泄漏。



###使用场景
1、跟踪一个请求，从接收请求，处理到返回的整个流程，Threadlocal 可以做到传递参数。这是ThreadLocal的一个功能，因为threadlocal 是局部变量，只要线程不销毁，就会一直存在，因此可以使用threadlocal来跟踪传递参数；

2、在hibernate的HibernateSessionFactroy（session工厂类）中就是使用Threadlocal 为每个线程都绑定一个session。使得各个线程对session的操作互不影响
>mybatis的sqlSession也有这样的实现
~~~
private static final ThreadLocal<Session> threadLocal = new ThreadLocal<Session>();
public static Session currentSession() throws HibernateException {
        Session session = (Session) threadLocal.get();
        if (session == null) {
            if (sessionFactory == null) {
                try {
                    cfg.configure(CONFIG_FILE_LOCATION);
                    sessionFactory = cfg.buildSessionFactory();
                }
                catch (Exception e) {
          
                    e.printStackTrace();
                }
            }
            session = sessionFactory.openSession();
            threadLocal.set(session);
        }
        return session;
    }
~~~


###最佳实践
线程的生命周期很长，如果我们往ThreadLocal里面set了很大很大的Object对象，虽然set、get等等方法在特定的条件会调用进行额外的清理，但是ThreadLocal被垃圾回收后，在ThreadLocalMap里对应的Entry的键值会变成null，但是后续在也没有操作set、get等方法了。

1、所以最佳实践，应该在我们不使用的时候，主动调用remove方法进行清理。
~~~
private static ThreadLocal<Integer> threadLocal = new ThreadLocal<>();
~~~
2、设置为static
这里把ThreadLocal定义为static还有一个好处就是，由于ThreadLocal有强引用在，那么在ThreadLocalMap里对应的Entry的键会永远存在，那么执行remove的时候就可以正确进行定位到并且删除！！！

3、最佳实践做法应该为： 在finally里面 调用 remove();
~~~
new Thread(() -> {
    try {
        for (int i = 0; i < 100; i++) {
            threadLocal.set(i);
            System.out.println(Thread.currentThread().getName() + "====" + threadLocal.get());
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    } finally {
        threadLocal.remove();
    }
}, "threadLocal1").start();


new Thread(() -> {
    try {
        for (int i = 0; i < 100; i++) {
            System.out.println(Thread.currentThread().getName() + "====" + threadLocal.get());
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    } finally {
        threadLocal.remove();
    }
}, "threadLocal2").start();
~~~
