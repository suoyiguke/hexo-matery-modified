---
title: java-基础知识3-数值类型之间的类型转换.md
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
###java中基本类型数值的取值范围和占用字节 
要明白java中的类型转换问题必须先要了解java中的各个基本数据类型数值类型的占用字节和取值范围
类型| 占用字节|   取值范围
-|-|-
byte|1字节| -128 ~ 127 
short| 2字节|-32768 ~ 32767
int| 4字节| -2147483648 ~ 2147483647 
long| 8字节| -9223372036854775808 ~ 9223372036854775807
float|	4字节|大约±3.40282347E+38F(6~7位有效数字)
double|8字节|大约±1.79769313486231570E+308(15位有效数字) 
byte==>字节
bit==>位
关系==>1byte = 8bit
~~~
boolean  8bit/1byte
byte      8bit/1byte
char      16bit/2byte
short     16bit/2byte
float      32bit/4byte
int        32bit/4byte
long      64bit/8byte
double  64bit/8byte
~~~

###隐式类型转换
从表示范围小的类型转换为表示范围大的类型，可以直接转换，称为隐式转换。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9e13e5b4ba06bca3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 6个实心箭头箭头表示无信息丢失的转换;
- 3个虚箭头表示可能有精度损失的转换.



**无信息丢失的隐式转换**
- byte==>short
- short==>int
- int==>long
- int==>double
- float==>double
- char==>int
~~~
    public static void main(String[] args) {
        byte a = 97;
        short b = a;//byte==>short
        System.out.println(b);//97
        int c = b;//short==>int
        System.out.println(c);//97
        long d = c;//int==>long
        System.out.println(d);//97

        double e = c;//int==>double
        System.out.println(e);//97.0

        float f = new Float(97);
        double g = f;//float==>double
        System.out.println(g);//97.0

        char h = 'a';
        int i = h;//char==>int
        System.out.println(i);//97


    }
~~~
**有信息丢失的隐式转换**
- int==>float
- long==>float
- long==>double
~~~
    public static void main(String[] args) {
        int a = 999999999;
        float b = a;//int==>float
        System.out.println(b);//1.0E9

        long c = 999999999999999999L;
        float d = c;//long==>float
        System.out.println(d);//9.9999998E17

        long e = 999999999999999999L;
        double f = e;//long==>double
        System.out.println(f);//1.0E18

    }
~~~

###显式类型转换
强制类型转换（显式类型转换），从存储范围大的类型到存储范围小的类型。该类类型转换很可能存在精度的损失。
`强制类型转换通常都会存储精度的损失，所以使用时需要谨慎。`
~~~
    public static void main(String[] args) {
        int a = 127;
        byte b = (byte)a;//int==>byte
        System.out.println(b);//127
        int c = 128;
        byte d = (byte)c;//int==>byte
        System.out.println(d);//-128 出现精度丢失
    }
~~~

###运算时会产生精度提升
当使用上面两个数值进行二元操作时,先要将两个操作数转换为同一类型,然后再进行计算。
规则:两个数中小类型的值将自动转换为大类型的值。
小转大可以,但是大转小会损失精度,则需要强制转换。

这里的b是byte类型的；`b*3`中，3是int类型。`b*3`精度提升成int类型了。所以这里又赋值给b会报错：`Error:(16, 13) java: 不兼容的类型: 从int转换到byte可能会有损失`,因此需要进行强制转换
![image.png](https://upload-images.jianshu.io/upload_images/13965490-75ca29d767944bae.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
byte b = 127;
b=(byte)(b*3);
System.out.println(b);//125 出现精度丢失
~~~
