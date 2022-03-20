---
title: redis实现session.md
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
title: redis实现session.md
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
###用户登录时，插入redis
- key：
~~~
String key = Md5Utils.md5(admin.getAdminID() + admin.getPhoneNum());
~~~

- value：
~~~
  String uuid = UUIDUtils.getUUID();
~~~
- 注意登录接口需要返回 这个value值（token）
- 所有用户相关接口都需要传入这个token

- 每次登录都生成新的uuid做redis的value；所以一个设备登录了之后，另一台设备用同样的账号登录会挤掉之前的登录


###拦截器中判断：
- 要求请求需要传入requestId、adminId、phonenum，如果为空则return false
- requestId 等于计算出来的(redis的key对应的value）则return true，否则return false
- 
