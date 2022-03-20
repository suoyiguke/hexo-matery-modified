---
title: jvm-crash2.md
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
title: jvm-crash2.md
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
~~~

# There is insufficient memory for the Java Runtime Environment to continue.
# Native memory allocation (malloc) failed to allocate 32756 bytes for ChunkPool::allocate
# Possible reasons:
#   The system is out of physical RAM or swap space
#   In 32 bit mode, the process size limit was hit
# Possible solutions:
#   Reduce memory load on the system
#   Increase physical memory or swap space
#   Check if swap backing store is full
#   Use 64 bit Java on a 64 bit OS
#   Decrease Java heap size (-Xmx/-Xms)
#   Decrease number of Java threads
#   Decrease Java thread stack sizes (-Xss)
#   Set larger code cache with -XX:ReservedCodeCacheSize=
# This output file may be truncated or incomplete.
#
#  Out of Memory Error (allocation.cpp:273), pid=5644, tid=0x000014d4
#
# JRE version: Java(TM) SE Runtime Environment (8.0_144-b01) (build 1.8.0_144-b01)
# Java VM: Java HotSpot(TM) Client VM (25.144-b01 mixed mode windows-x86 )
# Failed to write core dump. Call to MiniDumpWriteDump() failed (Error 0x80070008: 存储空间不足，无法处理此命令。

)
#

---------------  T H R E A D  ---------------

Current thread (0x14833c00):  JavaThread "C1 CompilerThread0" daemon [_thread_in_native, id=5332, stack(0x14c40000,0x14c90000)]

Stack: [0x14c40000,0x14c90000],  sp=0x14c8ed74,  free space=315k
Native frames: (J=compiled Java code, j=interpreted, Vv=VM code, C=native code)
V  [jvm.dll+0x1aa78b]
V  [jvm.dll+0x1a2fd8]
V  [jvm.dll+0x8cd71]
V  [jvm.dll+0x8cf4d]
V  [jvm.dll+0x8d3c7]
V  [jvm.dll+0xa4d34]
V  [jvm.dll+0x7624f]
V  [jvm.dll+0x76474]
V  [jvm.dll+0x256db]
V  [jvm.dll+0x25701]
V  [jvm.dll+0x2b1952]
V  [jvm.dll+0x2b4de7]
V  [jvm.dll+0x29ad5e]
V  [jvm.dll+0x2ac7ca]
V  [jvm.dll+0x29ab16]
V  [jvm.dll+0x28a3cf]
V  [jvm.dll+0x28a769]
V  [jvm.dll+0x28a83a]
V  [jvm.dll+0x28a9a8]
V  [jvm.dll+0x28ac22]
V  [jvm.dll+0x7069a]
V  [jvm.dll+0x70e4f]
V  [jvm.dll+0x17dc30]
V  [jvm.dll+0x17e4aa]
V  [jvm.dll+0x1c2ec6]
C  [msvcr100.dll+0x5c556]
C  [msvcr100.dll+0x5c600]
C  [KERNEL32.DLL+0x17c04]
C  [ntdll.dll+0x5ad8f]
C  [ntdll.dll+0x5ad5a]
C  0x00000000


Current CompileTask:
C1:48388758 8773   !         org.szwj.ca.identityauthsrv.SchedulingHandler::queryQRCodeStatus (1587 bytes)


---------------  P R O C E S S  ---------------

