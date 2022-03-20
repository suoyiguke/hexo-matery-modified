---
title: JUC-假设现在有10个任务，要求同时处理，并且必须所有任务全部完成才返回结果.md
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
title: JUC-假设现在有10个任务，要求同时处理，并且必须所有任务全部完成才返回结果.md
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
方法1、executorService.submit+Callable+FutureTask实现
FutureTask.get()实现主线程阻塞
~~~
import java.util.ArrayList;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ThreadPoolExecutor;

public class TenTask {

    public static void main(String[] args) throws ExecutionException, InterruptedException {

        ExecutorService executorService = Executors.newFixedThreadPool(10);
        ArrayList<Future> futures = new ArrayList<>(10);

        for (int i = 0; i < 10; i++) {
            int finalI = i;
            Future<?> submit = executorService.submit(new Callable<Object>() {
                @Override
                public Object call() throws Exception {
                    System.out.println(String.format("TASK %s 执行", finalI));
                    return 100-finalI;
                }

            });
            futures.add(submit);

        }

        Integer number =0;
        for (Future future : futures) {
            number = number + (Integer) future.get();
        }

        System.out.println(number);
    }

}

~~~

方法2、executorService.execute+Runnable+CountDownLatch
countDownLatch.await() 实现主线程阻塞
~~~
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class TenTask {

    public static void main(String[] args) throws ExecutionException, InterruptedException {

        CountDownLatch countDownLatch = new CountDownLatch(10);
        ExecutorService executorService = Executors.newFixedThreadPool(10);
        AtomicInteger atomicInteger = new AtomicInteger(0);

        for (int i = 0; i < 10; i++) {
            int finalI = i;
            executorService.execute(new Runnable() {
                @Override
                public void run() {
                    System.out.println(String.format("TASK %s 执行", finalI));
                    atomicInteger.addAndGet((100 - finalI));
                    countDownLatch.countDown();
                }
            });
        }
        countDownLatch.await();
        System.out.println(atomicInteger);
    }


}


~~~

方法3、CompletableFuture + Supplier

completableFuture.get()实现阻塞

~~~
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Supplier;

public class Main {

    public static void main(String[] args) throws Exception {

        AtomicInteger atomicInteger = new AtomicInteger(0);
        List<Future> futureList = new ArrayList<>(10);

        for (int i = 0; i < 10; i++) {
            int finalI = i;
            CompletableFuture<Integer> f = CompletableFuture
                .supplyAsync(new Supplier<Integer>() {
                    @Override
                    public Integer get() {
                        System.out.println(String.format("TASK %s 执行", finalI));
                        return 100 - finalI;
                    }
                });
            futureList.add(f);
        }

        for (Future future : futureList) {
            atomicInteger.addAndGet((Integer) future.get());
        }
        System.out.println(atomicInteger);
    }

}
~~~
