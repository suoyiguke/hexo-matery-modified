---
title: java-线程基础之如何让cpu利用率达到100%？.md
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
title: java-线程基础之如何让cpu利用率达到100%？.md
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
电脑8核处理器,只需要开启8个或者8个以上的线程就可以让CPU的利用率达到百分百了。一个线程一个处理器
~~~

class zzz{
    static  CountDownLatch latch = new CountDownLatch(1);
    public static void main(String[] args) {

        for (int i = 0; i <Runtime.getRuntime().availableProcessors() ; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        latch.await();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    while (true){
                        System.out.println(Thread.currentThread().getName());
                    }
                }
            },"线程"+(i+1)).start();

        }

        latch.countDown();

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5a38fa0014ac9465.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
