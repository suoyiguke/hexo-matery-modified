---
title: TCP-三次握手.md
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
title: TCP-三次握手.md
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
>TCP位于传输层，作用是提供可靠的字节流服务，为了准确无误地将数据送达目的地，TCP协议采纳三次握手策略。



1）发送端首先发送一个带有SYN（synchronize）标志地数据包给接收方。

2）接收方接收后，回传一个带有SYN/ACK标志的数据包传递确认信息，表示我收到了。

3）最后，发送方再回传一个带有ACK标志的数据包，代表我知道了，表示’握手‘结束。

通俗的说法

1）Client：嘿，李四，是我，听到了吗？

2）Server：我听到了，你能听到我的吗?

3）Client：好的，我们互相都能听到对方的话，我们的通信可以开始了。

![image](//upload-images.jianshu.io/upload_images/5700006-fffa4f696b215e66.png?imageMogr2/auto-orient/strip|imageView2/2/w/486/format/webp)
