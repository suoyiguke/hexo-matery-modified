---
title: 关于java类到底什么时候被初始化？.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: 关于java类到底什么时候被初始化？.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
只有当代码执行到调用了A类的方法时，才会去初始化A类。而且一个类只会初始化（装载）一次，后面再调用不用再初始化。

>idea中断点若里面有√则说明该类已经初始化，无√就是没有初始化。此时代码不会执行到这里来！


这种情况下，若authority只会取一种值。NetcaCloudsign和GdcaCloudsign 两个类只会初始化其中一个。
~~~
    /**
     * 根据颁发机构获取对应的接口实现类
     *
     * @return 接口实现类
     */
    static ICloudsignHelper GetCloudsignHelperImplByAuthority(String authority) {
        if (Constants.NETCA_AUTHORITY.equalsIgnoreCase(authority)) {
            return NetcaCloudsign.getInstance();
        } else if (Constants.GDCA_AUTHORITY.equalsIgnoreCase(authority)) {
            return GdcaCloudsign.getInstance();
        } else {
            return null;
        }
    }
~~~
