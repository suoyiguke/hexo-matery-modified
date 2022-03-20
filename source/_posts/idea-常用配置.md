---
title: idea-常用配置.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开发工具
categories: 开发工具
---
---
title: idea-常用配置.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开发工具
categories: 开发工具
---
######字符集设置
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8749545ac6327646.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######eclispe风格的快捷键
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c92bb573ad7ae1d8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######设置显示行数
![image.png](https://upload-images.jianshu.io/upload_images/13965490-04f76098c892fd80.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######idea中使用javac
先配置好
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6b24c75f28e4093c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
填上下面的参数即可
~~~
//javap.exe的文件路径
G:\Jdk\jdk1.8\bin\javap.exe
//反编译文件
-c $FileClass$
//项目路径
$OutputPath$
~~~
使用方法：右键java文件，选中即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-993aa770b2f43723.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

结果：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2ff6b1d9a9b63374.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######查看类的URM图

![image.png](https://upload-images.jianshu.io/upload_images/13965490-0c7d7fbf406f6831.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######查看URM图中接口的子接口或者实现类
![image.png](https://upload-images.jianshu.io/upload_images/13965490-57c96e2968446343.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b6defa06c5f909d7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2aa22dce73eac4ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###### 导入包配置

特别好用！！！自动生成import

![image.png](https://upload-images.jianshu.io/upload_images/13965490-60d6db70d5bb785a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######配置创建类自动生成注释
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c94d1ff2bc6f6690.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######查看maven依赖
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f256df4b72a23089.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######快速生成service类的单元测试
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0a72002126103a55.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
