---
title: 上传新版jar到仓库一直拉不到的问题解决（缓存问题）.md
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
title: 上传新版jar到仓库一直拉不到的问题解决（缓存问题）.md
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
# 解决maven构建时报错：was cached in the local repository...

 原创

[qianghong000](https://blog.51cto.com/qiangsh)<time class="fl" pubdate="2016-02-18 16:59:08" style="font-family: fontDIN; -webkit-font-smoothing: antialiased; margin: 0px; padding: 0px 12px 0px 0px; float: left;">2016-02-18 16:59:08</time>©著作权

***文章分类*[Linux运维](https://blog.51cto.com/qiangsh/category3)*****阅读数***130670****

**今天使用命令mvn compile编译maven项目时提示错误信息，错误信息如下：** 

```
[ERROR] Failed to execute goal on project <project_name>: Could not resolve dependencies
for project com.xxx.xxx:<project_name>:jar:1.0.7: Failure to find com.xxx.xxx:obj-test-client:jar:1.1.1
in http://maven-nexus.xxx.com/repository/maven-public/ was cached in the local repository, resolution 
will not be reattempted until the update interval of fintech has elapsed or updates are forced -> [Help 1]
```

**问题原因 :**
Maven默认会使用本地缓存的库来编译工程，对于上次下载失败的库，maven会在`~/.m2/repository/<group>/<artifact>/<version>/`目录下创建xxx.lastUpdated文件，一旦这个文件存在，那么在直到下一次nexus更新之前都不会更新这个依赖库。

**解决办法： **

**方法一：**

删除v~/.m2/repository/<group>/<artifact>/<version>/目录下的*.lastUpdated文件，然后再次运行mvn compile编译工程。

**方法二：**

修改~/.m2/settings.xml 或/opt/maven/conf/settings.xml文件，将其中的仓库添加 <updatePolicy>always</updatePolicy>来强制每次都更新依赖库。

```
<repositories>
        <repository>
                <id>central</id>
                <url>http://central</url>
                <releases>
                        <enabled>true</enabled>
                        <updatePolicy>always</updatePolicy>
                </releases>
                <snapshots>
                        <enabled>true</enabled>
                        <updatePolicy>always</updatePolicy>
                </snapshots>
        </repository>
</repositories>
```

**Jenkins构建时报错：**

通过jenkins编译时报此错，我的maven安装目录/opt/maven ，解决方法如下：

发现obj-test-client-1.1.1.jar下载到本地时失败，从提示可知是本地仓库的缓存（cached）造成，于是我删除目录/opt/maven/repo/<group>/obj-test-client/1.1.1后Jenkins重新构建（或在项目目录 mvn 重新编译）即可编译成功！ 

注意你要确定远程仓库中存在此jar（obj-test-client-1.1.1.jar）包
