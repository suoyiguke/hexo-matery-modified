---
title: javap--c--查看字节码.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: javap--c--查看字节码.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
javap -c D:\Hello.class便可以在dos窗口里看到我们需要的字节码文件：

~~~
G:\job\wk\demo\target\classes>javap -c Test.class
Compiled from "Test.java"
public class Test {
  public Test();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: bipush        127
       2: invokestatic  #2                  // Method java/lang/Byte.valueOf:(B)Ljava/lang/Byte;
       5: astore_1
       6: bipush        127
       8: invokestatic  #2                  // Method java/lang/Byte.valueOf:(B)Ljava/lang/Byte;
      11: astore_2
      12: getstatic     #3                  // Field java/lang/System.out:Ljava/io/PrintStream;
      15: aload_1
      16: aload_2
      17: if_acmpne     24
      20: iconst_1
      21: goto          25
      24: iconst_0
      25: invokevirtual #4                  // Method java/io/PrintStream.println:(Z)V
      28: ldc           #5                  // String 128
      30: invokestatic  #6                  // Method java/lang/Short.parseShort:(Ljava/lang/String;)S
      33: invokestatic  #7                  // Method java/lang/Short.valueOf:(S)Ljava/lang/Short;
      36: astore_3
      37: sipush        128
      40: invokestatic  #7                  // Method java/lang/Short.valueOf:(S)Ljava/lang/Short;
      43: astore        4
      45: getstatic     #3                  // Field java/lang/System.out:Ljava/io/PrintStream;
      48: aload_3
      49: aload         4
      51: if_acmpne     58
      54: iconst_1
      55: goto          59
      58: iconst_0
      59: invokevirtual #4                  // Method java/io/PrintStream.println:(Z)V
      62: sipush        128
      65: istore        5
      67: sipush        128
      70: invokestatic  #8                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
      73: astore        6
      75: getstatic     #3                  // Field java/lang/System.out:Ljava/io/PrintStream;
      78: iload         5
      80: invokestatic  #8                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
      83: aload         6
      85: invokevirtual #9                  // Method java/lang/Integer.equals:(Ljava/lang/Object;)Z
      88: invokevirtual #4                  // Method java/io/PrintStream.println:(Z)V
      91: bipush        10
      93: invokestatic  #8                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
      96: astore        7
      98: aload         7
     100: invokevirtual #10                 // Method java/lang/Integer.intValue:()I
     103: istore        8
     105: return
}

~~~
