---
title: Caused-by--java-lang-IllegalArgumentException--The-class-'com-ruoyi-we.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mq-kafka
categories: mq-kafka
---
---
title: Caused-by--java-lang-IllegalArgumentException--The-class-'com-ruoyi-we.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mq-kafka
categories: mq-kafka
---
spring:
  kafka:
    consumer:
      properties:
        spring:
          json:
            trusted:
              packages: com.ruoyi.web.kafka


Caused by: java.lang.IllegalArgumentException: The class 'com.ruoyi.web.kafka.Demo01Message' is not in the trusted packages: [java.util, java.lang, cn.iocoder.springboot.lab03.kafkademo.message]. If you believe this class is safe to deserialize, please provide its name. If the serialization is only done by a trusted source, you can also enable trust all (*).
