---
title: springboot-怎么做到将配置分离出jar包？.md
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
title: springboot-怎么做到将配置分离出jar包？.md
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
###先说方法
只需要在jar的同级目录下创建config文件夹，里面放上yml就行了

~~~
java -jar ruoyi-admin.jar 
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-11d33d966c263364.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>其实不需要注入这个参数spring.config.additional-location也行


###再来看看原理

这个类里面包含springboot加载配置的逻辑
org.springframework.boot.context.config.ConfigFileApplicationListener

~~~
EnvironmentPostProcessor that configures the context environment by loading properties from well known file locations. By default properties will be loaded from 'application.properties' and/or 'application.yml' files in the following locations:
file:./config/
file:./
classpath:config/
classpath:
The list is ordered by precedence (properties defined in locations higher in the list override those defined in lower locations).
Alternative search locations and names can be specified using setSearchLocations(String) and setSearchNames(String).
Additional files will also be loaded based on active profiles. For example if a 'web' profile is active 'application-web.properties' and 'application-web.yml' will be considered.
The 'spring.config.name' property can be used to specify an alternative name to load and the 'spring.config.location' property can be used to specify alternative search locations or specific files.

Since:
1.0.0
Author:
Dave Syer, Phillip Webb, Stephane Nicoll, Andy Wilkinson, Eddú Meléndez, Madhura Bhave
~~~

##注意
jar外面的配置和jar里面的配置是互补的。外面的优先级大于内部
