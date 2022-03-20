---
title: cmd-命令.md
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
title: cmd-命令.md
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

1、无线循环 + 睡眠1秒
~~~
:loop  
netstat -ano |find /i /c "TIME_WAIT" 
choice /t 1 /d y /n >nul 
goto loop
~~~

2、for i 循环

~~~
ECHO Start of Loop
 
FOR /L %%i IN (1,1,10) DO (
  ECHO %%i
)
~~~

3、变量和执行其它bat
~~~
set tomcat_start="G:\job\wk\identity-authentication-services-commit\Scripts\RunServer.bat"
start call %tomcat_start%
~~~

4、退出
~~~
exit
~~~
