---
title: "东胜物流软件 AttributeGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-Attributes-AttributeGridSource-sqli.html
asset_dir: assets/东胜物流软件-attributegridsource.aspx-sql注入漏洞
---

# 东胜物流软件 AttributeGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/21 08:36
- 205浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

Windows安全工具

Nessus

计算机安全

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 AttributeGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

文本剥离工具

企业安全咨询

云安全解决方案

根据 `AttributeGridSource.aspx` 的代码引用 `DSWeb.Modules.AttributeGridSource`，在dll中找到它的逻辑实现

[![东胜物流软件 AttributeGridSource.aspx SQL注入漏洞](images/img-001-db76c1fec24e.webp)](https://image.mrxn.net/a123b491333649f8ab7d5ce987e1ab91.webp)

当`handle=compattrlistpage`时，进入`GetCompanyAttributeListPage`方法，看下它的实现

SQL注入检测工具

深入探索

传输层安全性协议

安全运维咨询

SQL注入防护

[![东胜物流软件 AttributeGridSource.aspx SQL注入漏洞](images/img-002-3a54fad16e5f.webp)](https://image.mrxn.net/e5a7b7b3cc5e413ca90c7460dbeb7fea.webp)

参数`checkcompid`被直接带入sql语句中，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /Attributes/AttributeGridSource.aspx?handle=compattrlistpage&checkcompid=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 AttributeGridSource.aspx SQL注入漏洞](images/img-003-8e469e029d99.webp)](https://image.mrxn.net/c41ba01ece2041069b5b3a2d93a963f2.webp)

成功通过报错注入在响应中回显数据库版本信息。

代码安全审计

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
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
