---
title: "天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞"
source: https://mrxn.net/jswz/trwfe-identity-user-data-leak.html
asset_dir: assets/天锐绿盾审批系统-identityuser{userid}、identityinformationuser{userid}-未授权访问致敏感信息泄露漏洞
---

# 天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/12 08:27
- 432浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

加密

身份验证

安全

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。该系统旨在从源头上保障数据安全，防止[信息泄露](https://mrxn.net/tag/data-leak)。

漏洞存在于天锐绿盾审批系统，攻击者可以未经授权访问 `/identity/user/{userId}` 路径。利用此未授权访问漏洞，未经身份验证的攻击者能够获取系统内的[敏感信息](https://mrxn.net/tag/data-leak)。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息
>
> 网络安全

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"

# 漏洞分析

先看`/user/{userId}`路由实现

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-001-c1269c7864fd.webp)](https://image.mrxn.net/687e980a25aa4e08a07ce2fa22619608.webp)

直接将`userId`带入查询将结果响应在body里，从而导致敏感信息泄露。

漏洞预警服务

深入探索

云安全解决方案

网络安全课程

代码安全审计

`/identity/information/user/{userId}` 亦如此

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-002-bda34886e7b0.webp)](https://image.mrxn.net/8f47b75388d2423482e45cae72e40307.webp)

`/identity/information/dept/{deptId}` 亦如此

深入探索

文件大小转换

VPN服务

在线安全工具

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-003-a047568bdd09.webp)](https://image.mrxn.net/f31f572eb8124ff594d468a74cd8a031.webp)

`/identity/information/group/{groupId}` 亦如此

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-004-de3740f851c6.webp)](https://image.mrxn.net/928dc7d63ff245c79a0fd97f356bcab1.webp)

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-005-a9e3e201fe3c.webp)](https://image.mrxn.net/ce86ff721bb244218943fe6dc8cd2417.webp)

# 漏洞复现

```
GET /trwfe/ws/identity/user/admin HTTP/1.1
Host: trwfe.mrxn.net
```

即可获取到admin账户相关的信息如邮箱、姓名、密码等

Windows安全工具

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-006-55934c0891ff.webp)](https://image.mrxn.net/67534c270c1c4c90be8798a8f9c04827.webp)

md5解密即可得到对应账号的密码

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-007-cf92635f7fae.webp)](https://image.mrxn.net/04cc6a0a30ec4630afd2b424d6b9c9d2.webp)

其他用户如sysadmin、secadmin、logadmin 同样如此

计算机安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#data-leak](https://mrxn.net/tag/data-leak)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
