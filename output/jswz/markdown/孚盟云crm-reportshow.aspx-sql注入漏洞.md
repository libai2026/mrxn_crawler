---
title: "孚盟云CRM ReportShow.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-ReportShow-sqli.html
asset_dir: assets/孚盟云crm-reportshow.aspx-sql注入漏洞
---

# 孚盟云CRM ReportShow.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/11 11:08
- 762浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

计算机安全

鉴权

客户关系管理

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云ReportShow.aspx接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `ReportShow.aspx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **ReportShow** 方法的实现如下

[![孚盟云CRM ReportShow.aspx SQL注入漏洞](images/img-001-0ea89697735b.webp)](https://image.mrxn.net/eb6fea39c5fc4f71af27fbb275407ebf.webp)

GET请求里的参数**templateId**未过滤或校验就被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。只不过需要注意的是此处使用的是MySQL数据库，因此在进行测试需要使用MySQL相关payload。

# 漏洞复现

```
GET /m/Dingding/ActiveReport/ReportShow.aspx?templateId=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"admin","corpId": "1","loginUser":"admin"}
```

[![孚盟云CRM ReportShow.aspx SQL注入漏洞](images/img-002-ca3e947ed82b.webp)](https://image.mrxn.net/29d46cfc098d43c78b9c8cdcf972ac6e.webp)

成功延时 3 秒

SQL注入防护

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
