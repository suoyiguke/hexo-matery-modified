---
title: Jeecg-Boot-在线开发之表单.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---
---
title: Jeecg-Boot-在线开发之表单.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---
###在线创建数据库表（配置表单）
点击在线开下的 Online表单开发，右侧再点击新增按钮
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1f31a17ed5c91ff1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后弹出框如下，表单的插件共有6个模块
![image.png](https://upload-images.jianshu.io/upload_images/13965490-411e6895a81f0736.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

太多东西了，先不一一看了。等到用时再记录下，填上 `表名` 和`表描述`直接点击右下角确定。然后跳转到这个界面：可以看到这个即是我们刚才创建的表单
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8a1fcfec5b760974.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击更多上的`同步数据库`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8a366858a58524ca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

直接点击确定吧。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d857ed92f42c7fd1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后切达到数据库，可以看到tb_name表被建立
![image.png](https://upload-images.jianshu.io/upload_images/13965490-23f62977c876f262.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###表单配置的其它功能

######代码生成
勾上我们需要生成代码的表单，然后点击上面的代码生成按钮
![image.png](https://upload-images.jianshu.io/upload_images/13965490-25ab05405a32e6a0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

弹出这个生成配置，填写下包名，我这里设置成 com.yinkai
![image.png](https://upload-images.jianshu.io/upload_images/13965490-60378d5f4f4573a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击确认按钮，生成代码。
之后怎么将生成的代码放到工程中顺利运行和配置菜单可以看看这篇文章https://www.jianshu.com/p/9bba6729f8e4

不过我使用这个线上生成代码的功能是出现了这异常：
>Java stack trace (for programmers):
FTL stack trace ("~" means nesting-related):
	- Failed at: #if po.isQuery == "Y"  [in template "default\\one\\java\\${bussiPackage}\\${entityPackage}\\vue\\${entityName}List.vuei" at line 15, column 1]
Java stack trace (for programmers):
freemarker.core.InvalidReferenceException: [... Exception message was already printed; see it above ...]

这种框架的问题暂时没得到解决，先使用哪个java UI程序来生吧。哪一天解决了马上就把解决方式贴上来~


######页面属性板块
![image.png](https://upload-images.jianshu.io/upload_images/13965490-457935a320a96e67.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以看到包含字段名称、字段备注、表单显示、列表显示、是否只读、控件类型、控件长度、是等否查询、查询类型、扩展参数、填值规则 配置项

######表单显示和列表显示
勾上就能在表单预览里面看到显示列，在新建和编辑对话框中能看到对应的表单项

######是否只读
勾上它在新建和编辑对话框中对应的表单项就是置灰的，不可编辑的

######控件类型
选择表单项的控件类型，那么在我们新增记录和修改记录的时候就能够生效了。比如我选择了`用户选择器`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b9913386b1d65f79.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
那么在新增记录时可以看到：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b0dad753dd4ac977.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击选择用户看看，嗯很好我们可以选择部门下的人员
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0438ac9a990d1fb4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###创建表单的细节问题

######主键字段的字段类型默认是String，没办法改变
![image.png](https://upload-images.jianshu.io/upload_images/13965490-48baa4fa6a60a6dc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



