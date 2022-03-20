---
title: pip-配置国内镜像加速.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
---
title: pip-配置国内镜像加速.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
# Window

打开此电脑(win10)在地址栏输入：`%HOMEPATH%` ，如下图所示：
![在这里插入图片描述](https://upload-images.jianshu.io/upload_images/13965490-d599b2b1abad8881.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

按回车，会进入用户所在目录，在该目录中新建一个文件夹，名字为 `pip` ,如下图所示：
![在这里插入图片描述](https://upload-images.jianshu.io/upload_images/13965490-1eb54bb36d2d1e14.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

进入`pip`目录，并新建一个文件 `pip.ini`，如下图所示：
![在这里插入图片描述](https://upload-images.jianshu.io/upload_images/13965490-c6ae5e8ec60b710b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn

```

# Linux

```
cd ~
mkdir .pip
vim ~/.pip/pip.conf

```

`pip.conf`文件内容如下：

```
[global]
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
```
