---
title: Jeecg-Boot-权限控制之页面按钮权限.md
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
title: Jeecg-Boot-权限控制之页面按钮权限.md
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
######按钮的显示权限
前端按钮添加   `v-has="'box:create'" `
~~~
      <a-button @click="handleAdd" v-has="'box:create'" type="primary" icon="plus">新增</a-button>

~~~
或者是菜单栏按钮如下：
~~~
   <a-menu-item v-has="'box:del'">
                <a-popconfirm  title="确定删除吗?" @confirm="() => handleDelete(record.id)">
                  <a>删除</a>
                </a-popconfirm>
              </a-menu-item>

~~~


菜单出处添加二级菜单，设置菜单类型为 按钮/权限
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0db6c40b5d8fcf12.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

再填上授权标识为`box:create` 和上面的对应


然后再到角色授权处将这个二级菜单勾上即可，这样就保证只有手动授权的菜单（按钮）才能显示

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b60df7fabee0a8fd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######按钮的行为权限
