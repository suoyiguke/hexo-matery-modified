---
title: linux-防火墙设置.md
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
title: linux-防火墙设置.md
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
CentOS 7.0默认使用的是firewall作为防火墙，之前版本是使用iptables。 
所以在CentOS 7执行下面命令是无法查看防火墙状态的。

```
service iptables status
Redirecting to /bin/systemctl status iptables.service
Unit iptables.service could not be found.

```

### 查看防火墙是否关闭

firewall-cmd –state

```
[root@localhost ~]# firewall-cmd --state
not running
[root@localhost ~]#
```

### 开启防火墙

```
[root@localhost ~]# systemctl start firewalld
[root@localhost ~]# firewall-cmd --state
running
[root@localhost ~]# 

```

### 关闭防火墙

```
[root@localhost ~]# systemctl stop firewalld
[root@localhost ~]# firewall-cmd --state
not running
[root@localhost ~]# 

```

### 禁止firewall开机启动

```
[root@localhost ~]# systemctl disable firewalld
Removed symlink /etc/systemd/system/multi-user.target.wants/firewalld.service.
Removed symlink /etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service.
```

这样设置的话，下次重启开机的时候就会禁止firewall的启动，即关闭状态。

### 设置firewall开机启动

```
[root@localhost ~]# systemctl enable firewalld
Created symlink from /etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service to /usr/lib/systemd/system/firewalld.service.
Created symlink from /etc/systemd/system/multi-user.target.wants/firewalld.service to /usr/lib/systemd/system/firewalld.service.

```

这样设置之后，开机就会自动开启防火墙。

### 显示防火墙应用列表

```
[root@localhost ~]# firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: ens33
  sources: 
  services: ssh dhcpv6-client
  ports: 
  protocols: 
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 

[root@localhost ~]# firewall-cmd --add-service=ftp
success
[root@localhost ~]# firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: ens33
  sources: 
  services: ssh dhcpv6-client ftp
  ports: 
  protocols: 
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 

[root@localhost ~]# 

```

使用`firewall-cmd --add-service=ftp` 之后，列表显示出多了一个ftp服务。
