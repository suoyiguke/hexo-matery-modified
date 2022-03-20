---
title: 自旋锁浪费cpu资源.md
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
title: 自旋锁浪费cpu资源.md
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
在并发编程中，自旋锁想必大家都已经耳熟能详了。

自旋锁有个非常经典的使用场景就是：CAS（即比较和交换），它是一种无锁化思想（说白了用了一个死循环），用来解决高并发场景下，更新数据的问题。

而atomic包下的很多类，比如：AtomicInteger、AtomicLong、AtomicBoolean等，都是用CAS实现的。

我们以AtomicInteger类为例，它的incrementAndGet没有每次都给变量加1。
~~~
public final int incrementAndGet() {
    return unsafe.getAndAddInt(this, valueOffset, 1) + 1;
}
~~~
它的底层就是用的自旋锁实现的：
~~~
public final int getAndAddInt(Object var1, long var2, int var4) {
  int var5;
  do {
      var5 = this.getIntVolatile(var1, var2);
  } while(!this.compareAndSwapInt(var1, var2, var5, var5 + var4));

    return var5;
}
~~~
在do...while死循环中，不停进行数据的比较和交换，如果一直失败，则一直循环重试。

如果在高并发的情况下，compareAndSwapInt会很大概率失败，因此导致了此处cpu不断的自旋，这样会严重浪费cpu资源。

那么，如果解决这个问题呢？

答：使用LockSupport类的parkNanos方法。

具体代码如下：
~~~
private boolean compareAndSwapInt2(Object var1, long var2, int var4, int var5) {
     if(this.compareAndSwapInt(var1,var2,var4, var5)) {
          return true;
      } else {
          LockSupport.parkNanos(10);
          return false;
      }
 }
~~~
当cas失败之后，调用LockSupport类的parkNanos方法休眠一下，相当于调用了Thread.Sleep方法。这样能够有效的减少频繁自旋导致cpu资源过度浪费的问题。
