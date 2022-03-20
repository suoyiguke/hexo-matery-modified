---
title: 二次读取request-body中的参数数据.md
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
title: 二次读取request-body中的参数数据.md
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
有时候我们需要到拦截器中做下参数的预处理，如危险字符过滤、权限判断、打印请求参数日志 等操作。
以前使用url中以？和& 拼接或使用form-data等传参形式都没有问题。 而现在参数都以contentType="application/json;charset=utf-8" 的形式放到了request Body中，如果我们提前去拿一次，那么等程序运行到controller中时参数已经是为空再也获取不到了。所以我们得想办法解决这个问题。

如下先自定义一个Request类：RequestWrapper 继承HttpServletRequestWrapper 。
- 定义类属性HttpServletRequest，this.request保存request的引用。
- 定义类属性byte[] requestBody， 在重写的getInputStream方法中使用IOUtils.copy将输入流转输出流再转 byte[]，然后进行赋值。
- 最后构造一个ByteArrayInputStream 返回。这样就不会影响原来request的InputStream。


~~~
package org.szwj.ca.identityauthsrv.controller;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import javax.servlet.ReadListener;
import javax.servlet.ServletInputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletRequestWrapper;
import org.apache.commons.io.IOUtils;

public class RequestWrapper extends HttpServletRequestWrapper {

        private final Logger logger = LoggerFactory.getLogger(RequestWrapper.class);

        //参数字节数组
        private byte[] requestBody;
        //Http请求对象
        private HttpServletRequest request;

        public RequestWrapper(HttpServletRequest request) throws IOException {
            super(request);
            this.request = request;
            getInputStream();
        }

        /**
         * @return
         * @throws IOException
         */
        @Override
        public ServletInputStream getInputStream() throws IOException {
            /**
             * 每次调用此方法时将数据流中的数据读取出来，然后再回填到InputStream之中
             * 解决通过@RequestBody和@RequestParam（POST方式）读取一次后控制器拿不到参数问题
             */
            if (null == this.requestBody) {
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                ServletInputStream inputStream = request.getInputStream();
                IOUtils.copy(inputStream, baos);
                this.requestBody = baos.toByteArray();
                baos.close();
                inputStream.close();
            }

            /**
             * 关键一步，自己构造 ServletInputStream。没有这一部分后面再从request拿出来的参数还是空的
             */
            final ByteArrayInputStream bais = new ByteArrayInputStream(requestBody);
            return new ServletInputStream() {

                @Override
                public boolean isFinished() {
                    return false;
                }

                @Override
                public boolean isReady() {
                    return false;
                }

                @Override
                public void setReadListener(ReadListener listener) {

                }

                @Override
                public int read() {
                    int read = bais.read();
                    try {
                        bais.close();
                    } catch (IOException e) {
                        logger.error("bais.close() 异常", e);
                    }
                    return read;
                }
            };

        }

        public byte[] getRequestBody() {
            return requestBody;
        }

        @Override
        public BufferedReader getReader() throws IOException {
            return new BufferedReader(new InputStreamReader(this.getInputStream()));
        }

    }
}


~~~

编写Filter，将自定义的RequestWrapper对象传入 chain.doFilter。

~~~
@Component
@WebFilter(filterName = "proxyFilter", urlPatterns = {"/*"})
class ProxyFilter implements Filter {
    private static final Logger logger = LoggerFactory.getLogger(ProxyFilter.class);
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) {
        try {
            ServletRequest requestWrapper = null;
            if (request instanceof HttpServletRequest) {
                requestWrapper = new RequestWrapper((HttpServletRequest) request);
            }
            if (requestWrapper == null) {
                chain.doFilter(request, response);
            } else {
                chain.doFilter(requestWrapper, response);
            }
        } catch (IOException e) {
            logger.error("ProxyFilter.doFilter 异常", e);
        } catch (ServletException e) {
            logger.error("ProxyFilter.doFilter 异常", e);
        }
    }
    @Override
    public void destroy() {
    }
}
~~~


在拦截器中使用如下

~~~
        @Override
        protected void service(HttpServletRequest servletRequest,
            HttpServletResponse servletResponse) throws ServletException, IOException {
            String msg = "";
            RequestWrapper requestWrapper = null;
            String relBizNo = "";
            if (servletRequest instanceof RequestWrapper) {
                requestWrapper = (RequestWrapper) servletRequest;
                byte[] requestBody = requestWrapper.getRequestBody();
                String body = new String(requestBody);
~~~
