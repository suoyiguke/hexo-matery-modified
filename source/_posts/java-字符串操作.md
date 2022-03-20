---
title: java-字符串操作.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
###基础使用
1、java字符串占位符替换
~~~
java.text.MessageFormat.format("该域名{0}被访问了 {1} 次.", domain , iVisit);
~~~
或者使用
~~~
String domain = "www.baidu.com";
int iVisit = 0;
System.out.println(String.format("该域名%s被访问了%s次.", domain , iVisit));
~~~

注意：常见HTML标签的属性对用法有干扰，此时需要使用转义
比如：
~~~
String pattern = "<div class=\"content-img-wrapper\"><div class=\"content-img\" data-pending=\"false\" data-src={0} alt={1} style=\"width: 100%; height: 0px; padding-top: 66.5%; background-image: url({2});\"></div><div class=\"content-img-desc\"><div class=\"triangle\"></div>{3}</div></div>";
String format = MessageFormat.format(pattern, "\'http://bai\'", "\'你好\'", "\'http://bai\'", "你好");
System.out.println(format);
~~~

还可以直接：替代方法 相比字符串的格式化操作，使用字符串的替换更加安全，避免因为疏忽或者考虑不全等带来的崩溃问题。 
~~~
String s = "%country%/%city%".replace("%country%", "China").replace("%city%", "Beijing");
~~~


2、字符串中替换第一个出现的字符
~~~
String join = "hello,hello php";
join = join.replaceFirst("hello", "你好");
System.out.println(join);    //输出：你好 java,hello php
~~~

3、数组join成字符串
Jdk8的新方法，不用通过数组，直接连接字符串
~~~
String str = String.join(",", "a", "b", "c");
~~~
当然也提供了重载
~~~
String[] arr = {"a","b","c"};
String join = String.join(",", arr);
~~~
jdk1.8之前都是用apache的commons工具类吧
~~~
org.apache.commons.lang3.StringUtils.join(articleIds,",");
~~~

4、字符串前缀和后缀判断
如果字符串以指定的前缀开始，则返回 true；否则返回 false。
~~~
String Str = "www.runoob.com";
System.out.print("返回值 :" );
System.out.println(Str.startsWith("www") );
System.out.print("返回值 :" );
System.out.println(Str.startsWith("runoob") );
System.out.print("返回值 :" );
System.out.println(Str.startsWith("runoob", 4) );
~~~
同样 endsWith 就是针对后缀的方法

5、大小写转换
- 小写转大写
~~~
 String str = "nihao cai xu kun ";
 String s = str.toUpperCase();
 System.out.println(s);
~~~
- 大写转小写
~~~
String str = "NIHAO CAI XU KUN  ";
String s = str.toLowerCase();
System.out.println(s);
~~~

6、字符串非空判断
-  null 、“”、 “  ” 都被算为空
~~~
org.apache.commons.lang3.StringUtils.isBlank(string) 
~~~
- null、”” 为空
~~~
org.apache.commons.lang3.StringUtils.isEmpty(string) 
~~~
- “” 为空
~~~
String.isEmpty()
~~~
7、判断字符串中是否存在某个字符
~~~
  if("yinkai".indexOf("m") == -1){
            System.out.println("no exit");
  }
~~~
或
~~~
if(!"yinkai".contains("m")){
       System.out.println("no exit");
}
~~~
8、截取字符串
- 按字符索引截取
~~~
String substring = "yin_kai".substring(4,7);
System.out.println(substring);
~~~

9、忽略大小写的比较内容
~~~
if("XXX".equalsIgnoreCase("xxx")){
   System.out.println("yes");
}
~~~

10、把字符串按 "," 分为字符串数组
~~~
String[] a= "1,2,3,4,5".split(",");
for (String s : a) {
       System.out.println(s);
}
~~~

11、将字符串数组join成字符串
~~~
String[] arr = {"1","2","3","4","5"};
String join = String.join(",", arr);
System.out.println(join);
~~~
12、字符串去除空格
- 去除首尾空格（只限于半角空格）
~~~
String trim = " 1 2 ".trim();
System.out.println(trim);
~~~
- 去除所有空格（只限于半角空格）
~~~
String trim = " 1 2 ".replaceAll(" ", "");
System.out.println(trim);
~~~
- 去除所有空格，包括全角空格
~~~
String trim = " 1 ｄｓ 2 ".replaceAll("　| ", "");
System.out.println(trim);
~~~

13、去除半角空格、回车、换行符、制表符（只限于半角）
~~~
    public static String replaceBlank(String str) {
        String dest = "";
        if (str!=null) {
            Pattern p = Pattern.compile("\\s*|\t|\r|\n");
            Matcher m = p.matcher(str);
            dest = m.replaceAll("");
        }
        return dest;
    }
    public static void main(String[] args) {
        System.out.println(replaceBlank("just \n  \t    \t 　do it!"));
    }
~~~

14、字符串拼接
- 使用 +
- 使用 concat方法
~~~
String concat = "yin".concat("kai");
System.out.println(concat);
~~~
- 使用StringBuilder/StringBuffer

###实用场景
1、获取文件后缀
~~~
String orginalFilename = "file.txt";
String substring = orginalFilename.substring(orginalFilename.lastIndexOf("."));// 返回 图片 "1.jpg" 的后缀： ".jpg"
System.out.println(substring);
~~~

2、截取目标字符串的指定子字符串之后的字符串
~~~
String str="abcdefg";
System.out.println(str.substring(str.indexOf("c")+1));
~~~

3、干掉指定sql字符串中第一个AND
~~~
String sql = "select * from t_customer WHERE AND name='张三' AND sex='男' AND station='百度' AND salary BETWEEN 5001 AND 10000";
String s = org.apache.commons.lang.StringUtils.replaceOnce(sql, " AND", "");
System.out.println(s);
~~~

###生成字符串

生成32位的md5摘要
~~~
System.out.println(DigestUtils.md5DigestAsHex("1234".getBytes()));
~~~


生成32位的uuid
~~~
 String uuid = UUID.randomUUID().toString().replaceAll("-", "");
~~~

###字符串转码

~~~
String string = new String(str.toString().getBytes(), "UTF-8");
~~~

>GBK、GB2312等与UTF8之间都必须通过Unicode编码才能相互转换：
GBK、GB2312－－Unicode－－UTF8
UTF8－－Unicode－－GBK、GB2312


GBK转UTF-8
~~~

    public static byte[] getUTF8BytesFromGBKString(String gbkStr) {
        int n = gbkStr.length();
        byte[] utfBytes = new byte[3 * n];
        int k = 0;
        for (int i = 0; i < n; i++) {
            int m = gbkStr.charAt(i);
            if (m < 128 && m >= 0) {
                utfBytes[k++] = (byte) m;
                continue;
            }
            utfBytes[k++] = (byte) (0xe0 | (m >> 12));
            utfBytes[k++] = (byte) (0x80 | ((m >> 6) & 0x3f));
            utfBytes[k++] = (byte) (0x80 | (m & 0x3f));
        }
        if (k < utfBytes.length) {
            byte[] tmp = new byte[k];
            System.arraycopy(utfBytes, 0, tmp, 0, k);
            return tmp;
        }
        return utfBytes;
    }

    public static void main(String[] args) throws IllegalAccessException, PkiException, InvocationTargetException {

        try {
            byte[] str = "支持™".getBytes("gbk");
            String gbkStr = new String(str, "gbk");
            String utf8 = new String(getUTF8BytesFromGBKString(gbkStr), "UTF-8");
            System.out.println(utf8);
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

    }
~~~
