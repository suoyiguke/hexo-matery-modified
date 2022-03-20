---
title: maven+jetty-热部署.md
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
title: maven+jetty-热部署.md
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
###idea maven jetty插件热部署
intellij 的maven tomcat插件进行热部署,请参考我另一篇博文intellij的maven项目设置热部署

jetty可以如下配置实现热部署
~~~
<!-- jetty插件 -->
<plugin>
  <groupId>org.mortbay.jetty</groupId>
  <artifactId>maven-jetty-plugin</artifactId>
  <version>6.1.5</version>
  <configuration>
    <scanIntervalSeconds>2</scanIntervalSeconds><!-- 多少秒进行一次热部署 -->
    <connectors>
      <connector implementation="org.mortbay.jetty.nio.SelectChannelConnector">
        <port>8099</port>
      </connector>
    </connectors>

    <contextPath>/lalalala</contextPath>
  </configuration>
</plugin>
~~~

但是idea无法进行自动编译，所以需要如下快捷键

Ctrl+Shift+F9，编译当前修改的java文件
Ctrl+F9，编译整个项目


注意要reload class一下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8f2c3d9d93fb6c7f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###idea maven jetty+jbral热部署
