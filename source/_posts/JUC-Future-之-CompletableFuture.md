---
title: JUC-Future-之-CompletableFuture.md
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
title: JUC-Future-之-CompletableFuture.md
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
https://segmentfault.com/a/1190000014479792

想用好这个类不简单啊！

>CompletableFuture是1.8新特性，它充分利用了函数式编程
静态
CompletableFuture.supplyAsync();
CompletableFuture.anyOf();
CompletableFuture.allOf();
CompletableFuture.completedFuture();
CompletableFuture.runAsync();
实例


注意CompletableFuture的命名规则：
xxx()：表示该方法将继续在已有的线程中执行；
xxxAsync()：表示将异步在线程池中执行。


1、supplyAsync / runAsync
     supplyAsync表示创建带返回值的异步任务的，相当于ExecutorService submit(Callable<T> task) 方法，runAsync表示创建无返回值的异步任务，相当于ExecutorService submit(Runnable task)方法，这两方法的效果跟submit是一样的。这两方法各有一个重载版本，可以指定执行异步任务的Executor实现，如果不指定，默认使用ForkJoinPool.commonPool()，如果机器是单核的，则默认使用ThreadPerTaskExecutor，该类是一个内部类，每次执行execute都会创建一个新线程。



###小结
CompletableFuture可以指定异步处理流程：
thenAccept()处理正常结果；
exceptional()处理异常结果；
thenApplyAsync()用于串行化另一个CompletableFuture；
anyOf()和allOf()用于并行化多个CompletableFuture。



###Future 的局限性

1、不能手动完成（执行失败直接返回默认值）
当你写了一个函数，用于通过一个远程API获取一个电子商务产品最新价格。因为这个 API 太耗时，你把它允许在一个独立的线程中，并且从你的函数中返回一个 Future。现在假设这个API服务宕机了，这时你想通过该产品的最新缓存价格手工完成这个Future 。你会发现无法这样做。
greetingFuture.getNow 实现

