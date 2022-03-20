---
title: java-字符串拼接方式-+-、-concat-和-StringBuilder的性能比较.md
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
###字符串的concat()方法
~~~
    /**
     * Concatenates the specified string to the end of this string.
     * <p>
     * If the length of the argument string is {@code 0}, then this
     * {@code String} object is returned. Otherwise, a
     * {@code String} object is returned that represents a character
     * sequence that is the concatenation of the character sequence
     * represented by this {@code String} object and the character
     * sequence represented by the argument string.<p>
     * Examples:
     * <blockquote><pre>
     * "cares".concat("s") returns "caress"
     * "to".concat("get").concat("her") returns "together"
     * </pre></blockquote>
     *
     * @param   str   the {@code String} that is concatenated to the end
     *                of this {@code String}.
     * @return  a string that represents the concatenation of this object's
     *          characters followed by the string argument's characters.
     */
    public String concat(String str) {
        int otherLen = str.length();
        if (otherLen == 0) {
            return this;
        }
        int len = value.length;
        #使用 Arrays.copyOf()扩容
        char buf[] = Arrays.copyOf(value, len + otherLen);
        #使用 getChars()插入字符
        str.getChars(buf, len);
        # 使用到了new关键字拼接出来的字符串也是一个新对象
        return new String(buf, true);
    }
~~~
####concat和+、StringBuild相比的字符串拼接效率如何
~~~
/**
 * @author ceshi
 * @Title:
 * @Package
 * @Description:
 * @date 2020/2/218:03
 */
public class HelloTest {
    /**
     * 计算concat所用时间
     */
    public static void str1(){
        String s1 = "yinkai";
        String str1 = "";

        long str1Start = System.currentTimeMillis();
        for (int i = 0; i < 100000; i++) {
            str1 = str1.concat(s1);
        }
        long str1End = System.currentTimeMillis();
        System.out.println("concat计算时间为：" + (str1End - str1Start)+"  "+str1.length());
    }

    /**
     * 计算+所用时间
     */
    public static void str2(){
        String s2 = "yinkai";
        String str2 = "";

        long str2Start = System.currentTimeMillis();
        for (int i = 0; i < 100000; i++) {
            str2 = str2 + s2;
        }
        long str2End = System.currentTimeMillis();
        System.out.println("+计算时间为：" + (str2End - str2Start)+"  "+str2.length());

    }

    /**
     * 计算stringBuilder所用时间
     */
    public static void str3(){
        String s3 = "yinkai";
        String str3 = "";

        long str3Start = System.currentTimeMillis();
        StringBuilder stringBuilder = new StringBuilder(str3);
        for (int i = 0; i < 100000; i++) {
            stringBuilder.append(s3);
        }
        long str3End = System.currentTimeMillis();
        System.out.println("StringBuilder计算时间为：" + (str3End - str3Start)+"  "+stringBuilder.toString().length());


    }

    public static void main(String[] args) {
        str1();//14036
        str2();//52531
        str3();//10
    }

}
~~~
- 实验结果
性能上 StringBuilder > concat > +
- 使用建议
一两个字符串之间的拼接推荐使用concat ，多了就使用StringBuilder
+一般用在非字符串和字符串之间的拼接中
