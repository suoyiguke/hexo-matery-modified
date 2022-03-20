---
title: maven-插件docker-maven-plugin之构建docker镜像并运行（一）.md
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
title: maven-插件docker-maven-plugin之构建docker镜像并运行（一）.md
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
>众生皆苦

之前的文章https://www.jianshu.com/p/f954bf0486dd讲到了如何使用传统的方式将jar包上传至linux服务器且自动运行。

但是现在有另一种的方式可以更加简化部署，那就是docker容器化技术。通过docker镜像上线，能够大大提供上线效率，同时能够快速动态扩容，快速回滚。
咱们的maven可以整合docker一起使用，需要docker-maven-plugin插件。
这个插件就是为了帮助我们在maven工程中，通过简单的配置，自动生成镜像并推送到仓库中。

###在内网linux服务器的docker上构建镜像

先需要开启docker的远程访问，安装docker和docker-compose 等内容可以看看我这篇文章
https://www.jianshu.com/p/7e44556ddc08

然后在我们开发者机器上配置下访问docker的环境变量DOCKER_HOST，如果不配置maven会默认在开发者本机找docker了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3395b445aae3c96e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

编辑pom.xml添加 docker-maven-plugin 插件的配置，有两种方式
一种是直接在pom.xml文件里编写docker命令来构建，一种是另写一个dockerfile文件构建，但需要指定dockerfile的路径
 
######直接在pom.xml文件里编写docker构建命令
>- dockerHost 指定使用的客户端docker，如果不配这个就会去找DOCKER_HOST环境变量。以防外一还是配上吧
>- imageName 是镜像名，以192.168.10.11/ 开头表示要上传镜像到这个ip的服务器上的docker
>- baseImage 基础镜像，我们是springboot程序，当然写上java。可以指定版本号如 java:8
>- workdir 工作目录，我这里设置为ROOT
>- entryPoint  即是java中运行jar包的命令，如java -jar xxx.jar。这里的jar包名${pack-name}读的是上面的属性。
>- forceTags 设置为true，强制覆盖上次推送的重名tag镜像
>- 设置imageTags 即可指定镜像的tag
>- resource.directory 找到当前工程的target目录
>- resource.include jar包名

~~~
  <plugin>
                <groupId>com.spotify</groupId>
                <artifactId>docker-maven-plugin</artifactId>
                <version>1.0.0</version>
                <configuration>
                      <!--必须配置dockerHost标签（除非配置系统环境变量DOCKER_HOST）-->
                    <dockerHost>http://192.168.10.11:2375</dockerHost>
                    <!--Building image 192.168.10.11/demo1-->
                    <imageName>192.168.10.11/${project.artifactId}</imageName>
                    <!--FROM java:8-->
                    <baseImage>java:8</baseImage>
                    <!--WORKDIR /ROOT-->
                    <workdir>/ROOT</workdir>
                    <!--ENTRYPOINT ["java", "-jar", "demo1-0.0.1-SNAPSHOT.jar"]-->
                    <entryPoint>["java", "-jar", "${pack-name}"]</entryPoint>
                    <!--强制覆盖上次推送的重名tag镜像-->
                    <forceTags>true</forceTags>
                    <!--  给进行打上tag-->
                    <imageTags>
                        <imageTag>${project.version}</imageTag>
                        <!--<imageTag>latest</imageTag>-->
                    </imageTags>
                    <!-- jar包位置-->
                    <resources>
                        <resource>
                            <targetPath>/ROOT</targetPath>
                            <!-- target目录下-->
                            <directory>${project.build.directory}</directory>
                            <!--通过jar包名找到jar包-->
                            <include>${pack-name}</include>
                        </resource>
                    </resources>
                </configuration>
            </plugin>

~~~



进入目录执行下面命令，即可在内网linux的docker上build镜像了
~~~
mvn clean package docker:build -DskipTests
~~~

