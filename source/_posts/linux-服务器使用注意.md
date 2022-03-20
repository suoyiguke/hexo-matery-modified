---
title: linux-服务器使用注意.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
---
title: linux-服务器使用注意.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
1、授权一定要注意

chmod 777 -R ./*  不要把前面的点号落下了。否则将对服务器所有文件授权！若对ssh文件也授权777了。则下次的ssh连接就连不上了

2、没有使用docker时候，直接java -jar xxx.jar 运行，退出客户端后程序也跟着退出了。注意需要后台启动
~~~
1、
（1）执行java -jar xxx.jar后
（2）ctrl+z 退出到控制台,执行 bg
（3）exit
完成以上3步，退出SHELL后，jar服务一直在后台运行。

3、
nohup java -jar xxxx.jar & 
将java -jar xxxx.jar 加入  nohup   &中间，也可以实现
~~~


4、不小心把/etc/profile环境变量中的Path修改了，source /etc/profile 刷新配置后各种基础命令都不生效。

 如输入ls: 出现 -bash: ls: command not found 、输入 ipconfig 出现 -bash: ipconfig: command not found
 先 echo $PATH  发现  .显示JAVA_HOME/bin:.PATH:/root/bin

原因：在设置path环境变量时，编辑profile文件没有写正确，导致在命令行下命令不能够识别。

解决方案：手动设置path
~~~
 export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
~~~
再echo $PATH  发现  .显示 /usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
然后就可以使用vi去修改  /etc/profile了
到上面只会对此次登陆的shell有效，要是永久可用，必须再做如下：
~~~
#set java environment
JAVA_HOME=/usr/lib/jvm/jre-1.6.0-openjdk.x86_64
PATH=$PATH:$JAVA_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME CLASSPATH PATH
~~~

5、linux上最好不要去解压rar格式的压缩包

rar格式再linux上需要 yum -y install rar 安装rar依赖。而这个依赖很难下载。所以最好使用zip的格式


6、升级pyhon2到py3时需注意
不要卸载py2，这样会导致yum使用不了！linux很多核心功能依赖于py2
