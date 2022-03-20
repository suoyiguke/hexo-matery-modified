---
title: java持久化-jdbc开始事务、提交事务、回滚事务、设置savepoint.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: java持久化-jdbc开始事务、提交事务、回滚事务、设置savepoint.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
> 学海无涯

这次我们来学习基于jdbc的原生事务操作，不要小看jdbc喔~ mybatis、jpa等持久化框架都是在它上面的封装。

准备数据
~~~
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `age` int(11) NULL DEFAULT NULL COMMENT '年龄',
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 103 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

~~~

上代码

下面程序使用jdbc 发出了两个insert语句，并在insert语句之间设置了一个savepoint，在发出第二条insert之后直接回滚到指定savepoint了。所以最后提交事务后，只有第二个insert生效

>-  使用connection.setAutoCommit(false); 手动提交事务，让mysql隐式为我们开一个事务
>- 使用        Savepoint point_1 = connection.setSavepoint("point_1"); 创建名为point_1的保存点
>- 使用 connection.rollback(point_1); 回滚至特定的保存点；当然可以不指定savepoint参数，那么语义为直接回滚当前的事务到事务开始时
>- 使用  connection.commit(); 即可提交当前事务

~~~
import java.sql.*;

class JDBCUtils {


    public static void main(String[] args) throws SQLException, ClassNotFoundException {

        //加载驱动
        Class.forName("com.mysql.jdbc.Driver");
        //获得连接
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcstudy?characterEncoding=UTF-8", "root", "yk123");
        //手动提交事务
        connection.setAutoCommit(false);

        //PreparedStatement预编译sql，插入一条记录的sql
        PreparedStatement preparedStatement = connection.prepareStatement("INSERT INTO `jdbcstudy`.`users`( `name`, `age`, `email`) VALUES ('hh', 22, 'hh@qq.com');");
        //执行insert
        preparedStatement.executeUpdate();
        //创建一个savepoint命名为 point_1
        Savepoint point_1 = connection.setSavepoint("point_1");
        //再次插入
        preparedStatement = connection.prepareStatement("INSERT INTO `jdbcstudy`.`users`( `name`, `age`, `email`) VALUES ( 'yk', 23, 'yk@qq.com');");
        //回滚至指定savepoint
        connection.rollback(point_1);

        //查询最新结果
        ResultSet resultSet = preparedStatement.executeQuery("select * from users");

        //解析ResultSet
        while (resultSet != null && resultSet.next()) {
            System.out.println(resultSet.getInt("id"));
            System.out.println(resultSet.getString("name"));
            System.out.println(resultSet.getInt("age"));
            System.out.println(resultSet.getString("email"));
            System.out.println("记录===>" + resultSet.getInt("id") );
        }

        //提交事务
        connection.commit();

        //关资源
        resultSet.close();
        preparedStatement.close();
        connection.close();
    }
}
~~~

程序执行之前确保users表为空
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e5b7394d7709933c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

程序执行之后，控制台打印了最后提交的数据
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f2b80988cd995a19.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-cb2e9db5da00664e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上面发出的第一个insert语句没有得到提交，因为使用了 connection.rollback(point_1);代码让事务回滚到了执行它之后
>INSERT INTO `jdbcstudy`.`users`( `name`, `age`, `email`) VALUES ('hh', 22, 'hh@qq.com');
