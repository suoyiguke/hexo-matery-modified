---
title: java-多线程基础之synchronized的wait-notify机制.md
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
title: java-多线程基础之synchronized的wait-notify机制.md
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
###为什么要使用wait-notify？

为了避免处于blocked状态下的线程对监视器锁的竞争；
而竞争是会消耗计算机资源的




###正确使用wait-notify
- wait、notify/notifyAll方法一定要写在synchronized里面。wait、notify/notifyAll的作用是为了避免轮询带来的性能损失，而产生轮询的条件是多个线程对同一个资源进行操作。所以必须先获得监视器锁

- wait、notify/notifyAll方法定义在Object类里面。wait、notify/notifyAll必须写在synchronized里面，而synchronized的监视器锁可以是`任意对象`，所以wait、notify/notifyAll方法定义在`Object类`里面。

- 调用wait、notify/notifyAll方法的对象，必须和synchronized()的监视器锁一致

- wait()、notify/notifyAll() 方法是Object的本地final方法，无法被重写。

- `重要`在调用wait()的时候，线程自动释放其占有的监视器锁，同时不会去申锁（不会参与锁的竞争）。当线程被唤醒（notify）的时候，它才再次获得了去竞争监视器锁的权利。如果竞争到了锁，程序会从wait()方法处往下继续执行！
`当线程执行wait()方法时候，会立即释放当前的锁，然后让出CPU，进入等待状态。Runnbel==>waiting`

- `重要` 只有当 notify/notifyAll() 被执行时候，才会唤醒一个或多个正处于等待状态的线程，然后继续往下执行，直到执行完synchronized 代码块的代码或是中途遇到wait() ，再次释放锁。
notify/notifyAll() 的执行只是唤醒沉睡的线程，而不会立即释放锁，锁的释放要看代码块的具体执行情况(一般来说,退出临界区就是释放锁了)。所以在编程中，尽量在使用了notify/notifyAll() 后立即退出临界区，以唤醒其他线程 。

  `notify()只是允许调用了wait()方法的线程继续参与锁的竞争，而不会让它马上获得监视器锁，只是告诉它此时可以参与锁的竞争了（参与轮询）。同样，此时占有监视器锁的线程不会立即释放锁，必须等到同步代码块执行完毕才会释放。waiting==>blocked`

######wait
Object.wait方法将释放当前线程所持有的Object对象监视器锁，而不是当前线程释放所有持有的锁。因此在synchronized嵌套使用的时候就要注意并不是调用了某个Object的wait方法导致释放所有的锁

######notify和notifyAll的区别
notify `随机唤醒`在监视器对象上等待的单个线程，此时调用该方法的代码继续执行。
notifyAll 唤醒在监视器对象上等待的`所有线程`，此时调用该方法的代码继续执行。

######notify 和wait 的顺序不能错
如果A线程先执行notify方法，B线程后执行wait方法，那么B线程是无法被唤醒的。B线程会一直出于waiting状态。

可以看代码
~~~

    public static void main(String[] args) throws InterruptedException {

        new Thread(new Runnable() {
            @SneakyThrows
            @Override
            public void run() {

                synchronized (TestThread.class) {
                    System.out.println("A线程开始执行notify");
                    TestThread.class.notify();
                }
            }
        },"A").start();

        Thread.sleep(1000*1);

        new Thread(new Runnable() {
            @SneakyThrows
            @Override
            public void run() {
                synchronized (TestThread.class) {
                    System.out.println("B线程将一直等待下去....");
                    TestThread.class.wait();

                }
            }
        },"B").start();


    }
~~~



###使用wait、notify机制，线程状态的变化情况
~~~
class TestThread {

    private static Logger logger = Logger.getLogger(TestThread.class);

    private static Thread t6 = new Thread(new Runnable() {
        @Override
        public void run() {

            synchronized (TestThread.class) {
                System.out.println("t6: t6线程获得监视器锁进入临界区");
                System.out.println("t6: t6线程调用wait()方法释放监视器锁，进入等待队列");
                try {
                    TestThread.class.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("t6: t6线程被通知激活，从wait()方法后继续执行");
                System.out.println("t6: 打印t7此时状态"+t7.getName()+"==>"+t7.getState());

            }


        }
    }, "t6");

    private static Thread t7 =  new Thread(new Runnable() {
        @Override
        public void run() {
            synchronized (TestThread.class){
                System.out.println("t7: t7线程获得监视器锁进入临界区");
                System.out.println("t7: t7线程工作3秒");
                try {
                    Thread.sleep(1000*3);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("t7: t7线程工作完毕，通知t6线程可以参与锁的竞争了");
                System.out.println("t7: notify前打印"+t6.getName()+"==>"+t6.getState());
                TestThread.class.notify();
                System.out.println("t7: notify后打印"+t6.getName()+"==>"+t6.getState());
            }
            //死循环打印t6线程的状态
            while (true){
                logger.debug("t7: t7退出临界区后打印"+t6.getName()+"==>"+t6.getState());
            }


        }
    },"t7");



    public static void main(String[] args) throws InterruptedException {


        t6.start();
        //main线程睡眠1秒，确保t6线程先执行
        Thread.sleep(1000);
        t7.start();


    }
}
~~~
t6: t6线程获得监视器锁进入临界区
t6: t6线程调用wait()方法释放监视器锁，进入等待队列
t7: t7线程获得监视器锁进入临界区
t7: t7线程工作3秒
t7: t7线程工作完毕，通知t6线程可以参与锁的竞争了
t7: notify前打印t6==>WAITING
t7: notify后打印t6==>BLOCKED
t6: t6线程被通知激活，从wait()方法后继续执行
t6: 打印t7此时状态t7==>RUNNABLE
[DEBUG] 2020-02-11 14:16:42,966 method:test.TestThread$2.run(A.java:248)
t7: t7退出临界区后打印t6==>RUNNABLE
