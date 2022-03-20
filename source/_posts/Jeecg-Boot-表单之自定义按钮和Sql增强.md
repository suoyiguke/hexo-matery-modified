---
title: Jeecg-Boot-表单之自定义按钮和Sql增强.md
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
title: Jeecg-Boot-表单之自定义按钮和Sql增强.md
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
###自定义按钮
Jeecg-Boot 提供了自定义按钮的功能，让我们可以在表单上添加自定义按钮，并且添加的自定义按钮可以实现sql增强和js增强。如下

点击 表单开发==> 选择具体记录==>点击自定义按钮
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d9488c963fabac7b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

弹出按钮配置框：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-16a2de50c6c4d4a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


>1、按钮编码：该编码在一个智能表单配置中唯一，同时js增强中定义的函数名和该编码的值需要保持一致(详见js增强描述)

>2、 按钮名称：按钮上面显示的文本。

> 3、按钮样式：可选button/link。
button:即生成的按钮显示在导航工具栏上； link:显示在每一条数据的操作列的`更多`上。

如图工具栏上的按钮和 `更多`上的按钮：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c78768e36b44fac0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



> 4、动作类型：可选action/js。
action:该按钮会触发通用入口，挂接到SQL增强上（前提是SQL增强配置中配置了按钮编码对应的sql语句）。 
Js:该按钮会触发JS增强中类型为“list”的配置中编写了函数名为按钮编码的函数。

action应用于sql增强上，Js类型应用于Js增强上

>5、按钮图标：和antd-vue的icon保持一致 参考：https://vue.ant.design/components/icon-cn/ 

>6、显示表达式：按钮样式为link时起作用


###Sql增强
如下，点击 表单开发==>选中具体字段==>sql增强
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7b26cc2736b2ba88.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7c8f0d0242eea269.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>1、选择指定的页面按钮，这个按钮是我定义的action类型的按钮；sql增强按钮类型一定要是action的，因为js类型的是走的js增强
>2、增强sql 这里可以使用 `系统变量` 和 `表单字段`
3、表单字段如#{id}就是取id，id可以是任何当前表中的字段名
4、如果数据库定义的字段是数值类型的，这边是不需要加单引号('')的
5、系统变量有下面几种


其中系统变量有下面几种：
>`#{sys_user_code}`	登陆用户的ID
`#{sys_org_code}`	登陆用户所属机构编码
`#{sys_company_code}`	登陆用户所属公司编码
`#{sys_date}`	系统日期"yyyy-MM-dd"
`#{sys_time}`	系统时间"yyyy-MM-dd HH:mm"
`#{sys_user_name}`	登录用户真实姓名

示例SQL：

>update tb_point set name = '#{sys_user_name}' where id = '#{id}' 

我这里的用法是，当用户点击 `测试按钮3-action类型（sql增强）`按钮时触发该sql，将当前id记录的name 字段改为 登录用户真实姓名


