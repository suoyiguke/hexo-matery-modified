---
title: uibot-之数据抓取功能UiElement-DataScrap使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: uibot
categories: uibot
---
---
title: uibot-之数据抓取功能UiElement-DataScrap使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: uibot
categories: uibot
---

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1530d7f9975b47d6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**1、两次选择同一层级下的不同字段**
uibot需要至少两次选择不同条目（这里是商品）的相同字段才可以识别特定选中字段；比如这里我选择商品A的评价、然后又再选择商品B的评价；这样商品的评价字段就被识别到添加到返回列表了。

第一次选择
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d3981a4d9e13f574.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ce2221f5a269d8a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

第二次选择

![image.png](https://upload-images.jianshu.io/upload_images/13965490-ac65b8dfdc0d9153.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**2、使用抓取更多按钮来抓取结构化的更多字段数据**
使用数据抓取得到的页面是纯文本，不是结构化的！比如我要得到json，而他却将所有字段以文本加上空格返回了。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3f107b8b48a1312e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
应该是哪里有问题，我看到实例demo。抓取京东商品的程序打印数组其中的一个元素如下：明显使用数组的形式，使用逗号分割开了。肯定是我哪里还需要配置下。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-98cab9e12490cf42.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

皇天不负有心人，让我找到了。下面是区分字段后的效果：`需要点击抓取更多数据这个按钮添加新的要抓取的字段！`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f6c66ef51718cad1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**3、分页抓取**
如需要抓取其它页的数据就这样做。选择到翻页的“下一页按钮”，并将按钮位置信息xml设置到语句里面
![image.png](https://upload-images.jianshu.io/upload_images/13965490-042340e97c6bc255.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-ca22af301db090f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/13965490-3689857bb9891654.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这样就能做到一直往下自动翻页了。
当然想要做到没有数据就自动停止抓取那么就需要知道分页的总页数！在一些系统中可以得到（像这种电商网站不会给出的）。我们可以抓取这个数字然后设置到 UiElement.DataScrap的`页数`参数中。
