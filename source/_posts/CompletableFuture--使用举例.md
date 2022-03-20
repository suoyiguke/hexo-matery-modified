---
title: CompletableFuture--使用举例.md
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
title: CompletableFuture--使用举例.md
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
1、 exceptionally 相当于 catch
~~~
   public CompletableFuture<T> exceptionally(
        Function<Throwable, ? extends T> fn) {
        return uniExceptionallyStage(fn);
    }
~~~
~~~
    public static void main(String[] args) {
        CompletableFuture.runAsync(() -> {
            System.out.println("A begin" + Thread.currentThread().getName());
            try {
                TimeUnit.SECONDS.sleep(5);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("A end" + Thread.currentThread().getName());
            int i = 1 / 0;

        }).exceptionally(throwable -> {
            //会执行
            System.out.println(throwable);
            return null;
        }).runAfterBothAsync(CompletableFuture.runAsync(()
                        -> {
                    System.out.println("B begin" + Thread.currentThread().getName());
                    try {
                        TimeUnit.SECONDS.sleep(2);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    System.out.println("B end" + Thread.currentThread().getName());

                }),
                () -> {
                    System.out.println("C begin" + Thread.currentThread().getName());
                    try {
                        TimeUnit.SECONDS.sleep(1);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    System.out.println("C end" + Thread.currentThread().getName());

                }).exceptionally(throwable -> {
            //不会执行
            System.out.println(throwable);
            return null;
        });

        //这里需要将主线程sleep，不然程序就退出了
        try {
            Thread.sleep(100000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
~~~



2、runAfterBothAsync
this（CompletableFuture）和 CompletionStage（CompletableFuture）不同线程并发执行。都完毕后再异步执行 Runnable action
~~~
    public CompletableFuture<Void> runAfterBothAsync(CompletionStage<?> other,
                                                     Runnable action) {
        return biRunStage(asyncPool, other, action);
    }
~~~

~~~

    public static void main(String[] args) {
        CompletableFuture.runAsync(() -> {
                    System.out.println("A begin" + Thread.currentThread().getName());
                    try {
                        TimeUnit.SECONDS.sleep(5);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    System.out.println("A end" + Thread.currentThread().getName());

                })
                .runAfterBothAsync(CompletableFuture.runAsync(()
                                -> {
                            System.out.println("B begin" + Thread.currentThread().getName());
                            try {
                                TimeUnit.SECONDS.sleep(2);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                            System.out.println("B end" + Thread.currentThread().getName());

                        }),
                        () -> {
                            System.out.println("C begin" + Thread.currentThread().getName());
                            try {
                                TimeUnit.SECONDS.sleep(1);
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                            System.out.println("C end" + Thread.currentThread().getName());

                        });

//这里需要将主线程sleep，不然程序就退出了
        try {
            Thread.sleep(100000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
~~~

A beginForkJoinPool.commonPool-worker-1
B beginForkJoinPool.commonPool-worker-2
B endForkJoinPool.commonPool-worker-2
A endForkJoinPool.commonPool-worker-1
C beginForkJoinPool.commonPool-worker-1
C endForkJoinPool.commonPool-worker-1

2、runAfterBoth。当CompletionStage<?> other 的线程任务完毕，再去执行 Runnable action；
主线程不会阻塞
~~~
    public CompletableFuture<Void> runAfterBoth(CompletionStage<?> other,
                                                Runnable action) {
        return biRunStage(null, other, action);
    }

~~~

>runAfterBothAsync和runAfterBoth的区别在这个例子里没体现出来
