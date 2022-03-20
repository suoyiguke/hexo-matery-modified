---
title: java-调用ObjectInputStream-readObject()反序列化-java-io-EOFException异常-解决.md
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
title: java-调用ObjectInputStream-readObject()反序列化-java-io-EOFException异常-解决.md
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
调用ObjectInputStream.readObject() 反序列化读取磁盘文件到内存时出现 java.io.EOFException异常

这个问题其实是由线程安全问题所引起的，当一个线程执行ObjectInputStream.readObject()反序列化读取磁盘数据时。另一个线程让此时file为空，则容易爆出这个异常。我们可以通过给读、写加互斥锁解决，并在加锁临界区当中判断file.lengjt!=0才去进行readObject()。（已经通过实验验证，的确是要求读写互斥、读读可以并发，写写也必须互斥）

对于锁的选择，这里推荐使用读写锁 ReadWriteLock， 它是一个性能比较好的锁，他能让读操作并发。而我们这里主要是为了：`在读操作时禁止写的操作`

核心代码如下，注意输入、输出流也需要放到加锁临界区之内
~~~
     lock.writeLock().lock();
            try {
                fop = new FileOutputStream(path);
                oop = new ObjectOutputStream(fop);
                oop.writeObject(object);
            } finally {
                lock.writeLock().unlock();
            }
~~~
~~~
                lock.readLock().lock();
                try {
                    fi = new FileInputStream(path);
                    oi = new ObjectInputStream(fi);
                    if (file.length() != 0) {
                        set = (Set<SendLog>) oi.readObject();
                    }

                } finally {
                    lock.readLock().unlock();
                }
~~~

2、FileOutputStream、ObjectOutputStream的flush()方法的作用

outputSteam类，中flush()方法啥也没做,所以没效果,BufferedOutPutStream类中的flush方法才有效果
