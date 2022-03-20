---
title: 分析通过wait挂起线程.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: 分析通过wait挂起线程.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
实例2：

```
static class Task implements Runnable {   
 @Override    
public void run() {       
 synchronized (lock) {            
    try {                
      lock.wait();                
     //TimeUnit.SECONDS.sleep(100000);           
     } catch (InterruptedException e) {                
     e.printStackTrace();           
   }       
 }    
}}
```

dump结果

![image](https://upload-images.jianshu.io/upload_images/13965490-df9526920ac4ea62?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

线程1和2都处于WAITING状态
1、线程1和2都是先`locked <0x000000076bf62500>`，再`waiting on <0x000000076bf62500>`，之所以先锁再等同一个对象，是因为wait方法需要先通过synchronized获得该地址对象的monitor；
2、`waiting on <0x000000076bf62500>`说明线程执行了wait方法之后，释放了monitor，进入到"Wait Set"队列，等待其它线程执行地址为0x000000076bf62500对象的notify方法，并唤醒自己，具体实现可以参考[深入分析Object.wait/notify实现机制](http://www.jianshu.com/p/f4454164c017)；
