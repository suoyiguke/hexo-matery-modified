---
title: 找回因为切换分支丢失的未push的commit.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: git
categories: git
---
---
title: 找回因为切换分支丢失的未push的commit.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: git
categories: git
---
为了避免这种丢失coomit的问题，最后每次开发新需求先克隆一个新分支！

###git命令

先执行
~~~
git reflog
~~~

找到自己因为切换分支而丢失的未push的commit的id e2358dc 
~~~
$ git reflog
4f29558 (HEAD -> develop, origin/develop, origin/HEAD) HEAD@{0}: checkout: moving from master to develop
21eecb8 (tag: V2.2.8, admin/master, master) HEAD@{1}: checkout: moving from develop to master
4f29558 (HEAD -> develop, origin/develop, origin/HEAD) HEAD@{2}: checkout: moving from develop to develop
4f29558 (HEAD -> develop, origin/develop, origin/HEAD) HEAD@{3}: branch: Reset to origin/develop
ec41ed3 (repo/develop) HEAD@{4}: checkout: moving from develop to develop
ec41ed3 (repo/develop) HEAD@{5}: branch: Reset to repo/develop
e2358dc HEAD@{6}: commit: 删除redis自定义的切换数据库实现，使用spring.redis.database代替之
ec41ed3 (repo/develop) HEAD@{7}: checkout: moving from develop to develop
ec41ed3 (repo/develop) HEAD@{8}: branch: Reset to repo/develop
ec41ed3 (repo/develop) HEAD@{9}: checkout: moving from develop to develop
ec41ed3 (repo/develop) HEAD@{10}: branch: Reset to repo/develop
ec41ed3 (repo/develop) HEAD@{11}: checkout: moving from develop to develop
ec41ed3 (repo/develop) HEAD@{12}: branch: Reset to repo/develop
31f937d HEAD@{13}: pull --no-stat -v --progress repo develop: Merge made by the 'recursive' strategy.
dbc2915 HEAD@{14}: rebase (finish): returning to refs/heads/develop
dbc2915 HEAD@{15}: rebase (pick): 云签集成网证通token查询有效期接口
4f29558 (HEAD -> develop, origin/develop, origin/HEAD) HEAD@{16}: rebase (start):...skipping...
4f29558 (HEAD -> develop, origin/develop, origin/HEAD) HEAD@{0}: checkout: moving from master to develop
21eecb8 (tag: V2.2.8, admin/master, master) HEAD@{1}: checkout: moving from develop to master
4f29558 (HEAD -> develop, origin/develop, origin/HEAD) HEAD@{2}: checkout: moving from develop to develop
4f29558 (HEAD -> develop, origin/develop, origin/HEAD) HEAD@{3}: branch: Reset to origin/develop
ec41ed3 (repo/develop) HEAD@{4}: checkout: moving from develop to develop
ec41ed3 (repo/develop) HEAD@{5}: branch: Reset to repo/develop
e2358dc HEAD@{6}: commit: 删除redis自定义的切换数据库实现，使用spring.redis.database代替之
ec41ed3 (repo/develop) HEAD@{7}: checkout: moving from develop to develop
ec41ed3 (repo/develop) HEAD@{8}: branch: Reset to repo/develop
ec41ed3 (repo/develop) HEAD@{9}: checkout: moving from develop to develop
ec41ed3 (repo/develop) HEAD@{10}: branch: Reset to repo/develop
ec41ed3 (repo/develop) HEAD@{11}: checkout: moving from develop to develop
ec41ed3 (repo/develop) HEAD@{12}: branch: Reset to repo/develop
31f937d HEAD@{13}: pull --no-stat -v --progress repo develop: Merge made by the 'recursive' strategy.
dbc2915 HEAD@{14}: rebase (finish): returning to refs/heads/develop
dbc2915 HEAD@{15}: rebase (pick): 云签集成网证通token查询有效期接口
4f29558 (HEAD -> develop, origin/develop, origin/HEAD) HEAD@{16}: rebase (start): checkout origin/develop
9b2db59 HEAD@{17}: checkout: moving from 云签集成网证通token查询有效期接口 to develop
1b5c837 (云签集成网证通token查询有效期接口) HEAD@{18}: pull --no-stat -v --progress origin develop: Merge made by the 'recursive' strategy.
1f36bb5 (origin/云签集成网证通token查询有效期接口) HEAD@{19}: commit: 云签集成网证通token查询有效期接口
9b2db59 HEAD@{20}: checkout: moving from develop to 云签集成网证通token查询有效期接口
9b2db59 HEAD@{21}: commit: 云签集成网证通token查询有效期接口
fc2d373 HEAD@{22}: pull --no-stat -v --progress repo develop: Merge made by the 'recursive' strategy.
ad24ae3 HEAD@{23}: pull --no-stat -v --progress origin develop: Fast-forward
bb4e5c0 HEAD@{24}: checkout: moving from develop to develop
bb4e5c0 HEAD@{25}: branch: Reset to origin/develop
49923a7 HEAD@{26}: pull --no-stat -v --progress origin hh: Merge made by the 'recursive' strategy.
5060f3e HEAD@{27}: commit (merge): Merge branch 'develop' of https://gitee.com/sglkj/identity-authentication-services into develop
fff33dd HEAD@{28}: commit: 批量签名实现
5472927 HEAD@{29}: commit (merge): Merge branch 'develop' of https://gitee.com/sglkj/identity-authentication-services into develop

~~~

执行
~~~
git cherry-pick e2358dc 
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-121168d9cfd9803a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
已在特定分支下恢复！随后push即可

###也可以使用idea的git插件来做
