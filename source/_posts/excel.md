---
title: excel.md
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
title: excel.md
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

~~~
  <!-- https://mvnrepository.com/artifact/org.apache.poi/poi -->
    <dependency>
      <groupId>org.apache.poi</groupId>
      <artifactId>poi</artifactId>
      <version>3.14</version>
    </dependency>
    <!-- https://mvnrepository.com/artifact/org.apache.poi/poi-ooxml -->
    <dependency>
      <groupId>org.apache.poi</groupId>
      <artifactId>poi-ooxml</artifactId>
      <version>3.14</version>
    </dependency>
~~~


###读取excel为List<Map>，以第一行为key

~~~
package org.szwj.ca.identityauthsrv;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.apache.poi.hssf.usermodel.HSSFCell;
import org.apache.poi.hssf.usermodel.HSSFDateUtil;
import org.apache.poi.hssf.usermodel.HSSFRow;
import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.util.NumberToTextConverter;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class Ex {

    public static List<Map<String, Object>> readExcel(InputStream inputStream) throws Exception {
        int sheetnum = 0, startrow = 0, startcol = 0;
        List<Map<String, Object>> list = new ArrayList<Map<String, Object>>();
        try {
            Workbook workbook = new XSSFWorkbook(inputStream);
            Sheet sheet = workbook.getSheetAt(sheetnum);                     //sheet 从0开始
            int rowNum = sheet.getLastRowNum() + 1;                     //取得最后一行的行号
            Map<String, Object> Header = new HashMap<String, Object>();   //表头的下标和内容
            for (int i = startrow; i < rowNum; i++) {                    //行循环开始
                Map<String, Object> map = null;//每一行数据的map
                Row row = sheet.getRow(i);                             //行
                if (row == null) {
                    break; //中间如果有空行，则退出
                }
                int cellNum = row.getLastCellNum();                     //每行的最后一个单元格位置
                if (i != 0) {//记录数据的行号
                    map = new HashMap<String, Object>();
                    map.put("lineNumber", i + 1);
                }
                for (int j = startcol; j < cellNum; j++) {               //列循环开始
                    Cell cell2 = row.getCell(j);
                    //HSSFCell cell = row.getCell(Short.parseShort(j + ""));
                    //String cellValue = getCellValue(cell, format);
                    String cellValue = getCellValue(cell2);
                    //如果当前行的第一列为空,则跳过该行
                    /*if(j==0 && ("".equals(cellValue)||null==cellValue)){
                    	break;
                    }*/
                    if (i == 0) {
                        Header.put(j + "", cellValue);
                    } else {
                        map.put((String) Header.get(j + ""), cellValue);
                    }
                }
                //每一行数据的过滤,如果一行中所有列都为null,则不生成该行数据,
                if (null != map) {
                    Collection<Object> values = map.values();
                    Set<String> keySet = map.keySet();
                    long count2 = keySet.stream().filter(o -> !o.equals("lineNumber")).count();//总条数
                    long count = values.stream().filter(o -> null == o).count();//为空的条数
                    if (count < count2) {
                        list.add(map);
                    }
                }
            }
            workbook.close();
        } catch (Exception e) {
            throw e;
        }
        return list;
    }

    /**
     * 根据excel单元格类型获取excel单元格值
     *
     * @param cell
     * @return
     */


    private static String getCellValue(Cell cell) {
        String cellvalue = null;
        if (cell != null) {
            // 判断当前Cell的Type
            switch (cell.getCellType()) {
                // 如果当前Cell的Type为NUMERIC
                case HSSFCell.CELL_TYPE_NUMERIC: {
                    short format = cell.getCellStyle().getDataFormat();
                    if (format == 14 || format == 31 || format == 57
                        || format == 58) { //excel中的时间格式
                        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
                        double value = cell.getNumericCellValue();
                        Date date = org.apache.poi.ss.usermodel.DateUtil.getJavaDate(value);
                        cellvalue = sdf.format(date);
                    }
                    // 判断当前的cell是否为Date
                    else if (HSSFDateUtil.isCellDateFormatted(
                        cell)) { //先注释日期类型的转换，在实际测试中发现HSSFDateUtil.isCellDateFormatted(cell)只识别2014/02/02这种格式。 
                        // 如果是Date类型则，取得该Cell的Date值 // 对2014-02-02格式识别不出是日期格式
                        Date date = cell.getDateCellValue();
                        DateFormat formater = new SimpleDateFormat("yyyy-MM-dd");
                        cellvalue = formater.format(date);
                    } else { // 如果是纯数字
                        // 取得当前Cell的数值
                        cellvalue = NumberToTextConverter.toText(cell.getNumericCellValue());

                    }
                    break;
                }
                // 如果当前Cell的Type为STRIN
                case HSSFCell.CELL_TYPE_STRING:
                    // 取得当前的Cell字符串
                    cellvalue = cell.getStringCellValue().replaceAll("'", "''");
                    break;
                case HSSFCell.CELL_TYPE_BLANK:
                    cellvalue = null;
                    break;
                // 默认的Cell值
                default: {
                    cellvalue = "";
                }
            }
        } else {
            cellvalue = "";
        }
        return cellvalue;
    }

    public static void main(String[] args) throws Exception {
        FileInputStream fileInputStream = new FileInputStream(new File(
            "G:\\微信文档\\WeChat Files\\wxid_etg2ykli7u2v22\\FileStorage\\File\\2020-06\\市二院2013到2020年的统计\\市二院2013到2020年的统计\\补办丢失消化内科.xlsx")
        );

        List<Map<String, Object>> maps = readExcel(fileInputStream);
        System.out.println(maps);

    }

}

