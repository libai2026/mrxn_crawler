---
title: "金和OA CompanyBudgetCollect.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CompanyBudgetCollect-sqli.html
asset_dir: assets/金和oa-companybudgetcollect.aspx-sql注入漏洞
---

# 金和OA CompanyBudgetCollect.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/19 13:31
- 302浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

软件

服务器

木马

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CompanyBudgetCollect.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

授权

安全认证考试

在线安全工具

根据 `CompanyBudgetCollect.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **CompanyBudgetCollect** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (!this.IsPostBack)
  {
    if (!string.IsNullOrEmpty(this.Request["httpOID"]))
    {
      DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable("select * from BudgetCollectManage where CollectID = " + this.Request["httpOID"].ToString());
      if (dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0)
        ((HtmlInputControl) this.hidYear).Value = dataTable.Rows[0]["BudgetYear"].ToString();
    }
    else
```

参数`httpOID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Collect/CompanyBudgetCollect.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

httpOID=SQLI_POC
```

[![金和OA CompanyBudgetCollect.aspx SQL注入漏洞](images/img-001-4d5bfaa3c58d.webp)](https://image.mrxn.net/3e9ed38e21864ce8a40d1a09a76b6be5.webp)

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
