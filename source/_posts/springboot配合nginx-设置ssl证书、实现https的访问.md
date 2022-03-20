---
title: springboot配合nginx-设置ssl证书、实现https的访问.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
---
title: springboot配合nginx-设置ssl证书、实现https的访问.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
>  你好，朋友

我们在一些网站上生成一个证书压缩包如下，适用于4种应用服务器下的ssl配置。分别为 apache、iis、nginx、tomcat
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1c3e7cdcb473cf3a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###我们先来看如何在springboot中配置ssl证书，达到https访问的目的
我们知道springboot工程里面有内嵌tomcat，那就是要选择tomcat目录下的证书了。

选择tomcat文件夹内的xxx.jks 文件，将之复制到工程的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-432039dd23b2602c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

resources文件夹根目录下，即是classpath下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d23d56df896cf045.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


将之配置到yml下
> 注意这个 key-store-password即是tomcat文件夹内的`keystorePass.txt`中的内容；key-store指定jks文件的路径。
~~~
server:
  port: 8080
  ssl:
    key-store: classpath:xxx.jks
    key-store-password: 123456

~~~

重启项目报这个错，估计这个xxx.jks文件没有被编译打包到输出文件夹：
> Caused by: java.io.IOException: Invalid keystore format

解决：maven中添加 <filtering>false</filtering>
~~~
<build>
		<resources>
			<resource>
				<filtering>false</filtering>
			</resource>
		</resources>
	
	</build>
~~~

但是加了这个之后虽然支持https了，mybatis又报mapper.xml找不到的错误。。

所以只有一个两全其美的方式才行，为了能够将配置文件一并打包到工程的jar包中，就需要加入下面配置：

~~~
    <resources>
            <resource>
                <directory>src/main/java</directory>
                <!-- 此配置不可缺，否则mybatis的Mapper.xml将会丢失 -->
                <includes>
                    <include>**/*.xml</include>
                </includes>
            </resource>
            <!--指定资源的位置-->
            <resource>
                <directory>src/main/resources</directory>
                <includes>
                    <include>**/*.**</include>

                </includes>
            </resource>
            <resource>
                <directory>src/main/webapp</directory>
                <targetPath>META-INF/resources</targetPath>
                <includes>
                    <include>**/*.*</include>
                </includes>
            </resource>
        </resources>
~~~

而且现在前端的websocket 也报错了
>was loaded over HTTPS, but attempted to connect to the insecure WebSocket endpoint 'ws://111.231.198.149:8080//websocket/e9ca23d68d884d4ebb19d07889727dae'. This request has been blocked; this endpoint must be available over WSS.

这个问题先放下，有时间再来看看


![image.png](https://upload-images.jianshu.io/upload_images/13965490-9949a06fdd6e95e3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


配置完毕后部署到服务器，启动工程后访问如下：这样就能够通过https访问springboot工程了。不过不知道为什么这里的https图标不是绿色而是灰色的。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-073f4d11b7776ff6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###ngnix实现https，并代理springboot的请求、将http请求转为https


######首先，先使用docker-compose.yml部署ngnix 
~~~
version: "2"
services:
  https-nginx-server:
    image: nginx
    container_name: "https-nginx-server"
    ports:
      - 80:80
      - 443:443
    volumes:
      - ./conf.d:/etc/nginx/conf.d
      - ./conf/nginx.conf:/etc/nginx/nginx.conf
      - ./conf/xxx.crt:/etc/nginx/xxx.crt
      - ./conf/xxx.key:/etc/nginx/xxx.key
      - ./log:/var/log/nginx
      - ./www:/var/www
      - /etc/letsencrypt:/etc/letsencrypt

    network_mode: 'host'
    restart: always

~~~
conf文件夹下的文件如下 ，包含证书文件xxx.crt、秘钥文件 xxx.key、nginx.conf
![image.png](https://upload-images.jianshu.io/upload_images/13965490-21c8af18ba30775f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######nginx.conf文件
~~~
worker_processes  1;
events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    gzip  on;


    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name  xxx;
        ssl_certificate xxx.crt;
        ssl_certificate_key xxx.key;
        ssl_session_cache    shared:SSL:1m;
        ssl_session_timeout  5m;
        server_tokens off;
        fastcgi_param   HTTPS               on;
        fastcgi_param   HTTP_SCHEME         https;
        location / {
            proxy_pass https://xxx:8080/; #代理转发的路径
            proxy_redirect default;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-for $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            error_page 502 = /500.html;
        }

    }

   server {
        listen       80;
        server_name  xxx;#访问的路径
        return 301 https://$host$1;
    }

}
~~~

打开证书压缩包内的ngnix文件夹：可以看到一个 crt和一个key文件。将之复制到/conf下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f99dc3af03c98530.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

nginx中有配置两个server节点，一个监听443端口，一个监听80端口；443端口的server配置上证书和秘钥，并使用proxy_pass 代理到我们的springboot工程路径`https://xxx:8080/`下；80端口的server直接将请求重定向到https上，实现http转https。




> 注意点1：  proxy_pass https://xxx:8080/; 表示将https://xxx的请求代理至 https://xxx:8080/ 这里（这个路径即是上面的springboot工程的请求路径，而且这种`代理` 类似于咱们javaweb下的`服务器请求转发` ，意味着地址栏不会发生改变）


> 注意点2： return 301 https://\$host\$1; 表示将http://xxx的请求重定向到上面配置的https://xxx，实现http转https（这种功能还可以使用rewrit实现，类似于javaweb中的浏览器重定向。地址栏会变为目标地址）


配置完毕后，启动ngnix。如下，终于可以直接使用域名，不加8080端口来访问咱们的springboot工程了。而且这里的https图片是绿色的，虽然不知道是什么意思。绿色总比之前的灰色好吧？
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f4bb842053d5ad5f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######下面说一些注意事项
刚刚配置好了就是不能使用https访问，https请求总是阻塞很久然后失败。看看是不是端口没有开放出来。

1、我这里使用腾讯云服务器，必须先到腾讯云上将 443、80、8080端口打开；443是https的默认端口、80是http的默认端口、8080则是springboot工程的端口

2、如果仍然不能使用https访问，试下手动开启443端口，重启防火墙（我就是使用这个方式解决的~）

~~~
firewall-cmd --zone=public --add-port=443/tcp --permanent 
success
firewall-cmd --reload
success
~~~
