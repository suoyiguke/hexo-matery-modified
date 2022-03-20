---
title: spring-的-@PostConstruct-注解使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: spring-的-@PostConstruct-注解使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
 @PostConstruct 生效前提是当前类必须纳入spring容器管理！

spring的 @PostConstruct 执行顺序
构造方法  ——> @Autowired/@value —— > @PostConstruct ——> 静态方法 （按此顺序加载）



~~~
静态块
实例块1
实例块2
空构造器
2020-10-09 12:53:11.014  INFO 17860 --- [           main] c.a.d.s.b.a.DruidDataSourceAutoConfigure : Init DruidDataSource
2020-10-09 12:53:11.436  INFO 17860 --- [           main] com.alibaba.druid.pool.DruidDataSource   : {dataSource-1} inited
 _ _   |_  _ _|_. ___ _ |    _ 
| | |\/|_)(_| | |_\  |_)||_|_\ 
     /               |         
                        3.4.0 
PostConstruct执行
~~~

我们可以使用 @PostConstruct 来做一些`使用已经注入属性为原料的，再次使用的预处理操作`
例如下面，我将@PostConstruct声明到 init 方法上，对三个通过ioc注入的属性进一步操作。


~~~
    @Value("${businessOrgCode}")
    private String businessOrgCode;
    @Value("${eas.url}")
    private String easUrl;
    @Value("${businessOrgAppId}")
    private String businessOrgAppId;

    @PostConstruct
    public void init() 
        urlFormat = String.format(easUrl.concat(urlFormat), businessOrgCode, businessOrgAppId,"123");
    }
~~~


###@PostConstruct注解的应用

1、工具类里面的静态方法会去使用classpath下的资源文件。而这这个资源文件需要初始化一次。
如果放到static中初始化，会导致第一次调用类的静态方法时去加载资源文件导致请求被拖慢；
所以我们可以将它放到@PostConstruct里，在容器扫描时就加载好。优化第一次访问的速度

~~~
@Component
public class SignHelperUtils {
    @PostConstruct
    public void init(){
        /**
         * 只有配置GDCA云签时才去做这个操作
         */
        if (Constants.GDCA_AUTHORITY.equals("GDCA")) {
            try {
                ClassPathResource classPathResource = new ClassPathResource(
                    File.separator + "gdca.publickey");
                StringWriter writer = new StringWriter();
                IOUtils.copy(classPathResource.getInputStream(), writer, StandardCharsets.UTF_8.name());
                GDCA_PUBLICKEY = writer.toString();
            } catch (Exception e) {
                logger.error(e.toString());
            }
        }

    }
}

~~~

而不是写在static中：
~~~
    static {
        /**
         * 只有配置GDCA云签时才去做这个操作
         */
        if (Constants.GDCA_AUTHORITY.equals("GDCA")) {
            String userDir = System.getProperty("user.dir");
            FileSystemResource resource = new FileSystemResource(
                new File(userDir.concat("/config/gdca.publickey")));
            try {
                InputStream inputStream = resource.getInputStream();
                StringWriter writer = new StringWriter();
                IOUtils.copy(inputStream, writer, StandardCharsets.UTF_8.name());
                GDCA_PUBLICKEY = writer.toString();
            } catch (IOException e) {
                logger.error(e.toString());
            }
        }

    }
~~~

>为什么@PostConstruct写在内部类里不行？
