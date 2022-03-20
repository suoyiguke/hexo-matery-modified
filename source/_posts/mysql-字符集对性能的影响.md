---
title: mysql-字符集对性能的影响.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: mysql-字符集对性能的影响.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
** 解决方法：**

上面说了一大通，可能有点云里雾里，抱歉哈，我能力有限，不能把它解释得更通俗一些。

简而言之，就是证明了确实是字符集不一致，导致MySQL在语法解析的时候，对每一个用户输入的字符（MySQL关键字除外），都要进行若干次字符集检查，所以才会发生my_ismbchar_utf8mb4吃掉很多CPU资源这样一个故事 。

>要解决就很简单啦：保持character_set_server  &&  database characterset  &&  table characterset  &&  Client characterset一致！

我就是因为忽略了sysbench的字符集设置，所以才把自己给坑了。

既然sysbench没有提供字符集相关的选项和参数，那我就把MySQL的字符集统一成latin1来测吧（也可以去修改sysbench的mysql driver源码，让它支持设置字符集，但是我不擅长C……）

**最后总结：**

调整字符集之前，QPS最高只能压到73797，统一字符集之后，QPS达到了98272。  73797/98272*100%=75.09%

![image](https://upload-images.jianshu.io/upload_images/13965490-62c8baf0e30f66e1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

再来看看TPS，调整字符集之前，TPS最高只能压到3689，统一字符集之后，TPS达到了3689。  73797/4913*100%=75.08%

