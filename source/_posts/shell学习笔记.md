---
title: shell学习笔记.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: shell
categories: shell
---
---
title: shell学习笔记.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: shell
categories: shell
---

1、开始一个hello world
- 编辑shell脚本
vi test.sh
~~~
#!/bin/bash
echo "Hello World !"
~~~

- 添加执行权限
~~~
chmod +x ./test.sh
~~~

- 执行
~~~
./test.sh
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-696ca3b2c1c6e937.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、shell的加减乘除余

~~~
#!/bin/bash

a=10
b=20
c1=`expr $b + $a`
echo "The result is $c1"

c2=`expr $b - $a`
echo "The result is $c2"


c3=`expr $b \* $a`
echo "The result is $c3"

c4=`expr $b / $a`
echo "The result is $c4"

c5=`expr 8 % 3`
echo "The result is  $c5"
~~~

3、判断文件夹是否存在，不存在则创建
~~~
#!/usr/bin/env bash
BACKUP_DIR="E:/java/shell/shell/src/test"

if [ ! -d $BACKUP_DIR ]
then mkdir -p $BACKUP_DIR
fi
~~~
4、shell时间操作

当前时间
~~~
time=$(date "+%Y-%m-%d %H:%M:%S")
echo $time
~~~

5、获取当前脚本的路径
~~~
IR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $IR
~~~
6、迭加计数，每次加一，类似i++
~~~
#!/bin/bash
i=0
count=$((${i} + 1))
~~~
7、数组的遍历
~~~
#定义数组
arrayIndex[0]=1
arrayIndex[1]=2
arrayIndex[2]=3
arrayIndex[3]=4
arrayIndex[4]=5
#打印数组长度

echo "arrayIndex数组长度：${#arrayIndex[@]}"

#for 遍历数组
i=0
for var in ${arrayIndex[@]}
do
  i=$((${i} + 1))
  echo "第$i个$var"
done
~~~

或者使用这种方法定义数组
arrayIndex=('a' 'b' 'c' 'd' 'e')

8、字符串截取
1、直接截取
~~~
#!/bin/bash
url="https://www.baidu.com.cn"
# 从左数
echo ${url: 8: 13}
# 从右数
echo ${url: 0-16: 13}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-79ef89235713f2e8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、使用grep命令
~~~
#!/bin/bash
var="http://www.aaa.com/root/123.htm"
#3.模糊匹配http.开头，root结尾
echo $var |grep -o 'www.*htm'
~~~
