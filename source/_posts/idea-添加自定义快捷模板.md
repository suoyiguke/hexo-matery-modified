---
title: idea-添加自定义快捷模板.md
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
title: idea-添加自定义快捷模板.md
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
自定义快捷模板可以完成输入关键字生成相应代码或注释字符串的功能，非常方便~

######快速开始
File --> setting-->搜索 Live Templates

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b69dfc4abf26278f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击右上角加号，添加自定义模板组
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d22444c75733b2be.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
命名为java
![image.png](https://upload-images.jianshu.io/upload_images/13965490-35858eb3ad6701ad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
再次点击右上角加号，添加模板
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e34b6dbac3f10d58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######添加类注释
~~~
/**
 *@description: $classname$
 *@author: yinkai
 *@create: $date$ $time$
 */
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6dd5729dd53117de.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

第4步 给创建的模板作用到模板组，勾上java
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7f32d46a08972948.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


第5步的按钮本来是置灰的，需要在底下的Template text中 添加`$xx$` 的变量后才可恢复点击；可以看下具体
![image.png](https://upload-images.jianshu.io/upload_images/13965490-84c1b6ad39fbf398.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
完成上面6步后就配置完毕了~

######具体使用
在java文件中输入 `lzs` 上面定义的快捷键，按 TAB 键
![image.png](https://upload-images.jianshu.io/upload_images/13965490-af6626780e1354ac.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
自动生成了类注释
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ef675dd28dfa81e9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######定义常用的生成方法
使用psv生成test静态方法，省的去敲那些重复的东西了
~~~
public static void test(){

}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d5d82e25a5ec74da.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######idea提供的关键字
输入main即可快速生成main方法~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-22f292ce65914438.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

输出打印类的关键字
![image.png](https://upload-images.jianshu.io/upload_images/13965490-da034ecdc43dbf0d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

常用的定义方法的关键字
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e507dfa9edc5b1ac.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

循环语句关键字
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c3222e02a548fac5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

