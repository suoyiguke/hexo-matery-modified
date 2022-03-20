---
title: flutter环境搭建.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: flutter
categories: flutter
---
---
title: flutter环境搭建.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: flutter
categories: flutter
---
- 下载flutter-sdk

- 执行命令flutter doctor
第一次执行有点慢，我大概等了十分钟命令才有输出

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c2d6818030f8f201.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
Doctor summary (to see all details, run flutter doctor -v):
[√] Flutter (Channel stable, v1.12.13+hotfix.5, on Microsoft Windows [Version 10.0.14393], locale zh-CN)
[X] Android toolchain - develop for Android devices
    X Flutter requires Android SDK 28 and the Android BuildTools 28.0.3
      To update using sdkmanager, run:
        "G:\Android\android-sdk-windows\tools\bin\sdkmanager" "platforms;android-28" "build-tools;28.0.3"
      or visit https://flutter.dev/setup/#android-setup for detailed instructions.
[!] Android Studio (version 3.1)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] IntelliJ IDEA Ultimate Edition (version 2018.1)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] IntelliJ IDEA Ultimate Edition (version 2019.3)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] Connected device
    ! No devices available
~~~
- 安装 BuildTools 28.0.3
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d70167201677ca80.png?imageMogr2/autoorient/strip%7CimageView2/2/w/1240)

- 再次执行 flutter doctor
~~~
C:\Users\yinkai>flutter doctor
Doctor summary (to see all details, run flutter doctor -v):
[√] Flutter (Channel stable, v1.12.13+hotfix.5, on Microsoft Windows [Version 10.0.14393], locale zh-CN)
[!] Android toolchain - develop for Android devices (Android SDK version 28.0.3)
    X Android SDK file not found: G:\Android\android-sdk-windows\platforms\android-29\android.jar.
[!] Android Studio (version 3.1)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] IntelliJ IDEA Ultimate Edition (version 2018.1)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] IntelliJ IDEA Ultimate Edition (version 2019.3)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] Connected device
    ! No devices available
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-21f881174edf2b4e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 再次执行 flutter doctor
~~~
C:\Users\yinkai>flutter doctor
Doctor summary (to see all details, run flutter doctor -v):
[√] Flutter (Channel stable, v1.12.13+hotfix.5, on Microsoft Windows [Version 10.0.14393], locale zh-CN)
[!] Android toolchain - develop for Android devices (Android SDK version 28.0.3)
    X Android license status unknown.
      Try re-installing or updating your Android SDK Manager.
      See https://developer.android.com/studio/#downloads or visit https://flutter.dev/setup/#android-setup for detailed      instructions.
[!] Android Studio (version 3.1)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] IntelliJ IDEA Ultimate Edition (version 2018.1)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] IntelliJ IDEA Ultimate Edition (version 2019.3)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] Connected device
    ! No devices available

! Doctor found issues in 5 categories.
~~~
- 提示: Try re-installing or updating your Android SDK Manager.
 SDK Manager版本有问题

![image.png](https://upload-images.jianshu.io/upload_images/13965490-a7d6937c7a591eb9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 再次执行 flutter doctor

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7f9f4088050c9a0a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
C:\Users\yinkai>flutter doctor
Doctor summary (to see all details, run flutter doctor -v):
[√] Flutter (Channel stable, v1.12.13+hotfix.5, on Microsoft Windows [Version 10.0.14393], locale zh-CN)

[!] Android toolchain - develop for Android devices (Android SDK version 28.0.3)
    ! Some Android licenses not accepted.  To resolve this, run: flutter doctor --android-licenses
[!] Android Studio (version 3.1)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] IntelliJ IDEA Ultimate Edition (version 2018.1)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] IntelliJ IDEA Ultimate Edition (version 2019.3)
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
[!] Connected device
    ! No devices available

! Doctor found issues in 5 categories.

~~~

- 按照提示执行 flutter doctor --android-licenses
然后一直输入 y+回车

![image.png](https://upload-images.jianshu.io/upload_images/13965490-ed42f453d3bd5446.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 再次执行 flutter doctor

![image.png](https://upload-images.jianshu.io/upload_images/13965490-056252d4220ade54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 在Android  studio 里面安装两个插件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0f215a2ce07b89f3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-841711d006a3322d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
