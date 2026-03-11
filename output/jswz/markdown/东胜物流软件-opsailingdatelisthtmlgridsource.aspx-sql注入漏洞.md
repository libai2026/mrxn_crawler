---
title: "东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateListHtmlGridSource-sqli.html
asset_dir: assets/东胜物流软件-opsailingdatelisthtmlgridsource.aspx-sql注入漏洞
---

# 东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/15 08:45
- 251浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

SQL

木马

数据库

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 OpSailingDateListHtmlGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

软件

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `OpSailingDateListHtmlGridSource.aspx` 的代码引用 `DSWeb.PriceCarrier.OpSailingDateListHtmlGridSource`，在dll中找到它的逻辑实现

[![东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞](images/img-001-a47838f6a1d1.webp)](https://image.mrxn.net/dc537bc0c0314c53a40e36e3e039734e.webp)

[![东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞](images/img-002-644efcf25192.webp)](https://image.mrxn.net/7053fcc26652482ab37df2d80a68acb4.webp)

当`handle=list`时，进入`GetLogContent`方法

[![东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞](images/img-003-e81843594700.webp)](https://image.mrxn.net/400600be11ad494181b0ca88d83480da.webp)

1. 程序获取 `TITLE` 参数的值，并使用 `Regex.Unescape` 进行处理。此函数非安全函数，它仅对转义序列（如 `\n`, `\t`）进行解码，并不会对[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)相关的特殊字符（如 `'`, `;`, `-`）进行过滤或转义。
2. 处理后的字符串 `str` 被直接拼接到一个 `LIKE` 查询子句中。

`TITLE` 参数在未经过任何过滤或参数化处理的情况下，被直接使用字符串拼接的方式嵌入到 SQL 查询语句中。

SQL注入防护

深入探索

传输层安全性协议

防火墙软件

安全认证考试

# 漏洞复现

```
GET /PriceCarrier/OpSailingDateListHtmlGridSource.aspx?handle=list&cur_page=1&show_page=10&TITLE=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞](images/img-004-bb339bd5dfbc.webp)](https://image.mrxn.net/a9de541f054a4484bdf9908d7dd9e536.webp)

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
