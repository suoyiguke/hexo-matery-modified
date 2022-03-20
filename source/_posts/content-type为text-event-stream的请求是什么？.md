---
title: content-type为text-event-stream的请求是什么？.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
---
title: content-type为text-event-stream的请求是什么？.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
最近学习webpack热更新时发现，有一个__webpack_hmr请求，content-type为text/event-stream，没有见过，所以学习记录下。

webpack热更新需要向浏览器推送信息，一般都会想到websocket，但是还有一种方式，叫做Server-Sent Events（简称SSE）。

SSE是websocket的一种轻型替代方案。

和websocket有以下几点不同：

- SSE是使用http协议，而websocket是一种单独的协议
- SSE是单向传输，只能服务端向客户端推送，websocket是双向
- SSE支持断点续传，websocket需要自己实现
- SSE支持发送自定义类型消息

###SSE的原理：
相当于客户端向服务器发起下载请求，数据不是一次性传输的数据包，而是数据流，不断的传输向客户端，类似于视频下载一样。
