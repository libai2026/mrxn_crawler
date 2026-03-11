---
title: "用友U8+渠道管理(高级版) check.imgdo、delete.imgdo SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-business-test-imgdo-sqli.html
asset_dir: assets/用友u8+渠道管理(高级版)-check.imgdo、delete.imgdo-sql注入漏洞
---

# 用友U8+渠道管理(高级版) check.imgdo、delete.imgdo SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/20 12:16
- 684浏览
- [0评论](#comment)
- 1小时阅读

深入探索

代码安全审计

网络安全培训

授权

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友网络科技股份有限公司推出的企业管理综合平台，广泛应用于财务、进销存、人力资源等企业核心业务系统中。在U8+渠道管理（高级版）模块中，`check.imgdo`和 `delete.imgdo` 接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。该漏洞是由于页面在处理用户输入的参数时，未对输入内容进行充分过滤与安全校验，攻击者可构造恶意SQL语句，通过HTTP请求注入至后端数据库查询中。

SQL注入防护

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

## check.imgdo

直接看 `business/test/check.imgdo` URL对应的servlet在`web.xml`中的映射

代码安全审计

```
<!-- 查看图片 -->
<servlet>
    <servlet-name>CheckPicture</servlet-name>
    <servlet-class>com.gxfcsoft.framework.core.CheckPicture</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>CheckPicture</servlet-name>
    <url-pattern>/business/test/check.imgdo</url-pattern>
</servlet-mapping>
<servlet>
```

深入探索

SQL注入检测工具

技术文章订阅

文件大小转换

跟进`com.gxfcsoft.framework.core.CheckPicture` 看下它的实现

```
package com.gxfcsoft.framework.core;

import com.alibaba.fastjson.JSONObject;
import com.gxfcsoft.framework.action.users.UserManager;
import com.gxfcsoft.framework.base.util.UserState;
import com.gxfcsoft.framework.dao.ResManager;
import com.gxfcsoft.framework.dao.common.CommonDictDao;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import org.dom4j.Element;

public class CheckPicture extends HttpServlet {
    private static final long serialVersionUID = 7086934382711881762L;

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        super.doGet(req, resp);
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession();
        String sid = session.getId();
        UserState us = UserManager.getUserBySessionId(sid);
        Connection con = null;
        PrintWriter pw = resp.getWriter();

        try {
            con = ResManager.getConnection();
            String code = "";
            String delphotoName = "";
            BufferedReader br = new BufferedReader(new InputStreamReader(req.getInputStream(), "utf-8"));
            String line = null;
            StringBuilder sb = new StringBuilder();

            while((line = br.readLine()) != null) {
                sb.append(line);
            }

            String sdata = sb.toString();
            String[] ss = sdata.split("&");

            for(int i = 0; i < ss.length; ++i) {
                String temp = ss[i];
                String value = temp.substring(temp.indexOf("=") + 1);
                if (temp != null && temp.indexOf("_id") != -1) {
                    code = value;
                } else if (temp != null && temp.indexOf("photoName") != -1) {
                    delphotoName = value;
                }
            }

            CommonDictDao cDao = new CommonDictDao(con, us);
            String sql = "select id from arecord where code = '" + code + "'" + " and images like " + "'%" + delphotoName + "%'";
            Element eles = cDao.findOne(sql);
            String id = eles.attributeValue("id");
            String subsql = "select images,latitude,longitude,wdirection,jdirection,shootdate from photoexif where code = '" + id + "' and images like " + "'%" + delphotoName + "%'";
            Element ele = cDao.findOne(subsql);
```

将请求里的内容使用`&` 进行分割后，如果`_id` 存在则sql语句里的`code`的值就等于`_id` 参数的值；其次是如果存在`photoName`参数，那么sql语句里的`delphotoName`就等于参数`photoName`的值。而两个参数也没有经过任何过滤或校验就被直接拼接进SQL语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

## delete.imgdo

```
<!-- 删除图片 -->
<servlet>
    <servlet-name>DeletePictureServlet</servlet-name>
    <servlet-class>com.gxfcsoft.framework.core.DeletePictureServlet</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>DeletePictureServlet</servlet-name>
    <url-pattern>/business/test/delete.imgdo</url-pattern>
</servlet-mapping>
```

跟进 `com.gxfcsoft.framework.core.DeletePictureServlet` 看下它的实现

漏洞修复方案

```
package com.gxfcsoft.framework.core;

import com.gxfcsoft.framework.action.users.UserManager;
import com.gxfcsoft.framework.base.util.PathUtil;
import com.gxfcsoft.framework.base.util.UserState;
import com.gxfcsoft.framework.dao.ResManager;
import com.gxfcsoft.framework.dao.common.CommonDictDao;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.sql.Connection;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import org.dom4j.Element;

public class DeletePictureServlet extends HttpServlet {
    private static final long serialVersionUID = -57659135072396187L;

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession();
        String sid = session.getId();
        UserState us = UserManager.getUserBySessionId(sid);
        Connection con = null;
        String message = "0";

        try {
            con = ResManager.getConnection();
            String sql = "";
            String code = "";
            String delphotoName = "";
            BufferedReader br = new BufferedReader(new InputStreamReader(req.getInputStream(), "utf-8"));
            String line = null;
            StringBuilder sb = new StringBuilder();

            while((line = br.readLine()) != null) {
                sb.append(line);
            }

            String sdata = sb.toString();
            String[] ss = sdata.split("&");

            for(int i = 0; i < ss.length; ++i) {
                String temp = ss[i];
                String value = temp.substring(temp.indexOf("=") + 1);
                if (temp != null && temp.indexOf("_id") != -1) {
                    code = value;
                } else if (temp != null && temp.indexOf("photoName") != -1) {
                    delphotoName = value;
                }
            }

            CommonDictDao cDao = new CommonDictDao(con, us);
            sql = "select id ,images from arecord where code = '" + code + "'" + " and images like " + "'%" + delphotoName + "%'";
            Element ele = cDao.findOne(sql);
            String id = ele.attributeValue("id");
            String images = ele.attributeValue("images");
            String[] imagess = images.split(";");
            String sql1 = "";
            if (imagess.length == 1) {
                sql1 = "delete arecord where id = '" + id + "'";
            } else {
                String data = images.replace(delphotoName + ";", "").replace(delphotoName, "");
                if (data.lastIndexOf(";") + 1 == data.length()) {
                    data = data.substring(0, data.lastIndexOf(";"));
                }

                sql1 = "update arecord set images = '" + data + "'" + " where id = '" + id + "'";
            }

            cDao.update(sql1);
            String subsql = "delete photoexif where code= '" + id + "' and images like '%" + delphotoName + "%'";
            cDao.update(subsql);
```

造成[sql注入漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)的原因还是因为处理逻辑和上面的`check.imgdo` 一样的问题。

安全运维咨询

# 漏洞复现

## check.imgdo

```
POST /business/test/check.imgdo HTTP/1.1
Host: u8.mrxn.net
Content-Type: application/x-www-form-urlencoded

_id='_SQLI_POC-- -
```

[![用友U8+渠道管理(高级版) check.imgdo、delete.imgdo SQL注入漏洞](images/img-001-6369c16aec3a.webp)](https://image.mrxn.net/bccab36f86c44bc88dcf5343d12fa5ec.webp)

成功延时 5 秒

编程

以及参数**photoName，也是延时 5秒**

漏洞修复方案

[![用友U8+渠道管理(高级版) check.imgdo、delete.imgdo SQL注入漏洞](images/img-002-b0163f637a56.webp)](https://image.mrxn.net/5fd89294750d453583ce3163f6fa93cd.webp)

## delete.imgdo

[![用友U8+渠道管理(高级版) check.imgdo、delete.imgdo SQL注入漏洞](images/img-003-1b49b675fcc6.webp)](https://image.mrxn.net/a888e47e82fc4cb7aeb201bed0c82bf0.webp)

也是同样的延时 5 秒

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.check.imgdo](#toc-4-1-)
- [4.2.delete.imgdo](#toc-4-2-)
- [5.漏洞复现](#toc-5-)
- [5.1.check.imgdo](#toc-5-1-)
- [5.2.delete.imgdo](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
