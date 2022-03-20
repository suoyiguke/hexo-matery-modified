---
title: CompletableFuture-实践---泡茶任务.md
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
title: CompletableFuture-实践---泡茶任务.md
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
###1、泡茶任务
step1、烧水
2、洗杯子->拿茶叶
3、泡茶

~~~
package com.company;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
public class Main {

    public static void main(String[] args) {
        System.out.println(0 + Thread.currentThread().getName() + "开始");
        CompletableFuture completableFuture1 = CompletableFuture.runAsync(() -> {
            System.out.println(1+Thread.currentThread().getName()+"烧水开始");
            try {
                TimeUnit.SECONDS.sleep(5);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println(1+Thread.currentThread().getName()+"烧水结束");
        });

        CompletableFuture<Void> completableFuture2 = CompletableFuture.runAsync(() -> {
            System.out.println(2 + Thread.currentThread().getName() + "洗杯子开始");
            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println(2 + Thread.currentThread().getName() + "洗杯子结束");
        }).thenRun(() -> {
            //这里使用thenRun，拿茶叶就和洗杯子一个线程。
            //用thenRunAsync，拿茶叶会自己单独用个线程
            //二者都是then。表示拿茶叶一定是在洗杯子后执行（串行）
            System.out.println(3 + Thread.currentThread().getName() + "拿茶叶开始");
            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println(3 + Thread.currentThread().getName() + "拿茶叶结束");
        });


        //runAfterBothAsync 表示洗杯子、拿茶叶任务 和烧水任务 都完成了。就去泡茶
        CompletableFuture over = completableFuture1.runAfterBoth(completableFuture2, (Runnable) () -> {
            System.out.println(4 + Thread.currentThread().getName() + "泡茶");
        });
        Object o = null;
        try {
            o = over.get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }

        System.out.println(4 + Thread.currentThread().getName() + "结束");

    }
}

~~~

0main开始
1ForkJoinPool.commonPool-worker-1烧水开始
2ForkJoinPool.commonPool-worker-2洗杯子开始
2ForkJoinPool.commonPool-worker-2洗杯子结束
3ForkJoinPool.commonPool-worker-2拿茶叶开始
3ForkJoinPool.commonPool-worker-2拿茶叶结束
1ForkJoinPool.commonPool-worker-1烧水结束
4ForkJoinPool.commonPool-worker-1泡茶
4main结束

###2、获取子线程返回结果的
~~~
// 开个线程池，取任务执行
ExecutorService executor = new ThreadPoolExecutor(
  8, 100, 5,
  TimeUnit.MINUTES,
  new ArrayBlockingQueue<>(10000)
);
// 任务列表
List<CompletableFuture<Asset>> fList = new ArrayList<>();
for (int id : assetIds) {
  // 创建任务
  CompletableFuture<Asset> f = CompletableFuture.supplyAsync(
    () -> {
      Asset asset = getDetail();
      asset.xx = getXX();
      asset.yy = getYY();
      asset.zz = getZZ();
     return asset;
   },
    executor
  );
  fList.add(f);
}
// 阻塞，等待所有任务执行完成
List<Asset> CompletableFuture
  .allOf(fList.toArray(new CompletableFuture[0]))
  .get();
~~~




###3、 并行流 配合CompletableFuture和线程池的使用

~~~
public static void main(String[] args)  throws Exception{
    List<Integer> demo = Stream.iterate(0, item -> item + 1)
            .limit(5)
            .collect(Collectors.toList());
    //示例1
    Stopwatch stopwatch = Stopwatch.createStarted(Ticker.systemTicker());
    demo.stream().forEach(item -> {
        try {
            Thread.sleep(500);
            System.out.println("示例1-"+Thread.currentThread().getName());
        } catch (Exception e) { }
    });
    System.out.println("示例1-"+stopwatch.stop().elapsed(TimeUnit.MILLISECONDS));
 
    //示例2, 注意需要ForkJoinPool，parallelStream才会使用executor指定的线程，否则还是用默认的 ForkJoinPool.commonPool()
    ExecutorService executor = new ForkJoinPool(10);
    stopwatch.reset(); stopwatch.start();
    CompletableFuture.runAsync(() -> demo.parallelStream().forEach(item -> {
        try {
            Thread.sleep(1000);
            System.out.println("示例2-" + Thread.currentThread().getName());
        } catch (Exception e) { }
    }), executor).join();
    System.out.println("示例2-"+stopwatch.stop().elapsed(TimeUnit.MILLISECONDS));
    //示例３
    stopwatch.reset(); stopwatch.start();
    demo.parallelStream().forEach(item -> {
        try {
            Thread.sleep(1000);
            System.out.println("示例3-"+Thread.currentThread().getName());
        } catch (Exception e) { }
    });
    System.out.println("示例3-"+stopwatch.stop().elapsed(TimeUnit.MILLISECONDS));
    executor.shutdown();
}
~~~
