---
title: "东胜物流软件 MsOpSeaeController 多个SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsOpSeaeController-sqli.html
asset_dir: assets/东胜物流软件-msopseaecontroller-多个sql注入漏洞
---

# 东胜物流软件 MsOpSeaeController 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/23 08:41
- 227浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

木马

软件

服务器

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 MsOpSeaeController 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

找到**MsOpSeaeController**下的action方法**GetMblIsRepeat**

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-001-77a38b565af7.webp)](https://image.mrxn.net/b8e54ba668cc4b25bf552118353df490.webp)

`bsno` 和 `mblno` 参数被直接拼接进SQL语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

其他action也是一样的

SQL注入防护

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-002-4077ea230e1e.webp)](https://image.mrxn.net/3034205615194228bee9b7aef2401b03.webp)

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-003-f0905e994dc1.webp)](https://image.mrxn.net/e99270e7ab464656954291be9812abb0.webp)

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-004-527bb9072553.webp)](https://image.mrxn.net/1da949b495104c979e46c22ad96dd043.webp)

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-005-7aa18cb34633.webp)](https://image.mrxn.net/a783c814a6f244aaad57082572d9f9f2.webp)

# 漏洞复现

```
POST /MvcShipping/MsOpSeae/GetMblIsRepeat HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

bsno=1&mblno=SQLI_POC
```

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-006-290118d59e39.webp)](https://image.mrxn.net/610e45fb5ce243499f4221386e6bc2ce.webp)

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
