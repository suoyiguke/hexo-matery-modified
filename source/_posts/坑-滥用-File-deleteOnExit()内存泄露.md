---
title: 坑-滥用-File-deleteOnExit()内存泄露.md
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
对不经常使用的黑盒api一定不能直接使用。最好去看下文档说明和使用注意。甚至是源码。
如果在使用delete的场景下用错了File.deleteOnExit()可以导致内存溢出宕机的生产事故！
这个方法如果只看字面意思很容易将它理解为：删除仅仅存在的文件，其实并不是这样的！如果要实现存在就删除，那么普通的File.delete()就可以做到。
###File.deleteOnExit() 导致内存泄露
~~~
/**
     * Requests that the file or directory denoted by this abstract
     * pathname be deleted when the virtual machine terminates **虚拟机终止时删除路径名**.
     * Files (or directories) are deleted in the reverse order that
     * they are registered. Invoking this method to delete a file or
     * directory that is already registered for deletion has no effect.
     * Deletion will be attempted only for normal termination of the
     * virtual machine, as defined by the Java Language Specification.
     *
     * <p> Once deletion has been requested, it is not possible to cancel the
     * request.  This method should therefore be used with care**这种方法应该谨慎使用** .
     *
     * <P>
     * Note: this method should <i>not</i> be used for file-locking, as
     * the resulting protocol cannot be made to work reliably. The
     * {@link java.nio.channels.FileLock FileLock}
     * facility should be used instead.
     *
     * @throws  SecurityException
     *          If a security manager exists and its <code>{@link
     *          java.lang.SecurityManager#checkDelete}</code> method denies
     *          delete access to the file
     *
     * @see #delete
     *
     * @since 1.2
     */
    public void deleteOnExit() {
        SecurityManager security = System.getSecurityManager();
        if (security != null) {
            security.checkDelete(path);
        }
        if (isInvalid()) {
            return;
        }
        DeleteOnExitHook.add(path);
    }

~~~

问题定位于 File.deleteOnExit() 方法的调用，导致内存泄漏。调用该方法只会将需要删除文件的路径，维护在类 DeleteOnExit 的一个 LinkedHashSet 中，在 JVM 关闭时，才会去真正执行删除文件操作。
这样导致 DeleteOnExitHook 这个对象越来越大，最终内存溢出。
File.delete() 与 File.deleteOnExit() 的区别：
当调用 delete() 方法时，直接删除文件，不管该文件是否存在，一经调用立即执行。


###那么这两种写法：的区别在哪？

1、if(file.exists()) file.deleteOnExit();
2、if(file.exists()) file.delete();

当调用delete()方法时，直接删除文件，不管该文件是否存在，一经调用立即执行；

当调用 deleteOnExit() 方法时，只是相当于对 deleteOnExit() 作一个声明，当程序运行结束，JVM 终止时才真正调用 deleteOnExit() 方法实现删除操作。


###File.deleteOnExit()场景
大概意思是在删除文件使用 File.deleteOnExit() 方法时，并不是立刻删除文件，而是将该文件路径维护在类 DeleteOnExit 的一个 LinkedHashSet 中，最后在 JVM 关闭的时候，才会去删除这里面的文件，这个方法不能用于长时间运行的服务。

程序有个需求需要创建临时文件，这个临时文件可能作为存储使用，但是程序运行结束后，这个文件应该就被删除了。在哪里做删除操作呢，需要监控程序关闭吗，如果有很多地方可以中止程序，这个删除操作需要都放置一份吗？其实只要这么写,程序结束后文件就会被自动删除了：

  File file=File.createTempFile("tmp",null);
  //这里对文件进行操作
  file.deleteOnExit();