2、实现类似ajax的结果回调
Future 不会通知你它已经完成了，它提供了一个阻塞的 get() 方法通知你结果。你无法给 Future 植入一个回调函数，当 Future 结果可用的时候，用该回调函数自动的调用 Future 的结果。
可以使用 thenApply(), thenAccept() 和thenRun()方法附上一个回调给CompletableFuture。
~~~
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
public class TenTask {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        CompletableFuture<String> whatsYourNameFuture = CompletableFuture.supplyAsync(() -> {
            try {
                System.out.println("线程池线程" + Thread.currentThread().getName());
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                throw new IllegalStateException(e);
            }
            //模拟异步执行3秒的网络请求
            try {
                TimeUnit.SECONDS.sleep(3);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return "网络请求结果";
        });
        final String[] zz = new String[1];
        /**
         * 回调
         */
        CompletableFuture<String> greetingFuture = whatsYourNameFuture.thenApply(name -> {
            System.out.println("回调线程" + Thread.currentThread().getName());
            zz[0] =  name;
            return name;
        });
        //模拟主线程去做别的事情,1秒
        try {
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println(greetingFuture.getNow("默认值"));
        System.out.println(greetingFuture.get());
    }
}
~~~

3、你有10个不同的Future，你想并行的运行，然后在它们运行未完成后运行一些函数


4、多个CompletableFuture可以串行/并行执行，而Future做不到

除了anyOf()可以实现“任意个CompletableFuture只要一个成功”
allOf()可以实现“所有CompletableFuture都必须成功”，这些组合操作可以实现非常复杂的异步流程控制。

- 多个任串型执行
~~~
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
public class TenTask {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        CompletableFuture<String> whatsYourNameFuture = CompletableFuture.supplyAsync(() -> {
            try {
                System.out.println("线程池线程" + Thread.currentThread().getName());
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                throw new IllegalStateException(e);
            }
            //模拟异步执行3秒的网络请求
            try {
                TimeUnit.SECONDS.sleep(3);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return "网络请求结果";
        });
        final String[] zz = new String[1];
        /**
         * 回调
         */
        CompletableFuture<String> greetingFuture = whatsYourNameFuture.thenApply(name -> {
            System.out.println("回调线程" + Thread.currentThread().getName());
            zz[0] =  name;
            return name;
        });
        //模拟主线程去做别的事情,1秒
        try {
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println(greetingFuture.getNow("默认值"));
        System.out.println(greetingFuture.get());
    }
}
~~~

- 多个任务并行执行，而Future做不到
~~~
import java.util.concurrent.CompletableFuture;
public class Main {
    public static void main(String[] args) throws Exception {
        // 两个CompletableFuture执行异步查询:
        CompletableFuture<String> cfQueryFromSina = CompletableFuture.supplyAsync(() -> {
            System.out.println("异步1" + Thread.currentThread().getName());
            return queryCode("中国石油", "https://finance.sina.com.cn/code/");
        });
        CompletableFuture<String> cfQueryFrom163 = CompletableFuture.supplyAsync(() -> {
            System.out.println("异步2" + Thread.currentThread().getName());

            return queryCode("中国石油", "https://money.163.com/code/");
        });

        // 用anyOf合并为一个新的CompletableFuture;anyOf会去并行执行两个任务
        CompletableFuture<Object> cfQuery = CompletableFuture
            .anyOf(cfQueryFromSina, cfQueryFrom163);

        // 两个CompletableFuture执行异步查询:
        CompletableFuture<Double> cfFetchFromSina = cfQuery.thenApplyAsync((code) -> {
            System.out.println("异步3" + Thread.currentThread().getName());

            return fetchPrice((String) code, "https://finance.sina.com.cn/price/");
        });
        CompletableFuture<Double> cfFetchFrom163 = cfQuery.thenApplyAsync((code) -> {
            System.out.println("异步4" + Thread.currentThread().getName());

            return fetchPrice((String) code, "https://money.163.com/price/");
        });

        // 用anyOf合并为一个新的CompletableFuture:
        CompletableFuture<Object> cfFetch = CompletableFuture
            .anyOf(cfFetchFromSina, cfFetchFrom163);

        // 最终结果:
        cfFetch.thenAccept((result) -> {
            System.out.println("price: " + result);
        });
        // 主线程不要立刻结束，否则CompletableFuture默认使用的线程池会立刻关闭:
        Thread.sleep(200);
    }

    static String queryCode(String name, String url) {
        System.out.println("query code from " + url + "...");
        try {
            Thread.sleep((long) (Math.random() * 100));
        } catch (InterruptedException e) {
        }
        return "601857";
    }

    static Double fetchPrice(String code, String url) {
        System.out.println("query price from " + url + "...");
        try {
            Thread.sleep((long) (Math.random() * 100));
        } catch (InterruptedException e) {
        }
        return 5 + Math.random() * 20;
    }
}
~~~

4、有时候你需要执行一个长时间运行的计算任务，并且当计算任务完成的时候，你需要把它的计算结果发送给另外一个长时间运行的计算任务等等。你会发现你无法使用 Future 创建这样的一个工作流。






6、没有异常处理，下面用CompletableFuture看看它如何支持异常处理的；
使用CompletableFuture.exceptionally
~~~
    public static void main(String[] args) throws Exception {
        // 创建异步执行任务:
        CompletableFuture<Double> cf = CompletableFuture.supplyAsync(TenTask::fetchPrice);
        // 如果执行成功:
        cf.thenAccept((result) -> {
            System.out.println("price: " + result);
        });
        // 如果执行异常:
        cf.exceptionally((e) -> {
            e.printStackTrace();
            return null;
        });
        // 主线程不要立刻结束，否则CompletableFuture默认使用的线程池会立刻关闭:
        Thread.sleep(200);

    }
    static Double fetchPrice() {
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
        }
        if (Math.random() < 0.3) {
            throw new RuntimeException("fetch price failed!");
        }
        return 5 + Math.random() * 20;
    }

~~~