~~~


###读取文件夹下的所有excel文件，全部拼接到一个list<map>里。以列序号为key。从0开始
~~~
package org.szwj.ca.identityauthsrv;

import com.sun.media.sound.InvalidFormatException;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PushbackInputStream;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.apache.poi.POIXMLDocument;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.openxml4j.opc.OPCPackage;
import org.apache.poi.poifs.filesystem.POIFSFileSystem;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.DateUtil;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.util.NumberToTextConverter;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mybatis.spring.boot.test.autoconfigure.MybatisTest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;


@MybatisTest    //缓存mybatsitest注解
@RunWith(SpringJUnit4ClassRunner.class)
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Rollback(false)
public class Ex {


    public static Workbook create(InputStream in) throws
        IOException, InvalidFormatException, org.apache.poi.openxml4j.exceptions.InvalidFormatException {
        if (!in.markSupported()) {
            in = new PushbackInputStream(in, 8);
        }
        if (POIFSFileSystem.hasPOIFSHeader(in)) {
            return new HSSFWorkbook(in);
        }
        if (POIXMLDocument.hasOOXMLHeader(in)) {
            return new XSSFWorkbook(OPCPackage.open(in));
        }
        throw new IllegalArgumentException("你的excel版本目前poi解析不了");
    }

    public static List<Map<String, Object>> readExcel(File file) throws Exception {
        int sheetnum = 0, startrow = 0, startcol = 0;
        List<Map<String, Object>> list = new ArrayList<Map<String, Object>>();
        Workbook workbook = null;
        try {

            workbook = create(new FileInputStream(file));

            for (int m = 0; m < workbook.getNumberOfSheets(); m++) {
                Sheet sheet = workbook.getSheetAt(m);
                int rowNum = sheet.getLastRowNum() + 1;                     //取得最后一行的行号
                Map<String, Object> Header = new HashMap<String, Object>();   //表头的下标和内容
                for (int i = startrow; i < rowNum; i++) {                    //行循环开始
                    Map<String, Object> map = null;//每一行数据的map
                    Row row = sheet.getRow(i);                             //行
                    if (row == null) {
                        break; //中间如果有空行，则退出
                    }
                    int cellNum = row.getLastCellNum();                     //每行的最后一个单元格位置
                    if (i != 0) {//记录数据的行号
                        map = new HashMap<String, Object>();
                        map.put("lineNumber", i + 1);
                    }
                    for (int j = startcol; j < cellNum; j++) {               //列循环开始
                        Cell cell2 = row.getCell(j);
                        //HSSFCell cell = row.getCell(Short.parseShort(j + ""));
                        //String cellValue = getCellValue(cell, format);
                        String cellValue = getCellValue(cell2);
                        //如果当前行的第一列为空,则跳过该行
                    /*if(j==0 && ("".equals(cellValue)||null==cellValue)){
                    	break;
                    }*/
                        if (i == 0) {
                            Header.put(j + "", cellValue);
                        } else {
                            map.put(j + "", cellValue);
                        }
                    }
                    //每一行数据的过滤,如果一行中所有列都为null,则不生成该行数据,
                    if (null != map) {
                        Collection<Object> values = map.values();
                        Set<String> keySet = map.keySet();
                        long count2 = keySet.stream().filter(o -> !o.equals("lineNumber"))
                            .count();//总条数
                        long count = values.stream().filter(o -> null == o).count();//为空的条数
                        if (count < count2) {
                            list.add(map);
                        }
                    }
                }
                workbook.close();
            }
            return list;
        } catch (Exception e) {
            System.out.println(file.getAbsolutePath());
            throw e;
        }


    }

