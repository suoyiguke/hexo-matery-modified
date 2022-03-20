---
title: Jeecg-Boot-开发经验积累.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---
---
title: Jeecg-Boot-开发经验积累.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---

######1、排除token验证
如下图，访问自己写的接口无效。提示token失效
![image.png](https://upload-images.jianshu.io/upload_images/13965490-44866afaf77ce0c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们可以找到这个ShiroConfig.java类，将以下注册 jwt 的代码注释掉，如下图

![image.png](https://upload-images.jianshu.io/upload_images/13965490-6bd6a19ed1f1d197.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>注意这种方法会让获得用户失效，只会获得null。这样像一些授权操作就会失效了。然后提示没有权限请联系管理员

######2、前端是如何传token到后端的？
抓取一个请求，可以看到有一个名为X-Access-Token的Request headers
![image.png](https://upload-images.jianshu.io/upload_images/13965490-829d239c413c644f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######3、在controller上使用 @RequiresRoles("admin")
直接访问则会报错如下，只有当前用户的角色是admin的情况下才能访问
![image.png](https://upload-images.jianshu.io/upload_images/13965490-10fd7998a7b3a68a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

再来看org.jeecg.common.exception.JeecgBootExceptionHandler这个类，是全局异常处理器，里面有这个方法。即是它截获了UnauthorizedException.class, AuthorizationException.class两个异常。然后在这里处理
![image.png](https://upload-images.jianshu.io/upload_images/13965490-243ac9e5663375d8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果要正常访问被这个注解所修饰的接口，那么请不要按照第一步的方式注释掉那段代码。

然后将已经登录admin账户后的浏览器请求的的这段信息copy下来
![image.png](https://upload-images.jianshu.io/upload_images/13965490-45a386686a613c41.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
粘贴到postman里，带上token后请求即可！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4b9e16d734ca940e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######4、获得当前用户

1、直接获取，注意若不传token则获取的将是null
~~~
LoginUser sysUser = (LoginUser) SecurityUtils.getSubject().getPrincipal();
System.out.println(sysUser);
~~~

2、或者使用根据token获取用户信息
~~~
    //username账号是唯一的
        String username = JwtUtil.getUsername(TokenUtils.getTokenByRequest(request));
        // 查询用户信息
        LoginUser user = sysBaseAPI.getUserByName(username);
~~~

######5、打印sql
application-dev.yml文件
~~~
#Mybatis输出sql日志,keyi1
logging:
  level:
    org.jeecg.modules.system.mapper : debug
    org.jeecg.modules.app.mapper: debug
  
~~~
这个org.jeecg.modules.app.mapper包是我们创建的包


再配合mybatis-log-plugin插件即可完成打印真实sql

######6、使用原生sql进行分页查询

mapper
~~~
    @Select("SELECT * FROM tb_user where name LIKE  concat('%',#{name},'%') ")
    List<TUser> queryPage(Page<TUser> page,@Param("name") String name);
~~~
TUserService
~~~
  Page<TUser> queryPage(Page<TUser> page, TUser tUser);
~~~
TUserServiceImpl
~~~
 @Override
    public Page<TUser> queryPage(Page<TUser> page, TUser tUser) {
        return page.setRecords(baseMapper.queryPage(page,tUser.getName()));
    }
~~~

TUserController
~~~
@AutoLog(value = "测试-分页")
    @ApiOperation(value = "测试-分页", notes = "测试-分页")
    @RequestMapping(value = "/getListFy", method = RequestMethod.GET)
    public Result<?> getListFy(TUser tUser,
                               @RequestParam(name = "pageNo", defaultValue = "1") Integer pageNo,
                               @RequestParam(name = "pageSize", defaultValue = "10") Integer pageSize) {
        Result<Page<TUser>> result = new Result<>();
        Page<TUser> page = new Page<>(pageNo, pageSize);
        page = tUserService.queryPage(page,tUser);//通知公告消息
        log.info("查询当前页：" + page.getCurrent());
        log.info("查询当前页数量：" + page.getSize());
        log.info("查询结果数量：" + page.getRecords().size());
        log.info("数据总数：" + page.getTotal());
        result.setSuccess(true);
        result.setResult(page);
        return result;
    }
~~~

######7、接口文档

http://localhost:8080/jeecg-boot/swagger-ui.html#/


######8、从库中表导入到表单的单独数据库连接
这个配置的链接库和springboot连接库是分开的
jeecg_database.properties

######9、对于系统中的org.jeecg.common.api.vo.Result类
请不要添加lombok的 `@Accessors(chain = true)` 虽然写起来很舒服，但是加上这个表单预览页面就报错了~

所以还是请这样写：
~~~
Result<Object> ok = Result.ok(tbBox);
        ok.setMessage("操作成功");
        return ok;
~~~

######10、全局异常处理，自定义返回响应状态码 2020/5/10 22:38
 
JeecgBootException 类有两处修改：
1、添加status字段，加上set和get
2、添加一个构造器，传入status
~~~
package org.jeecg.common.exception;

public class JeecgBootException extends RuntimeException {
	private static final long serialVersionUID = 1L;

	/**
	 *@description: 自定义状态
	 *@author: yinkai
	 *@create: 2020/5/10 22:35
	 */
	private Integer status;
	public Integer getStatus() {
		return this.status;
	}
	public void setStatus(final Integer status) {
		this.status = status;
	}

	public JeecgBootException(String message){
		super(message);
	}
	
	public JeecgBootException(Throwable cause)
	{
		super(cause);
	}

	
	public JeecgBootException(String message,Throwable cause)
	{
		super(message,cause);
	}

	/**
	 * 添加一个构造器，传入status
	 * @param message
	 * @param status
	 * @param cause
	 */
	public JeecgBootException(String message,Integer status, Throwable cause)
	{
		super(message,cause);
		this.status = status;
	}
}

~~~

JeecgBootExceptionHandler异常处理类修改
~~~
package org.jeecg.common.exception;

import io.lettuce.core.RedisConnectionException;
import org.apache.shiro.authz.AuthorizationException;
import org.apache.shiro.authz.UnauthorizedException;
import org.jeecg.common.api.vo.Result;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.data.redis.connection.PoolException;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.multipart.MaxUploadSizeExceededException;
import org.springframework.web.servlet.NoHandlerFoundException;

import lombok.extern.slf4j.Slf4j;

/**
 * 异常处理器
 * 
 * @Author scott
 * @Date 2019
 */
@RestControllerAdvice
@Slf4j
public class JeecgBootExceptionHandler {

	/**
	 * 处理自定义异常
	 */
	@ExceptionHandler(JeecgBootException.class)
	public Result<?> handleRRException(JeecgBootException e){
		log.error(e.getMessage(), e);
		/**
		 *@description: 根据状态码构造
		 *@author: yinkai
		 *@create: 2020/5/10 22:38
		 */
		return  e.getStatus()==null? Result.error(e.getMessage()): Result.error(e.getStatus(),e.getMessage());
	}

	@ExceptionHandler(NoHandlerFoundException.class)
	public Result<?> handlerNoFoundException(Exception e) {
		log.error(e.getMessage(), e);
		return Result.error(404, "路径不存在，请检查路径是否正确");
	}

	@ExceptionHandler(DuplicateKeyException.class)
	public Result<?> handleDuplicateKeyException(DuplicateKeyException e){
		log.error(e.getMessage(), e);
		return Result.error("数据库中已存在该记录");
	}

	@ExceptionHandler({UnauthorizedException.class, AuthorizationException.class})
	public Result<?> handleAuthorizationException(AuthorizationException e){
		log.error(e.getMessage(), e);
		return Result.noauth("没有权限，请联系管理员授权");
	}

	@ExceptionHandler(Exception.class)
	public Result<?> handleException(Exception e){
		log.error(e.getMessage(), e);
		return Result.error("操作失败，"+e.getMessage());
	}
	
	/**
	 * @Author 政辉
	 * @param e
	 * @return
	 */
	@ExceptionHandler(HttpRequestMethodNotSupportedException.class)
	public Result<?> HttpRequestMethodNotSupportedException(HttpRequestMethodNotSupportedException e){
		StringBuffer sb = new StringBuffer();
		sb.append("不支持");
		sb.append(e.getMethod());
		sb.append("请求方法，");
		sb.append("支持以下");
		String [] methods = e.getSupportedMethods();
		if(methods!=null){
			for(String str:methods){
				sb.append(str);
				sb.append("、");
			}
		}
		log.error(sb.toString(), e);
		//return Result.error("没有权限，请联系管理员授权");
		return Result.error(405,sb.toString());
	}
	
	 /** 
	  * spring默认上传大小100MB 超出大小捕获异常MaxUploadSizeExceededException 
	  */
    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public Result<?> handleMaxUploadSizeExceededException(MaxUploadSizeExceededException e) {
    	log.error(e.getMessage(), e);
        return Result.error("文件大小超出10MB限制, 请压缩或降低文件质量! ");
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public Result<?> handleDataIntegrityViolationException(DataIntegrityViolationException e) {
    	log.error(e.getMessage(), e);
        return Result.error("字段太长,超出数据库字段的长度");
    }

    @ExceptionHandler(PoolException.class)
    public Result<?> handlePoolException(PoolException e) {
    	log.error(e.getMessage(), e);
        return Result.error("Redis 连接异常!");
    }

}

~~~

使用如下，指定状态码为201
~~~
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    public Result test(HttpServletRequest request) {

        try {
            int i = 1 / 0;
        }catch (Exception e){
            throw new JeecgBootException("除0异常",201,e);
        }
        return Result.ok();

    }
~~~
执行效果：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ea635e29444c4906.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
