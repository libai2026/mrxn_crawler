---
title: "东胜物流软件 MsAnnounceController SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html
asset_dir: assets/东胜物流软件-msannouncecontroller-sql注入漏洞
---

# 东胜物流软件 MsAnnounceController SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/25 08:40
- 248浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

SQL

软件

身份验证

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 MsAnnounceController 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

看下`MsAnnounceController`方法下的**GetDataList** action是如何实现的

[![东胜物流软件 MsAnnounceController SQL注入漏洞](images/img-001-54682f68f7ff.webp)](https://image.mrxn.net/dcf0fef26b154ca28c2f13b1f8253bd0.webp)

[![东胜物流软件 MsAnnounceController SQL注入漏洞](images/img-002-2cb0bdcd2b43.webp)](https://image.mrxn.net/c5f6e1a7401c44fc87c716277a721075.webp)

如上图所示，参数**condition**是被直接拼接进SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /MvcShipping/MsAnnounce/GetData?handle=edit&condition=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 MsAnnounceController SQL注入漏洞](images/img-003-87ffadc06fce.webp)](https://image.mrxn.net/7ec3c5af92dd40c88a77b189c77001f0.webp)

成功利用报错注入在响应里回显数据库版本信息

SQL注入防护

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
