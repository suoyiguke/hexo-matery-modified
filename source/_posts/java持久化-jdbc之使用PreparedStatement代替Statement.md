---
title: java持久化-jdbc之使用PreparedStatement代替Statement.md
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
title: java持久化-jdbc之使用PreparedStatement代替Statement.md
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
######相对于Statement，PreparedStatement的优点是什么？


- PreparedStatement有助于防止SQL注入，因为它会自动对特殊字符转义。
- PreparedStatement预编译sql。尤其当你重用它或者使用它的拼量查询接口执行多条语句时。因此执行起来效率比Statement高
- 使用Statement只能使用字符串拼接的方式传参，而PreparedStatement可以使用“?”充当占位符进动态查询

###PreparedStatement能够防止sql注入
######使用Statement无法杜绝sql注入问题

如一下代码,模拟通过用户名密码查询user记录，如果提交的密码字符串是1' OR 1='1 的话，是能够查询到user表中所有记录的！
~~~
String password = "1' OR 1='1";
String sql = "SELECT * FROM users WHERE name = 'zhansan' AND password = '"+password+"'";

~~~
~~~
import java.sql.*;

class JDBCUtils {


    public static void main(String[] args) throws SQLException, ClassNotFoundException {

        String password = "1' OR 1='1";
        Connection connection = null;
        Statement statement = null;
        ResultSet resultSet = null;


        Class.forName("com.mysql.jdbc.Driver");
        connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcstudy?characterEncoding=UTF-8", "root", "yk123");
        statement = connection.createStatement();
        String sql = "SELECT * FROM users WHERE name = 'zhansan' AND password = '"+password+"'";
        System.out.println(sql);

        resultSet = statement.executeQuery(sql);
        while (resultSet.next()) {
            System.out.println(resultSet.getString("name"));
            System.out.println(resultSet.getString("password"));
        }

        resultSet.close();
        statement.close();
        connection.close();
    }
}
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-0469207964e80ff9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

更有甚者，可以使用sql注入攻击达到清空表数据或删表删库的目的！
如果使用 `1';DELETE FROM users WHERE id = 1 OR 1='1` 字符串当做之前password 
~~~
String password = "1';DELETE FROM users WHERE id = 1 OR 1='1";

~~~

######使用PreparedStatement杜绝sql注入攻击

换成PreparedStatement的方式发出sql语句，上面的sql注入没有出现。这就是PreparedStatement的优势之一！
~~~
import java.sql.*;

class JDBCUtils {


    public static void main(String[] args) throws SQLException, ClassNotFoundException {

        String password = "1' OR 1='1";
        Connection connection = null;
        PreparedStatement preparedStatement = null;
        ResultSet resultSet = null;

        Class.forName("com.mysql.jdbc.Driver");
        connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcstudy?characterEncoding=UTF-8", "root", "yk123");
        String sql = "SELECT * FROM users WHERE name = 'zhansan' AND password=?;";
        System.out.println(sql);
        preparedStatement = connection.prepareStatement(sql);
        //参数 绑定
        preparedStatement.setString(1,password);

        resultSet = preparedStatement.executeQuery();
        while (resultSet.next()) {
            System.out.println(resultSet.getString("name"));
            System.out.println(resultSet.getString("password"));
        }

        resultSet.close();
        preparedStatement.close();
        connection.close();
    }
}
~~~

######PreparedStatement防止sql注入的原理？
我开启了mysql的全日志，只要是执行的sql都会被纪录到mysql.log文件里面。那么就来看看PreparedStatement发出的sql吧。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c9ef1afc052123e3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
看来在password字符串中刻意写下的单引号被转义了，这样1' OR 1='1只是当做普通的字符串来执行了



###PreparedStatement处理in条件语句
由于PreparedStatement的`预编译`，in(?) 是没法发接受多个参数的。
但是可以在sql传入connection.prepareStatement(sql);方法之前，可以将“?”的个数确定下来，拼接成指定个数的in条件语句

~~~
import java.sql.*;

class JDBCUtils {


