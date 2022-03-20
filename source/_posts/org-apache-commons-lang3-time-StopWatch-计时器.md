---
title: org-apache-commons-lang3-time-StopWatch-计时器.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: org-apache-commons-lang3-time-StopWatch-计时器.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
~~~
     StopWatch started = StopWatch.createStarted();

        for (int i = 0; i <1000000 ; i++) {
            System.out.println(i);
        }
        started.suspend();

        long time = started.getTime(TimeUnit.SECONDS);
        System.out.println(time);

~~~
