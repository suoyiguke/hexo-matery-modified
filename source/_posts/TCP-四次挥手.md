---
title: TCP-四次挥手.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: TCP
categories: TCP
---
---
title: TCP-四次挥手.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: TCP
categories: TCP
---
>当被动方收到主动方的FIN报文通知时，它仅仅表示主动方没有数据再发送给被动方了。但未必被动方所有的数据都完整的发送给了主动方，所以被动方不会马上关闭SOCKET,它可能还需要发送一些数据给主动方后，再发送FIN报文给主动方，告诉主动方同意关闭连接，所以这里的ACK报文和FIN报文多数情况下都是分开发送的。



 1）第一次挥手：Client发送一个FIN，用来关闭Client到Server的数据传送，Client进入FIN_WAIT_1状态。

 2）第二次挥手：Server收到FIN后，发送一个ACK给Client，确认序号为收到序号+1（与SYN相同，一个FIN占用一个序号），Server进入CLOSE_WAIT状态。

 3）第三次挥手：Server发送一个FIN，用来关闭Server到Client的数据传送，Server进入LAST_ACK状态。

 4）第四次挥手：Client收到FIN后，Client进入TIME_WAIT状态，接着发送一个ACK给Server，确认序号为收到序号+1，Server进入CLOSED状态，完成四次挥手

通俗的说法

1）Client：我所有东西都说完了

2）Server：我已经全部听到了，但是等等我，我还没说完

3）Server：好了，我已经说完了

4）Client：好的，那我们的通信结束l

![image](//upload-images.jianshu.io/upload_images/5700006-5df84e66a25f23e5.png?imageMogr2/auto-orient/strip|imageView2/2/w/522/format/webp)



![image.png](https://upload-images.jianshu.io/upload_images/13965490-940c93a9c45f5365.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### MSL 时间

1、第三次握手之后客户端会进入TIME_WAIT
2、处于TIME_WAIT状态下的客户端会等待2MSL 时间后变成CLOSED状态

MSL是Maximum Segment Lifetime英文的缩写，中文可以译为“报文最大生存时间”，他是任何报文在网络上存在的最长时间，超过这个时间报文将被丢弃。

因为tcp报文（segment）是ip数据报（datagram）的数据部分，具体称谓请参见《数据在网络各层中的称呼》一文，而ip头中有一个TTL域，TTL是time to live的缩写，中文可以译为“生存时间”，这个生存时间是由源主机设置初始值但不是存的具体时间，而是存储了一个ip数据报可以经过的最大路由数，每经过一个处理他的路由器此值就减1，当此值为0则数据报将被丢弃，同时发送ICMP报文通知源主机。

RFC 793中规定MSL为2分钟，实际应用中常用的是30秒，1分钟和2分钟等。 windows是2分钟。


2MSL即两倍的MSL，TCP的TIME_WAIT状态也称为2MSL等待状态，当TCP的一端发起主动关闭，在发出最后一个ACK包后，即第3次握手完成后发送了第四次握手的ACK包后就进入了TIME_WAIT状态，必须在此状态上停留两倍的MSL时间，等待2MSL时间主要目的是怕最后一个ACK包对方没收到，那么对方在超时后将重发第三次握手的FIN包，主动关闭端接到重发的FIN包后可以再发一个ACK应答包。在TIME_WAIT状态时两端的端口不能使用，要等到2MSL时间结束才可继续使用。当连接处于2MSL等待阶段时任何迟到的报文段都将被丢弃。不过在实际应用中可以通过设置SO_REUSEADDR选项达到不必等待2MSL时间结束再使用此端口。 
TTL与MSL是有关系的但不是简单的相等的关系，MSL要大于等于TTL。

> 若MSL时间过小，则会造成服务器端last_ack状态下的tcp连接过多。

###last_ack状态下的关闭连接策略
last_ack状态下的tcp会使用 保活计时器（keepalive timer）
若一定时间内（默认两小时）没有收到客户端的数据，服务器就发送一个探测报文段，以后每隔一段时间（默认75分钟）再发送一次，若10次都无响应，则关闭这个连接。



###情景模拟
我：远程发给我
李旭：好的，稍等
李旭：远程发给你：12121321321  123213
我：ok



![image.png](https://upload-images.jianshu.io/upload_images/13965490-251f8aaf1149e24a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###为什么客户端要进入TIME_WAIT状态并且等待2MSL
从上面可以看到，主动发起关闭连接的操作的一方将达到TIME_WAIT状态，而且这个状态要保持Maximum Segment Lifetime的两倍时间。为什么要这样做而不是直接进入CLOSED状态？

原因有二：
一、保证TCP协议的全双工连接能够可靠关闭
二、保证这次连接的重复数据段从网络中消失

先说第一点，如果Client直接CLOSED了，那么由于IP协议的不可靠性或者是其它网络原因，导致Server没有收到Client最后回复的ACK。那么Server就会在超时之后继续发送FIN，此时由于Client已经CLOSED了，就找不到与重发的FIN对应的连接，最后Server就会收到RST而不是ACK，Server就会以为是连接错误把问题报告给高层。这样的情况虽然不会造成数据丢失，但是却导致TCP协议不符合可靠连接的要求。所以，Client不是直接进入CLOSED，而是要保持TIME_WAIT，当再次收到FIN的时候，能够保证对方收到ACK，最后正确的关闭连接。

再说第二点，如果Client直接CLOSED，然后又再向Server发起一个新连接，我们不能保证这个新连接与刚关闭的连接的端口号是不同的。也就是说有可能新连接和老连接的端口号是相同的。一般来说不会发生什么问题，但是还是有特殊情况出现：假设新连接和已经关闭的老连接端口号是一样的，如果前一次连接的某些数据仍然滞留在网络中，这些延迟数据在建立新连接之后才到达Server，由于新连接和老连接的端口号是一样的，又因为TCP协议判断不同连接的依据是socket pair，于是，TCP协议就认为那个延迟的数据是属于新连接的，这样就和真正的新连接的数据包发生混淆了。所以TCP连接还要在TIME_WAIT状态等待2倍MSL，这样可以保证本次连接的所有数据都从网络中消失。

各种协议都是前人千锤百炼后得到的标准，规范。从细节中都能感受到精巧和严谨。每次深入都有同一个感觉，精妙。


windows系统怎么修改MSL时间？可以看看这篇 https://www.jianshu.com/p/9ee0166aa01c
linuxfmysql
