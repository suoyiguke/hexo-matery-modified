---
title: maven-插件之使用wagon-maven-plugin上传jar包到服务器上运行.md
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
title: maven-插件之使用wagon-maven-plugin上传jar包到服务器上运行.md
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
>学海无涯

上篇文章 https://www.jianshu.com/p/29fdbfa40809 讲述了如何将工程打包成jar文件。这次再来看如何将jar包上传到linux服务器并运行~

使用wagon-maven-plugin插件可以自动将到包好的jar包通过ssh的方式上传到linux服务器上。所以先要有一台linux，我这里使用vm虚拟机安装了一个centeros。
使用xshell连上后，查看下端口是192.168.10.11。记得密码是123456，所以下面的属性配置直接填上这几个就行了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3d75785f1d5f3281.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


项目基础属性配置，默认打包出来的jar文件就是按artifactId、version这些属性名生成的
~~~
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.springboot.study</groupId>
    <artifactId>demo1</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo1</name>
    <packaging>jar</packaging>
    <description>Demo project for Spring Boot</description>
~~~
properties属性配置，这里的属性在后面的插件配置里有引用
~~~
<properties>
    <!--wagon plugin 配置-->

    <!--服务器上的路径-->
    <service-path>/work/${project.artifactId}</service-path>
    <!--jar包名-->
    <pack-name>${project.artifactId}.jar</pack-name>
    <!--服务器ip-->
    <remote-addr>192.168.10.11:22</remote-addr>
    <!--服务器用户-->
    <remote-username>root</remote-username>
    <!--服务器密码-->
    <remote-passwd>123456</remote-passwd>
</properties>
~~~

ssh依赖和插件配置
~~~
<build>

	<extensions>
		<extension>
			<groupId>org.apache.maven.wagon</groupId>
			<artifactId>wagon-ssh</artifactId>
			<version>2.8</version>
		</extension>
	</extensions>

  <plugins>


            <!-- 跳过单元测试 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <configuration>
                    <skipTests>true</skipTests>
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>wagon-maven-plugin</artifactId>
                <version>1.0</version>
                <configuration>
                    <fromFile>target/${pack-name}</fromFile>
                    <url><![CDATA[scp://${remote-username}:${remote-passwd}@${remote-addr}${service-path}]]></url>
                </configuration>
            </plugin>
        </plugins>

		
</build>
~~~

配置完毕后刷新下配置，可以看到右面的maven控制面板多了个选项
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cf1cf99e162c17a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

打开看看，常用的就是这个 wagon:upliad-single
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c8656a949041f715.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击运行，输出了一些日志就等待用户交互了。这里按提示输入下yes继续
![image.png](https://upload-images.jianshu.io/upload_images/13965490-93c361b4cd139639.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后报错
>Failed to execute goal org.codehaus.mojo:wagon-maven-plugin:1.0:upload-single (default-cli) on project demo1: Error handling resource

猜测是jar包名字的问题。默认打包生成的jar包名字是这样的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-af560c9c474de036.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

而我配置的名字是这样：
<pack-name>${project.artifactId}.jar</pack-name>
那么maven就会去找  demo1.jar 文件。当然是找不到了。
所以改成这样
~~~
<!--jar包名-->
<pack-name>${project.artifactId}-${project.version}.jar</pack-name>
~~~

要么在打包时指定jar包的名字来符合之前的标准也是一样

这样就算是成功了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a20aecb73e13241b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

那么到服务器上找找上传的jar包吧，在/work/demo1中已经已经存在jar包，上传成功！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7f7aa57f72699ba6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######wagon的运行功能
其实还可以使用wagon来自动化运行jar包，给wagon-maven-plugin插件添加commands命令节点，一共配置类4条命令。还有一个displayCommandOutputs属性设为true，目的是输出命令日志

~~~
    <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>wagon-maven-plugin</artifactId>
                <version>1.0</version>
                <configuration>
                    <fromFile>target/${pack-name}</fromFile>
                    <url><![CDATA[scp://${remote-username}:${remote-passwd}@${remote-addr}${service-path}]]></url>
                    <commands>
                        <!-- 杀死原来的jar进程 -->
                        <command>pkill -f ${pack-name}</command>
                        <!-- 重启工程，输出日志到test.log -->
                        <command><![CDATA[nohup java -jar ${service-path}/${pack-name} --spring.profiles.active=test > ${service-path}/test.log 2>&1 & ]]></command>
                        <!-- 输出端口占用情况 -->
                        <command><![CDATA[netstat -nptl]]></command>
                        <!-- 输出java进程 -->
                        <command><![CDATA[ps -ef | grep java | grep -v grep]]></command>
                    </commands>
                    <!-- 运行命令 mvn clean package wagon:upload-single wagon:sshexec-->
                    <displayCommandOutputs>true</displayCommandOutputs>
                </configuration>
            </plugin>
~~~
配置完后，点击这个选项即可直接在linux服务器上运行工程了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-60102f39f2608bbb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###手动使用命令
之前讲的都是通过idea提供的图形化界面来操作的，分为了三个步骤：
package 打包、wagon:upload-single 上传、wagon:sshexec 运行
为了方便可以使用一条命令直接部署启动

在项目的根目录（和pom.xml平级）打开cmd，执行下面命令即可
~~~
mvn clean package wagon:upload-single wagon:sshexec
~~~
