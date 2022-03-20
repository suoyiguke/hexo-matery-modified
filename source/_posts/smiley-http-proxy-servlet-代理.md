---
title: smiley-http-proxy-servlet-代理.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: smiley-http-proxy-servlet-代理.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
>https://github.com/mitre/HTTP-Proxy-Servlet/

最近接到一个需求：统一一个入口，将不同医院的职工人员请求转发到各个医院的服务。
通过用户工号查数据库得到所属医院服务地址。然后代理过去就行了。

查了查资料，smiley-http-proxy-servlet这个二方库不错。可以完成动态的代理。

~~~
    <dependency>
      <groupId>org.mitre.dsmiley.httpproxy</groupId>
      <artifactId>smiley-http-proxy-servlet</artifactId>
      <systemPath>${pom.basedir}/jar/smiley-http-proxy-servlet-1.12.jar</systemPath>
      <scope>system</scope>
      <version>1.12</version>
    </dependency>
~~~


~~~
package org.szwj.ca.identityauthsrv.controller;
import com.alibaba.fastjson.JSONObject;
import com.google.common.collect.ImmutableMap;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.URI;
import java.util.Map;
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.lang3.StringUtils;
import org.apache.http.HttpHost;
import org.apache.http.client.utils.URIUtils;
import org.mitre.dsmiley.httpproxy.ProxyServlet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;
import org.szwj.ca.identityauthsrv.dao.DataDao;
import org.szwj.ca.identityauthsrv.entity.exception.CaHelperException;
import org.szwj.ca.identityauthsrv.entity.jwt.JwtVO;
import org.szwj.ca.identityauthsrv.service.intfc.JwtService;
import org.szwj.ca.identityauthsrv.util.common.json.JsonHelper;

@Configuration
public class ProxyConfig {

    private static Logger logger = LoggerFactory.getLogger(ProxyConfig.class);
    @Autowired
    private MyProxyServlet myProxyServlet;


    @Bean
    public ServletRegistrationBean proxyServletRegistration() {
        ServletRegistrationBean registrationBean = new ServletRegistrationBean(myProxyServlet,
            "/*");
        //设置网址以及参数
        Map<String, String> params = ImmutableMap
            .of("targetUri", StringUtils.EMPTY, "log", "true");
        registrationBean.setInitParameters(params);
        return registrationBean;
    }


    @Component
    static class MyProxyServlet extends ProxyServlet {

        private static Logger logger = LoggerFactory.getLogger(ProxyServlet.class);
        private static final String URL_FORMAT = "http://%s";
        @Autowired
        private DataDao dataDao;
        @Autowired
        private JwtService jwtService;

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
                JSONObject param = JSONObject.parseObject(body);
                relBizNo = param.getString("relBizNo");
                if (StringUtils.isBlank(relBizNo)) {
                    String encryptedToken = param.getString("encryptedToken");

                    JwtVO jwtVO = null;
                    try {
                        jwtVO = jwtService.decryptToken(encryptedToken);
                    } catch (CaHelperException e) {
                        msg = "代理失败，encryptedToken非法" + e.getMessage();
                        logger.error("[End] {}, 业务系统编码:{}, ip:{}", msg);
                        write(servletResponse, msg, -12);
                    }
                    relBizNo = jwtVO.getEmployeeNum();

                    if (StringUtils.isBlank(relBizNo)) {
                        msg = "代理失败，relBizNo、encryptedToken 均为为空，请检查参数";
                        logger.error(msg);
                        write(servletResponse, msg, -11);
                        return;
                    }

                }

                if (StringUtils.isBlank(relBizNo)) {
                    msg = "代理失败，relBizNo 为空，请检查参数";
                    logger.error(msg);
                    write(servletResponse, msg, -13);
                    return;
                }

                String userServerIp = dataDao.getUserServerIp(relBizNo);
                if (StringUtils.isBlank(userServerIp)) {
                    msg = String.format(
                        String.format("代理失败，serverIp为空，请检查数据库中的对应关系 relBizNo=%s", relBizNo));
                    logger.error(msg);
                    write(servletResponse, msg, -24);
                    return;

                }
                String serverUrl = String.format(URL_FORMAT, userServerIp);
                servletRequest.setAttribute(ATTR_TARGET_URI, serverUrl);
                try {
                    URI url = new URI(serverUrl);
                    HttpHost httpHost = URIUtils.extractHost(url);
                    servletRequest.setAttribute(ATTR_TARGET_HOST, httpHost);
                } catch (Exception e) {
                    msg = String.format("代理失败，new URI失败，url=%s", serverUrl, e.toString());
                    logger.error(msg, e);
                    write(servletResponse, msg, -15);
                    return;
                }
                super.service(servletRequest, servletResponse);

            }
        }

    }


    private static void write(HttpServletResponse response, String msg, Integer code) {
        String responseJson = JsonHelper.generateResponse(code, msg, null);
        response.setContentType("application/json;charset=utf-8");
        PrintWriter writer = null;
        try {
            writer = response.getWriter();
        } catch (IOException e) {
            logger.error("response.getWriter 异常", e);
        }
        writer.write(responseJson);
        writer.close();


    }
}
~~~


但是现在还有些问题：

1、想要根据request参数选择是否进行代理，目前还做不到。如根据工号是否为空，为空则不进行代理直接访问localhost。如果只是将代理ip设置为localhost或者使用请求转发到localhost对应接口，那么会陷入无限循环之中。
现在的处理方案是另写一份目标接口代码，然后代理到上面去就不会死循环了。但是不够优雅，本想查阅smiley-http-proxy-servlet文档看看有没有解决方案。由于时间不够等多方面原因就暂时这样写了。

