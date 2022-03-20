---
title: javaweb-知识回顾之使用servlet（一）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
---
title: javaweb-知识回顾之使用servlet（一）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
> 学以致用

记得刚刚接触javaweb编程的时候最先学的是servlet。时间过的快呀~

记得大学时用servlet和 jsp来实现了一个购物商城，然后当了我的最后的毕业设计。虽然说工作中不会使用这么基础这么底层的东西，但是还是有必要回顾下servlet，而且偶尔怀念一下过去也不错呀。spriingmvc和struts2再厉害也只是servlet的封装而已。而且还有个目的就是等之后想使用servlet和tomcat来实现session会话共享和session复制，只是做一个实验的demo不需要使用别的web框架了


######来看如何在idea中创建servlet并使用tomcat运行项目

file==> new  project==>选择web application 并点击next
![image.png](https://upload-images.jianshu.io/upload_images/13965490-16eb299342a2cfd6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

设定工程名，点击finish
![image.png](https://upload-images.jianshu.io/upload_images/13965490-86d844f3d8894094.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在web目录下创建一个lib文件夹，用于存放jar包。使用servlet就必须加入servlet的依赖
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cf915e436c5f47cc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后配置项目 点击 file==> project structure
![image.png](https://upload-images.jianshu.io/upload_images/13965490-55797e226246cae4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
在弹出来的项目配置面板，选择libraries，点击加号，选择 java依赖
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2dc8c01aca599dc7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

选中lib文件夹，将依赖添加即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-330b2b708c948ac2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


创建一个com.servlet.HelloWorld类继承HttpServlet ，并重写doGet和doPost方法
~~~
package com.servlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
public class HelloWorld extends HttpServlet {

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)  {
        System.out.println("你发起了get请求");
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) {

        System.out.println("你发起了post请求");
    }

}

~~~



WEB-INFO 下编辑web.xml文件，配置servlet的映射
>- servlet-class指定servlet类的全限定名
>- servlet.servlet-name和 servlet-mapping.servlet-name 需要保持一致且成对出现
>- servlet-mapping.url-pattern 指定servler的访问url路径
~~~
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

    <servlet>
        <servlet-name>HelloWorld</servlet-name>
        <servlet-class>com.servlet.HelloWorld</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>HelloWorld</servlet-name>
        <url-pattern>/helloworld</url-pattern>
    </servlet-mapping>


</web-app>
~~~

最后配置下运行环境

点击 add configuration 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b85b0726fb1bc904.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

弹出一些运行时环境配置，选择tomcat，点击加号。选择local本地的tomcat
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d739bfb384e39112.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

进一步配置tomcat和指定部署工程，当然我这里已经存在tomcat8的版本了就不需要配了。点击 fix
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fa5432e32c657c6b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

再次弹出了项目配置面板，点击如下操作，选择web application:explded
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c688f18f2868eb9a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
 再弹出了一个选择modules的框，我们这里只有一个。无需选择点击ok即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9db9f9df495a264f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后弹出这个，不用管
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6d12fec365e3bdf0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击mdules版块查看两个路径配置是否正确！这个配置非常关键不能出错
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a417ff7f33a0c35e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

配置ok后点击完毕，可以修改下根访问url为/test
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fbfe9dbe227023d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

完了后点击ok

最后点击小瓢虫运行即可，然后访问之前编写的serlvet
http://localhost:8088/test/helloworld
