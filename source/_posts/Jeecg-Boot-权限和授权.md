---
title: Jeecg-Boot-权限和授权.md
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
title: Jeecg-Boot-权限和授权.md
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
######java接口授权

org.jeecg.modules.shiro.authc.ShiroRealm 这个类即是授权的核心类


>指的是@RequiresRoles("admin")注解么，使用这个那么只有管理员可以访问被申明的接口。还有一个是@RequiresPermissions("user:add")，这个就是需要user:add权限才能访问被申明的接口

######手机登录
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1b14614d767945e4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




######角色的菜单授权
角色菜单授权直接决定了该菜单要不要显示

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f85901f8cedcf44c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######部门的菜单授权
对应组织架构的部门的授权，如下图。期初不知道这个东西的作用。后来发现如果不勾选具体菜单，那么具体部门下的人员登录后点击为授权的菜单请求不会发出，加载动画会一直存在！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ad13c864c9899efa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
