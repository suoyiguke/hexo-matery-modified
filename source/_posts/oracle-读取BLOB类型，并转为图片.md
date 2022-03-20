---
title: oracle-读取BLOB类型，并转为图片.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: oracle
categories: oracle
---
---
title: oracle-读取BLOB类型，并转为图片.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: oracle
categories: oracle
---
~~~

    public static void main(String[] args) throws SQLException, IOException {
        QueryRunner queryRunner = new QueryRunner();
        LisDBUtil instance = getInstance();
        Connection connection = instance.getConnection();

        List<Map<String, Object>> list = queryRunner
            .query(connection, "SELECT * FROM EMR_WH_QMXX", new MapListHandler());
        //遍历list,再遍历map
        for (Map<String, Object> map : list) {
            for (Object key : map.keySet()) {
                BLOB blob = (BLOB) map.get("QMXX");

                String jlgh = (String) map.get("JLGH");
                while (jlgh.length()<5){
                    jlgh = "0".concat(jlgh);
                }
                System.out.println(jlgh);

                InputStream inStream = blob.getBinaryStream();
                byte[] data = null;
                try {
                    long nLen = blob.length();
                    int nSize = (int) nLen;
                    data = new byte[nSize];
                    inStream.read(data);
                    inStream.close();
                } catch (IOException e) {
                    System.out.println("获取图片数据失败,原因:" + e.getMessage());
                }
                byte2image(data, "D://zzz//".concat(jlgh.concat(".jpg")));
            }

        }

}

    public byte[] image2byte(String path) {
        byte[] data = null;
        FileImageInputStream input = null;
        try {
            input = new FileImageInputStream(new File(path));
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            byte[] buf = new byte[1024];
            int numBytesRead = 0;
            while ((numBytesRead = input.read(buf)) != -1) {
                output.write(buf, 0, numBytesRead);
            }
            data = output.toByteArray();
            output.close();
            input.close();
        } catch (FileNotFoundException ex1) {
            ex1.printStackTrace();
        } catch (IOException ex1) {
            ex1.printStackTrace();
        }
        return data;
    }

    //byte数组到图片
    public static void byte2image(byte[] data, String path) {
        if (data.length < 3 || path.equals("")) {
            return;
        }
        try {
            FileImageOutputStream imageOutput = new FileImageOutputStream(new File(path));
            imageOutput.write(data, 0, data.length);
            imageOutput.close();
            System.out.println("Make Picture success,Please find image in " + path);
        } catch (Exception ex) {
            System.out.println("Exception: " + ex);
            ex.printStackTrace();
        }
    }

    //byte数组到16进制字符串
    public String byte2string(byte[] data) {
        if (data == null || data.length <= 1) {
            return "0x";
        }
        if (data.length > 200000) {
            return "0x";
        }
        StringBuffer sb = new StringBuffer();
        int buf[] = new int[data.length];
        //byte数组转化成十进制
        for (int k = 0; k < data.length; k++) {
            buf[k] = data[k] < 0 ? (data[k] + 256) : (data[k]);
        }
        //十进制转化成十六进制
        for (int k = 0; k < buf.length; k++) {
            if (buf[k] < 16) {
                sb.append("0" + Integer.toHexString(buf[k]));
            } else {
                sb.append(Integer.toHexString(buf[k]));
            }
        }
        return "0x" + sb.toString().toUpperCase();
    }

~~~
