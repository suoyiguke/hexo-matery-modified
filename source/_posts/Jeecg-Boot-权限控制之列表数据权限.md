---
title: Jeecg-Boot-权限控制之列表数据权限.md
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
title: Jeecg-Boot-权限控制之列表数据权限.md
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
http://jeecg-boot.mydoc.io/?t=345676


######行级别数据过滤



######列级别数据过滤

1、首先配置下 按钮/权限菜单。设置授权标识为 `qx_point:point`;
其中`point`就是指定进行权限控制的列名（注意是java实体类属性名而不是mysql表的字段名）
![image.png](https://upload-images.jianshu.io/upload_images/13965490-653344f920ed2b53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

指定的字段名如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1ad4f8c41870052c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、角色授权，设置可以看到该列的角色
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ff6feeedf754126b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、前端修改
注意这个前缀`qx_point:` 就是上面指定的授权标识。一般来说一张表就对应一个前缀即可
~~~
import { colAuthFilter } from "@/utils/authFilter"
。。。。
 created() {
      this.columns = colAuthFilter(this.columns,'qx_point:');
      this.loadData();
    },
~~~


4、如果需要实现多个字段，比如我需要再进行name字段的权限控制。就再到菜单中创建权限菜单，并设置授权规则为 `qx_point: name` 即可
