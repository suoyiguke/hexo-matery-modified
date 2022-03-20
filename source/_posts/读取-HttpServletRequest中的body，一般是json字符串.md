---
title: 读取-HttpServletRequest中的body，一般是json字符串.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
---
title: 读取-HttpServletRequest中的body，一般是json字符串.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
~~~
package netca.servlet;


import javax.servlet.ServletInputStream;
import javax.servlet.http.HttpServletRequest;
import java.io.*;

public class HttpServletRequestReader {

    /**
     * 读取 HttpServletRequest中的body，一般是json字符串.可以将字节数组转成 utf8的字符粗
     * new String(HttpServletRequestReader.readAsBytes(req),"UTF-8")
     *
     * @param request
     * @return
     */

    // 二进制读取
    public static byte[] readAsBytes(HttpServletRequest request) {

        int len = request.getContentLength();
        byte[] buffer = new byte[len];
        ServletInputStream in = null;

        try {
            in = request.getInputStream();
            in.read(buffer, 0, len);
            in.close();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (null != in) {
                try {
                    in.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return buffer;
    }


}
~~~
