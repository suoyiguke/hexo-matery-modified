---
title: ruoyi--day1---初探代码生成.md
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
title: ruoyi--day1---初探代码生成.md
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
来看看如何使用代码生成器对某张表进行快速的CRUD开发
###1、准备数据表

~~~
CREATE TABLE `ry-vue`.`mydemo`  (
  `user_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户Id',
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '姓名',
  `employee_num` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '工号',
  `gender` tinyint(4) NOT NULL COMMENT '性别：0表示女，1表示男',
  `dept_id` int(11) NULL DEFAULT NULL COMMENT '科室Id',
  `identity_type` tinyint(4) NOT NULL COMMENT '证件类型',
  `identity_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '证件号码',
  `mobile` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '手机号',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `created_at` datetime(0) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(0) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
INSERT INTO `ry-vue`.`mydemo`(`user_id`, `user_name`, `employee_num`, `gender`, `dept_id`, `identity_type`, `identity_number`, `mobile`, `email`, `created_at`, `updated_at`) VALUES ('095868a19df053ab4edddf45b4babb98', '小红', '8888', 0, 11, 7, '12312312', '12343123123', '3213123213s@qq.com', '2020-07-31 09:20:01', '2020-07-31 09:20:01');
INSERT INTO `ry-vue`.`mydemo`(`user_id`, `user_name`, `employee_num`, `gender`, `dept_id`, `identity_type`, `identity_number`, `mobile`, `email`, `created_at`, `updated_at`) VALUES ('2c5536e9d535157113f7d6f4fb573d37', '小明', 'admin', 0, 22, 1, '1234567890', '123123123', '3213123213s@qq.com', '2020-07-30 17:32:39', '2020-08-03 17:47:12');
INSERT INTO `ry-vue`.`mydemo`(`user_id`, `user_name`, `employee_num`, `gender`, `dept_id`, `identity_type`, `identity_number`, `mobile`, `email`, `created_at`, `updated_at`) VALUES ('46d1cb5fea24e44b83fa9905506ade2', '小米', '290116', 0, 550, 1, '3111312311', '123123123', '3213123213s@qq.com', '2020-07-01 16:26:24', '2020-07-01 16:27:13');
INSERT INTO `ry-vue`.`mydemo`(`user_id`, `user_name`, `employee_num`, `gender`, `dept_id`, `identity_type`, `identity_number`, `mobile`, `email`, `created_at`, `updated_at`) VALUES ('46d1cb5fea24e44b83fa9905506ade82', '小兰', '290116', 0, 22, 0, '1231231231231', '12312312', '3213123213s@qq.com', '2020-08-31 09:20:01', '2020-07-31 09:20:01');
INSERT INTO `ry-vue`.`mydemo`(`user_id`, `user_name`, `employee_num`, `gender`, `dept_id`, `identity_type`, `identity_number`, `mobile`, `email`, `created_at`, `updated_at`) VALUES ('b4ecec49918ef0fdf37ba4374d037890', '小亮', '13826504867', 1, 33, 1, '12312312312', '123123123', '3213123213s@qq.com', '2021-02-06 11:34:30', '2021-01-06 11:34:30');

~~~


>注意表名不要设置微user、test这种，我之前连续设置了这两个名字，最终导入代码后运行出现名称冲突的错误。

###2、点击代码生成-导入
![image.png](https://upload-images.jianshu.io/upload_images/13965490-85e6cbc1832b1915.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

找到刚刚创建的mydemo表，勾上点击确定
![image.png](https://upload-images.jianshu.io/upload_images/13965490-505942ca346eb256.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


mydemo已经识别到列表中；然后点击生成代码
![image.png](https://upload-images.jianshu.io/upload_images/13965490-919a1751e8ad3029.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


之后我们就得到一个包含生成代码的压缩包
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a0b7f8851d8a1de6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

里面内容包含了vue页面和java的mvc三层代码、数据表的菜单sql文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e9ea6a144f17f2cf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###3、把生成的代码添加到前后端工程和数据库中

1、先将菜单数据sql导入数据库
![image.png](https://upload-images.jianshu.io/upload_images/13965490-26ed49626903ad57.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、再来看看后端代码的操作
可以直接将上述压缩包内的main文件夹整个copy到  RuoYi-Vue\ruoyi-admin\src\main，将两者合并；注意后台管理页面接口服务是在\ruoyi-admin这个maven module下；

3、来看前端
将上述压缩包内的vue内的api和views两个文件夹一起copy到 RuoYi-Vue\ruoyi-ui\src目录之下；
之后代码结构如下：

下面绿色的都是刚刚通过代码生成器生成的文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e3e97aaa07a07b20.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、最后重启后端工程和前端工程；最终效果如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-377af14ebb441328.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###4、还有其他功能可以顺带提下
细心的同学可以看到上述操作还有很多细节问题：

1、查询条件定制生成
- 查询条件包含了所有字段而我们系统通常不需要这么多查询条件
- 查询条件直接对应了数据表字段的备注信息
- 查询条件的类型都是文本框的形式，我们还需要其它的如复选框、下拉框等类型
- 有些查询方式需要配置like < > 等，现在默认生成的是= 

2、列表的定制
-   列名直接对应了数据表字段的备注信息，而我们需要自己定制
-   有些列数据我们需要关联查询到其他表的某个字段而不是直接查询出来；如上诉`科室id`字段
-  有些列我们需要隐藏

3、增加、删除表单的定制
- 必填和选题
- 有些字段不想出现在增加或删除的表单里

带着问题去学习使用ruoyi

tips：上诉的问题几乎都可以在这里解决
![image.png](https://upload-images.jianshu.io/upload_images/13965490-708f82756265f419.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
