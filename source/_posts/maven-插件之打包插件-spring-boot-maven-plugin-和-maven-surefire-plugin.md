---
title: maven-插件之打包插件-spring-boot-maven-plugin-和-maven-surefire-plugin.md
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
title: maven-插件之打包插件-spring-boot-maven-plugin-和-maven-surefire-plugin.md
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
>万丈高楼平地起

spring-boot-maven-plugin这个插件是针对springboot项目运行打包用的，公司项目有用到这些maven插件。于是自己来试下能不能使用这种方式部署。

添加spring-boot-maven-plugin 插件
~~~
          <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <fork>true</fork>
                </configuration>
            </plugin>
~~~

然后看看idea的maven控制面板，多了一个spring-boot的插件选项
![image.png](https://upload-images.jianshu.io/upload_images/13965490-20817431352ffd04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点开看看，包含了6个操作
![image.png](https://upload-images.jianshu.io/upload_images/13965490-65eeaf8ea96e7583.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


使用help操作，有具体的用法提示如下


>spring-boot:build-info
  Generate a build-info.properties file based the content of the 
  current
  MavenProject.

>spring-boot:help
  Display help information on spring-boot-maven-plugin.
  Call mvn spring-boot:help -Ddetail=true -Dgoal=<goal-name> to display
  parameter details.

>spring-boot:repackage
  Repackages existing JAR and WAR archives so that they can be executed from the
  command line using java -jar. With layout=NONE can also be used simply to
  package a JAR with nested dependencies (and no main class, so not executable).

>spring-boot:run
  Run an executable archive application.

>spring-boot:start
  Start a spring application. Contrary to the run goal, this does not block and
  allows other goal to operate on the application. This goal is typically used
  in integration test scenario where the application is started before a test
  suite and stopped after.

>spring-boot:stop
  Stop a spring application that has been started by the 'start' goal. Typically
  invoked once a test suite has completed.


run 和 start、stop  就是运行和停止项目咯，但是一般不会使用这种方式来运行和停止啊。
最多用上spring-boot:repackage命令来打包项目了，使用一下看看。结果报这个错。。
>Failed to execute goal org.springframework.boot:spring-boot-maven-plugin:2.2.4.RELEASE:repackage (default-cli) on project demo1: Execution default-cli of goal org.springframework.boot:spring-boot-maven-plugin:2.2.4.RELEASE:repackage failed: Source file must be provided

这个插件对入口类有一定要求，不想做过多的配置（就是懒）此处不留爷，自有留爷处。换个插件走起。使用maven自带的 maven-surefire-plugin岂不美哉？
![image.png](https://upload-images.jianshu.io/upload_images/13965490-348d8f11a44c0040.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>- 虽然说不使用spring-boot-maven-plugin了，但是还是要将这个插件的依赖加上，不然打出来的jar包没有包含maven依赖。
>- maven-compiler-plugin这个插件 配置了java的开发环境和运行环境。还有文件编码
>- maven-surefire-plugin 要注意需要跳过单元测试，如果工程里存在对数据库进行操作的单元测试必须要使用以下配置将之跳过！
~~~
           <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.2</version>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>

           <!--不加上这个springboot打出来的jar包将不包含依赖-->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
            <!-- 跳过单元测试 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <configuration>
                    <skipTests>true</skipTests>
                </configuration>
            </plugin>

~~~
运行完毕，查看taget输出目录，已经有jar包了

![image.png](https://upload-images.jianshu.io/upload_images/13965490-755e2a8225808f4f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


打开jar包，里面的依赖确认是完整的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f4827e93e8bb9473.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用 java -jar demo1-0.0.1-SNAPSHOT.jar 执行下看看
![image.png](https://upload-images.jianshu.io/upload_images/13965490-74d0af923a638f8e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

没问题~
