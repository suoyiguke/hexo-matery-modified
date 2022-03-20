---
title: Elasticsearch--使用script-解决排序问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 全文搜索
categories: 全文搜索
---
---
title: Elasticsearch--使用script-解决排序问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 全文搜索
categories: 全文搜索
---
elasticsearch解决某一字段值等于某字符串时优先排序问题



elasticsearch解决某一字段值等于某字符串时优先排序问题，这个很让我困扰，数据库中source字段为qyer时排在前面，对，就是这样用script完成这个排序
 

public Map<String, Object> findByQuestion(String content,int page){
		Map<String, Object> results=new HashMap<>();
		MatchQueryBuilder matchQueryBuilder=new MatchQueryBuilder("contents", content);
		matchQueryBuilder.analyzer("ik");
		TermQueryBuilder termQueryType=new TermQueryBuilder("type", "question");
		Page<QA> questionQa=qaRepository.search(new NativeSearchQueryBuilder()
				.withQuery(new AndQueryBuilder().add(matchQueryBuilder).add(termQueryType))
				.withPageable(new PageRequest(page, 10))
				.withSort(new ScoreSortBuilder().order(SortOrder.DESC))
				.withSort(new ScriptSortBuilder("'qyer'==doc['source'].value?0:('mafengwo'==doc['source'].value?1:2)","number").order(SortOrder.ASC))
				.withSort(new FieldSortBuilder("view_cnt").order(SortOrder.DESC))
				.build());
		System.err.println("----------------------------------------");
		System.err.println("总问题数:"+questionQa.getTotalElements());
		System.err.println("总页数:"+questionQa.getTotalPages());
		System.err.println("----------------------------------------");
		Map<String, Object> map=new HashMap<>();
		List<Map<String, Object>> listmap=new ArrayList<>();
		for(QA qa:questionQa.getContent()){
			
			map.put("question",qa);
			Page<QA> answerQas=qaRepository.search(new NativeSearchQueryBuilder()
			.withQuery(new AndQueryBuilder().add(new TermQueryBuilder("qid", qa.getQid())).add(new TermQueryBuilder("type", "answer")))
			.withSort(new FieldSortBuilder("view_cnt").order(SortOrder.DESC))
			.build());
			List<QA> qas=new ArrayList<QA>();
			for(QA answerQa:answerQas.getContent()){
				qas.add(answerQa);
			}
			map.put("answer", qas);
			listmap.add(map);
		}
		results.put("results", listmap);
		return results;
	}
————————————————
版权声明：本文为CSDN博主「张小竟」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/zhanglu1236789/article/details/56678443