Java Threads: ( => current thread )
  0x16c81400 JavaThread "logback-2" daemon [_thread_blocked, id=6996, stack(0x18dc0000,0x18e10000)]
  0x16c80000 JavaThread "logback-1" daemon [_thread_blocked, id=3204, stack(0x18730000,0x18780000)]
  0x16c7fc00 JavaThread "Java2D Disposer" daemon [_thread_blocked, id=5756, stack(0x17870000,0x178c0000)]
  0x16c7e800 JavaThread "DestroyJavaVM" [_thread_blocked, id=3972, stack(0x00390000,0x003e0000)]
  0x16c7e000 JavaThread "http-nio-8087-AsyncTimeout" daemon [_thread_blocked, id=6056, stack(0x1aa10000,0x1aa60000)]
  0x16c7f400 JavaThread "http-nio-8087-Acceptor-0" daemon [_thread_in_native, id=4884, stack(0x1a980000,0x1a9d0000)]
  0x16c7dc00 JavaThread "http-nio-8087-ClientPoller-1" daemon [_thread_in_native, id=472, stack(0x1a8f0000,0x1a940000)]
  0x16c7f000 JavaThread "http-nio-8087-ClientPoller-0" daemon [_thread_in_native, id=5744, stack(0x1a860000,0x1a8b0000)]
  0x16c7d000 JavaThread "http-nio-8087-exec-10" daemon [_thread_blocked, id=5368, stack(0x1a7d0000,0x1a820000)]
  0x16c7d400 JavaThread "http-nio-8087-exec-9" daemon [_thread_blocked, id=6464, stack(0x1a740000,0x1a790000)]
  0x16c7c800 JavaThread "http-nio-8087-exec-8" daemon [_thread_blocked, id=6216, stack(0x1a6b0000,0x1a700000)]
  0x16b23400 JavaThread "http-nio-8087-exec-7" daemon [_thread_blocked, id=120, stack(0x1a620000,0x1a670000)]
  0x16b20c00 JavaThread "http-nio-8087-exec-6" daemon [_thread_blocked, id=3256, stack(0x1a590000,0x1a5e0000)]
  0x16b20800 JavaThread "http-nio-8087-exec-5" daemon [_thread_blocked, id=3656, stack(0x1a500000,0x1a550000)]
  0x16b20000 JavaThread "http-nio-8087-exec-4" daemon [_thread_blocked, id=4960, stack(0x1a470000,0x1a4c0000)]
  0x16b22400 JavaThread "http-nio-8087-exec-3" daemon [_thread_blocked, id=5624, stack(0x1a3e0000,0x1a430000)]
  0x16b23800 JavaThread "http-nio-8087-exec-2" daemon [_thread_blocked, id=4564, stack(0x1a350000,0x1a3a0000)]
  0x16b22000 JavaThread "http-nio-8087-exec-1" daemon [_thread_blocked, id=4924, stack(0x1a2c0000,0x1a310000)]
  0x16b21800 JavaThread "NioBlockingSelector.BlockPoller-1" daemon [_thread_in_native, id=2708, stack(0x1a230000,0x1a280000)]
  0x16b22c00 JavaThread "pool-2-thread-1" [_thread_blocked, id=948, stack(0x1a1a0000,0x1a1f0000)]
  0x1578d400 JavaThread "Abandoned connection cleanup thread" daemon [_thread_blocked, id=6740, stack(0x19af0000,0x19b40000)]
  0x1556c800 JavaThread "Tomcat JDBC Pool Cleaner[1742101:1609143751686]" daemon [_thread_blocked, id=6140, stack(0x19a60000,0x19ab0000)]
  0x14978000 JavaThread "check-redis-thread" [_thread_blocked, id=6016, stack(0x19200000,0x19250000)]
  0x15545400 JavaThread "commons-pool-EvictionTimer" daemon [_thread_blocked, id=7048, stack(0x198d0000,0x19920000)]
  0x152e8400 JavaThread "container-0" [_thread_blocked, id=6844, stack(0x19030000,0x19080000)]
  0x15098c00 JavaThread "ContainerBackgroundProcessor[StandardEngine[Tomcat]]" daemon [_thread_blocked, id=5104, stack(0x18f40000,0x18f90000)]
  0x1488b800 JavaThread "Service Thread" daemon [_thread_blocked, id=3788, stack(0x14cd0000,0x14d20000)]
=>0x14833c00 JavaThread "C1 CompilerThread0" daemon [_thread_in_native, id=5332, stack(0x14c40000,0x14c90000)]
  0x14833400 JavaThread "Attach Listener" daemon [_thread_blocked, id=5820, stack(0x14bb0000,0x14c00000)]
  0x14860c00 JavaThread "Signal Dispatcher" daemon [_thread_blocked, id=5564, stack(0x14b20000,0x14b70000)]
  0x1481a000 JavaThread "Finalizer" daemon [_thread_blocked, id=5852, stack(0x14a40000,0x14a90000)]
  0x14804400 JavaThread "Reference Handler" daemon [_thread_blocked, id=4828, stack(0x047a0000,0x047f0000)]

