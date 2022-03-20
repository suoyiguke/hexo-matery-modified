---
title: springboot-配置静态资源映射.md
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
title: springboot-配置静态资源映射.md
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
######配置web页面资源的映射
实现在springboot工程中访问静态的html页面；前端工程化，使用npm run build 打包生成的静态文件(html+js+css)直接拖到springboot工程下可实现部署

编辑 application.yml
~~~
spring:
    resources: # 指定静态资源的路径
        static-locations: classpath:/static/
~~~
上面配置的classpath:/static/ 路径就是指这里
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e5e71dd5dc214bcb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

编辑test.html示例页面
~~~
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
hello world

</body>
</html>
~~~

重启工程，访问 http://localhost:8080/test/test.html
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2c046bcfbcb59190.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######映射到磁盘的绝对路径
我在E:\test里放了张图片，想通过http来访问
![image.png](https://upload-images.jianshu.io/upload_images/13965490-65595480651c5134.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


编辑配置文件
- imagePath为磁盘路径
- httpImagePath 为访问的url的前缀
~~~
image:
  imagePath: file:E:/test/
  httpImagePath: /image/**
~~~
需要写一个配置类了，实现WebMvcConfigurer 接口，重写ImageWebAppConfig 方法
~~~
package com.springboot.study.demo1.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class ImageWebAppConfig implements WebMvcConfigurer {

    @Value("${image.imagePath}")
    private String imagePath;

    @Value("${image.httpImagePath}")
    private String httpImagePath;

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler(httpImagePath).addResourceLocations(imagePath);
    }
}

~~~

重启工程，访问http://localhost:8080/test/image/z3f.jpg

![image.png](https://upload-images.jianshu.io/upload_images/13965490-db004f0a856a391f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

成功
