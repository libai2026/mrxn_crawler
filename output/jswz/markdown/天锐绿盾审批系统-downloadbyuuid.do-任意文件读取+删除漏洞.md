---
title: "天锐绿盾审批系统 downloadByUuid.do 任意文件读取+删除漏洞"
source: https://mrxn.net/jswz/trwfe-downloadByUuid-file-read.html
asset_dir: assets/天锐绿盾审批系统-downloadbyuuid.do-任意文件读取+删除漏洞
---

# 天锐绿盾审批系统 downloadByUuid.do 任意文件读取+删除漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/12 08:28
- 372浏览
- [0评论](#comment)
- 12分钟阅读

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。

漏洞预警服务

该系统的 `downloadByUuid.do` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。未经身份验证的攻击者可以通过该漏洞读取系统上的任意文件，从而可能获取数据库敏感信息或其他重要配置信息，导致数据泄露。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全工具开发

# 漏洞分析

先看`downloadByUuid.do`的实现

[![天锐绿盾审批系统 downloadByUuid.do 任意文件读取+删除漏洞](images/img-001-9e5e82fdf081.webp)](https://image.mrxn.net/19c5f81c6a10467fa3069fb599401d16.webp)

通过调试可知`String filePath = this.DISC.replace("//", "/") + uuid + fileName;`值如下

[![天锐绿盾审批系统 downloadByUuid.do 任意文件读取+删除漏洞](images/img-002-119f9acbe0ef.webp)](https://image.mrxn.net/71b71e24faa048cfbfbdc2b499724f02.webp)

[![天锐绿盾审批系统 downloadByUuid.do 任意文件读取+删除漏洞](images/img-003-b93c6149b806.webp)](https://image.mrxn.net/d66789b602f14be5b32f8c9570767dcb.webp)

其中**this.DISC=D:/TRWfe/tomcat/temp/** 即一般安装目录下的tomcat下的temp目录为基础目录。

漏洞预警服务

跟进`fileService.downLoadFile` 方法，看下`fileService.downLoadFile`的实现逻辑

[![天锐绿盾审批系统 downloadByUuid.do 任意文件读取+删除漏洞](images/img-004-dca817a3a8c9.webp)](https://image.mrxn.net/6aa7e5879c92414096e96e7e0ccf01bb.webp)

**直接将从用户端接收的** `fileName` **参数，**拼接进 `String filePath = this.DISC.replace("//", "/") + uuid + fileName;`后**，不经验证地用于** `new FileInputStream(((DownFileMsg)files.get(0)).getFile())` **来实例化文件对象，并最终传递给** `FileInputStream` **进行读取**，攻击者可以构造包含绝对路径或 `../` 目录遍历序列的恶意 fileName或uuid参数，读取服务器文件系统上任意位置的、具有应用运行权限可读的任何文件。

网络安全

`fileService.downLoadFile`最终会删除读取的文件

[![天锐绿盾审批系统 downloadByUuid.do 任意文件读取+删除漏洞](images/img-005-4d80db14bdd6.webp)](https://image.mrxn.net/c6922cf8916541a688156fe78cfa11b4.webp)

测试时应该谨慎测试，最好自己上传一个文件来测试，避免删除了系统重要文件导致系统宕机的尴尬。

# 漏洞复现

> 漏洞测试会删除对应文件，谨慎测试
>
> 漏洞预警服务

可测试tomcat根目录下的BUILDING.txt、CONTRIBUTING.md、LICENSE、NOTICE、README.md、RELEASE-NOTES以及RUNNING.txt等文件来进行验证测试。

```
POST /trwfe/file/downloadByUuid.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileName=../../../NOTICE&uuid=x
```

成功读取到tomcat根目录下的NOTICE文件内容

[![天锐绿盾审批系统 downloadByUuid.do 任意文件读取+删除漏洞](images/img-006-e917ea798b93.webp)](https://image.mrxn.net/33ceed024c7b43068183a2ff35ed3e02.webp)

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