Other Threads:
  0x0095d000 VMThread [stack: 0x04710000,0x04760000] [id=6756]
  0x148e8400 WatcherThread [stack: 0x14d60000,0x14db0000] [id=5632]

VM state:not at safepoint (normal execution)

VM Mutex/Monitor currently owned by a thread: None

Heap:
 def new generation   total 31168K, used 12525K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K,  44% used [0x04800000, 0x05427768, 0x06310000)
  from space 3456K,   2% used [0x06310000, 0x06323cf8, 0x06670000)
  to   space 3456K,   0% used [0x06670000, 0x06670000, 0x069d0000)
 tenured generation   total 69200K, used 66484K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  96% used [0x09d50000, 0x0de3d150, 0x0de3d200, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K

Card table byte_map: [0x00a40000,0x00ad0000] byte_map_base: 0x00a1c000

Polling page: 0x003e0000

CodeCache: size=32768Kb used=2899Kb max_used=5168Kb free=29868Kb
 bounds [0x02710000, 0x02c28000, 0x04710000]
 total_blobs=1492 nmethods=954 adapters=468
 compilation: enabled

Compilation events (10 events):
Event: 48136.830 Thread 0x14833c00 nmethod 8768 0x02a36a88 code [0x02a36b80, 0x02a36c00]
Event: 48136.830 Thread 0x14833c00 8769             java.util.concurrent.locks.ReentrantReadWriteLock::readLock (5 bytes)
Event: 48136.830 Thread 0x14833c00 nmethod 8769 0x0285f6c8 code [0x0285f7c0, 0x0285f840]
Event: 48272.447 Thread 0x14833c00 8770             java.lang.CharacterDataLatin1::toUpperCase (53 bytes)
Event: 48272.447 Thread 0x14833c00 nmethod 8770 0x0289be08 code [0x0289bf00, 0x0289bff0]
Event: 48371.498 Thread 0x14833c00 8771   !         sun.reflect.GeneratedMethodAccessor77::invoke (62 bytes)
Event: 48371.498 Thread 0x14833c00 nmethod 8771 0x02897348 code [0x028974a0, 0x02897798]
Event: 48377.468 Thread 0x14833c00 8772             java.util.regex.Pattern$BnM::optimize (179 bytes)
Event: 48377.468 Thread 0x14833c00 nmethod 8772 0x02965588 code [0x029656d0, 0x02965b4c]
Event: 48379.497 Thread 0x14833c00 8773   !         org.szwj.ca.identityauthsrv.SchedulingHandler::queryQRCodeStatus (1587 bytes)

GC Heap History (10 events):
Event: 41890.531 GC heap before
{Heap before GC invocations=482 (full 21):
 def new generation   total 31168K, used 27712K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K, 100% used [0x04800000, 0x06310000, 0x06310000)
  from space 3456K,   0% used [0x06670000, 0x06670000, 0x069d0000)
  to   space 3456K,   0% used [0x06310000, 0x06310000, 0x06670000)
 tenured generation   total 69200K, used 38056K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  54% used [0x09d50000, 0x0c27a180, 0x0c27a200, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K
Event: 41890.536 GC heap after
Heap after GC invocations=483 (full 21):
 def new generation   total 31168K, used 285K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K,   0% used [0x04800000, 0x04800000, 0x06310000)
  from space 3456K,   8% used [0x06310000, 0x063577c0, 0x06670000)
  to   space 3456K,   0% used [0x06670000, 0x06670000, 0x069d0000)
 tenured generation   total 69200K, used 47118K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  68% used [0x09d50000, 0x0cb53910, 0x0cb53a00, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K
}
Event: 41890.871 GC heap before
{Heap before GC invocations=483 (full 21):
 def new generation   total 31168K, used 23300K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K,  83% used [0x04800000, 0x05e79a20, 0x06310000)
  from space 3456K,   8% used [0x06310000, 0x063577c0, 0x06670000)
  to   space 3456K,   0% used [0x06670000, 0x06670000, 0x069d0000)
 tenured generation   total 69200K, used 47118K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  68% used [0x09d50000, 0x0cb53910, 0x0cb53a00, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K
Event: 41890.874 GC heap after
Heap after GC invocations=484 (full 21):
 def new generation   total 31168K, used 325K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K,   0% used [0x04800000, 0x04800000, 0x06310000)
  from space 3456K,   9% used [0x06670000, 0x066c16c0, 0x069d0000)
  to   space 3456K,   0% used [0x06310000, 0x06310000, 0x06670000)
 tenured generation   total 69200K, used 47118K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  68% used [0x09d50000, 0x0cb53910, 0x0cb53a00, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K
}
Event: 41890.925 GC heap before
{Heap before GC invocations=484 (full 21):
 def new generation   total 31168K, used 21028K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K,  74% used [0x04800000, 0x05c379b8, 0x06310000)
  from space 3456K,   9% used [0x06670000, 0x066c16c0, 0x069d0000)
  to   space 3456K,   0% used [0x06310000, 0x06310000, 0x06670000)
 tenured generation   total 69200K, used 47118K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  68% used [0x09d50000, 0x0cb53910, 0x0cb53a00, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K
Event: 41890.930 GC heap after
Heap after GC invocations=485 (full 21):
 def new generation   total 31168K, used 322K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K,   0% used [0x04800000, 0x04800000, 0x06310000)
  from space 3456K,   9% used [0x06310000, 0x06360810, 0x06670000)
  to   space 3456K,   0% used [0x06670000, 0x06670000, 0x069d0000)
 tenured generation   total 69200K, used 57376K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  82% used [0x09d50000, 0x0d558020, 0x0d558200, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K
}
Event: 41891.129 GC heap before
{Heap before GC invocations=485 (full 21):
 def new generation   total 31168K, used 28029K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K,  99% used [0x04800000, 0x0630ec28, 0x06310000)
  from space 3456K,   9% used [0x06310000, 0x06360810, 0x06670000)
  to   space 3456K,   0% used [0x06670000, 0x06670000, 0x069d0000)
 tenured generation   total 69200K, used 57376K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  82% used [0x09d50000, 0x0d558020, 0x0d558200, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K
Event: 41891.134 GC heap after
Heap after GC invocations=486 (full 21):
 def new generation   total 31168K, used 199K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K,   0% used [0x04800000, 0x04800000, 0x06310000)
  from space 3456K,   5% used [0x06670000, 0x066a1fd8, 0x069d0000)
  to   space 3456K,   0% used [0x06310000, 0x06310000, 0x06670000)
 tenured generation   total 69200K, used 66484K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  96% used [0x09d50000, 0x0de3d150, 0x0de3d200, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K
}
Event: 43520.865 GC heap before
{Heap before GC invocations=486 (full 21):
 def new generation   total 31168K, used 27911K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K, 100% used [0x04800000, 0x06310000, 0x06310000)
  from space 3456K,   5% used [0x06670000, 0x066a1fd8, 0x069d0000)
  to   space 3456K,   0% used [0x06310000, 0x06310000, 0x06670000)
 tenured generation   total 69200K, used 66484K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  96% used [0x09d50000, 0x0de3d150, 0x0de3d200, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K
Event: 43520.872 GC heap after
Heap after GC invocations=487 (full 21):
 def new generation   total 31168K, used 79K [0x04800000, 0x069d0000, 0x09d50000)
  eden space 27712K,   0% used [0x04800000, 0x04800000, 0x06310000)
  from space 3456K,   2% used [0x06310000, 0x06323cf8, 0x06670000)
  to   space 3456K,   0% used [0x06670000, 0x06670000, 0x069d0000)
 tenured generation   total 69200K, used 66484K [0x09d50000, 0x0e0e4000, 0x14800000)
   the space 69200K,  96% used [0x09d50000, 0x0de3d150, 0x0de3d200, 0x0e0e4000)
 Metaspace       used 39405K, capacity 39861K, committed 40192K, reserved 40320K
}

Deoptimization events (0 events):
No events
~~~
