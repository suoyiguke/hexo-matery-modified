---
title: uni-app为啥没有package-json，是因为两种安装方式有区别.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: web
categories: web
---
---
title: uni-app为啥没有package-json，是因为两种安装方式有区别.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: web
categories: web
---

通过HBuilderX可视化界面创建的：


在uniapp-test1项目下：

| components | uni-app组件目录，放可复用的组件 |
| pages | 业务页面文件存放的目录 |
| static | 存放应用引用静态资源（如图片、视频等）的地方，注意：静态资源只能存放于此 |
| App.vue | 应用配置，用来配置App全局样式以及监听 [应用生命周期](https://www.oschina.net/action/GoToLink?url=https%3A%2F%2Funiapp.dcloud.io%2Fframe%3Fid%3D%25E5%25BA%2594%25E7%2594%25A8%25E7%2594%259F%25E5%2591%25BD%25E5%2591%25A8%25E6%259C%259F) |
| main.js | Vue初始化入口文件 |
| mainfest.json | 配置应用名称、appid、logo、版本等打包信息，[详见](https://www.oschina.net/action/GoToLink?url=https%3A%2F%2Funiapp.dcloud.io%2Fcollocation%2Fmanifest) |
| pages.json | 配置页面路由、导航条、选项卡等页面类信息，[详见](https://www.oschina.net/action/GoToLink?url=https%3A%2F%2Funiapp.dcloud.io%2Fcollocation%2Fpages) |

这种方式安装的uni-app项目需要使用HBuilderX运行。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3e37994ea80f128d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意要安装sass插件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2df28f841ea2a9c8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




*   通过vue-cli命令行方式快速创建的：

    [图片上传失败...(image-83356e-1635321811169)]

在my-project项目下：

| dist ->build | 存放通过build编译的各个平台的代码，如mp-weixin |
| node_modules | 项目依赖包模块 |
| public | 放置的为公共文件，比如index.html文件，为项目的生成模板，我们写的vue的代码，在webpack打包项目的时候，最后都会基于该模板转换为浏览器可读的三大件：html+javascript+css |
| src | 存放通过HBuilderX可视化界面创建的的所有目录，为源码目录 |
| .gitignore | git上传需要忽略的文件格式 |
| babel.config.js | ES6语法编译配置 |
| package.json | 项目基本信息 |
| package-lock.json | 锁定安装时的包的版本号，并且需要上传到git，以保证其他人在npm install时大家的依赖能保证一致 |
| postcss.config.js | postcss-loader 的配置文件名，通过js对 CSS 进行处理 |
| README.md | 项目说明 |
