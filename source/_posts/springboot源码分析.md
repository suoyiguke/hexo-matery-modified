---
title: springboot源码分析.md
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
title: springboot源码分析.md
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
默认允许的最大线程数 200
org.apache.tomcat.util.net.AbstractEndpoint

~~~
  /**
     * Maximum amount of worker threads.
     */
    private int maxThreads = 200;
    public void setMaxThreads(int maxThreads) {
        this.maxThreads = maxThreads;
        Executor executor = this.executor;
        if (internalExecutor && executor instanceof java.util.concurrent.ThreadPoolExecutor) {
            // The internal executor should always be an instance of
            // j.u.c.ThreadPoolExecutor but it may be null if the endpoint is
            // not running.
            // This check also avoids various threading issues.
            ((java.util.concurrent.ThreadPoolExecutor) executor).setMaximumPoolSize(maxThreads);
        }
    }
~~~

默认最大连接数 10000
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d1e1de776562706e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
