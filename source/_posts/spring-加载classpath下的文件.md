---
title: spring-加载classpath下的文件.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: spring-加载classpath下的文件.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
使用org.springframework.core.io.ClassPathResource类

pfxFileName传入文件名即可
~~~

    @PostConstruct
    void init() {
        ClassPathResource classPathResource = new ClassPathResource(File.separator + pfxFileName);
        try {
            ks = KeyStore.getInstance(keyStoreName);
            ks.load(classPathResource.getInputStream(), pfxPass.toCharArray());
            priv = (PrivateKey) ks.getKey(alias, pfxPass.toCharArray());
            rsa = Signature.getInstance(pfxSha);
            rsa.initSign(priv);
        } catch (Exception e) {
            logger.error(e.getMessage());
        }
    }

~~~
