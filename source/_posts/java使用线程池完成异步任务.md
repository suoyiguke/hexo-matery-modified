---
title: java使用线程池完成异步任务.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
---
title: java使用线程池完成异步任务.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
管理系统中，在执行耗时的操作时阻塞用户主线程。用户界面迟迟得不到返回信息，甚至是超时；在这种业务场景下可以使用异步任务

- 用户发出了一个耗时操作请求，主线程立即return
- 如果当前异步任务没有被执行完，用户再次发起提示“有任务正在执行“，直到当前任务执行完毕才允许再次执行
- 提供中断当前正在执行的任务功能

###先看看效果

![gif.gif](https://upload-images.jianshu.io/upload_images/13965490-430197a8888cfe68.gif?imageMogr2/auto-orient/strip)


###java代码
~~~

package io.renren.modules.generator.service.impl;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.support.spring.FastJsonJsonView;
import com.baomidou.mybatisplus.mapper.EntityWrapper;
import com.baomidou.mybatisplus.mapper.Wrapper;
import com.baomidou.mybatisplus.plugins.Page;
import com.baomidou.mybatisplus.service.impl.ServiceImpl;
import com.hankcs.hanlp.HanLP;
import io.netty.handler.codec.http.websocketx.TextWebSocketFrame;
import io.renren.common.utils.PageUtils;
import io.renren.common.utils.Query;
import io.renren.common.utils.R;
import io.renren.modules.backstage.service.ArticleService;
import io.renren.modules.generator.dao.KeywordDao;
import io.renren.modules.generator.entity.KeywordEntity;
import io.renren.modules.generator.service.KeywordService;
import io.renren.modules.main.entity.Article;
import io.renren.modules.websocket.handler.MyChannelHandlerPool;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.text.DecimalFormat;
import java.util.List;
import java.util.Map;
import java.util.concurrent.*;


@Service("keywordService")
public class KeywordServiceImpl extends ServiceImpl<KeywordDao, KeywordEntity> implements KeywordService {
    @Autowired
    private ArticleService articleService;

    private KeywordDao getMapper() {
        return this.baseMapper;
    }


    //单线程的线程池
    private ExecutorService executor = Executors.newSingleThreadExecutor();
    private ExecutorService executorFlag = Executors.newSingleThreadExecutor();

    private Future<?> future;

    private FutureTask getTask() {
        FutureTask<Boolean> booleanFutureTask = new FutureTask<Boolean>(new Callable<Boolean>() {
            @Override
            public Boolean call() {
                List<Article> textAll = articleService.getMapper().getTextAll();
                for (Article article : textAll) {
                    List<String> keywordList = HanLP.extractKeyword(article.getContent(), 5);
                    String[] arr = keywordList.toArray(new String[keywordList.size()]);
                    String join = String.join(",", arr);
                    KeywordEntity keyWord = new KeywordEntity();
                    keyWord.setKeyWord(join);
                    keyWord.setArticleId(article.getNewId().intValue());
                    keyWord.setType(article.getType());
                    getMapper().insert(keyWord);
                }
                return true;
            }
        });
        return booleanFutureTask;
    }


    @Override
    public PageUtils queryPage(Map<String, Object> params) {
        //查询参数
        String key = (String) params.get("key");
        //Wrapper
        Wrapper<KeywordEntity> wrapper = new EntityWrapper<KeywordEntity>().like("key_word", key);
        //解析分页参数
        Page<KeywordEntity> pa = new Query<KeywordEntity>(params).getPage();
        //设置总数
        pa.setTotal(this.selectCount(wrapper));
        //分页查询
        Page<KeywordEntity> page = this.selectPage(
                pa,
                wrapper
        );
        //构造pageBean
        return new PageUtils(page);
    }

    @Override
    public R generateKeyWord() {

        String msg;
        if (future == null || future.isDone()) {
            future = executor.submit(getTask());
            msg = "开始新任务";
            //子线程去推送生成进度
            executorFlag.submit(() -> {
                while (!(future == null || future.isDone())) {
                    MyChannelHandlerPool.channelGroup.writeAndFlush(new TextWebSocketFrame(getProgress().toString()));
                }
            });


        } else {
            msg = "任务未结束！不能重复生成，请等待片刻";
        }
        System.out.println("============执行后===================");
        System.out.println(future.isCancelled());
        System.out.println(future.isDone());
        System.out.println("=============执行后==================");
        return R.ok(msg);
    }

    @Override
    public R truncateKeyWord() {
        if (future != null && !future.isDone()) {
            //结束生成任务
            future.cancel(true);
        }
        baseMapper.truncateKeyWord();
        return R.ok();
    }

    @Override
    public Float getProgress() {
        return articleService.getMapper().getAllIdCount().floatValue();
    }

}

~~~

###关键点
- 通过future.isDone() 判断当前任务是否完成
- 通过future.cancel(true) 终止当前正在执行的任务
