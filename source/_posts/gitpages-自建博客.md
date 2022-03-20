---
title: gitpages-自建博客.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: git
categories: git
---
---
title: gitpages-自建博客.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: git
categories: git
---
gitpages

###地址
源码地址 https://github.com/suoyiguke/hexo-matery-modified
访问地址 https://suoyiguke.github.io/
文件地址 https://github.com/suoyiguke/suoyiguke.github.io
###问题
hexo g  打包0kb导致上传到github上也无法正常显示样式。网上搜了下也有人遇到。有人说重新安装node等环境。
我重新 生成就行了

###打包上传git服务器步骤
hexo g 生成静态文件到./public
hexo s 本地运行
hexo d 上传github，其实就是git 将静态资源push到github下

###文件目录
source 博客源文件
source\_posts 文章源

public 执行hexo 后生成的文件夹。就是博客静态的html+css+js资源




# 写文章、发布文章
- 首先在博客根目录下右键打开git bash，安装一个扩展`npm i hexo-deployer-git`。
- 然后输入`hexo new post "article title"`，新建一篇文章。
- 然后打开`D:\study\program\blog\source\_posts`的目录，可以发现下面多了一个文件夹和一个`.md`文件，一个用来存放你的图片等数据，另一个就是你的文章文件啦。
- 编写完markdown文件后，source 根目录下输入`hexo g`生成静态网页，然后输入`hexo s`可以本地预览效果
- 最后输入`hexo d`上传到github上。这时打开你的github.io主页就能看到发布的文章啦。
# [](https://godweiyang.com/2018/04/13/hexo-blog/#%E7%BB%91%E5%AE%9A%E5%9F%9F%E5%90%8D "绑定域名")




###注意上传图片：
这个kw.jpeg图片直接放到source/文章名/ 下。然后first.md写上这个即可,根本不需要加上`文章名`上级路径：
~~~
![](./kw.jpeg)
~~~

  
