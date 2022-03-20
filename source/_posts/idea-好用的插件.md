---
title: idea-好用的插件.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开发工具
categories: 开发工具
---
---
title: idea-好用的插件.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开发工具
categories: 开发工具
---
###Key Promoter X
快捷键熟悉

###`必装`mybatis-log-plugin
sql执行完整日志打印
这个已经收费了，可以使用github上。
https://github.com/Link-Kou/intellij-mybaitslog

这个插件生效的前提是mybatis的打印sql日志已经配置：
~~~
#mybatis部分
log4j.logger.com.ibatis=DEBUG
log4j.logger.com.ibatis.common.jdbc.SimpleDataSource=DEBUG
log4j.logger.com.ibatis.common.jdbc.ScriptRunner=DEBUG
log4j.logger.com.ibatis.sqlmap.engine.impl.SqlMapClientDelegate=DEBUG
#与sql相关
log4j.logger.java.sql.Connection=DEBUG
log4j.logger.java.sql.Statement=DEBUG
log4j.logger.java.sql.PreparedStatement=DEBUG
~~~

### `必装`alibaba 代码规范检测


###`必装`SGsonFormat
根据json生成javabean
将光标放到空的类文件里，ALT + S 或这样调出面板
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aba05d8e57f0e9a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

输入json字符串转换即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5afad0d73ca7982a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###Grep Console 日志颜色


###JUnitGenerator 单元测试

###findbugs

![image.png](https://upload-images.jianshu.io/upload_images/13965490-584823557140f8d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f85bad93e93d961e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###JProfiler
内存分析插件

![image.png](https://upload-images.jianshu.io/upload_images/13965490-cc71452a5b19b3d1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
需要先下载一个exe
https://www.ej-technologies.com/download/jprofiler/files

###`必装`GenerateAllSetter
生成调用对象的set方法

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7df3907d87bfe167.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


输入allSet 按tab键生成即可


###`必装`mybatisx
java类和xml一一映射,点击互相跳转

在线安装
https://plugins.jetbrains.com/plugin/10119-mybatisx/versions/

![image.png](https://upload-images.jianshu.io/upload_images/13965490-a4782f964f44a818.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###Translation
翻译
https://plugins.jetbrains.com/plugin/8579-translation

###`必装`CameLCase
https://plugins.jetbrains.com/plugin/7160-camelcase
Shift + Alt + U 切换下划线和驼峰写法
Editor.CameLCase 这里可以进行各种风格命名的设置
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bf769251c3ee141a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###164-ideavim
http://plugins.jetbrains.com/plugin/164-ideavim
默认开启/关闭Vim模拟器快捷键是Ctrl+Alt+v




###`必装`save action

![image.png](https://upload-images.jianshu.io/upload_images/13965490-bf88e5e781fb327b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- ctivate save actions on save，在save的时候激活，通常是crtl+s的时候
- add missing @Override，在actions激活的时候直接添加override（免得你以后忘记下了）
- add a serialVersionUID，自动添加序列化id，这个在dubbo对外开放接口的时候经常会忘记，现在可以自动添加了
- optimize imports，没有用的imports代码全部删除掉，免得以后自己按快捷键删了。。
其他功能，咱就不一一说了，看下英语提示即可

###`必装`Codota 

用了Codota 后不再怕对API不会用，举个栗子：当我们用stream().filter()对List操作，可是对filter()用法不熟，按常理我们会百度一下，而用Codota 会提示很多filter()用法，节省不少查阅资料的时间。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b30aa7d53fd5da50.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###TabNine
