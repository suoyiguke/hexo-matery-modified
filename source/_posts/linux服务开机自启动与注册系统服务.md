---
title: linux服务开机自启动与注册系统服务.md
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
title: linux服务开机自启动与注册系统服务.md
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
1、  注册系统服务
我想使用"service xxxx start"这样的简短命令来管理，就必须注册成为系统服务，那就是在目录 /etc/init.d/ 下，新建一个以服务名为文件名的文件。

如果我们打开目录 /etc/init.d/，看到的文件其实都是服务程序文件，每个文件的内容都大同小异，我们会看到，这里的文件在文件结构上几乎是一样的。几乎每个文件都有 start、stop、restart和status这样的标志，对，我们新建的这个文件也必须具有相同的结构，即可以接受start和stop参数并完成相应的操作。可以这么理解：

service httpd 等价 /etc/rc.d/init.d/httpd

service httpd start 等价 /etc/rc.d/init.d/httpd  start

service httpd stop 等价 /etc/rc.d/init.d/httpd  stop

所以/etc/init.d/下的这个脚本一般都会有start、stop等方法。这里可以参考mysql公司提供的写好的mysqld，所以我们装mysql的时候一般都会cp mysql.server /etc/init.d/mysql。
