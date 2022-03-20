---
title: webflux-主动推送数据.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
---
title: webflux-主动推送数据.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
1、主动推送数据
~~~
    @GetMapping(value = "/test", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<Book> sseBook() {
        return Flux.interval(Duration.ofSeconds(1))
                .map(
                        second ->
                                new Book()
                                        .setId(String.valueOf(second))
                                        .setName("深入浅出Flux响应式Web编程" + second)
                                        .setPrice("12")
                ).take(5);
    }


    @Data
    @Accessors(chain = true)
    class Book {
        private String id;
        private String name;
        private String price;
        private Date createTime = new Date();
    }

~~~
