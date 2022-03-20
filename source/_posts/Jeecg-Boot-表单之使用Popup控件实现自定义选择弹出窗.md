---
title: Jeecg-Boot-表单之使用Popup控件实现自定义选择弹出窗.md
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
title: Jeecg-Boot-表单之使用Popup控件实现自定义选择弹出窗.md
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
> 学以致用

我们需要实现： 新增/编辑表单记录时，选择自定义报表弹出框。将选择的字段带回到表单列中。如图，点击一下这个表单项
![image.png](https://upload-images.jianshu.io/upload_images/13965490-74ca9ee1423594a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



之后 弹出一个可选择的报表窗口。选择具体一个后点击确定按钮
![image.png](https://upload-images.jianshu.io/upload_images/13965490-36c6201367407d00.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样 name字段的值就带入到当前报表中特定字段中了！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b3ae5df5f2d59879.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######实现步骤

1、首先我我们需要定义一个报表。定义报表的细节就不多说了。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bc2bd9f0702cbbf4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

需要注意 该报表的编码是 `tb_point_select`，这个非常重要


2、编辑目标表单，将目标表单字段 launch_point 的 页面属性-控件类型 设置为popup弹出框
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c14709482f85bdbf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、再设置表单字段 launch_point 的校验字段三个空填上；
分别为：

>字典Table、字典Code、字典Text项填写对应的Online报表信息
1、字典Table :填写online报表编码
2、字典Code:填写 需要写入表单中的字段名
3、字典Text: 填写online报表列表字段名 

如下设置的意思就是：
把报表tb_point_select查出的字段 id,name 选择后分别先后写入表单中point_id和launch_point 字段


![image.png](https://upload-images.jianshu.io/upload_images/13965490-64f7f9735315ec51.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 注意这个 point_id字段我设置为隐藏了，不会在新增表单中出现。但是我们又需要一并将id回写
