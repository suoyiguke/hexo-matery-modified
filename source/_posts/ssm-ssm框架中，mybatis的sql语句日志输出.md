---
title: ssm-ssm框架中，mybatis的sql语句日志输出.md
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
title: ssm-ssm框架中，mybatis的sql语句日志输出.md
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

log4j.properties 文件中
~~~
#mybatis部分
log4j.logger.com.ibatis=DEBUG
log4j.logger.com.ibatis.common.jdbc.SimpleDataSource=DEBUG
log4j.logger.com.ibatis.common.jdbc.ScriptRunner=DEBUG
log4j.logger.com.ibatis.sqlmap.engine.impl.SqlMapClientDelegate=DEBUG
#与sql相关
log4j.logger.java.sql.Connection=DEBUG
log4j.logger.java.sql.Statement=DEBUG
log4j.logger.java.sql.PreparedStatement=DEBUG
~~~
>注意要是debug级别


打印的sql
~~~
2021-06-01 09:32:37,057 [// -  - ] DEBUG java.sql.Connection - ooo Using Connection [com.mysql.jdbc.JDBC4Connection@43f36453]
2021-06-01 09:32:37,057 [// -  - ] DEBUG java.sql.Connection - ==>  Preparing: select id, member_no, create_date, creator, modify_date, modifier, template_name, seq, uuid, is_default, printer, system_template_id, is_print_picker_info, is_print_send_date, is_print_pack_weight, is_print_post_fee_and_pack_weight, is_print_declared_value, picker_info, user_member_no, cainiao_token, address_id, is_print_goods, account_id, is_dense_encrypt, is_print_re_addr_memo, is_print_pickup_date, is_print_pay_method, is_print_cod_card_no, is_print_cod_amount, is_print_express_type, is_print_trade_no, not_print_logo, is_print_insurance_amount, is_print_bar_code, shipper_company_flag, shipper_name_flag, shipper_phone_flag, shipper_address_flag, shipper_remark_flag, receiver_company_flag, receiver_name_flag, receiver_phone_flag, receiver_address_flag, pay_cust_id_flag, order_ext_flag, return_remark_flag, is_auto_add from client_print_template WHERE ( member_no = ? and id = ? ) 
2021-06-01 09:32:37,058 [// -  - ] DEBUG java.sql.PreparedStatement - ==> Parameters: 16224543761249(Long), 3256(Long)
~~~
