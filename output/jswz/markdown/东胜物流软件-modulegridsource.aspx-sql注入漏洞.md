---
title: "东胜物流软件 ModuleGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-Modules-ModuleGridSource-sqli.html
asset_dir: assets/东胜物流软件-modulegridsource.aspx-sql注入漏洞
---

# 东胜物流软件 ModuleGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/20 08:42
- 225浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

软件

身份验证

数据库

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 ModuleGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `ModuleGridSource.aspx` 的代码引用 `DSWeb.Modules.ModuleGridSource`，在dll中找到它的逻辑实现

[![东胜物流软件 ModuleGridSource.aspx SQL注入漏洞](images/img-001-cab6fb0390b5.webp)](https://image.mrxn.net/2a65567ae9c542a78c6824d204920b79.webp)

[![东胜物流软件 ModuleGridSource.aspx SQL注入漏洞](images/img-002-87f2b5d9a518.webp)](https://image.mrxn.net/b690853a26f94ceca5710d59fb7bcc6f.webp)

当`handle=list`时

深入探索

安全认证考试

漏洞扫描服务

安全研究工具

[![东胜物流软件 ModuleGridSource.aspx SQL注入漏洞](images/img-003-9448cb23f1a9.webp)](https://image.mrxn.net/6a2d7d2d1a5b45f09ec303309c137040.webp)

参数`search`被直接带入sql语句中，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

深入探索

安全工具开发

云安全解决方案

文本剥离工具

# 漏洞复现

```
GET /Modules/ModuleGridSource.aspx?handle=list&search=name:a%'SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 ModuleGridSource.aspx SQL注入漏洞](images/img-004-1f3383a42d48.webp)](https://image.mrxn.net/14d2cfd03e664c458691af1dae1d56ca.webp)

成功通过报错注入在响应中回显数据库版本信息。

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
