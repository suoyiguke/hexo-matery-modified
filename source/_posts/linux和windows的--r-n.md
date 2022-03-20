---
title: linux和windows的--r-n.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
---
title: linux和windows的--r-n.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
\n   为ASCII的0x0a   换行 
\r   为ASCII的0x0d   回车 

在linux下的回车键只代表\n，linux/unix下只用\n,它就表示回车+换行 
而在windows下的回车键表示\r\n  \n为进入下一行,\r为打印头回到行首上，而windows下,\r只回车不换行的,\n是换行,但在有些编辑中,单独的\n是不会换行的(如notepad) 
             

>一般在程序中,写\n就可以了,它在linux或windows中都能实现回车+换行的功能(只是在文本文件中,linux只会有0x0a,windows会自动换为0x0d   0x0a)

linux中不能识别\r的，所以在java代码里需要把所有的\r干掉！不然字符串里可能多出其它字符！



兼容Windows和linux的写法
~~~~
 sourceData.replaceAll("\r|\n", "");
~~~~
