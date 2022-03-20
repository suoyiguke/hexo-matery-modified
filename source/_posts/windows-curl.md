---
title: windows-curl.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
---
title: windows-curl.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
~~~
curl -X POST -H "Content-Type: application/json" -d "{\"businessOrgCode\": \"455767873\",\"businessSystemCode\":\"9998\",\"businessSystemAppID\":\"o7d7q8ehm4tkrc6o\"}" "http://testca.top:8077/v1.0/cloudsign/genloginqrcode"
~~~

~~~
curl -X POST -H "Content-Type: application/json" -d "{\"businessOrgCode\": \"455767873\",\"businessSystemCode\":\"9998\",\"businessSystemAppID\":\"o7d7q8ehm4tkrc6o\",\"relBizNo\":\"3420\"}" "http://10.169.130.27:8087/v1.0/cloudsign/getstamp"
~~~
