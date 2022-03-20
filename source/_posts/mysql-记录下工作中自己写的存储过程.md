---
title: mysql-记录下工作中自己写的存储过程.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: mysql-记录下工作中自己写的存储过程.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
1、 随机读a表的一行数据，循环插入到b表
~~~
CREATE DEFINER="root"@"%" PROCEDURE "updateDate"()
BEGIN

declare countNumber int(225);  
declare userName varchar(225);  
declare employeeNum varchar(225);  
declare identityNumber varchar(225);  
declare certId varchar(225);  
DECLARE i int unsigned DEFAULT 1;



 WHILE i <= 3827 DO


SELECT user_name,employee_num,identity_number,id INTO userName,employeeNum,identityNumber,certId FROM biz_cloudsign_cert_info ORDER BY RAND() LIMIT 1;

update biz_cloudsign_login_mock set user_name = userName ,identity_number = employeeNum ,employee_num = identityNumber,cert_id=certId where id =i;

set i = i+1;

SELECT userName,employeeNum,identityNumber,certId;

 END WHILE;


         


END
~~~

2、使用游标实现： 遍历表a，将部分字段插入到表b。其中有字段需要通过关联查询其它表来得到

其中使用IFNULL + max 可以解决游标没有完全遍历完就退出的问题

>SELECT IFNULL(max(dept_id),0)   
~~~
BEGIN
  DECLARE userId varchar(225);
  DECLARE userName varchar(225);
  DECLARE employeeNum varchar(225);
	DECLARE identityNumber varchar(225);
	DECLARE mobile_ varchar(225);
	DECLARE userDepartment varchar(225);
	DECLARE userDepartmentint int;
    # 定义循环退出标志符变量
    DECLARE flag INT DEFAULT 0;

    DECLARE getgoods CURSOR FOR  SELECT user_id,user_name,employee_num,identity_number,user_department  FROM biz_cloudsign_cert_info WHERE user_id not in(SELECT user_id FROM biz_user ) GROUP BY user_id;
  # 定义监听器
    DECLARE CONTINUE HANDLER FOR NOT FOUND set flag :=1;

    OPEN getgoods;
    # 提前FETCH下
    FETCH getgoods INTO userId, userName, employeeNum,identityNumber,userDepartment;
    
  # 换成while循环，就不会当返回集为null时查出数据为空的了
    # 注意while循环的循环条件为true时才进入循环
  WHILE flag=0 DO
 
        FETCH getgoods INTO  userId, userName, employeeNum,identityNumber,userDepartment;
				SELECT IFNULL(max(mobile),'')  INTO mobile_ FROM biz_cert_apply_record WHERE employee_num=employeeNum limit 1;
				SELECT IFNULL(max(dept_id),0)  INTO userDepartmentint  from biz_department WHERE dept_name= if((ISNULL(userDepartment)=1) || (LENGTH(trim(userDepartment))=0),'Administrator',userDepartment)  limit 1;

				
				INSERT INTO `biz_user`(`user_id`, `user_name`, `employee_num`, `gender`, `dept_id`, `identity_type`, `identity_number`, `mobile`, `email`, `postal_address`, `post_code`, `status`, `job_posts`, `qualification`, `license`, `note`, `ttp_user_oid`, `authentication_mark`, `enabled`, `created_at`, `updated_at`) VALUES (userId, userName, employeeNum, 0, userDepartmentint, 0, identityNumber,mobile_, '', '', '', 0, '', '', '', '', '', CONCAT('SF',identityNumber), 0, '2020-07-31 09:20:01', '2020-07-31 09:20:01');
			
  END WHILE;
    CLOSE getgoods;  

END
~~~
