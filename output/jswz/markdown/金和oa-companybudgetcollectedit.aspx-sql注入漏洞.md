---
title: "金和OA CompanyBudgetCollectEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CompanyBudgetCollectEdit-sqli.html
asset_dir: assets/金和oa-companybudgetcollectedit.aspx-sql注入漏洞
---

# 金和OA CompanyBudgetCollectEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/20 13:32
- 301浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

服务器

软件

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CompanyBudgetCollectEdit.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `CompanyBudgetCollectEdit.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **CompanyBudgetCollectEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.strAppId = this.Request["httpAppID"].ToString();
  this.strCollectId = this.Request["httpOID"].ToString();
  if (!this.IsPostBack)
  {
    this.strAppNow = this.GetAppNow("Budget_Collect", this.strAppId);
```

参数`httpAppID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

深入探索

授权

安全运维咨询

漏洞预警服务

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Collect/CompanyBudgetCollectEdit.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

httpAppID=SQLI_POC&httpOID=1
```

[![金和OA CompanyBudgetCollectEdit.aspx SQL注入漏洞](images/img-001-6ebb0cacb203.webp)](https://image.mrxn.net/b29702f8efb64d9da967ca3a2c98f3f5.webp)

成功延时 4 秒

代码安全审计

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
