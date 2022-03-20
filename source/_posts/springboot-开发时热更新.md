---
title: springboot-开发时热更新.md
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
title: springboot-开发时热更新.md
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
springboot提供了spring-boot-devtools的依赖，可以做到修改java代码和springboot配置文件后工程立即自动重启，这样就避免了手动重启。非常方便

maven引入依赖
~~~
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-devtools</artifactId>
   <optional>true</optional>
</dependency>
~~~

添加一个maven插件
~~~
<plugin>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-maven-plugin</artifactId>
   <configuration>
      <fork>true</fork>
   </configuration>
</plugin>
~~~
配置idea
File->Settings->Compiler
勾上如图所示的选项
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3613bb3e71d3e1b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


使用ctrl + shift + alt + /快捷键，选择Registry

![image.png](https://upload-images.jianshu.io/upload_images/13965490-927661d6fdeecf92.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

勾上这个，点击close
![image.png](https://upload-images.jianshu.io/upload_images/13965490-acc57688e4bb4a0f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

编辑application.yml文件
~~~
devtools:
  livereload:
    enabled: true
    port: 9527
  restart:
    enabled: true
~~~
配置运行，点击 Edit Configurations
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b8a563884a3ee741.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
将下面的选择项选为 update classes and resources
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6554453768b6cbd3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



配置完成后启动工程，修改一处java代码后可见控制台：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b58361d765c93f89.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######因为devtools导致的异常
~~~
ScheduleJobEntity scheduleJob = (ScheduleJobEntity) context.getMergedJobDataMap()
      .get(ScheduleJobEntity.JOB_PARAM_KEY);
~~~
代码报错
~~~
java.lang.ClassCastException: io.renren.modules.job.entity.ScheduleJobEntity cannot be cast to io.renren.modules.job.entity.ScheduleJobEntity
~~~

解决： 使用instanceof 关键字判断类型
~~~
Object obj = context.getMergedJobDataMap().get(ScheduleJobEntity.JOB_PARAM_KEY);
ScheduleJobEntity scheduleJob;
if(obj instanceof ScheduleJobEntity) {
   scheduleJob = (ScheduleJobEntity) obj;
} else {
   scheduleJob = JSON.parseObject(JSON.toJSON(obj).toString(), ScheduleJobEntity.class);
}
~~~
