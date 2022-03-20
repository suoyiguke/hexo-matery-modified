---
title: git使用笔记.md
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
title: git使用笔记.md
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
###基本用法
1、安装git
- linux安装git
~~~
yum -y install git
~~~
- windows安装

https://git-scm.com
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2870dc8c7b80772d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
一直使用缺省选项安装！一直下一步就行了
安装完了验证下
~~~
git --version
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e84269728cf5fd05.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、配置用户名和邮箱
- 全局配置

设置
~~~
git config --global user.name  "username"  
git config --global user.email  "email"
~~~
查看
~~~
//查看user.name 
git config user.name 
//查看user.email 
git config user.email
~~~



3、克隆项目
git clone https://github.com/xxxxxx/app_game.git

4、配置SSH
~~~
ssh-keygen -t rsa -C "github的账号用户名"
~~~
一直按回车
![image.png](https://upload-images.jianshu.io/upload_images/13965490-85425a9c53606540.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

cat 一下公钥地址，在控制台将公钥复制下来。 
~~~
cat /root/.ssh/id_rsa.pub
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-96ca05c919623ee1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

github网站右上角
![image.png](https://upload-images.jianshu.io/upload_images/13965490-509a3df076088372.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-a0484d1c8a10b8ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-22dbbccda5acf363.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

把长长的公钥字符串粘贴进去，点击 绿色按钮就行了~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b54cdd144e60cb00.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8af8d2eceb2d772b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


5、在使用git推送项目时候出现 “fatal: The remote end hung up unexpectedly ” 
原因是推送的文件太大。
在克隆/创建版本库生成的 .git目录下面修改生成的config文件增加如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a28cbaaa65577e3b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

6、git提交的忽略文件示例
编辑 .gitignore
~~~
# Compiled class file
*.class
.idea/
target/
/target/
/*.iml
tian


# Log file
*.log

# BlueJ files
*.ctxt

# Mobile Tools for Java (J2ME)
.mtj.tmp/

# Package Files #
*.war
*.ear
*.zip
*.tar.gz
*.rar
*.iml
.idea

# virtual machine crash logs, see http://www.java.com/en/download/help/error_hotspot.xml
hs_err_pid*
~~~

7、commit之后，想撤销commit

写完代码后，我们一般这样
~~~
git add . //添加所有文件
git commit -m "本功能全部完成"
~~~
执行完commit后，想撤回commit。可以执行

~~~
git reset --soft HEAD^
~~~
这样就成功的撤销了你的commit
注意，仅仅是撤回commit操作，您写的代码仍然保留。

8、git 导出版本之间差异文件

①、查看 commit id,首先用 git log 查看版本库日志，找出需要导出的 commit id  注意是前六位数
~~~
git log --pretty=oneline
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-676310e5d55ce12c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

②、找出差异文件，使用 git diff 命令可以查看提交之间的插件，使用 --name-only 参数只显示文件名
~~~
git diff 617810 3327ae --name-only
~~~
输出结果就是所有的差异文件，下面再使用 xargs 将文件进行下一步处理
③、将差异文件打包
~~~
git diff 617810 3327ae --name-only | xargs tar -czvf ../update-kk.tar.gz
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cb65d101d85b145c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-db258012ac38a762.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

9、修改git的remote url
①、修改项目的remote url
git remote set-url git@github.com:xxx/xxxx.git
②、查看
~~~
git remote -v
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4abe4e50d4236b53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###新建立一个库，推送项目到git仓库
~~~
git init
git add .
git remote add origin https://gitee.com/suoyiguke_yinkai/CAService.git
git commit -m "添加注释信息"
git push -u origin master -f
~~~

###在idea中操作git




####提交自己修改代码流程
1、在提交自己的修改之前注意先要pull最新的代码，防止冲突
![image.png](https://upload-images.jianshu.io/upload_images/13965490-65c912a799fb04fd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、提交自己的修改代码
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fc6668e26980b665.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、push之前也要pull一下最新的代码，防止冲突


4、push到git服务器

![image.png](https://upload-images.jianshu.io/upload_images/13965490-0a5c88e4ee473aa0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####分支开发
1、拉取/切换分支

![image.png](https://upload-images.jianshu.io/upload_images/13965490-e369e011f101c691.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-152d9c5f5c8e8f3d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、创建分支

小A接受了一个新功能的任务，创建了一个分支并在分支上开发
建分支也是一个常用的操作，例如临时修改bug、开发不确定是否加入的功能等，都可以创建一个分支，再等待合适的时机合并到主干。
创建流程如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-989f250b740b842b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3822d426b3a994b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、强制推送
>git push -f origin master

4、remove掉origin
>git remote remove origin


5、撤销commit
>git reset --soft HEAD^
