---
title: BufferedOutputStream.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-io
categories: java-io
---
---
title: BufferedOutputStream.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-io
categories: java-io
---
**可以这么理解，BufferedOutputStream类就是对FileInputStream类的加强。它是一个加强流。**
The class implements a buffered output stream. By setting up such an output stream, an application can write bytes to the underlying output stream without necessarily causing a call to the underlying system for each byte written.
该类实现一个缓冲输出流。通过设置这样的输出流，应用程序可以将字节写入底层输出流，而不必为写入的每个字节调用底层系统。

为什么成为加强流？就是因为这个加强流在进行输出时会在内存中开辟一块缓冲区。因为缓冲区在内存中的读写速度很快，以此来达到提升输出流的效率

参考：缓冲流帮助理解

看一下BufferedOutputStream的构造方法

//构造方法，从构造方法可以看出它需要一个底层输出流。
BufferedOutputStream(OutputStream out);  //创建一个新的缓冲输出流，以将数据写入指定的底层输出流。
BufferedOutputStream(OutputStream out,int size);  //创建一个新的缓冲输出流，以便以指定的缓冲区大小将数据写入指定的底层输出流。



原理
![image.png](https://upload-images.jianshu.io/upload_images/13965490-34fe978787a3a752.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

/*普及：计算机中内存的访问速度（运算效率）比硬盘的访问速度（运算效率）要高得多*/

在代码中使用BufferedInputStream和BufferedOutputStream能够提高数据的传输效率原因如下：

①当只使用FileInputStream和FileOutputStream进行数据复制时，每次FileInputStram从数据源（硬存）中读取一个字节，然后交给b，再把b给FileOutputStream写入存储目的地（硬存），每存储一个字节需要访问硬存两次，以此往复直至存储完毕。

②当使用BufferedInputStream和BufferedOutputStream作为缓冲区后，BufferedInputStream内自带一个8192大小的字节数组，每次可从数据源（硬存）读取8192个字节的数据，然后一个一个的交给b，再由b存入BufferedOutputStream的8192大小的数组中，直到BufferedOutputStream中的数组存满时，然后写入数据传输终点，然后BufferedInputStream从数据源重新读取8192大小的数据，以此往复直至存储完毕。

假设现在数据源是一个8KB（8192个字节）大小的数据，需要复制到终点：

若使用FileInputStream和FileOutputStream进行传输，每次传输一个字节需要访问一次数据源一次数据传输终点，共访问两次硬存。若传输8KB则需要访问8*1024*2=16384次硬存。

若使用BufferedInputStream和BufferedOutputStream作为缓冲区进行传输，BufferedInputStream一次将所有数据读取完毕存入数组中，然后一个一个给b再存入BufferedOutputStream的数组，最终一次存入硬盘，访问硬盘两次。

有的人可能会疑问，使用BufferedInputStream和BufferedOutputStream虽然传输8KB的数据只需要访问2次硬盘，但是同样也需要在内存中一个一个的进行转存，这样感觉不是没什么区别吗？

此时就是计算机中最重要的特点了：内存的访问速度（运算效率）比硬盘的访问速度（运算效率）要高得多的多，然后BufferedInputStream和BufferedOutputStream的工作基本都是在内存中完成的，对硬盘的操作次数十分少，这就相对的提高了效率。现在举例只是以8KB为例，使用BufferedInputStream和BufferedOutputStream就能比单使用FileInputStream和FileOutputStream的效率提高很多很多，我们现实生活中随便一个文件基本都是以MB为单位或者GB为单位，这时两者的效率就天差地别了，所以这就是使用BufferedInputStream和BufferedOutputStream作为缓冲区传输的原因。


###创建BufferedOutputStream对象的方法 
方法一：
~~~
File  file = new File("D:\\www\\abc.txt");
OutputStream out = new FileOutputStream(file);
BufferedOutputStream buffer = new BufferedOutputStream(out);
~~~
注：方法一的创建比较麻烦，因此不怎么使用，但是这种创建方法可以让我们清晰的看出字节缓冲输出流的一个流向，它是怎么输出文件中的。

方法二：
~~~
OutputStream buffer = new BufferedOutputStream(new FileOutputStream("D:\\www\\abc.txt"));
//方法二的创建过程比较简洁，使用比较多
~~~

创建了对象后我们看一下怎么使用吧
~~~
import java.io.*;
public class Text {
	public static void main(String[] args) throws Exception{
		//创建BufferedOutputStream字节缓冲输出流
		OutputStream buffer = new BufferedOutputStream(new FileOutputStream("D:\\www\\abc.txt"));
		buffer.write(97);
		byte[] bytes = {97,98,99}; 
		buffer.write(bytes);
		buffer.write(bytes,1,2);
		buffer.write("我爱中国".getBytes());
		buffer.write("\r\n".getBytes());
		buffer.write("Java".getBytes());
		buffer.flush();  //刷新缓冲输出流
		buffer.close();  //关闭流(默认会刷新)
		}
		/*
~~~
输出结果：
aabcbc我爱中国

缓冲字节输出流的使用比较简单，使用方法和普通的字节输出流使用方式一致。
