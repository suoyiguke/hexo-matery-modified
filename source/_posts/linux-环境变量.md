---
title: linux-环境变量.md
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
title: linux-环境变量.md
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

###$PATH环境变量详解
首先就要考虑root 的$PATH里是否已经包含了这些环境变量。 

主要是这四个：/bin ,/usr/bin,/sbin,/usr/sbin。 



./bin: 

bin为binary的简写主要放置一些系统的必备执行档例如:cat、cp、chmod df、dmesg、gzip、kill、ls、mkdir、more、mount、rm、su、tar等。 

/usr/bin: 
主要放置一些应用软体工具的必备执行档例如c++、g++、gcc、chdrv、diff、dig、du、eject、elm、free、gnome*、 gzip、htpasswd、kfm、ktop、last、less、locale、m4、make、man、mcopy、ncftp、 newaliases、nslookup passwd、quota、smb*、wget等。 


/sbin: 
主要放置一些系统管理的必备程式例如:cfdisk、dhcpcd、dump、e2fsck、fdisk、halt、ifconfig、ifup、 ifdown、init、insmod、lilo、lsmod、mke2fs、modprobe、quotacheck、reboot、rmmod、 runlevel、shutdown等。 


/usr/sbin: 
放置一些网路管理的必备程式例如:dhcpd、httpd、imap、in.*d、inetd、lpd、named、netconfig、nmbd、samba、sendmail、squid、swap、tcpd、tcpdump等。 
