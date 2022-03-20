---
title: springboot-定时调度.md
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
title: springboot-定时调度.md
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
当初使用ssm框架的时候集成定时调度需要配置很多xml。而SpringBoot为我们内置了Scheduled定时任务，使用非常方便。


找到springboot的启动类，添加@EnableScheduling注解如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b27377cb8ead6892.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



创建一个类，加上@Component注解申明这是一个需要被spring容器管理的bean；在任务方法上加上 @Scheduled(cron = "0/5 * * * * ? ") 里面的cron表达式可以到这个网站http://cron.qqe2.com/ 上得到，需要什么规则自己生成，copy进来即可。

我这里是每5秒打印一次
~~~
package com.springboot.study.demo1.scheduled;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;


@Component
public class Mytest {
    @Scheduled(cron = "0/5 * * * * ? ")
    public  void mytest(){
        System.out.println("hello Scheduled");
    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b6630d2b1bd41a8c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


若想要自定义这个定时任务的线程池，可以声明一个Bean，再加上 @Async 注解

~~~
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
        return executor;
    }
~~~



**配置文件中设置cron表达式**
在yml文件中配置cron表达式的值：
~~~
blog:
  sche:
    cron: 0 0/1 * * * ?  
~~~
在@Scheduled注解中引用：

@Scheduled(cron = "${blog.sche.cron}")
可以直接读取yml文件中的值，不需要配置config类
