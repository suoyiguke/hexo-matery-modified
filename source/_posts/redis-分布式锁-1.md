---
title: redis-分布式锁-1.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
---
title: redis-分布式锁-1.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
 SETNX key value

第一次执行 SETNX  key=name value=yinkai
第二次执行 SETNX key=name value =yinkai666

第一次执行完成的话，第二次执行不会成功！

SETNX   对应代码

Boolean b =  setIfAbsent("key","value");




###策略1
1、setIfAbsent返回false直接返回系统繁忙，请稍后再试


###问题
1、释放锁
加锁之后必须释放锁，不然这个商品后面线程进来直接false
delete(lockkey)

2、锁住的临界区要是包异常了怎么办？
使用 try{}finally{} ，在finally中释放锁


try{
setIfAbsent("key","value");

}finally{
delete(lockkey)
}

3、如果运维在停止进程时，代码刚好执行到临界区。那么finally的释放锁操作就不会执行了。
这个时候商品又一直买不了了

设置一个超时时间，超时了的锁会被redis清理
Boolean b =  setIfAbsent("key","value");
expire(lockkey,10,TimeUtil.SECONDS)


4、当执行完setIfAbsent后，正准备执行设置超时时间exprire时，要是应用宕机了。又没有解锁，商品又卖不出去了。

解决：把两行代码写成一句。保证原子性，redis底层会把这两条命令一起执行！
setIfAbsent(lockKey,"yinkai",10,TimeUnit.SECONDS)

>这样写在低并发软件公司下还行，高并发下就会有问题


5、第一个线程超时时间过了，临界区业务还没走完。那第二个线程马上拿到了这把锁
； 此时第一个线程执行释放锁，把第二个线程的锁给释放了。
依次类推，第二线程又会把第三个线程锁给释放。
 样接下来的业务就锁不住了。超卖！

>刚刚加的锁可能被其它线程提前释放，一直循环下去锁会永久失效！


解决：
1、使用UUID给线程加一个唯一标识， 把uuid存入redis的value，
setIfAbsent(lockKey,clientId,10,TimeUnit.SECONDS)

 2、在finally里加上一个条件判断；保证当前线程只能释放属于自己的锁

finally{
 if(clientId,equest(redisTemplate.opsForValue().get(lockKey))){
   delete(lockkey)
  }
}



6，10秒锁超时时间过了，临界区业务还没走完，那么这个时候会有线程安全问题！那到底如何设置合适的超时时间？

思路：使用子线程去定时轮询爬判断锁是否还持有，若持有则重置超时时间（给锁续命）

>轮询循环时间间隔建议设置为 超时时间的三分之一 1/3



###使用redission
1、redis主从同步过程中，redis主节点挂了，redis从节点变成主节点。那么新的主节点还没有这个lock key；还没来得及同步过去。这种情况要怎么解决？



2、高并发额分布式锁如何实现？
把库存
分段锁机制


