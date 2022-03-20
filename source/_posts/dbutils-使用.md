---
title: dbutils-使用.md
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
title: dbutils-使用.md
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
###依赖
~~~

    <dependency>
      <groupId>commons-dbutils</groupId>
      <artifactId>commons-dbutils</artifactId>
      <version>1.6</version>
    </dependency>

    <dependency>
      <groupId>com.mchange</groupId>
      <artifactId>c3p0</artifactId>
      <version>0.9.5.2</version>
    </dependency>
    <dependency>
      <groupId>com.oracle</groupId>
      <artifactId>ojdbc6</artifactId>
      <version>11.2.0.3</version>
    </dependency>

~~~

###代码
~~~
package utils;

import com.mchange.io.FileUtils;
import com.mchange.v2.c3p0.ComboPooledDataSource;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.imageio.stream.FileImageInputStream;
import javax.imageio.stream.FileImageOutputStream;
import oracle.sql.BLOB;
import org.apache.commons.dbutils.BasicRowProcessor;
import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.ResultSetHandler;
import org.apache.commons.dbutils.RowProcessor;
import org.apache.commons.dbutils.handlers.MapListHandler;

public class LisDBUtil {

    private static LisDBUtil instance;

    //c3p0被称为数据库连接池，用来管理数据库的连接
    //c3p0连接池的ComboPooledDataSource类
    private ComboPooledDataSource dataSource;

    private LisDBUtil() throws Exception {
        dataSource = new ComboPooledDataSource();
        dataSource.setUser("BSOFT");
        dataSource.setPassword("BSOFT");
        dataSource.setJdbcUrl("jdbc:oracle:thin:@192.168.1.11:1521:orcl");
        dataSource.setDriverClass("oracle.jdbc.driver.OracleDriver");
        dataSource.setMinPoolSize(5);//设置连接池的最小连接数
        dataSource.setMaxPoolSize(50);//设置连接池的最大连接数
        dataSource.setInitialPoolSize(10);//初始化时获取的连接数，取值应在minPoolSize与maxPoolSize之间。Default: 3
        dataSource.setMaxIdleTime(10);//最大空闲时间,10秒内未使用则连接被丢弃。若为0则永不丢弃。Default: 0
        dataSource.setAcquireIncrement(5);//当连接池中的连接耗尽的时候c3p0一次同时获取的连接数。Default: 3
        dataSource.setCheckoutTimeout(10000);//连接池用完时客户调用getConnection()后等待获取连接的时间，单位：毫秒
        dataSource.setBreakAfterAcquireFailure(false);//为true会导致连接池占满后不提供服务。所以必须为false
        dataSource.setIdleConnectionTestPeriod(30);//每30秒检查一次空闲连接，加快释放连接。
    }

    public static final LisDBUtil getInstance() {

        if (instance == null) {
            try {
                instance = new LisDBUtil();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return instance;

    }

    //返回一个连接
    public synchronized final Connection getConnection() {
        Connection conn = null;
        try {
            conn = dataSource.getConnection();
            conn.setAutoCommit(false);//设置自动提交为否
            System.out.println("连接成功！");
            return conn;

        } catch (Exception e) {
            e.printStackTrace();

        }

        return null;

    }

    /**
     * 提交数据
     *
     * @throws Exception
     */
    public static void commit(Connection conn) throws Exception {
        if (null != conn) {
            conn.commit();//提交
        }
        if (null != conn) {
            conn.close();//关闭，其实连接并未真正的关闭，而是放回连接池中
        }
    }

    /**
     * 回滚
     *
     * @throws Exception
     */
    public static void rollback(Connection conn) throws Exception {
        if (null != conn) {
            conn.rollback();//LIS数据回滚
        }
        if (null != conn) {
            conn.close();

        }
    }

    public static void connColse(Connection conn) {
        if (null != conn) {
            try {
                conn.close();
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
    }

    public static void main(String[] args) throws SQLException, IOException {
        QueryRunner queryRunner = new QueryRunner();
        LisDBUtil instance = getInstance();
        Connection connection = instance.getConnection();

        List<Map<String, Object>> list = queryRunner
            .query(connection, "SELECT * FROM EMR_WH_QMXX", new MapListHandler());
        //遍历list,再遍历map
        for (Map<String, Object> map : list) {
            for (Object key : map.keySet()) {
                BLOB blob = (BLOB) map.get("QMXX");

                String jlgh = (String) map.get("JLGH");
                while (jlgh.length()<5){
                    jlgh = "0".concat(jlgh);
                }
                System.out.println(jlgh);

                InputStream inStream = blob.getBinaryStream();
                byte[] data = null;
                try {
                    long nLen = blob.length();
                    int nSize = (int) nLen;
                    data = new byte[nSize];
                    inStream.read(data);
                    inStream.close();
                } catch (IOException e) {
                    System.out.println("获取图片数据失败,原因:" + e.getMessage());
                }
                byte2image(data, "D://zzz//".concat(jlgh.concat(".jpg")));
            }

        }

}

    public byte[] image2byte(String path) {
        byte[] data = null;
        FileImageInputStream input = null;
        try {
            input = new FileImageInputStream(new File(path));
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            byte[] buf = new byte[1024];
            int numBytesRead = 0;
            while ((numBytesRead = input.read(buf)) != -1) {
                output.write(buf, 0, numBytesRead);
            }
            data = output.toByteArray();
            output.close();
            input.close();
        } catch (FileNotFoundException ex1) {
            ex1.printStackTrace();
        } catch (IOException ex1) {
            ex1.printStackTrace();
        }
        return data;
    }

    //byte数组到图片
    public static void byte2image(byte[] data, String path) {
        if (data.length < 3 || path.equals("")) {
            return;
        }
        try {
            FileImageOutputStream imageOutput = new FileImageOutputStream(new File(path));
            imageOutput.write(data, 0, data.length);
            imageOutput.close();
            System.out.println("Make Picture success,Please find image in " + path);
        } catch (Exception ex) {
            System.out.println("Exception: " + ex);
            ex.printStackTrace();
        }
    }

    //byte数组到16进制字符串
    public String byte2string(byte[] data) {
        if (data == null || data.length <= 1) {
            return "0x";
        }
        if (data.length > 200000) {
            return "0x";
        }
        StringBuffer sb = new StringBuffer();
        int buf[] = new int[data.length];
        //byte数组转化成十进制
        for (int k = 0; k < data.length; k++) {
            buf[k] = data[k] < 0 ? (data[k] + 256) : (data[k]);
        }
        //十进制转化成十六进制
        for (int k = 0; k < buf.length; k++) {
            if (buf[k] < 16) {
                sb.append("0" + Integer.toHexString(buf[k]));
            } else {
                sb.append(Integer.toHexString(buf[k]));
            }
        }
        return "0x" + sb.toString().toUpperCase();
    }


}

~~~
