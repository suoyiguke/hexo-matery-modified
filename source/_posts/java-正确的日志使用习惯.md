---
title: java-正确的日志使用习惯.md
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
**禁止使用e.printStackTrace()**
 
e.printStackTrace()打印的是异常堆栈信息，会额外的占用内存空间。正确的姿势是把日志打印到文件中。如下
~~~
    public static void main(String[] args) {
        try {
            int i = 1/0;
        }catch (Exception e){
            //禁止使用 e.printStackTrace() 
            logger.error("错误",e);
        }
    }
~~~
>注意log.error()最后一个参数要填捕获到的异常e，这样才能将异常详细堆栈信息打印到log

**使用合适的日志级别**
 
Slf4j有四个级别的log level可供选择，级别从上到下由低到高，优先级高的将被打印出来。
Debug：简单来说，对程序调试有利的信息都可以debug输出。
info：对用户有用的信息，比如最常见的打印接口入参和返参。
warn：可能会导致错误的信息，比如某个对象可能为null的场景判断。
error：顾名思义，发生错误的地方，最常见的catch代码块中的日志。
 
这里以error日志为例，举一个例子，在合适的场合打印合适的日志，是我们日志界的规范。
~~~
    public static void main(String[] args) {
        try {
            int i = 1 / 0;
        } catch (Exception e) {
            //catch中不适合使用info级别
            // logger.info("错误",e); 
            logger.error("错误", e);
        }
    }

~~~
 

**使用占位符，而不是字符串拼接**

Slf4j打印日志使用了占位符，避免了字符串拼接操作。字符串拼接最大的弊端，就是需要new新的字符串对象，增加了内存的开销。
~~~
    public static void main(String[] args) {
        int a = 1;
        int b = 0;
        try {
            int i = a / b;
        } catch (Exception e) {
            //不要使用+字符串直接拼接
            //logger.error("错误 a="+a+" b="+b,e);
            logger.error("错误 a={} b={}", a, b, e);
        }
    }
 ~~~

**尽量打印更少的日志，能一行打印的不要分为多行**
不要打印无用的日志，不要重复打印日志，尽量不要在for循环中打印日志。
~~~
    public static void main(String[] args) {
        int a = 1;
        int b = 0;
        try {
            int i = a / b;

        } catch (Exception e) {
//            //能一行打印的不要分为多行
//            logger.error("错误 a={}", a);
//            logger.error("错误 b={}", b);
//            logger.error("错误 ", e);
            logger.error("错误 a={} b={}", a, b, e);
        }
    }
 
~~~
 
 

###从源码角度看看log打印和e.printStackTrace()的区别

1、log.error底层实现
ch.qos.logback.core.spi.AppenderAttachableImpl#appendLoopOnAppenders
循环迭代appenderArray数组，一般是三个元素分别为：控制台、全日志、错误日志。三个输出目标依次执行！
~~~
    /**
     * Call the <code>doAppend</code> method on all attached appenders.
     */
    public int appendLoopOnAppenders(E e) {
        int size = 0;
        final Appender<E>[] appenderArray = appenderList.asTypedArray();
        final int len = appenderArray.length;
        for (int i = 0; i < len; i++) {
            appenderArray[i].doAppend(e);
            size++;
        }
        return size;
    }

~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b4a97887ebee045a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

分支逻辑 ch.qos.logback.core.UnsynchronizedAppenderBase#doAppend
 this.append(eventObject);this有连个两个多态实现：ch.qos.logback.core.ConsoleAppender[STDOUT]和ch.qos.logback.core.rolling.RollingFileAppender[FILE]分别表示控制台输出和日志文件输出

~~~

    public void doAppend(E eventObject) {
        // WARNING: The guard check MUST be the first statement in the
        // doAppend() method.

        // prevent re-entry.
        if (Boolean.TRUE.equals(guard.get())) {
            return;
        }

        try {
            guard.set(Boolean.TRUE);

            if (!this.started) {
                if (statusRepeatCount++ < ALLOWED_REPEATS) {
                    addStatus(new WarnStatus("Attempted to append to non started appender [" + name + "].", this));
                }
                return;
            }

            if (getFilterChainDecision(eventObject) == FilterReply.DENY) {
                return;
            }

            // ok, we now invoke derived class' implementation of append
            this.append(eventObject);

        } catch (Exception e) {
            if (exceptionCount++ < ALLOWED_REPEATS) {
                addError("Appender [" + name + "] failed to append.", e);
            }
        } finally {
            guard.set(Boolean.FALSE);
        }
    }
~~~





**2、e.printStackTrace()底层实现**
java.lang.Throwable#printStackTrace(java.lang.Throwable.PrintStreamOrWriter)