    /**
     * 根据excel单元格类型获取excel单元格值
     *
     * @param cell
     * @return
     */


    private static String getCellValue(Cell cell) {
        String cellvalue = null;
        if (cell != null) {
            // 判断当前Cell的Type
            switch (cell.getCellType()) {
                // 如果当前Cell的Type为NUMERIC
                case Cell.CELL_TYPE_NUMERIC: {
                    short format = cell.getCellStyle().getDataFormat();
                    if (format == 14 || format == 31 || format == 57
                        || format == 58) { //excel中的时间格式
                        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
                        double value = cell.getNumericCellValue();
                        Date date = org.apache.poi.ss.usermodel.DateUtil.getJavaDate(value);
                        cellvalue = sdf.format(date);
                    }
                    // 判断当前的cell是否为Date
                    else if (DateUtil.isCellDateFormatted(
                        cell)) { //先注释日期类型的转换，在实际测试中发现HSSFDateUtil.isCellDateFormatted(cell)只识别2014/02/02这种格式。 
                        // 如果是Date类型则，取得该Cell的Date值 // 对2014-02-02格式识别不出是日期格式
                        Date date = cell.getDateCellValue();
                        DateFormat formater = new SimpleDateFormat("yyyy-MM-dd");
                        cellvalue = formater.format(date);
                    } else { // 如果是纯数字
                        // 取得当前Cell的数值
                        cellvalue = NumberToTextConverter.toText(cell.getNumericCellValue());

                    }
                    break;
                }
                // 如果当前Cell的Type为STRIN
                case Cell.CELL_TYPE_STRING:
                    // 取得当前的Cell字符串
                    cellvalue = cell.getStringCellValue().replaceAll("'", "''");
                    break;
                case Cell.CELL_TYPE_BLANK:
                    cellvalue = null;
                    break;
                // 默认的Cell值
                default: {
                    cellvalue = "";
                }
            }
        } else {
            cellvalue = "";
        }
        return cellvalue;
    }


    private static List<File> readFile(String fileDir) {
        List<File> fileList = new ArrayList<>();
        File file = new File(fileDir);
        File[] files = file.listFiles();// 获取目录下的所有文件或文件夹
        if (files == null) {// 如果目录为空，直接退出
            return fileList;
        }
        // 遍历，目录下的所有文件
        for (File f : files) {
            if (f.isFile()) {
                fileList.add(f);
            } else if (f.isDirectory()) {
                fileList.addAll(readFile(f.getAbsolutePath()));
            }
        }

        return fileList;
    }

    @Test
    public void zz() throws Exception {
        ArrayList<Map> li = new ArrayList<>(10000);//15223
        List<File> files = readFile(
            "G:\\微信文档\\WeChat Files\\wxid_etg2ykli7u2v22\\FileStorage\\File\\2020-06\\市二院2013到2020年的统计\\市二院2013到2020年的统计");
        for (int i = 0; i < files.size(); i++) {
            List<Map<String, Object>> list = readExcel(files.get(i));
            li.addAll(list);
        }

        List<Map<String, Object>> tmpList = new ArrayList<Map<String, Object>>();
        Set<String> keysSet = new HashSet<String>();
        for (Map<String, Object> collisionMap : li) {
            String keys = (String) collisionMap.get("6");
            int beforeSize = keysSet.size();
            keysSet.add(keys);
            int afterSize = keysSet.size();
            if (afterSize == beforeSize + 1) {
                tmpList.add(collisionMap);
            }
        }

        //根据字段去重之后的list
        System.out.println(tmpList);

    }

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public void insert(String name, String phone, String depart, String pass) {

        jdbcTemplate
            .update("INSERT INTO `iam`.`test`(`name`, `phone`,`depart`,pass) VALUES ( ?, ?, ?,?);",
                name, phone, depart, pass);
    }


}

~~~
