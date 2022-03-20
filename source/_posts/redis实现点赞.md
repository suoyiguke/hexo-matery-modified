---
title: redis实现点赞.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
---
title: redis实现点赞.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
用 Redis 存储两种数据
- 一种是记录点赞人、被点赞人、点赞状态的数据，另一种是每个-
- 用户被点赞了多少次，做个简单的计数。

由于需要记录点赞人和被点赞人，还有点赞状态（点赞、取消点赞），还要固定时间间隔取出 Redis 中所有点赞数据，分析了下 Redis 数据格式中 Hash 最合适。

因为 Hash 里的数据都是存在一个键里，可以通过这个键很方便的把所有的点赞数据都取出。这个键里面的数据还可以存成键值对的形式，方便存入点赞人、被点赞人和点赞状态。

设点赞人的 id 为 likedPostId，被点赞人的 id 为 likedUserId ，点赞时状态为 1，取消点赞状态为 0。将点赞人 id 和被点赞人 id 作为键，两个 id 中间用 :: 隔开，点赞状态作为值。

所以如果用户点赞，存储的键为：likedUserId::likedPostId，对应的值为 1 。

取消点赞，存储的键为：likedUserId::likedPostId，对应的值为 0 。

取数据时把键用 :: 切开就得到了两个id，也很方便。


![image.png](https://upload-images.jianshu.io/upload_images/13965490-7c80062efd3fd430.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
