---
title: linux常用命令.md
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
title: linux常用命令.md
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
###压缩和解压
1、.gz
解压 gzip -d 2020_01_28.sql.gz
2、zip
unzip
3、tar
tar -xvf 


###文件和目录
1、查看目录结构
yum -y install tree
![image.png](https://upload-images.jianshu.io/upload_images/13965490-760e5d6d219b6eaa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、在文件追加一行
echo 'add content'>>test.sh

3、覆盖
echo 'add content'>test.sh

5、监视文件变动
tail -f test.txt
6、删除
rm -rf xxx
删除几个文件  rm 文件1 文件2
删除文件夹下面所有文件  rm * -rf
删除某些固定字母开头的文件  rm  xxx* 
删除一类文件         rm   *.txt

7、移动和重命名
mv old new
8、授权
chmod 777 -R *
可执行授权 chmod +x xx.sh
9、查看当前目录下所有文件和文件夹
ls -la 或 ll
10、复制
cp file newFile
11、清空文件
\> file.txt
12、将当前文件夹内所有文件移动到上级目录
mv * ../

###系统类
1、重启
  reboot

2、查看网卡信息和ip
ip addr 或 ifconfig

3、查看物理CPU个数
~~~
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l
~~~
4、查看每个物理CPU中core的个数(即核数)
~~~
cat /proc/cpuinfo| grep "cpu cores"| uniq
~~~
5、查看逻辑CPU的个数
~~~
cat /proc/cpuinfo| grep "processor"| wc -l
~~~
6、查看CPU信息（型号）
~~~
cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c
~~~

7、查看端口占用
~~~
netstat -antp|grep 8080
~~~

8、查看进程的pid
~~~
ps -ef |grep java
~~~

9、杀死指定pid的进程
~~~
kill -9 pidxxx
~~~
10、直接杀死包含关键词java 的进程
~~~
 ps -ef | grep java | grep -v grep | awk '{print $2}' | xargs kill -9
~~~

###安装软件类
1、安装git

yum -y install git

###xshell连接linux使用
1、上传文件
~~~
yum   -y  install  lrzsz
~~~
2、rz -y