贴上执行日志
~~~
E:\java\springboot_study\demo1>mvn clean package docker:build
[INFO] Scanning for projects...
[INFO]
[INFO] ---------------------< com.springboot.study:demo1 >---------------------
[INFO] Building demo1 0.0.1-SNAPSHOT
[INFO] --------------------------------[ jar ]---------------------------------
[INFO]
[INFO] --- maven-clean-plugin:3.1.0:clean (default-clean) @ demo1 ---
[INFO] Deleting E:\java\springboot_study\demo1\target
[INFO]
[INFO] --- maven-resources-plugin:3.1.0:resources (default-resources) @ demo1 ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] Copying 2 resources
[INFO] Copying 3 resources
[INFO]
[INFO] --- maven-compiler-plugin:3.2:compile (default-compile) @ demo1 ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 27 source files to E:\java\springboot_study\demo1\target\classes
[INFO] /E:/java/springboot_study/demo1/src/main/java/com/springboot/study/demo1/config/ImageWebAppConfig.java: E:\java\springboot_study\demo1\src\main\java\com\springboot\study\demo1\config\ImageWebAppConfig.java使用或覆盖了已过时的 API。
[INFO] /E:/java/springboot_study/demo1/src/main/java/com/springboot/study/demo1/config/ImageWebAppConfig.java: 有关详细信息, 请使用 -Xlint:deprecation 重新编译。
[INFO]
[INFO] --- maven-resources-plugin:3.1.0:testResources (default-testResources) @ demo1 ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] skip non existing resourceDirectory E:\java\springboot_study\demo1\src\test\resources
[INFO]
[INFO] --- maven-compiler-plugin:3.2:testCompile (default-testCompile) @ demo1 ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 5 source files to E:\java\springboot_study\demo1\target\test-classes
[INFO]
[INFO] --- maven-surefire-plugin:2.22.2:test (default-test) @ demo1 ---
[INFO] Tests are skipped.
[INFO]
[INFO] --- maven-jar-plugin:3.1.2:jar (default-jar) @ demo1 ---
[INFO] Building jar: E:\java\springboot_study\demo1\target\demo1-0.0.1-SNAPSHOT.jar
[INFO]
[INFO] --- spring-boot-maven-plugin:2.2.4.RELEASE:repackage (repackage) @ demo1 ---
[INFO] Replacing main artifact with repackaged archive
[INFO]
[INFO] --- docker-maven-plugin:1.0.0:build (default-cli) @ demo1 ---
[INFO] Using authentication suppliers: [ConfigFileRegistryAuthSupplier]
[INFO] Copying E:\java\springboot_study\demo1\target\demo1-0.0.1-SNAPSHOT.jar -> E:\java\springboot_study\demo1\target\docker\ROOT\demo1-0.0.1-SNAPSHOT.jar
[INFO] Building image 192.168.10.11/demo1
Step 1/4 : FROM java:8

 ---> d23bdf5b1b1b
Step 2/4 : WORKDIR /ROOT

 ---> Running in c9e5ec39b8e5
Removing intermediate container c9e5ec39b8e5
 ---> 15b1b172e469
Step 3/4 : ADD /ROOT/demo1-0.0.1-SNAPSHOT.jar /ROOT/

 ---> c69f058f1f17
Step 4/4 : ENTRYPOINT ["java", "-jar", "demo1-0.0.1-SNAPSHOT.jar"]

 ---> Running in d3ea777b001f
Removing intermediate container d3ea777b001f
 ---> 914cf45c8f9d
ProgressMessage{id=null, status=null, stream=null, error=null, progress=null, progressDetail=null}
Successfully built 914cf45c8f9d
Successfully tagged 192.168.10.11/demo1:latest
[INFO] Built 192.168.10.11/demo1
[INFO] Tagging 192.168.10.11/demo1 with 0.0.1-SNAPSHOT
[INFO] Tagging 192.168.10.11/demo1 with latest
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  40.542 s
[INFO] Finished at: 2020-03-07T09:50:55+08:00
[INFO] ------------------------------------------------------------------------
~~~

到linux上看看，这个两个镜像即是刚刚在内网build 的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d732c76b61f3584a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######使用dockerfile的方式

配置插件
> 这里使用dockerDirectory指定Dockerfile 在根目录下
~~~ 
 <plugin>
                <groupId>com.spotify</groupId>
                <artifactId>docker-maven-plugin</artifactId>
                <version>1.0.0</version>
                <configuration>
                      <!--必须配置dockerHost标签（除非配置系统环境变量DOCKER_HOST）-->
                    <dockerHost>http://192.168.10.11:2375</dockerHost>
                    <!--Building image 192.168.10.11/demo1-->
                    <imageName>192.168.10.11/${project.artifactId}</imageName>
                    <!-- 指定 Dockerfile 路径-->
                    <dockerDirectory>${basedir}/</dockerDirectory>
                    <!-- jar包位置-->
                    <resources>
                        <resource>
                            <targetPath>/ROOT</targetPath>
                            <!-- target目录下-->
                            <directory>${project.build.directory}</directory>
                            <!--通过jar包名找到jar包-->
                            <include>${pack-name}</include>
                        </resource>
                    </resources>
                </configuration>
            </plugin>
~~~

在根目录下添加Dockerfile 文件
> 虽然使用这种方式能够使用docker的更多的命令，但是要
注意使用这种方式更改了工程版本号之后就必须在Dockerfile 中做对应修改。比如版本号改成了1，那么jar包名字就是 demo1-1.jar了。
~~~
FROM java:8
WORKDIR /ROOT
ADD /ROOT/demo1-0.0.1-SNAPSHOT.jar /ROOT/
ENTRYPOINT ["java", "-jar", "demo1-0.0.1-SNAPSHOT.jar"]
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-5cad7676875ede68.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

同样执行mvn clean package docker:build命令即可


#####使用docker-compose 运行springboot的docker镜像
既然已经在docker上构建了工程镜像，那么如何运行呢？

添加docker-compose.yml文件
~~~
version: '2'
services:
  demo:
    image: 192.168.10.11/demo1:0.0.1-SNAPSHOT
    ports:
      - "8080:8080"
    environment:
      - spring.profiles.active=dev
~~~

使用docker-compose up 运行
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c5c6f6118f5360c0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

