---
title: 前端工具之yarn-使用笔记.md
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
title: 前端工具之yarn-使用笔记.md
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
> 非宁静无以致远

由于jeecg-boot是使用yarn 来管理依赖的啊，所以需要学习一波yarn 。之前使用的是npm的，换换口味尝尝鲜也不错
######全局安装yarn 
>npm i yarn -g


![image.png](https://upload-images.jianshu.io/upload_images/13965490-281d187fbb9154a6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######为前端工程安装依赖
cd进入到工程根目录内，执行：
>yarn install

好的，报错
~~~
"G:\webStorm\WebStorm 2018.1.4\bin\runnerw.exe" G:\node\node.exe C:\Users\yinkai\AppData\Roaming\npm\node_modules\yarn\bin\yarn.js install
yarn install v1.22.4
[1/4] Resolving packages...
[2/4] Fetching packages...
info There appears to be trouble with your network connection. Retrying...
error vue-ls@3.2.1: The engine "node" is incompatible with this module. Expected version ">=6.11.5". Got "6.11.1"
errorinfo Found incompatible module.
 Visit https://yarnpkg.com/en/docs/cli/install for documentation about this command.
~~~
提示node引擎版本不符？ 重新安装提示的6.11.5版本的node吧，如果嫌麻烦可以使用这个东西 `nvw-windows ` 它可以使用命令轻松切换node版本，非常方便 https://www.jianshu.com/p/7eb5d660a95b



安装node6.11.5后 继续安装工程依赖。又出错了
~~~
E:\java\jeecg-boot\ant-design-vue-jeecg>yarn install
info fsevents@1.2.11: The platform "win32" is incompatible with this module.
info "fsevents@1.2.11" is an optional dependency and failed compatibility check. Excluding it from installation.
error default-gateway@5.0.5: The engine "node" is incompatible with this module. Expected version "^8.12.0 || >=9.7.0". Got "8.9.3"
error Found incompatible module.
info Visit https://yarnpkg.com/en/docs/cli/install for documentation about this command.
~~~


网上找了找，执行下这个即可解决
~~~
 yarn config set ignore-engines true
~~~


再次安装依赖，成功
~~~
"G:\webStorm\WebStorm 2018.1.4\bin\runnerw.exe" G:\node\node.exe C:\Users\yinkai\AppData\Roaming\npm\node_modules\yarn\bin\yarn.js install
yarn install v1.22.4
[1/4] Resolving packages...
[2/4] Fetching packages...
info fsevents@1.2.11: The platform "win32" is incompatible with this module.
info "fsevents@1.2.11" is an optional dependency and failed compatibility check. Excluding it from installation.
[3/4] Linking dependencies...
warning " > vue-loader@15.9.0" has unmet peer dependency "css-loader@*".
warning " > vue-loader@15.9.0" has unmet peer dependency "webpack@^3.0.0 || ^4.1.0 || ^5.0.0-0".
warning " > html-webpack-plugin@4.0.0-beta.11" has unmet peer dependency "webpack@^4.0.0".
warning " > less-loader@4.1.0" has unmet peer dependency "webpack@^2.0.0 || ^3.0.0 || ^4.0.0".
[4/4] Building fresh packages...
success Saved lockfile.
Done in 56.54s.
~~~


######运行工程

>yarn run serve

![image.png](https://upload-images.jianshu.io/upload_images/13965490-48e96794c462b26c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######打包
yarn build
下面的dist即是打包后的文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2c0ca7f1fbc9714b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######webstrom中使用yarn
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d189cd56fdc15d5c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
