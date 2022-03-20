---
title: maven-引入第三方的不存在于仓库中的jar.md
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
title: maven-引入第三方的不存在于仓库中的jar.md
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
###方式1，maven注册jar包
注意下mvn命令的环境变量指定的maven程序是不是project指定的maven，若不是同一个那还是找不到依赖。
~~~
mvn install:install-file -DgroupId=com.jztechplus -DartifactId=jztechplus -Dversion=1.0 -Dpackaging=jar -Dfile=jztechplus-poi-2016.jar
~~~

pom
~~~
     <dependency>
        <groupId>com.jztechplus</groupId>
        <artifactId>jztechplus</artifactId>
        <version>1.0</version>
      </dependency>
~~~

###方式2，直接引入本地jar
这种方式就不需要去注册jar到本地仓库了，不过得定义下jar路径。
如果是单个简单工程，使用${pom.basedir}就行了。
~~~
   <dependency>
      <groupId>org.mitre.dsmiley.httpproxy</groupId>
      <artifactId>smiley-http-proxy-servlet</artifactId>
      <systemPath>${pom.basedir}/jar/smiley-http-proxy-servlet-1.12.jar</systemPath>
      <scope>system</scope>
      <version>1.12</version>
    </dependency>
~~~

若有父级子级的maven modul的话就这样：
注意`${basedir}`变量表示当前的项目根目录，儿子pom.xml中需要设置为`${basedir}/../`，否则会去找儿子module的根目录，报找不到依赖。

父级pom
定义变量和依赖
~~~
    <myproject.root>${basedir}</myproject.root>
~~~
~~~
     <dependency>
        <groupId>com.jztechplus</groupId>
        <artifactId>jztechplus</artifactId>
        <version>1.0</version>
        <systemPath>${myproject.root}/jar/jztechplus-poi-2016.jar</systemPath>
        <scope>system</scope>
      </dependency>

~~~


子pom
~~~
  <properties>
    <myproject.root>${basedir}/../</myproject.root>
  </properties>
~~~
~~~
   <dependency>
      <groupId>com.jztechplus</groupId>
      <artifactId>jztechplus</artifactId>
    </dependency>

~~~

还需要修改下maven插件配置，添加 `<includeSystemScope>true</includeSystemScope>` 不添加的话项目打包成jar时这些scope为system的jar不会一起打包进去。报NoClassDefFoundError。
~~~
  <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>2.1.1.RELEASE</version>
                <configuration>
                    <fork>true</fork> <!-- 如果没有该配置，devtools不会生效 -->
                    <includeSystemScope>true</includeSystemScope><!-- 如果没有该配置，System下的jar打包不进去-->
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
~~~

###方式3，使用maven私服Nexus
把jar上传到Nexus仓库，project再关联下即可
