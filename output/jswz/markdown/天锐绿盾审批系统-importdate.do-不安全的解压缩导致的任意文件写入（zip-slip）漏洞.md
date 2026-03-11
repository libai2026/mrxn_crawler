---
title: "天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞"
source: https://mrxn.net/jswz/trwfe-importDate-rce.html
asset_dir: assets/天锐绿盾审批系统-importdate.do-不安全的解压缩导致的任意文件写入（zip-slip）漏洞
---

# 天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/5 08:23
- 817浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

数据压缩

软件

SQL

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。

安全工具开发

在其 `importDate.do` 接口中存在一个不安全的解压缩漏洞。攻击者可以利用“Zip Slip”技术，通过构造恶意的压缩文件，在系统解压缩时，利用文件路径遍历的缺陷，将文件写入到任意指定位置。

这可能导致敏感文件被覆盖、恶意文件被植入，进而引发[远程代码执行](https://mrxn.net/tag/rce)、系统功能破坏或数据泄露等严重安全风险。

计算机科学

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

深入探索

漏洞修复方案

在线安全工具

代码安全审计

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 漏洞预警服务

# 漏洞分析

先看`importDate.do`的实现

[![天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](images/img-001-a489f0df1548.webp)](https://image.mrxn.net/2e004cb0213647f1b710959bf085dd8e.webp)

跟进`configService.importDate` 看下实现逻辑

深入探索

企业安全咨询

服务器安全服务

安全研究报告

[![天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](images/img-002-a162a9c25601.webp)](https://image.mrxn.net/cfcf93acb1d24aceb135bc05bee96b42.webp)

接收一个文件上传的file参数内容

计算机安全

[![天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](images/img-003-b84af67d972c.webp)](https://image.mrxn.net/ba691f4c41bc4c4a975ce0f1ea21267f.webp)

处理用户上传的 zip 压缩包，该功能旨在实现数据库的导入恢复。它首先将上传的 `MultipartFile` 保存为临时 zip 文件，然后调用 `ZipUtil.getInstance().unZip()` 方法将该 zip 文件解压到服务器上的一个临时目录中。

安全工具开发

深入探索

恶意软件分析工具

Web安全书籍

安全研究工具

由于代码在解压 zip 文件之前，**完全没有对压缩包内的文件名进行合法性校验，特别是没有检查文件名中是否包含目录遍历序列（如** `../`**）**，造成了**致命的 Zip Slip 漏洞**。攻击者可以精心构造一个 zip 压缩包，其中包含一个文件名形如 `../../../../../../../../tmp/pwned.txt` 的文件。当 `ZipUtil.unZip()` 方法解压这个文件时，它会跳出预设的临时解压目录 `tempPath`，将 `pwned.txt` 文件写入到服务器的文件系统根目录下的 `/tmp` 目录中。通过这种方式，攻击者可以在服务器上任意位置写入任意内容的文件，例如上传一个 [WebShell](https://mrxn.net/tag/rce)、覆盖关键配置文件、或写入一个定时任务脚本。

漏洞预警服务

# 漏洞复现

> 创建一个带有目录穿越文件名的压缩包，只需要向上跳一级即可跳到根目录

[![天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](images/img-004-4777fdcf554c.webp)](https://image.mrxn.net/5ef93ad5dd4845ea87eef8560a1c7415.webp)

访问解压到根目录的测试文件test.jsp

[![天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](images/img-005-d6ea9cfa7fd1.webp)](https://image.mrxn.net/cfa21975357942e5b3f3b5bff27bba9d.webp)

成功[执行](https://mrxn.net/tag/rce)打印随机uuid后，删除自身，完成Zip Slip漏洞利用。

计算机科学

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

  
  

![](data:image/png;base64,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)

手机扫码阅读
