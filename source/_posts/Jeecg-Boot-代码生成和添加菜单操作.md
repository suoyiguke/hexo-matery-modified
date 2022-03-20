---
title: Jeecg-Boot-代码生成和添加菜单操作.md
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
title: Jeecg-Boot-代码生成和添加菜单操作.md
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
> 永远在时光中充满激情

###数据准备
首先创建一张mysql表 名为tb_test
~~~

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_test
-- ----------------------------
DROP TABLE IF EXISTS `tb_test`;
CREATE TABLE `tb_test`  (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `bh` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `lever` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `bm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `jl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `ssss` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `hyfl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `sfsm` int(1) NULL DEFAULT NULL,
  `sjgs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `hzrq` date NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_test
-- ----------------------------
INSERT INTO `tb_test` VALUES ('1', '吴振元\r\nt', '吴振元\r\nccc', '三级客户\r\n三级客户\r\n三级客户\r\n三级客户\r\n三级客户\r\n', '代理商', 't', '123', '213', 123, '21', NULL, NULL);
INSERT INTO `tb_test` VALUES ('1242756086864371713', '123213213', '尹凯', '第一级别客户', '编码', '尹凯', '广东省-深圳市', '行业分类', 1, '中润（深圳）物联网科技有限公司', '2020-03-25', NULL);

SET FOREIGN_KEY_CHECKS = 1;
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b185731a63f9f077.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 注意tb_test.create_time是必要的字段，如果无此字段则查询报错；id需要为字符类型，因为默认id是使用UUID的

###代码生成
使用Jeecg-Boot 的代码生成器按数据库表生成代码。先找到这个配置文件 jeecg_database.properties，修改下自己mysql的地址、账号、密码、库名
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d7374fdeb6706913.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

再找到这个类：org.jeecg.JeecgOneGUI。 执行之，填下表格实体信息。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-744dc856e28b6242.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击生成按钮，如下已经提示生成成功！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7a730e9f194dc1ef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

那么默认生成的代码在哪里呢？
看看这个配置文件：jeecg_config.properties，这里规定了生成文件的路径
![image.png](https://upload-images.jianshu.io/upload_images/13965490-466f7fe2dea7ed43.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

那么我们打开这个文件夹看看，嗯很好代码都在这了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-17ea91b0fd2f8f80.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###先看后端工程
######那么现在我们把这个代码挪到我们工程的包下：
先是后端，我们从com包这里开始吧
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f633226539767fd3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

将这个com文件夹整个复制，然后进入idea，粘贴到如图所示的包下。那么我们的com包会和这个com包合并了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-024d8a7af3efd8b7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

代码放到这里后，可见如下的类。即是刚刚咱们生成的类
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1b1adda908feadcc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

好了，现在可以启动后端的springboot工程了


###再来看前端工程

######将生成的vue代码移动到前端工程的目录之下
首先我们需要将生成的前端代码放到前端工程里，我们先在前端工程中src/views目录下创建一个文件夹作为TbTest的模块目录，命名为tbtest；
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d07371770df40723.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


然后将前端代码移到此目录下即可，如下图标识就是前端代码
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7edfa92234b168e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

移动之后如图
![image.png](https://upload-images.jianshu.io/upload_images/13965490-77ebcbd24a0cc2f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

移动代码完毕后yarn run serve 重启前端工程


######再来看如何新建一个一级目录
如果想要在前端页面中展示出来，那么接下来我们就需要配置一下菜单，先来配置一个一级的菜单吧。这个菜单仅仅当做二级菜单的目录。
如下，点击新增
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4f4c443a917c2f83.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

右侧弹出窗，配置如图所示
> 创建一级菜单时注意 菜单路径 `/layouts/tbtest` 必须以/layouts/开头，后面跟着的就是上面创建的文件夹tbtest；
前端组件 `tbtest/TbTestList` 必须以上面创建的文件夹tbtest/开头，后面跟着的即是TbTestList.vue的前缀名

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c08b5000a9b91b87.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



那么创建完毕刷新页面后，看看咱们刚刚配置的一级菜单出来没。是的无论刷新多少次还是不会出来。即是重启前后也是一样
![image.png](https://upload-images.jianshu.io/upload_images/13965490-00639e6accd8bac6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

事实上我们还需要一个步骤，那就是需要`配置权限` 咱么现在登录的是admin账号，它是管理员的身份。那么我们需要对管理员进行授权，如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-beeec89f8ac674d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
勾上这个复选框！对管理员这个角色授权。点击保存并关闭后
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0807338ffd707a4e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

刷新页面，如图自己配置的一级菜单就出来了。点击它，已经将数据展示出来了

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7feeed3104181b77.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######如何新建一个二级目录
点击这个刚刚创建的一级目录最右边的更多按钮，选择添加子菜单
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1f902be818825ba6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 注意`菜单路径` 填写 /tbtest/TbTestList ; tbtest则是之前创建的文件夹名
`前端组件` 填写 tbtest/TbTestList ; 只是比`菜单路径`少一个斜杆

![image.png](https://upload-images.jianshu.io/upload_images/13965490-df918311c9d779fc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

当然添加二级菜单后也得授权~ 勾上这个点击保存
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e230d1c2681ea464.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

刷新页面，好了我们的二级菜单出来了!

![image.png](https://upload-images.jianshu.io/upload_images/13965490-59f6fcfad8f5fd5b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 值得注意的是当我们创建了二级菜单授权后，点击一级菜单已经不会跳转到数据列表页面了