    public static void main(String[] args) throws SQLException, ClassNotFoundException {
        String[] arr = {"yinkai","yinxuan","yinfuc","yinwenchu"};
        String sql = "SELECT * FROM users WHERE name in (?);";
        String inSql = getInSql(arr);
        sql = sql.replace("in (?)", inSql);

        Connection connection = null;
        PreparedStatement preparedStatement = null;
        ResultSet resultSet = null;

        Class.forName("com.mysql.jdbc.Driver");
        connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcstudy?characterEncoding=UTF-8", "root", "yk123");

        System.out.println(sql);
        preparedStatement = connection.prepareStatement(sql);

        //参数 绑定
        for (int i = 0; i < arr.length; i++) {
            preparedStatement.setString(i+1,arr[i]);
        }

        resultSet = preparedStatement.executeQuery();
        while (resultSet.next()) {
            System.out.println(resultSet.getString("name"));
            System.out.println(resultSet.getString("password"));
        }

        resultSet.close();
        preparedStatement.close();
        connection.close();
    }

    /**
     *
     * 传入in的参数数组，返回in条件的sql
     *
     */
    public static  String  getInSql (Object[] arr ){
        String[] carr = new String[arr.length];
        for (int i = 0; i < arr.length; i++) {
            carr[i] = "?";
        }
        String inSql = "in (".concat(String.join(",", carr)).concat(")");
        return inSql;

    }
}
~~~


###PreparedStatement的三个常用接口

######方法executeQuery 
executeQuery()方法用来发出select语句



######方法executeUpdate
executeUpdate()方法 用于执行 INSERT、UPDATE 或 DELETE 语句以及 SQL DDL `数据定义语言` 语句
- executeUpdate 的返回值是一个整数，指示受影响的行数（即更新计数）。
- 对于 CREATE TABLE 或 DROP TABLE  等`数据定义语言`不操作行的语句，executeUpdate 的返回值总为零。

使用executeUpdate()方法 发出insert示例；这里注意下preparedStatement.setDate()方法的date参数是java.sql.Date，而非java.util.Date，想要获得java.sql.Date可以这样：
~~~
Date date = new Date(new java.util.Date().getTime());
~~~


~~~
import java.sql.*;

class JDBCUtils {


    public static void main(String[] args) throws SQLException, ClassNotFoundException {

        Connection connection = null;
        PreparedStatement preparedStatement = null;

        Class.forName("com.mysql.jdbc.Driver");
        connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcstudy?characterEncoding=UTF-8", "root", "yk123");
        String sql = "INSERT INTO `jdbcstudy`.`users`(`id`, `name`, `password`, `email`, `birthday`) VALUES (?, ?, ?, ?, ?);";
        System.out.println(sql);
        preparedStatement = connection.prepareStatement(sql);
        preparedStatement.setInt(1, 6);
        preparedStatement.setString(2, "haha");
        preparedStatement.setString(3, "123456");
        preparedStatement.setString(4, "haha@qq.com");
        preparedStatement.setDate(5, new Date(new java.util.Date().getTime()));
        int i = preparedStatement.executeUpdate();
        System.out.println(i);
        preparedStatement.close();
        connection.close();
    }
}
~~~


######方法execute：
execute()方法用于执行返回多个结果集、多个更新计数或二者组合的语句。

下面的程序通过调用`存储过程`来达到处理多个返回集的目的
~~~
CREATE PROCEDURE select_double_users()    
BEGIN    
  select * from users;
  select * from users;     
END; 
~~~

~~~
import java.sql.*;

class JDBCUtils {


    public static void main(String[] args) throws SQLException, ClassNotFoundException {

        Connection connection = null;
        PreparedStatement preparedStatement = null;
        ResultSet resultSet = null;

        Class.forName("com.mysql.jdbc.Driver");
        connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcstudy?characterEncoding=UTF-8", "root", "yk123");

        //调用存储过程
        String sql = "{call select_double_users()}";
        preparedStatement = connection.prepareCall(sql);
        int i = 0;
        boolean execute = preparedStatement.execute();
        while (execute) {
            System.out.println("result No:=================================================================="+(++i));
            resultSet = preparedStatement.getResultSet();
            while (resultSet != null && resultSet.next()) {
                System.out.println(resultSet.getInt("id"));
                System.out.println(resultSet.getString("name"));
                System.out.println(resultSet.getString("password"));
                System.out.println(resultSet.getString("email"));
                System.out.println(resultSet.getDate("birthday"));
            }
            execute = preparedStatement.getMoreResults(); //检查是否存在更多结果集
        }

        resultSet.close();
        preparedStatement.close();
        connection.close();
    }
}
~~~
