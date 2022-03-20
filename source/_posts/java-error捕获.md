---
title: java-error捕获.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
~~~
package org.szwj.ca.identityauthsrv;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import java.io.InputStream;
import javax.imageio.ImageIO;
import javax.imageio.stream.ImageOutputStream;
import org.apache.commons.io.FileUtils;
import org.szwj.ca.identityauthsrv.util.common.ImageUtils;

public class DrawDemo {

    public static void main(String[] args) throws FileNotFoundException, IOException {

        /**
         * 直接捕获error
         */
        try {
            byte[] bytes = new byte[1024 * 1024 * 10*10];
        }catch (Error error){
            System.out.println(error.getMessage());
        }

        /**
         * 捕获error和exption的分类Throwable
         */
        try {
            byte[] bytes = new byte[1024 * 1024 * 10*10];
        }catch (Throwable throwable){
            System.out.println(throwable.getMessage());
        }


    }
}
~~~
