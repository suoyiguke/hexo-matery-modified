---
title: tomcat-启动报错日志查看.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: tomcat
categories: tomcat
---
---
title: tomcat-启动报错日志查看.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: tomcat
categories: tomcat
---
控制台打印的信息，最后几句话。提示可以去看tomcat的log
~~~
Connected to server
[2020-08-04 11:19:10,680] Artifact h5demo:Web exploded: Artifact is being deployed, please wait...
04-Aug-2020 11:19:10.858 信息 [RMI TCP Connection(3)-127.0.0.1] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
04-Aug-2020 11:19:10.865 严重 [RMI TCP Connection(3)-127.0.0.1] org.apache.catalina.core.StandardContext.startInternal One or more listeners failed to start. Full details will be found in the appropriate container log file
04-Aug-2020 11:19:10.866 严重 [RMI TCP Connection(3)-127.0.0.1] org.apache.catalina.core.StandardContext.startInternal Context [/h5demo_Web_exploded] startup failed due to previous errors
[2020-08-04 11:19:10,881] Artifact h5demo:Web exploded: Error during artifact deployment. See server log for details.
~~~

项目启动不了，又没有详细的报错信息，可以到tomcat下查看报错信息。比如说web.xml中引用的类不存在的问题：

我本机tomcat的logs 路径是 E:\tomcat\tomcat8.0.52\logs

查看的log
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f5b872b0406db492.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
04-Aug-2020 11:19:10.860 严重 [RMI TCP Connection(3)-127.0.0.1] org.apache.catalina.core.StandardContext.listenerStart Error configuring application listener of class org.springframework.web.util.IntrospectorCleanupListener
 java.lang.ClassNotFoundException: org.springframework.web.util.IntrospectorCleanupListener
	at org.apache.catalina.loader.WebappClassLoaderBase.loadClass(WebappClassLoaderBase.java:1352)
	at org.apache.catalina.loader.WebappClassLoaderBase.loadClass(WebappClassLoaderBase.java:1180)
	at org.apache.catalina.core.DefaultInstanceManager.loadClass(DefaultInstanceManager.java:542)
	at org.apache.catalina.core.DefaultInstanceManager.loadClassMaybePrivileged(DefaultInstanceManager.java:523)
	at org.apache.catalina.core.DefaultInstanceManager.newInstance(DefaultInstanceManager.java:150)
	at org.apache.catalina.core.StandardContext.listenerStart(StandardContext.java:4822)
	at org.apache.catalina.core.StandardContext.startInternal(StandardContext.java:5363)
	at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:145)
	at org.apache.catalina.core.ContainerBase.addChildInternal(ContainerBase.java:755)
	at org.apache.catalina.core.ContainerBase.addChild(ContainerBase.java:731)
	at org.apache.catalina.core.StandardHost.addChild(StandardHost.java:717)
	at org.apache.catalina.startup.HostConfig.manageApp(HostConfig.java:1730)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:483)
	at org.apache.tomcat.util.modeler.BaseModelMBean.invoke(BaseModelMBean.java:300)
	at 

~~~

没找到org.springframework.web.util.IntrospectorCleanupListener这个类。确定是没有将maven中引用的jar包打包到输出目录！


所以需要在项目配置中将jar包先put into到工程下

![image.png](https://upload-images.jianshu.io/upload_images/13965490-53debbe6d7bb667a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

重启即可
