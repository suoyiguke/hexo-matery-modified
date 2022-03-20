---
title: jmm-volatile关键字之64位写入的原子性（三）.md
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
title: jmm-volatile关键字之64位写入的原子性（三）.md
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
volatile这个关键字很不起眼，其使用场景和语义不像synchroni
zed、wait（）和notify（）那么明显。正因为其隐晦，volatile 关 键字可能是在多线程编程领域中被误解最多的一个。而关键字越隐 晦，背后隐含的含义往往越复杂、越深刻。接下来的几个小节将一步步由浅入深地从使用场景讨论到其底层的实现。
1.5.1 64位写入的原子性（Half Write） 举一个简单的例子，对于一个long型变量的赋值和取值操作而 言，在多线程场景下，线程A调用set（100），线程B调用get（），在某些场景下，返回值可能不是100。

这有点反直觉，如此简单的一个赋值和取值操作，在多线程下面 为什么会不对呢？这是因为JVM的规范并没有要求64位的long或者double的写入是原子的。在32位的机器上，一个64位变量的写入可能被拆 分成两个32位的写操作来执行。这样一来，读取的线程就可能读到 “一半的值”。解决办法也很简单，在long前面加上volatile关键字。
~~~
package com.company;


public class AccountingSync  {

    public long testLong = 0;


    public static void main(String[] args) {
        AccountingSync accountingSync = new AccountingSync();

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                accountingSync.testLong = 999999999999999999L;
            }
        }).start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(20);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.exit(10);
            }
        }).start();
        int i=0;
        while (true){
            System.out.println( accountingSync.testLong+"==>"+(++i));
        }


    }
}
~~~


###volatile只能保证64位long和double的写入原子性但是普通的i++不能保证
简单的说，修改volatile变量分为四步：
1）读取volatile变量到local
2）修改变量值
3）local值写回
4）插入内存屏障，即lock指令
让其他线程可见这样就很容易看出来，前三步都是不安全的，取值和写回之间，不能保证没有其他线程修改。原子性需要锁来保证。这也就是为什么，volatile只用来保证变量可见性，但不保证原子性。

