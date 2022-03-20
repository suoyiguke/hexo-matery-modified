---
title: Elasticsearch7-6-2.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 全文搜索
categories: 全文搜索
---
---
title: Elasticsearch7-6-2.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 全文搜索
categories: 全文搜索
---
###安装和注册服务启动
[root@localhost ~]# rpm -ivh elasticsearch-7.15.1-x86_64.rpm 
警告：elasticsearch-7.15.1-x86_64.rpm: 头V4 RSA/SHA512 Signature, 密钥 ID d88e42b4: NOKEY
准备中...                          ################################# [100%]
Creating elasticsearch group... OK
Creating elasticsearch user... OK
正在升级/安装...
   1:elasticsearch-0:7.15.1-1         ################################# [100%]
### NOT starting on installation, please execute the following statements to configure elasticsearch service to start automatically using systemd
~~~
 sudo systemctl daemon-reload
 sudo systemctl enable elasticsearch.service
~~~
### You can start elasticsearch service by executing
~~~
 sudo systemctl start elasticsearch.service
~~~
warning: usage of JAVA_HOME is deprecated, use ES_JAVA_HOME
Future versions of Elasticsearch will require Java 11; your Java version from [/root/jdk1.8.0_144/jre] does not meet this requirement. Consider switching to a distribution of Elasticsearch with a bundled JDK. If you are already using a distribution with a bundled JDK, ensure the JAVA_HOME environment variable is not set.
Created elasticsearch keystore in /etc/elasticsearch/elasticsearch.keystore
[root@localhost ~]# 


es的端口是9200
~~~
[root@localhost ~]# lsof -i:9200
COMMAND  PID          USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
java    1489 elasticsearch  289u  IPv6  22829      0t0  TCP localhost:wap-wsp (LISTEN)
java    1489 elasticsearch  290u  IPv6  22830      0t0  TCP localhost:wap-wsp (LISTEN)

~~~



###开启远程访问
修改/etc/elasticsearch/elasticsearch.yml文件，使其可以支持任意主机访问
~~~
network.host: 0.0.0.0
http.port: 9200
~~~
###重启
sudo systemctl restart elasticsearch.service
查看启动状态
 sudo systemctl status elasticsearch.service



###tar安装

在 Linux 环境中，elasticsearch 不允许以 root 权限来运行！所以需要创建一个非root用户，以非root用户来起es，这里我直接有创建好的非root用户。

或者也可以通过网上方法：
~~~
创建elsearch用户组及elsearch用户
groupadd elsearch
useradd elsearch -g elsearch -p elasticsearch
~~~
2.更改文件夹及内部文件的所属用户及组为elsearch:elsearch

chown -R elsearch:elsearch <ElasticSearch>



启动
~~~
[elsearch@localhost ~]$ cd /data/elasticsearch-6.7.2/bin/
[elsearch@localhost bin]$ ./elasticsearc
~~~


###启动问题
1、linux 打开文件数量限制
ERROR: [2] bootstrap checks failed
[1]: max file descriptors [4096] for elasticsearch process is too low, increase to at least [65535]
[2]: max number of threads [3833] for user [elsearch] is too low, increase to at least [4096]

2、

ERROR: [1] bootstrap checks failed
[1]: max number of threads [4069] for user [elsearch] is too low, increase to at least [4096]


解决： vi /etc/security/limits.conf  添加后reboot即可
~~~
*               soft    nofile            65536
*               hard    nofile            131072
*               hard    nproc             4096
*               soft    nproc             2096
~~~

http://192.168.2.155:9200/


