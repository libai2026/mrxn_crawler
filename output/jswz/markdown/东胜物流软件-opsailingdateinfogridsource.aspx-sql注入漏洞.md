---
title: "东胜物流软件 OpSailingDateInfoGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateInfoGridSource-sqli.html
asset_dir: assets/东胜物流软件-opsailingdateinfogridsource.aspx-sql注入漏洞
---

# 东胜物流软件 OpSailingDateInfoGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/16 08:50
- 200浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

SQL

服务器

木马

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 OpSailingDateInfoGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `OpSailingDateInfoGridSource.aspx` 的代码引用 `DSWeb.PriceCarrier.OpSailingDateInfoGridSource`，在dll中找到它的逻辑实现

[![东胜物流软件 OpSailingDateInfoGridSource.aspx SQL注入漏洞](images/img-001-f2cb50d09d2c.webp)](https://image.mrxn.net/4de4b8730a9b407580815d4ca67c9e85.webp)

当`handle=delete`时，进入`setDel`方法后，参数`gids`经过逗号分割后被直接拼接进SQL语句中，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /PriceCarrier/OpSailingDateInfoGridSource.aspx?handle=delete&gids=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 OpSailingDateInfoGridSource.aspx SQL注入漏洞](images/img-002-14da6ea171eb.webp)](https://image.mrxn.net/20e25d345fd845b6ba31f4345e54cc1e.webp)

通过报错注入在响应里回显数据库版本信息。

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
