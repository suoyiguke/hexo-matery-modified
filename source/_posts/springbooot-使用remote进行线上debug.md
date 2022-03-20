---
title: springbooot-使用remote进行线上debug.md
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
title: springbooot-使用remote进行线上debug.md
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
>沧海横流，方显英雄本色

只需要使用以下命令运行springboot工程的jar包

>java -jar -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005  springboot.jar

然后在idea里配置下remote即可，如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d7148055e3753b1c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在使用上面的命令启动工程后，点击debug选项即可。这样对线上的debug就像在自己机器下一样
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c4014e2969c81b32.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######使用docker-compose以jdk为基础环境如何进行Xdebug？

来看看这个docker-compose.yml文件，这种方式是将工程打成jar包，然后放到指定的jdk环境下运行docker-compose
>- ports端口开放了 8080 和 5005；8080是工程的端口，5005是remote调试的端口
>- command 命令即是上面的调试命令
~~~
version: "3"
services:
  jdk:
    image: java:8
    volumes:
      - ./work:/work
    ports:
      - "8080:8080"
      - "5005:5005"
    command: java -jar -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 /work/demo1-4.jar

~~~


为了解决手动上传jar包的问题，可以配合maven的ssh上传插件 wagon-maven-plugin插件一起使用

> /data/docker/jdk/work/ 路径就是存放docker-compsoe.yml脚本中指定的jar包路径，执行upload-single命令可直接将jar包上传至docker-compose挂载的目录下。如此做就不用手动去将jar包上传到linux服务器上了

>执行sshexec命令，即可直接重启服务器上的工程；
>cd /data/docker/jdk/ &amp;&amp; docker-compose down &amp;&amp; docker-compose up
~~~
   <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>wagon-maven-plugin</artifactId>
                <version>1.0</version>
                <configuration>
                    <!--本地jar包路径-->
                    <fromFile>target/${project.artifactId}-${project.version}.jar</fromFile>
                    <!--上传服务器路径-->
                    <url><![CDATA[scp://root:123456@192.168.10.11:22/data/docker/jdk/work/]]></url>
                    <commands>
                        <!-- 重启工程 -->
                        <command>cd /data/docker/jdk/ &amp;&amp; docker-compose down &amp;&amp; docker-compose up </command>
                    </commands>
                    <displayCommandOutputs>true</displayCommandOutputs>
                </configuration>
            </plugin>
~~~


######docker-maven-plugin插件中进行Xdebug
这种方式是以java:8为基础构建整个工程的docker镜像

修改Dockerfile中的运行命令为 Xdebug
~~~
FROM java:8
WORKDIR /ROOT
ADD /ROOT/demo1-4.jar /ROOT/
# ENTRYPOINT ["java", "-jar", "demo1-4.jar"]
ENTRYPOINT ["java", "-jar","-Xdebug","-Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005","/demo1-4.jar"]
~~~
