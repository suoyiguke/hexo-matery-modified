---
title: jvm-直接崩溃.md
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
title: jvm-直接崩溃.md
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
###1、jacob的问题

![image.png](https://upload-images.jianshu.io/upload_images/13965490-76dbf2e00506d531.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这个mdmp文件会在每次jvm崩溃的时候生成，意思是：小型转储文件，是一种记录程序崩溃的原因及详细行为的开发者文件。不仅仅是mdmp还有对应的log都会在jar包所在的目录生成！


######对应的log如下
~~~

# A fatal error has been detected by the Java Runtime Environment:
#
#  EXCEPTION_ACCESS_VIOLATION (0xc0000005) at pc=0x010dcc7d, pid=11352, tid=0x0000360c
#
# JRE version: Java(TM) SE Runtime Environment (8.0_144-b01) (build 1.8.0_144-b01)
# Java VM: Java HotSpot(TM) Client VM (25.144-b01 mixed mode, sharing windows-x86 )
# Problematic frame:
# C  [jacob.dll+0xcc7d]
#
# Core dump written. Default location: C:\ca\IAS\hs_err_pid11352.mdmp
#
# If you would like to submit a bug report, please visit:
#   http://bugreport.java.com/bugreport/crash.jsp
# The crash happened outside the Java Virtual Machine in native code.
# See problematic frame for where to report the bug.
#

---------------  T H R E A D  ---------------

Current thread (0x160c5800):  JavaThread "http-nio-8087-exec-4" daemon [_thread_in_native, id=13836, stack(0x1b830000,0x1b880000)]

siginfo: ExceptionCode=0xc0000005, reading address 0x00000000

Registers:
EAX=0x17b09890, EBX=0x17b005a0, ECX=0x17b0da54, EDX=0x00000000
ESP=0x1b87dcf0, EBP=0x1b87dd10, ESI=0x7fffffff, EDI=0x00000036
EIP=0x010dcc7d, EFLAGS=0x00010286

Top of Stack: (sp=0x1b87dcf0)
0x1b87dcf0:   160c5800 00000010 1b87dd58 00000000
0x1b87dd00:   00000020 17b0da54 ffffffff 00000020
0x1b87dd10:   00000022 010dae64 17b005a0 160c5940
0x1b87dd20:   010dae35 00000010 010da777 00000010
0x1b87dd30:   00000001 010d90e0 00000010 160c5800
0x1b87dd40:   1b87dd7c 1b87dd68 1791fce8 015403d3
0x1b87dd50:   160c5940 1b87dd58 035f6aa0 08b96e18
0x1b87dd60:   035f6aa0 00000008 1b87dda0 012d4854 

Instructions: (pc=0x010dcc7d)
0x010dcc5d:   ce 75 0d 8b 8c 90 c4 00 00 00 6a 20 23 4d f8 5f
0x010dcc6d:   85 c9 7c 05 d1 e1 47 eb f7 8b 4d f4 8b 54 f9 04
0x010dcc7d:   8b 0a 2b 4d f0 8b f1 89 4d f8 c1 fe 04 4e 83 fe
0x010dcc8d:   3f 7e 03 6a 3f 5e 3b f7 0f 84 0d 01 00 00 8b 4a 


Register to memory mapping:

EAX=0x17b09890 is an unknown value
EBX=0x17b005a0 is an unknown value
ECX=0x17b0da54 is an unknown value
EDX=0x00000000 is an unknown value
ESP=0x1b87dcf0 is pointing into the stack for thread: 0x160c5800
EBP=0x1b87dd10 is pointing into the stack for thread: 0x160c5800
ESI=0x7fffffff is an unknown value
EDI=0x00000036 is an unknown value


Stack: [0x1b830000,0x1b880000],  sp=0x1b87dcf0,  free space=311k
Native frames: (J=compiled Java code, j=interpreted, Vv=VM code, C=native code)
C  [jacob.dll+0xcc7d]
C  [jacob.dll+0xae64]

Java frames: (J=compiled Java code, j=interpreted, Vv=VM code)
J 10919  com.jacob.com.Variant.init()V (0 bytes) @ 0x0154038f [0x01540350+0x3f]
j  com.jacob.com.Variant.<init>(Ljava/lang/String;)V+10
j  com.jacob.com.Dispatch.obj2variant(Ljava/lang/Object;)Lcom/jacob/com/Variant;+61
J 61753 C1 com.jacob.com.Dispatch.obj2variant([Ljava/lang/Object;)[Lcom/jacob/com/Variant; (31 bytes) @ 0x01381f0c [0x01381e50+0xbc]
j  com.jacob.com.Dispatch.callN(Lcom/jacob/com/Dispatch;Ljava/lang/String;[Ljava/lang/Object;)Lcom/jacob/com/Variant;+4
j  com.jacob.com.Dispatch.call(Lcom/jacob/com/Dispatch;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;)Lcom/jacob/com/Variant;+14
j  org.szwj.ca.helper.bjca.XTXAppCOM.SOF_GetCertInfo(Ljava/lang/String;I)Ljava/lang/String;+22
j  org.szwj.ca.helper.bjca.Bjca.GetCertInfo(Ljava/lang/String;I)Ljava/lang/String;+199
j  org.szwj.ca.identityauthsrv.util.common.SignHandleUtil.GetCertInfo(Lorg/szwj/ca/identityauthsrv/service/intfc/CertInfoService;Lorg/szwj/ca/helper/ICaHelper;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Lorg/szwj/ca/identityauthsrv/entity/dao/CertInfoPO;+58
j  org.szwj.ca.identityauthsrv.controller.LoginController.verifyUkeyLogin(Lorg/szwj/ca/identityauthsrv/entity/httpRequest/LoginVO;Ljava/lang/String;)Lorg/springframework/http/ResponseEntity;+873
j  org.szwj.ca.identityauthsrv.controller.LoginController.verifyBoundValue(Lorg/szwj/ca/identityauthsrv/entity/httpRequest/LoginVO;Ljavax/servlet/http/HttpServletRequest;)Lorg/springframework/http/HttpEntity;+168
j  sun.reflect.GeneratedMethodAccessor150.invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;+48
J 870 C1 sun.reflect.DelegatingMethodAccessorImpl.invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object; (10 bytes) @ 0x014a7100 [0x014a70d0+0x30]
J 869 C1 java.lang.reflect.Method.invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object; (62 bytes) @ 0x014a6e14 [0x014a6d40+0xd4]
j  org.springframework.web.method.support.InvocableHandlerMethod.doInvoke([Ljava/lang/Object;)Ljava/lang/Object;+16
j  org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(Lorg/springframework/web/context/request/NativeWebRequest;Lorg/springframework/web/method/support/ModelAndViewContainer;[Ljava/lang/Object;)Ljava/lang/Object;+75
j  org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(Lorg/springframework/web/context/request/ServletWebRequest;Lorg/springframework/web/method/support/ModelAndViewContainer;[Ljava/lang/Object;)V+4
j  org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Lorg/springframework/web/method/HandlerMethod;)Lorg/springframework/web/servlet/ModelAndView;+262
j  org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Lorg/springframework/web/method/HandlerMethod;)Lorg/springframework/web/servlet/ModelAndView;+81
j  org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Ljava/lang/Object;)Lorg/springframework/web/servlet/ModelAndView;+7
j  org.springframework.web.servlet.DispatcherServlet.doDispatch(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;)V+318
j  org.springframework.web.servlet.DispatcherServlet.doService(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;)V+301
j  org.springframework.web.servlet.FrameworkServlet.processRequest(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;)V+71
j  org.springframework.web.servlet.FrameworkServlet.doPost(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;)V+3
j  javax.servlet.http.HttpServlet.service(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;)V+149
j  org.springframework.web.servlet.FrameworkServlet.service(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;)V+33
j  javax.servlet.http.HttpServlet.service(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V+30
J 5108 C1 org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (388 bytes) @ 0x015cd778 [0x015cd5e0+0x198]
J 5107 C1 org.apache.catalina.core.ApplicationFilterChain.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (105 bytes) @ 0x01527668 [0x01527640+0x28]
j  org.apache.tomcat.websocket.server.WsFilter.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;Ljavax/servlet/FilterChain;)V+21
J 5108 C1 org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (388 bytes) @ 0x015cd918 [0x015cd5e0+0x338]
J 5107 C1 org.apache.catalina.core.ApplicationFilterChain.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (105 bytes) @ 0x01527668 [0x01527640+0x28]
j  org.springframework.web.filter.CorsFilter.doFilterInternal(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Ljavax/servlet/FilterChain;)V+55
J 5676 C1 org.springframework.web.filter.OncePerRequestFilter.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;Ljavax/servlet/FilterChain;)V (139 bytes) @ 0x01429588 [0x01429360+0x228]
J 5108 C1 org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (388 bytes) @ 0x015cd918 [0x015cd5e0+0x338]
J 5107 C1 org.apache.catalina.core.ApplicationFilterChain.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (105 bytes) @ 0x01527668 [0x01527640+0x28]
j  org.springframework.web.filter.RequestContextFilter.doFilterInternal(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Ljavax/servlet/FilterChain;)V+21
J 5676 C1 org.springframework.web.filter.OncePerRequestFilter.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;Ljavax/servlet/FilterChain;)V (139 bytes) @ 0x01429588 [0x01429360+0x228]
J 5108 C1 org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (388 bytes) @ 0x015cd918 [0x015cd5e0+0x338]
J 5107 C1 org.apache.catalina.core.ApplicationFilterChain.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (105 bytes) @ 0x01527668 [0x01527640+0x28]
j  org.springframework.web.filter.HttpPutFormContentFilter.doFilterInternal(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Ljavax/servlet/FilterChain;)V+95
J 5676 C1 org.springframework.web.filter.OncePerRequestFilter.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;Ljavax/servlet/FilterChain;)V (139 bytes) @ 0x01429588 [0x01429360+0x228]
J 5108 C1 org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (388 bytes) @ 0x015cd918 [0x015cd5e0+0x338]
J 5107 C1 org.apache.catalina.core.ApplicationFilterChain.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (105 bytes) @ 0x01527668 [0x01527640+0x28]
j  org.springframework.web.filter.HiddenHttpMethodFilter.doFilterInternal(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Ljavax/servlet/FilterChain;)V+64
J 5676 C1 org.springframework.web.filter.OncePerRequestFilter.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;Ljavax/servlet/FilterChain;)V (139 bytes) @ 0x01429588 [0x01429360+0x228]
J 5108 C1 org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (388 bytes) @ 0x015cd918 [0x015cd5e0+0x338]
J 5107 C1 org.apache.catalina.core.ApplicationFilterChain.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (105 bytes) @ 0x01527668 [0x01527640+0x28]
j  org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(Ljavax/servlet/http/HttpServletRequest;Ljavax/servlet/http/HttpServletResponse;Ljavax/servlet/FilterChain;)V+53
J 5676 C1 org.springframework.web.filter.OncePerRequestFilter.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;Ljavax/servlet/FilterChain;)V (139 bytes) @ 0x01429588 [0x01429360+0x228]
J 5108 C1 org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (388 bytes) @ 0x015cd918 [0x015cd5e0+0x338]
J 5107 C1 org.apache.catalina.core.ApplicationFilterChain.doFilter(Ljavax/servlet/ServletRequest;Ljavax/servlet/ServletResponse;)V (105 bytes) @ 0x01527668 [0x01527640+0x28]
j  org.apache.catalina.core.StandardWrapperValve.invoke(Lorg/apache/catalina/connector/Request;Lorg/apache/catalina/connector/Response;)V+688
j  org.apache.catalina.core.StandardContextValve.invoke(Lorg/apache/catalina/connector/Request;Lorg/apache/catalina/connector/Response;)V+166
j  org.apache.catalina.authenticator.AuthenticatorBase.invoke(Lorg/apache/catalina/connector/Request;Lorg/apache/catalina/connector/Response;)V+272
j  org.apache.catalina.core.StandardHostValve.invoke(Lorg/apache/catalina/connector/Request;Lorg/apache/catalina/connector/Response;)V+138
j  org.apache.catalina.valves.ErrorReportValve.invoke(Lorg/apache/catalina/connector/Request;Lorg/apache/catalina/connector/Response;)V+6
j  org.apache.catalina.core.StandardEngineValve.invoke(Lorg/apache/catalina/connector/Request;Lorg/apache/catalina/connector/Response;)V+71
j  org.apache.catalina.connector.CoyoteAdapter.service(Lorg/apache/coyote/Request;Lorg/apache/coyote/Response;)V+199
J 5642 C1 org.apache.coyote.http11.Http11Processor.service(Lorg/apache/tomcat/util/net/SocketWrapperBase;)Lorg/apache/tomcat/util/net/AbstractEndpoint$Handler$SocketState; (1248 bytes) @ 0x01443308 [0x014427d0+0xb38]
j  org.apache.coyote.AbstractProcessorLight.process(Lorg/apache/tomcat/util/net/SocketWrapperBase;Lorg/apache/tomcat/util/net/SocketEvent;)Lorg/apache/tomcat/util/net/AbstractEndpoint$Handler$SocketState;+113
j  org.apache.coyote.AbstractProtocol$ConnectionHandler.process(Lorg/apache/tomcat/util/net/SocketWrapperBase;Lorg/apache/tomcat/util/net/SocketEvent;)Lorg/apache/tomcat/util/net/AbstractEndpoint$Handler$SocketState;+378
j  org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun()V+191
j  org.apache.tomcat.util.net.SocketProcessorBase.run()V+21
J 14681% C1 java.util.concurrent.ThreadPoolExecutor.runWorker(Ljava/util/concurrent/ThreadPoolExecutor$Worker;)V (225 bytes) @ 0x0152ada4 [0x0152aba0+0x204]
j  java.util.concurrent.ThreadPoolExecutor$Worker.run()V+5
j  org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run()V+4
j  java.lang.Thread.run()V+11
v  ~StubRoutines::call_stub
~~~

######mdmp文件该用 visual studio 打开

![image.png](https://upload-images.jianshu.io/upload_images/13965490-bd6adb4ff3e7bd8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
