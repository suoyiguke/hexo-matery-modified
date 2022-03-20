---
title: git-fock-主库到本用户下。进行提pull-request.md
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
title: git-fock-主库到本用户下。进行提pull-request.md
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
本用户下的库需要和主仓库进行同步代码，将仓库check到本地。就要 添加一个remote
>git remote add repo https://gitee.com/sglkj/identity-authentication-services.git
~~~
yinkai@DESKTOP-HVQ75BP MINGW64 /g/job/wk/identity-authentication-services (develop)
$ git remote -v
origin  https://gitee.com/suoyiguke_yinkai/identity-authentication-services.git (fetch)
origin  https://gitee.com/suoyiguke_yinkai/identity-authentication-services.git (push)

yinkai@DESKTOP-HVQ75BP MINGW64 /g/job/wk/identity-authentication-services (develop)
$ git add repo https://gitee.com/sglkj/identity-authentication-services.git
fatal: pathspec 'repo' did not match any files

yinkai@DESKTOP-HVQ75BP MINGW64 /g/job/wk/identity-authentication-services (develop)
$ git remote add repo https://gitee.com/sglkj/identity-authentication-services.git

yinkai@DESKTOP-HVQ75BP MINGW64 /g/job/wk/identity-authentication-services (develop)
$ git pull repo develop
remote: Enumerating objects: 1, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (1/1), 344 bytes | 3.00 KiB/s, done.
From https://gitee.com/sglkj/identity-authentication-services
 * branch            develop    -> FETCH_HEAD
 * [new branch]      develop    -> repo/develop
error: Your local changes to the following files would be overwritten by merge:
        config/application.properties
Please commit your changes or stash them before you merge.
Aborting
Updating 4163761..484624d

yinkai@DESKTOP-HVQ75BP MINGW64 /g/job/wk/identity-authentication-services (develop)
$ git checkout config/application.properties
Updated 1 path from the index

yinkai@DESKTOP-HVQ75BP MINGW64 /g/job/wk/identity-authentication-services (develop)
$ git pull repo develop
From https://gitee.com/sglkj/identity-authentication-services
 * branch            develop    -> FETCH_HEAD
Updating 4163761..484624d
Fast-forward
 config/CaHelper.properties                         |   2 +-
 config/application.properties                      |   7 +-
 pom.xml                                            |   2 +-
 .../szwj/ca/identityauthsrv/SchedulingHandler.java |   7 +-
 .../ca/identityauthsrv/constants/Constants.java    |  26 +-
 .../identityauthsrv/controller/CertController.java |   1 -
 .../controller/CloudsignController.java            | 167 +++++++++---
 .../controller/PatientSignController.java          | 301 +++++----------------
 .../identityauthsrv/controller/SignController.java |  27 +-
 .../identityauthsrv/controller/SsoController.java  |  65 +++--
 .../controller/VerifyController.java               |  10 +-
 .../controller/cloudsign/ICloudsignHelper.java     |   3 +
 .../controller/cloudsign/gdca/GdcaCloudsign.java   |   6 +
 .../controller/cloudsign/netca/NetcaCloudsign.java | 126 ++++++++-
 .../szwj/ca/identityauthsrv/dao/SignedPDFDAO.java  |  24 +-
 .../dao/cloudsign/CloudsignCertInfoDAO.java        |  14 +-
 .../identityauthsrv/entity/EventValueEntity.java   |  10 +
 .../entity/dao/SignedPDFDetailsPO.java             |  32 +--
 .../ca/identityauthsrv/entity/dao/SignedPDFPO.java |  12 +-
 .../entity/dao/cloudsign/CloudsignCertInfoPO.java  |  20 ++
 .../service/impl/CloudsignServiceImpl.java         | 190 ++++++++++++-
 .../service/impl/PatientSignServiceImpl.java       |   5 +
 .../service/impl/UkeyLoginServiceImpl.java         |   6 +-
 .../service/intfc/CloudsignService.java            |   5 +
 .../util/common/SignHelperUtils.java               |   3 +-
 25 files changed, 676 insertions(+), 395 deletions(-)

yinkai@DESKTOP-HVQ75BP MINGW64 /g/job/wk/identity-authentication-services (develop)
$

~~~
