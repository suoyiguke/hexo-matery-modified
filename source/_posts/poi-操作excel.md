---
title: poi-操作excel.md
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
title: poi-操作excel.md
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
导入execl到数据库
~~~
package org.szwj.ca.identityauthsrv;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.List;
import java.util.Map;
import org.apache.commons.lang3.StringUtils;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mybatis.spring.boot.test.autoconfigure.MybatisTest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@MybatisTest    //缓存mybatsitest注解
@RunWith(SpringJUnit4ClassRunner.class)
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Rollback(false)
public class IdentityauthsrvApplicationTests {


    @Autowired
    private JdbcTemplate jdbcTemplate;

    /**
     * 插入部门或忽略,返回id
     *
     * @param name
     */
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    @Rollback(false)
    public Integer insertOrIgnoreDepart(String name) {
        if (StringUtils.isBlank(name)) {
            return 0;
        }

        List<Map<String, Object>> maps = jdbcTemplate
            .queryForList("select 1 from biz_department where dept_name = ? limit 1", name);

        if (maps.isEmpty()) {
            jdbcTemplate.update(
                "INSERT INTO `iam`.`biz_department`( `parent_dept_id`, `dept_name`, `dept_code`, `seq`, `created_at`, `updated_at`) VALUES (?, ?, ?, ?, now(),now());"
                , 0, name, "", 1);
        }
        maps = jdbcTemplate
            .queryForList("select dept_id id from biz_department where dept_name = ? limit 1",
                name);
        Map<String, Object> map = maps.get(0);
        Integer id = (Integer) map.get("id");
        return id;


    }

    /**
     * 插入用户
     *
     * @param name
     */

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    @Rollback(false)
    public void insertUser(String mobile, String identity_number, Integer dept_id,
        String user_name) {
        if (StringUtils.isBlank(user_name)) {
            return;
        }

//
//        List<Map<String, Object>> maps = jdbcTemplate
//            .queryForList("select 1 from biz_user where mobile = ? limit 1", mobile);
//
//        if (maps.isEmpty()) {
        int name1 = jdbcTemplate.update(
            "INSERT INTO biz_user(user_id,mobile,identity_number,dept_id,user_name) values( REPLACE(UUID(),'-',''),?,?,?,?)",
            mobile, identity_number, dept_id, user_name);
//        }

    }


    public Workbook getExcel(String filePath) {
        Workbook wb = null;
        File file = new File(filePath);
        if (!file.exists()) {
            System.out.println("文件不存在");
            wb = null;
        } else {
            String fileType = filePath.substring(filePath.lastIndexOf("."));//获得后缀名
            try {
                InputStream is = new FileInputStream(filePath);
                if (".xls".equals(fileType)) {
                    wb = new HSSFWorkbook(is);
                } else if (".xlsx".equals(fileType)) {
                    wb = new XSSFWorkbook(is);
                } else {
                    System.out.println("格式不正确");
                    wb = null;
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return wb;
    }

    @Transactional(propagation = Propagation.NEVER)
    public void analyzeExcel(Workbook wb) {
        for (int i = 0; i < wb.getNumberOfSheets(); i++) {
            Sheet sheet = wb.getSheetAt(i);
            for (int j = 0; j <= sheet.getLastRowNum(); j++) {

                Row row = sheet.getRow(j);

                Cell cell2 = null;
                try {
                    cell2 = row.getCell(2);
                } catch (Exception e) {
                }

                Cell cell4 = null;
                try {
                    cell4 = row.getCell(4);
                } catch (Exception e) {
                }
                Cell cell18 = null;
                try {
                    cell18 = row.getCell(18);
                } catch (Exception e) {
                }

                insertUser(cell18 == null ? "" : cell18.toString(), "",
                    cell4 == null ? 0 : insertOrIgnoreDepart(cell4.toString()),
                    cell2 == null ? "" : cell2.toString());


            }


        }
    }


    @Test
    @Rollback(false)
    @Transactional(propagation = Propagation.NEVER)
    public void contextLoads() {


        Workbook wb = getExcel("D:\\QQ文档\\2542847562\\FileRecv\\市二医院的名单.xlsx");

        if (wb == null) {
            System.out.println("文件读入出错");
        } else {
            analyzeExcel(wb);
        }
    }

}

~~~
