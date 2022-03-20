---
title: 两个jar包含相同类怎么解决？.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: maven
categories: maven
---
---
title: 两个jar包含相同类怎么解决？.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: maven
categories: maven
---
问题背景：我在工程中引入了smiley-http-proxy-servletjar包
~~~
    <dependency>
      <groupId>org.mitre.dsmiley.httpproxy</groupId>
      <artifactId>smiley-http-proxy-servlet</artifactId>
      <version>1.7</version>
    </dependency>
~~~

然后运行报错 java..NoSuchMethodError: org.apache.http.util.EntityUtils.consume(Lorg/apache/http/HttpEntity;)V

给我的第一感觉就是一个jar冲突的问题，引入了这个smiley-http-proxy-servlet依赖之后自动隐式引入了httpcore。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f0b381419218466e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


如下在idae中搜索类全限定名org.apache.http.util.EntityUtils。发现有两个jar中都包含了这个。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4f2c57971e105800.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
且二者的version.properties中版本不通。
httpcore-4.4.8.jar 是4.4.8版本；
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d2429c319d283106.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

GMServiceClient-1.0.jar 的httpcore版本是4.0；
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ebdd1c007ac66746.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

因为java运行时去找的版本是httpcore-4.0.jar，而EntityUtils.consume方法在4.0版本中不存在的。因此报错 java..NoSuchMethodError: org.apache.http.util.EntityUtils.consume(Lorg/apache/http/HttpEntity;)V

**解决方法**
方法1、将smiley-http-proxy-servlet依赖移动到GMServiceClient-1.0.jar依赖之前，这样的话运行时就会去找httpcore-4.4.8.jar 了

方法2、自己创建所有冲突的类





