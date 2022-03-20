---
title: java-具有定任务功能的线程池-ThreadPoolTaskScheduler.md
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
title: java-具有定任务功能的线程池-ThreadPoolTaskScheduler.md
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
使用声明bean的方式配置一个 ThreadPoolTaskScheduler。这种方式有一个问题就是会代替 springboot的  @Scheduled 使用线程池。 @Scheduled使用的线程池应该是类似于@Autowired按类型注入。
~~~
 @Autowired
    private ThreadPoolTaskScheduler threadPoolTaskScheduler;

    @Autowired
    private DataDao dataDao;

    @Bean
    public ThreadPoolTaskScheduler threadPoolTaskScheduler() {
        ThreadPoolTaskScheduler threadPoolTaskScheduler = new ThreadPoolTaskScheduler();
        threadPoolTaskScheduler.setPoolSize(8);

        ThreadFactory threadFactory = new ThreadFactory() {
            AtomicInteger nextId = new AtomicInteger(1);

            @Override
            public Thread newThread(Runnable task) {
                return new Thread(null, task, "定时数据上报线程" + nextId.getAndIncrement(), 0);
            }
        };
        threadPoolTaskScheduler.setThreadFactory(threadFactory);
        return threadPoolTaskScheduler;
    }
~~~



使用

~~~
    /**
     * 开始新任务
     */
    @RequestMapping("/start")
    @ResponseBody
    public String start(@RequestParam(name = "tableName", required = true) String tableName,
        @RequestParam(name = "sDate", required = true) @DateTimeFormat(pattern = DateUtils.DateFormat) Date sDate,
        @RequestParam(name = "eDate", required = true) @DateTimeFormat(pattern = DateUtils.DateFormat) Date eDate,
        @RequestParam(name = "cronStr", required = true) String cronStr) {
        ScheduledFuture<?> schedule = threadPoolTaskScheduler
            .schedule(new JobClass(dataSendMain, tableName, sDate, eDate), new Trigger() {
                @Override
                public Date nextExecutionTime(TriggerContext triggerContext) {
                    return new CronTrigger(cronStr).nextExecutionTime(triggerContext);
                }
            });

        /**
         * 使用表名做key
         */
        futureMap.put(tableName, schedule);

        return "start cron";

    }
~~~



ThreadPoolTaskScheduler


