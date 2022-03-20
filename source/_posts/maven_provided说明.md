---
title: maven_provided说明.md
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
title: maven_provided说明.md
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

1.test范围是指测试范围有效,在编译和打包时都不会使用这个依赖
2.compile范围是指编译范围内有效,在编译和打包时都会将依赖存储进去
3.provided依赖,在编译和测试过程中有效,最后生成的war包时不会加入 例如:
   servlet-api,因为servlet-api  tomcat服务器已经存在了,如果再打包会冲突
4.runtime在运行时候依赖,在编译时候不依赖，如jdbc驱动
~~~
		<dependency>
			<groupId>mysql</groupId>
			<artifactId>mysql-connector-java</artifactId>
			<scope>runtime</scope>
		</dependency>
~~~
默认依赖范围是compile
