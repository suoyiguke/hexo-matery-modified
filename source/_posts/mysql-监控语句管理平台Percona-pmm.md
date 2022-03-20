---
title: mysql-监控语句管理平台Percona-pmm.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: mysql-监控语句管理平台Percona-pmm.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---


> zabbix、Lepus、PMM 都是比较出名的数据库监控软件

Percona监控和管理（PMM）是一个用于管理和监控MySQL和MongoDB性能的开源平台。 它由Percona与托管数据库服务，支持和咨询领域的专家合作开发。 PMM是一个免费的开源解决方案，您可以在自己的环境中运行，以实现最大的安全性和可靠性。 它为MySQL和MongoDB服务器提供全面的基于时间的分析，以确保您的数据尽可能高效地工作。
包含以下模块：
1）PMM Client安装在您要监视的每个数据库主机上。它收集服务器指标，一般系统指标和查询分析数据，以获得完整的性能概述。收集的数据发送到PMM服务器。
2）PMM Server是PMM的核心部分，它聚合收集的数据，并以Web界面的表格，仪表板和图形的形式呈现。



~~~
[root@localhost ~]# docker search pmm-client
~~~


###docke安装 PMM Server 
1、下载PMM Server Docker镜像

docker create -v /opt/prometheus/data -v /opt/consul-data -v /var/lib/mysql -v /var/lib/grafana --name pmm-data percona/pmm-server:1.14.1 /bin/true

2、启动

docker run -d -p 80:80  --volumes-from pmm-data --name pmm-server --restart always percona/pmm-server:1.14.1
端口默认是 80 ，如果80端口被占用，可改为其它端口号   比如 81

3、查看docker运行状态

[root@open-falcon mysql]# docker ps
CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS              PORTS                         NAMES
59455e7fa828        percona/pmm-server:1.14.1   "/opt/entrypoint.sh"     18 hours ago        Up 7 minutes        443/tcp, 0.0.0.0:81->80/tcp   pmm-server


###安装pmm-client客户端。

wget https://www.percona.com/downloads/pmm-client/pmm-client-1.14.1/binary/tarball/pmm-client-1.14.1.tar.gz
tar -zxvf pmm-client-1.14.1.tar.gz
cd pmm-client-1.14.1 && ./install
此时你会发现可以使用pmm-admin指令

###客户端开始上报数据
pmm-client 客户端执行命令

1、先连接服务端
~~~
pmm-admin config --server 192.168.6.128:80
~~~

2、检查server和clilen的连接情况

>pmm-admin check-network
~~~
[root@localhost percona]# pmm-admin check-network
PMM Network Status

Server Address | 192.168.6.128:80
Client Address | 192.168.6.128 

* System Time
NTP Server (0.pool.ntp.org)         | 2020-11-06 08:20:30 +0000 UTC
PMM Server                          | 2020-11-06 08:20:17 +0000 GMT
PMM Client                          | 2020-11-06 16:20:23 +0800 CST
PMM Server Time Drift               | OK
PMM Client Time Drift               | OK
PMM Client to PMM Server Time Drift | OK

* Connection: Client --> Server
-------------------- -------      
SERVER SERVICE       STATUS       
-------------------- -------      
Consul API           OK
Prometheus API       OK
Query Analytics API  OK

Connection duration | 670.79µs
Request duration    | 6.775517ms
Full round trip     | 7.446307ms


* Connection: Client <-- Server
-------------- ------ -------------------- ------- ---------- ---------
SERVICE TYPE   NAME   REMOTE ENDPOINT      STATUS  HTTPS/TLS  PASSWORD 
-------------- ------ -------------------- ------- ---------- ---------
linux:metrics  mysql  192.168.6.128:42000  OK      YES        -        
mysql:metrics  mysql  192.168.6.128:42002  OK      YES        -    
~~~


3、开始上报指定mysql的数据
~~~
pmm-admin add mysql --host 192.168.1.126 --port 3306 --user root --password Sgl20@14 &
~~~


--server 192.168.6.128:80 指定PMM Server 的host
--server-user PMM Server 用户账号
--server-password PMM Server 用户密码

4、查看上报配置
>pmm-admin list
~~~
[root@localhost percona]# pmm-admin list
pmm-admin 1.14.1

PMM Server      | 192.168.6.128:80 
Client Name     | mysql
Client Address  | 192.168.6.128 
Service Manager | linux-systemd

-------------- ------ ----------- -------- --------------------------------- ---------------------------------------------
SERVICE TYPE   NAME   LOCAL PORT  RUNNING  DATA SOURCE                       OPTIONS                                      
-------------- ------ ----------- -------- --------------------------------- ---------------------------------------------
mysql:queries  mysql  -           YES      root:***@tcp(192.168.1.126:3306)  query_source=perfschema, query_examples=true 
linux:metrics  mysql  42000       YES      -                                                                              
mysql:metrics  mysql  42002       YES      -    
~~~

###
### 六、查看监控和管理平台

使用运行PMM Server的主机的IP地址访问PMM Web界面。目标网页链接到相应的PMM工具：

| Component | URL | 备注 |
| --- | --- | --- |
| PMM landing page | [http://10.10.0.188](http://10.10.0.188/) | PMM跳转页 |
| Query Analytics (QAN web app) | [http://10.10.0.188/qan](http://10.10.0.188/qan) | SQL慢日志分析 |
| Metrics Monitor (Grafana) | [http://10.10.0.188/graph](http://10.10.0.188/graph) | user name: admin password: admin监控指标图表 |
| Orchestrator | [http://10.10.0.188/orchestrator](http://10.10.0.188/orchestrator) | MySQL集群拓扑结构 |



###面版记录
1、MySQL Overview
2、MySQL Table Statistics
3、PMM Query Analytics 慢查询日志
