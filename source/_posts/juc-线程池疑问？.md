---
title: juc-线程池疑问？.md
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
title: juc-线程池疑问？.md
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
>这种初始化的线程池，我一开始认为根本不会有线程在工作。实际运行起来真的是有的。不知道为什么！！！
>     ThreadPoolExecutor cancellator = new ThreadPoolExecutor(0, 1, 1000, TimeUnit.MILLISECONDS,
            linkedBlockingQueue);

~~~
     LinkedBlockingQueue<Runnable> runnables = new LinkedBlockingQueue<>();
        System.out.println(runnables.size());
        ThreadPoolExecutor cancellator = new ThreadPoolExecutor(0, 1, 1000, TimeUnit.MILLISECONDS,
            runnables);

        ArrayList<FutureTask> objects = new ArrayList<>(100);
        for (int i = 0; i < 100; i++) {
            FutureTask<Integer> futureTask = new FutureTask<>(new Callable<Integer>() {
                @Override
                public Integer call() throws Exception {
                    Integer n = 0;
                    for (int i = 0; i < 10000; i++) {
                        i++;
                        n = n + i;
                    }
                    Thread.sleep(100000);
                    return n;
                }

            });
            cancellator.submit(futureTask);
            objects.add(futureTask);
        }

        for (FutureTask futureTask : objects) {
//            Object o = null;
//            try {
//                o = futureTask.get();
//            } catch (InterruptedException e) {
//                e.printStackTrace();
//            } catch (ExecutionException e) {
//                e.printStackTrace();
//            }
//            System.out.println(o);

            System.out.println(runnables.size());
            System.out.println(runnables.remainingCapacity());


        }
~~~
