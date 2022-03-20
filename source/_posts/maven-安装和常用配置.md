---
title: maven-安装和常用配置.md
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
title: maven-安装和常用配置.md
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
> 会当凌绝顶，一览众山小

###maven安装和idea中的配置
maven是java中常用的构建工具，使用它可以进行jar包管理和依赖管理。方便解决依赖冲突问题。下面记录下它的安装和使用。

其实idea中自带了maven，不需要自己再去独立安装了。路径为
>XXXXX\IntelliJ IDEA 2019.3\plugins\maven

为了能够方便全局使用maven命令，需要配置下环境变量
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7310e16bdfd6a0e8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
在path下添加 %MAVEN_HOME%\bin
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6040e97a2e6b3587.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
完了之后，打开cmd。输入 mvn - v 出现以下内容则安装成功
![image.png](https://upload-images.jianshu.io/upload_images/13965490-17dcfe73b8fbc334.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


setting.xml文件即是maven的核心配置文件，它的路径为
>XXXX\plugins\maven\lib\maven3\conf\setting.xml

然后在idea中配置maven插件，如图所示三个地方
![image.png](https://upload-images.jianshu.io/upload_images/13965490-74bdf1ce5d717135.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###maven常用操作


######修改为阿里镜像，提升拉取依赖的速度
maven默认拉取依赖的地址是国外的，由于墙的原因速度很慢。所以需要换成国内的

~~~
  <mirrors>
     <mirror>  
        <id>alimaven</id>  
        <name>aliyun maven</name>  
        <url>http://maven.aliyun.com/nexus/content/groups/public/</url>  
        <mirrorOf>central</mirrorOf>         
    </mirror>

  </mirrors>
~~~


######指定本地的jar包仓库位置
我这里指定的是G盘根目录的MavenLocalWarehouse文件夹
~~~
  <localRepository>G:\MavenLocalWarehouse</localRepository>
~~~


######导入maven源码和javadocs
如果我们要看jar包的源码和文档，可以做如下操作

1、在pom.xml文件同级目录下，使用下面两条命令
~~~
mvn dependency:sources
mvn dependency:resolve -Dclassifier=javadoc
~~~

2、编辑maven的配置文件 setting.xml，加入以下配置

~~~
<profiles>
<profile>
    <id>downloadSources</id>
    <properties>
        <downloadSources>true</downloadSources>
        <downloadJavadocs>true</downloadJavadocs>           
    </properties>
</profile>
</profiles>
 
<activeProfiles>
  <activeProfile>downloadSources</activeProfile>
</activeProfiles>
~~~

3、idea改下配置
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bd74ea2ab1791500.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######安装仓库中不存在的jar包

先把jar包放到lib目录下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8a47793534ea921e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

到控制台下执行
~~~
mvn install:install-file -Dfile=./lib/ueditor-1.1.2.jar -DgroupId=com.baidu.ueditor -DartifactId=ueditor -Dversion=1.1.2 -Dpackaging=jar
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-abe2cf874df81078.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后在项目的pom.xml里添加插件
> 注意 maven坐标要和上面命令的一致
~~~
<plugin>
   <groupId>org.apache.maven.plugins</groupId>
   <artifactId>maven-install-plugin</artifactId>
   <executions>
      <execution>
         <phase>initialize</phase>
         <goals>
            <goal>install-file</goal>
         </goals>
         <configuration>
            <groupId>com.baidu.ueditor</groupId>
            <artifactId>ueditor</artifactId>
            <version>1.1.2</version>
            <packaging>jar</packaging>
            <file>${basedir}/lib/ueditor-1.1.2.jar</file>
         </configuration>
      </execution>
   </executions>
</plugin>
~~~