~~~
    private void printStackTrace(PrintStreamOrWriter s) {
        // Guard against malicious overrides of Throwable.equals by
        // using a Set with identity equality semantics.
        Set<Throwable> dejaVu =
            Collections.newSetFromMap(new IdentityHashMap<Throwable, Boolean>());
        dejaVu.add(this);

        synchronized (s.lock()) {
            // Print our stack trace
            s.println(this);
            StackTraceElement[] trace = getOurStackTrace();
            for (StackTraceElement traceElement : trace)
                s.println("\tat " + traceElement);

            // Print suppressed exceptions, if any
            for (Throwable se : getSuppressed())
                se.printEnclosedStackTrace(s, trace, SUPPRESSED_CAPTION, "\t", dejaVu);

            // Print cause, if any
            Throwable ourCause = getCause();
            if (ourCause != null)
                ourCause.printEnclosedStackTrace(s, trace, CAUSE_CAPTION, "", dejaVu);
        }
    }
~~~

java.lang.Throwable.WrappedPrintStream#println
~~~
   void println(Object o) {
            printStream.println(o);
        }
~~~
java.io.PrintStream#println(java.lang.Object)
~~~
    public void println(Object x) {
        String s = String.valueOf(x);
        synchronized (this) {
            print(s);
            newLine();
        }
    }
~~~
java.io.PrintStream#write(java.lang.String)
~~~ 
    private void write(String s) {
        try {
            synchronized (this) {
                ensureOpen();
                textOut.write(s);
                textOut.flushBuffer();
                charOut.flushBuffer();
                if (autoFlush && (s.indexOf('\n') >= 0))
                    out.flush();
            }
        }
        catch (InterruptedIOException x) {
            Thread.currentThread().interrupt();
        }
        catch (IOException x) {
            trouble = true;
        }
    }

~~~

>e.printStackTrace()使用BufferedWriter.write(s);输出到控制台，而且是逐行输出，存在资源浪费的性能问题。



###补充一下alibaba开发手册中日志规范内容

1、应用中不可直接使用日志系统（Log4j、Logback）中的API，而应依赖使用日志框架 SLF4J中的API，使用门面模式的日志框架，有利于维护和各个类的日志处理方式统一。
~~~
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
private static final Logger logger = LoggerFactory.getLogger(Test.class);
~~~


2、在日志输出时，字符串变量之间的拼接使用占位符的方式。 说明：因为String字符串的拼接会使用StringBuilder的append()方式，有一定的性能损耗。使用占位符仅是替换动作，可以有效提升性能。 正例：
~~~
logger.debug("Processing trade with id: {} and symbol: {}", id, symbol);
~~~

3、对于trace/debug/info级别的日志输出，必须进行日志级别的开关判断。 说明：虽然在debug(参数)的方法体内第一行代码isDisabled(Level.DEBUG_INT)为真时（Slf4j的常见实现Log4j和Logback），就直接return，但是参数可能会进行字符串拼接运算。此外，如果debug(getName())这种参数内有getName()方法调用，无谓浪费方法调用的开销。
 正例： // 如果判断为真，那么可以输出trace和debug级别的日志
~~~
      if(log.isTraceEnabled()){
           log.trace("111");
        }
        if(log.isDebugEnabled()){
           log.debug("111");
        }
        if(JgRulaUnsuitableGoodsServiceImpl.log.isInfoEnabled()){
            log.info("111");
        }
~~~

4、【强制】避免重复打印日志，浪费磁盘空间，务必在log4j.xml中设置additivity=false。
 正例：
~~~
<logger name="com.taobao.dubbo.config" additivity="false">
~~~

5、【强制】异常信息应该包括两类信息：案发现场信息和异常堆栈信息。如果不处理，那么通过关键字throws往上抛出。

 正例：
~~~
logger.error(各类参数或者对象toString() + "_" + e.getMessage(), e);
~~~

6、【推荐】谨慎地记录日志。`生产环境禁止输出debug日志`；有选择地输出info日志；如果使用warn来记录刚上线时的业务行为信息，一定要注意日志输出量的问题，避免把服务器磁盘撑爆，并记得及时删除这些观察日志。 说明：大量地输出无效日志，不利于系统性能提升，也不利于快速定位错误点。记录日志时请思考：这些日志真的有人看吗？看到这条日志你能做什么？能不能给问题排查带来好处？ 

7、  `重要` 异常信息应该包括两类信息：案发现场信息和异常堆栈信息。如果不处理，那么通过
关键字 throws 往上抛出。
正例：logger.error("inputParams:{} and errorMessage:{}", 各类参数或者对象 toString(), e.getMessage(), e);


8、`重要`日志打印时禁止直接用 JSON 工具将对象转换成 String。说明：如果对象里某些 get 方法被覆写，存在抛出异常的情况，则可能会因为打印日志而影响正常业务流
程的执行。
正例：打印日志时仅打印出业务相关属性值或者调用其对象的 toString()方法。
