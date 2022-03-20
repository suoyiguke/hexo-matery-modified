---
title: java持久化-jdbc基本用法.md
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
title: java持久化-jdbc基本用法.md
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
jdbc是java中进行数据库操作的基本工具，像mybatis和hibernate均是它的封装

###JDBC代码的规定步骤

1、加载驱动（装载相应的JDBC驱动并进行初始化）
~~~
 Class.forName("com.mysql.jdbc.Driver");
~~~
2、获取与数据库的连接（建立JDBC和数据库之间的Connection连接）
~~~
Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcstudy?characterEncoding=UTF-8","root", "yk123");

~~~

3、获取向数据库发送SQL语句的statement或preparedstatement
~~~
Statement  statement = connection.createStatement();
~~~
4、用statement向数据库发送SQL，并返回结果集resultset
~~~
ResultSet  resultSet = statement.executeQuery(sql);
~~~

5、解析结果集，封装数据返回
~~~
  //打印查询出来的结果集
        while(resultSet.next()){
            System.out.println(resultSet.getString("name"));
            System.out.println(resultSet.getString("password"));
        }
~~~
6、关闭连接释放资源（释放资源）
~~~
  public static void closeAll(Connection connection,Statement statement,ResultSet resultSet) throws SQLException {
        if(connection!=null){
            connection.close();
            connection = null;
        }

        if(statement!=null){
            statement.close();
            statement = null;
        }
        if(resultSet!=null){
            resultSet.close();
            resultSet = null;
        }

    }

~~~


###jdbc使用示例

1、pom.xml

~~~
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>jdbc</artifactId>
    <version>1.0-SNAPSHOT</version>

    <dependencies>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.4</version>
        </dependency>

        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.38</version>
        </dependency>
    </dependencies>


</project>
~~~


2、JDBCUtils
~~~
import java.sql.*;

 class JDBCUtils {

    /**
     * 取得数据库的连接
     * @return 一个数据库的连接
     */
    public static Connection getConnection(){
        Connection conn = null;
        try {
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcstudy?characterEncoding=UTF-8","root", "yk123");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }catch (SQLException e) {
            e.printStackTrace();
        }
        return conn;
    }

    public static void closeAll(Connection connection,Statement statement,ResultSet resultSet) throws SQLException {
        if(connection!=null){
            connection.close();
            connection = null;
        }

        if(statement!=null){
            statement.close();
            statement = null;
        }
        if(resultSet!=null){
            resultSet.close();
            resultSet = null;
        }

    }

    public static void main(String[] args) throws SQLException {
        String name="lisi";

        Connection connection=null;
        Statement statement=null;
        ResultSet resultSet=null;

        //1.获取数据库连接
        //2.创建statement对象
        //3.编写Sql语句
        //4.执行sql语句
        //5.释放资源
        connection=JDBCUtils.getConnection();

        statement = connection.createStatement();

        String sql ="select * from users where name ='"+name+"'";
        System.out.println(sql);

        resultSet = statement.executeQuery(sql);

        //打印查询出来的结果集
        while(resultSet.next()){
            System.out.println(resultSet.getString("name"));
            System.out.println(resultSet.getString("password"));
        }
        //5.
        JDBCUtils.closeAll(connection,statement,resultSet);
    }
}
~~~

3、sql脚本
~~~


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(11) NOT NULL,
  `name` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `birthday` date NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'yinkai', '123456', 'yinkai@qq.com', '1987-12-04');
INSERT INTO `users` VALUES (2, 'yinxuan', '123456', 'yinxuan@sina.com', '1982-12-04');
INSERT INTO `users` VALUES (3, 'yinwenchu', '123456', 'yinwenchu@sina.com', '1988-12-04');
INSERT INTO `users` VALUES (4, 'yinfuc', '123456', 'yinfuc@sina.com', '1990-12-04');

SET FOREIGN_KEY_CHECKS = 1;

~~~
