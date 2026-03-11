---
title: "友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞"
source: https://mrxn.net/jswz/youjiasoft-fw-xxe.html
asset_dir: assets/友加畅捷管理系统-fw.asmx-xml实体注入（xxe）漏洞
---

# 友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/6 08:35
- 369浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

SQL

Web服务

计算机安全

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理软件，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

该系统fw.asmx下的`ZTList`、`login`、`OrderPost`、`OrderUpdate`、`QueryUnit`、`QueryUnit_Sup`、`QueryUnit_Cus`、`QueryStoreHouse`、`QueryEmp`、`QueryDept`、`QueryMoneyAccount`、`GetBillSN`、`QueryProd`、`QueryBarCode`、`QueryProdUnit`、`QueryProdBatch`、`GetPrice`、`QueryOutStorBillDraft`、`QuerySaleOrder`、`QueryProdPrice`、`QuerySaleOrderDetail`、`QuerySaleBillDrafeDetail`、`GetUserList`、`GetPriceNameList`等方法均存在 XML实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞，是由于其在处理XML输入时，未能有效禁用外部实体加载所导致。攻击者可以通过构造恶意的XML数据，并在其中引用外部实体，当系统解析这些未经严格过滤的XML数据时，便会触发漏洞。

成功利用此漏洞可能导致多种严重的安全风险，包括但不限于敏感信息泄露（如读取系统文件）、执行任意系统命令、对内网进行端口扫描、攻击内部网络服务，甚至发起拒绝服务（DoS）攻击等。

# 影响版本

18.8000.1095.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

直接查看 `fw.asmx` 文件的代码引用

深入探索

漏洞预警服务

安全认证考试

SQL注入检测工具

```
<%@ WebService Language="C#" CodeBehind="fw.asmx.cs" Class="CnSub.Web.fw" %>
```

直接在 `bin` 目录下反编译 `CnSub.Web.dll` 获取 **fw** 的`ZTList`处理逻辑

[![友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞](images/img-001-b12d0a468195.webp)](https://image.mrxn.net/dbc00c7f3c8447eeb75143f48581ea18.webp)

可以看到`xmldata`被直接带入`setXmlData`方法，跟进`setXmlData`方法看下它的实现逻辑

[![友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞](images/img-002-7297d1680d63.webp)](https://image.mrxn.net/2a363b50d4b5413c8100acc53f010c0d.webp)

可以看到`setXmlData`方法直接将`xmldata`使用XmlDocument的LoadXml进行XML反序列化操作，但是并没有对参数`xmldata` 传递的数据进行过滤或校验，造成[XML实体注入](https://mrxn.net/tag/XXE)（XXE）漏洞。

其他方法也是存在同样的[XXE](https://mrxn.net/tag/XXE)漏洞

[![友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞](images/img-003-c3ce419ad955.webp)](https://image.mrxn.net/a17ab000ac5c4eeeaca115b09f37f8db.webp)

# 漏洞复现

```
POST /fw.asmx HTTP/1.1
Host: youjiasoft.mrxn.net
SOAPAction: http://tempuri.org/ZTList
Content-Type: application/xml

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:ZTList>
         <!--type: string-->
         <tem:xmldata>XXE_POC</tem:xmldata>
      </tem:ZTList>
   </soapenv:Body>
</soapenv:Envelope>
```

[![友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞](images/img-004-135bcc35865e.webp)](https://image.mrxn.net/562a12e49fcb45db8f6fe8706d4b2a71.webp)

成功在DNSLOG平台获得HTTP响应。

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#XXE](https://mrxn.net/tag/XXE)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
