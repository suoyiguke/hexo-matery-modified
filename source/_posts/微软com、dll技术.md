---
title: 微软com、dll技术.md
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
title: 微软com、dll技术.md
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
微软的 COM 技术生成的，它可以被多种语言如 C#、VC、
JavaScript、ASP 和 Delphi 方便的调用。


组件名为 XTXAppCOM.dll，包含一个应用接口类为 XTXApp,符合证书应用综
合服务接口--国密局规范。
XTXAppCOM.dll 通过证书应用环境安装。
XTXApp 对 应 的 `0CLSID`:3F367B74-92D9-4C5E-AB93-234F8A91D5E6 ， 对 应 的
ActiveX 对象名称为 "XTXAppCOM.XTXApp"，设备插拔时响应 OnUsbkeyChange 事
件。
