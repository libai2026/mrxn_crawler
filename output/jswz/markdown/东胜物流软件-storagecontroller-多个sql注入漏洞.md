---
title: "东胜物流软件 StorageController 多个SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-StorageController-sqli.html
asset_dir: assets/东胜物流软件-storagecontroller-多个sql注入漏洞
---

# 东胜物流软件 StorageController 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/22 08:41
- 212浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

Nessus

文本剥离工具

授权

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 StorageController 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

软件

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据**Storage**路由下的mvc的定义

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-001-b1858e652564.webp)](https://image.mrxn.net/64e0bad691f249e48695998110eb43cd.webp)

比如找到**StorageController**下的action方法**DQStorageData**

SQL注入防护

深入探索

VPN服务

防火墙软件

漏洞预警服务

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-002-b6a24a6a7661.webp)](https://image.mrxn.net/e61627b40bfa4f37afea38bfb24288a3.webp)

`openid`参数带入`GetDQKuCunDataList`方法中

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-003-56e08b3a8c88.webp)](https://image.mrxn.net/3432764c679a46079dac4cf0da3daa96.webp)

可以看到`openid`参数被直接拼接进SQL语句中，从而造成了SQL注入漏洞。

代码安全审计

其他action也是一样的

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-004-5f92b0c85be6.webp)](https://image.mrxn.net/a69ceb885fe048bf920db23ef0bd6caa.webp)

看下`GetIndoDataList`方法的实现

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-005-e21262140f87.webp)](https://image.mrxn.net/c8d8fa2030dd48fc94e547e7c8efebb9.webp)

参数**mblno**也是被直接拼接进SQL语句中导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

其他的action如**OutDoListData**、**StorageInDetailData**、**StorageOutDetailData**一样

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-006-954dac02c4e6.webp)](https://image.mrxn.net/3dce2fe803fd49c5985bcfb902de7829.webp)

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-007-c49ce8b37f10.webp)](https://image.mrxn.net/4a7dfd325ca54a75aa9594ad7ee6c508.webp)

StorageInDetailData

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-008-e666004f20b2.webp)](https://image.mrxn.net/6f746b649b7b44018fe365bd85c30c8c.webp)

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-009-d30920293eff.webp)](https://image.mrxn.net/1f007c6bb82f4756b4bd2f18bdd8c43c.webp)

StorageOutDetailData

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-010-e6c21983ae7a.webp)](https://image.mrxn.net/f3b0a8cea3154290b8204934a1f65a5d.webp)

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-011-6ae9cbbafce0.webp)](https://image.mrxn.net/fb83bd34a15e44eb918a616ce2fcc525.webp)

# 漏洞复现

```
GET /Storage/Storage/DQStorageData?openid=SQLI_POC&mblno=111&page=1&pageSize=10 HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-012-6a20871f653a.webp)](https://image.mrxn.net/f715bc4bbca94b1b8dde49a8ea3b2c39.webp)

成功通过报错注入在响应中回显数据库版本信息。

漏洞修复方案

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-013-ed23e34a81c9.webp)](https://image.mrxn.net/31da42f94112463d968e50162dc75954.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
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
