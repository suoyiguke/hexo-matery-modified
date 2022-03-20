---
title: Primary.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
---
title: @Primary.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
当系统中存在多个相同类型的bean声明时，我们想使用自己的。请使用注解  @Primary

~~~


    @Primary
    @Bean
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);        // 设置核心线程数
        executor.setMaxPoolSize(2);        // 设置最大线程数
        executor.setQueueCapacity(20);      // 设置队列容量
        executor.setKeepAliveSeconds(60);   // 设置线程活跃时间（秒）
        executor.setThreadNamePrefix("轮询访问中心端接口线程");  // 设置默认线程名称
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());// 设置拒绝策略
        executor.setWaitForTasksToCompleteOnShutdown(true); // 等待所有任务结束后再关闭线程池
        executor.setAllowCoreThreadTimeOut(true);
        return executor;
    }


    @Primary
    @Bean
    public ThreadPoolExecutor ExecutorService() {

        ThreadFactory threadFactory = new ThreadFactory() {
            AtomicInteger nextId = new AtomicInteger(1);

            @Override
            public Thread newThread(Runnable task) {
                return new Thread(null, task, "直接触发数据上报线程" + nextId.getAndIncrement(), 0);
            }
        };

        ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(
            0,
            3,
            30, TimeUnit.MINUTES,
            new LinkedBlockingQueue<>(10),
            threadFactory,
            new ThreadPoolExecutor.CallerRunsPolicy());

        return threadPoolExecutor;


    }
~~~
