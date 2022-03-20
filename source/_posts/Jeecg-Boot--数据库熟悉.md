---
title: Jeecg-Boot--数据库熟悉.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---
---
title: Jeecg-Boot--数据库熟悉.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---
 1、部门表 SELECT * FROM  sys_depart 
  
2、用户表 sys_user  (depart_ids 负责部门 org_code 机构编码)

3、管理员admin 的 部门id是 c6d7cb4deeac411cb3384b1b31278596


4、sys_org_code = A01 而不是 那个UUID，那个UUID其实是部门记录的id

5、记录在sys_org_code 字段中出现UUID的问题

SELECT number,sys_org_code FROM tb_box 
SELECT name,sys_org_code FROM tb_point
SELECT model,sys_org_code FROM tb_equipment 

手动去选择`所属部门就就会出现这个问题` 所以默认隐藏的那几个表单字段 ：创建者、创建时间、修改者、修改时间、所属部门都不要去改它！让它隐藏就好了！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-415cf992739e05f5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


6、redis中缓存了用户信息
![image.png](https://upload-images.jianshu.io/upload_images/13965490-18a9722b46b37afc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
所以有时候用户信息被改，如sys_org_code被改。不会及时出效果

代码如下 
org.jeecg.modules.system.service.impl.SysBaseApiImpl#getUserByName

![image.png](https://upload-images.jianshu.io/upload_images/13965490-a77a3d9d27705254.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

7、SysUser做修改 LoginUser做查询

SysUser和LoginUser要同步修改字段



8、sys_user_depart 用户部门多对多中间表
