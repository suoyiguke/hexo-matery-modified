---
title: Jeecg-Boot-在线开发之报表.md
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
title: Jeecg-Boot-在线开发之报表.md
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
>不畏浮云遮望眼

Jeecg-Boot这东西真的强大。但是要会用，将它的功能发挥出来。提升工作效率。
上篇文章https://www.jianshu.com/p/edf1ced010b5讲到了如何配置表单。这次在上次表单的基础上配置一个报表。

######配置报表级别流程记录

点击 报表配置右侧的录入按钮
![image.png](https://upload-images.jianshu.io/upload_images/13965490-08d68e401149601b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

填上报表编码和报表名、选择好数据源； 再填上报表sql如
>SELECT * FROM \`tb_name\`

然后点击右侧的SQL解析
![image.png](https://upload-images.jianshu.io/upload_images/13965490-131c18651defad7c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
那么底下的`动态报表配置明细`就自动生成了，如下生成的字段类型全都为字符类型，需要将时间类型的字段改成时间类型，不然等下预览报表就是个空的。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a2db637e3e3c60ec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


然后点击右下角确认按钮，确认创建表单。成功后找到咱们刚创建的报表，点击更多下的`功能测试`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c208ad5f5250a829.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

好了，我们刚刚配置的报表就出来了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8ea42b7dff487d38.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######我们该如何获得报表的链接？
找到我们的报表，点击更多的`配置地址`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8acb6df1791d5fb1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

弹出一个对话框，点击下复制即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a51a046214308669.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

粘贴到浏览器上，访问：
http://localhost:3000/online/cgreport/79d403a75ab24f14afe6b83eebd59d1e

嗯，这样就出来了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b27e787485145a62.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###动态报表配置明细
我们来看看一些报表配置的细节
######字段href
比如下面的create_by字段上需要配置一个超链接如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-de94bff599bc40dc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击确定后，再预览这个报表。嗯更好，已经变成蓝色了。说明上面有超链接
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8f688c37a6ff286d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击之就能跳转到指定的连接了。当然我这里配置的是另一张报表的连接/online/cgreport/7ba25f4797f8444f8c003e717e3f7f99


######查询模式
有两个选项： 单条件和范围查询
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9efd0c6dd17320f9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
如果在id字段上配置上单条件，则如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f6d4dc068fa58b16.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
如果在id字段上配置上多条件，则如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-002c5d4b2f8c2253.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######取值表达式
这些还没研究，等到用到了在看看吧
######字典code
