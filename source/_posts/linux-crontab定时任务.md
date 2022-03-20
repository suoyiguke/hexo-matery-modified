---
title: linux-crontab定时任务.md
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
title: linux-crontab定时任务.md
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

###安装
~~~
yum -y install crontab
~~~
###使用示例
1、编写shell脚本文件
vi /data/docker/mysql/slave/test.sh
~~~
#!/bin/sh
echo hello >> /home/hello.txt
~~~
2、编辑crontab 文件
~~~
crontab -e 
~~~
输入下面命令；表示每秒钟执行一次test.sh文件
~~~
* * * * * bash /data/docker/mysql/slave/test.sh
~~~
保存退出
3、编辑完重启服务
~~~
systemctl restart crond 
~~~
4、查看/home/hello.txt文件变更情况
~~~
tail -f /home/hello.txt
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-44c8b143f5435ede.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###查看crond 状态
~~~
service crond status
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-edec4e8a8bacde90.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###查看当前用户的crontab 
~~~
crontab -l
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3e454c3e2ffa2845.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 
###任务示例
####定时请求某一个url 
每天03点00去请求百度
~~~
00 03 * * * /usr/bin/curl http://www.baidu.com
~~~
注意:一定要加上这个 /usr/bin/curl

####每分钟执行一次
~~~
* * * * * bash /data/docker/mysql/slave/test.sh
~~~

####每隔十秒执行一次
~~~

* * * * * sleep 10; /bin/php /www/web/test.php

* * * * * sleep 20; /bin/php /www/web/test.php

* * * * * sleep 30; /bin/php /www/web/test.php

* * * * * sleep 40; /bin/php /www/web/test.php

* * * * * sleep50; /bin/php /www/web/test.php

每五分钟执行  */5 * * * *  /bin/php /www/web/test.php

每小时执行     0 * * * *  /bin/php /www/web/test.php

每天执行       0 0 * * *  /bin/php /www/web/test.php

每周执行       0 0 * * 0  /bin/php /www/web/test.php

每月执行       0 0 1 * *  /bin/php /www/web/test.php

每年执行       0 0 1 1 *  /bin/php /www/web/test.php
~~~
###crontab的输出日志
1、错误和正确的日志都被纪录到 /tmp/load.log
~~~
* * * * * bash /data/docker/mysql/slave/test.sh > /tmp/load.log 2>&1 &
~~~
