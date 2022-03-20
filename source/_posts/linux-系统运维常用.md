---
title: linux-系统运维常用.md
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
title: linux-系统运维常用.md
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
###看各个程序占用cpu、内存百分比
ps -auxw|head -n 1;ps -auxw|sort -rn -k 4|head -n 5
~~~
[root@localhost ~]# ps -auxw|head -n 1;ps -auxw|sort -rn -k 4|head -n 5
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root      2381  0.2 37.5 3600096 706248 ?      Sl   5月06   8:34 /home/jdk/bin/java -Xms512m -Xmx512m -Xmn256m -Dnacos.standalone=true -Dnacos.member.list= -Djava.ext.dirs=/home/jdk/jre/lib/ext:/home/jdk/lib/ext -Xloggc:/home/ca/nacos/nacos-server-2.0.0-BETA/nacos/logs/nacos_gc.log -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M -Dloader.path=/home/ca/nacos/nacos-server-2.0.0-BETA/nacos/plugins/health,/home/ca/nacos/nacos-server-2.0.0-BETA/nacos/plugins/cmdb -Dnacos.home=/home/ca/nacos/nacos-server-2.0.0-BETA/nacos -jar /home/ca/nacos/nacos-server-2.0.0-BETA/nacos/target/nacos-server.jar --spring.config.additional-location=file:/home/ca/nacos/nacos-server-2.0.0-BETA/nacos/conf/ --logging.config=/home/ca/nacos/nacos-server-2.0.0-BETA/nacos/conf/nacos-logback.xml --server.max-http-header-size=524288 nacos.nacos
root      1154  0.0 21.5 3016700 404936 ?      Sl   5月05   2:50 /home/jdk/bin/java -jar identityauthsrv-2.0.6.1-ias-compatible.jar --server.port=8077
root      1329  0.0 12.7 1603556 239244 ?      Sl   5月05   1:32 /home/mysql/bin/mysqld --basedir=/home/mysql --datadir=/home/mysql/data --plugin-dir=/home/mysql/lib/plugin --user=root --log-error=/var/log/mariadb/mariadb.log --pid-file=/home/mysql/data/localhost.localdomain.pid --socket=/var/lib/mysql/mysql.sock
root      1001  0.0  0.7 573844 14768 ?        Ssl  5月05   0:20 /usr/bin/python -Es /usr/sbin/tuned -l -P
polkitd    741  0.0  0.5 538464 10640 ?        Ssl  5月05   0:00 /usr/lib/polkit-1/polkitd --no-debug
~~~




###看内存占用和剩余
free -m 以M为单位
free -g 以G为单位


###磁盘满了问题

![image.png](https://upload-images.jianshu.io/upload_images/13965490-fa7aee7ad8c7813c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

查看硬盘情况 df -h

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c428c921230e6465.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
/dev/mapper/centos-root分区的磁盘用完了

那么进入/根目录执行下
du --max-depth=1 -h   

可以查看当前目录下哪个目录占用最大逐一排查下去， 发现是 /var/lib/docker占用了9.6G
![image.png](https://upload-images.jianshu.io/upload_images/13965490-31b380b86ae39dbb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

那么就必须处理下这个目录了，这个是docker的镜像文件

