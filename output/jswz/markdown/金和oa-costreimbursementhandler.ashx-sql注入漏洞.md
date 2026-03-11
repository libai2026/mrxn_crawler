---
title: "金和OA CostReimbursementHandler.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CostReimbursementHandler-sqli.html
asset_dir: assets/金和oa-costreimbursementhandler.ashx-sql注入漏洞
---

# 金和OA CostReimbursementHandler.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/22 13:05
- 276浏览
- [0评论](#comment)
- 25分钟阅读

深入探索

软件

服务器

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CostReimbursementHandler.ashx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

恶意软件分析工具

编程语言教程

Nessus

根据 `CostReimbursementHandler.ashx` 的源码，在 bin 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **CostReimbursementHandler** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["action"];
  string str2;
  if (string.IsNullOrEmpty(str1) || (str2 = str1) == null)
    return;
  if (!string.op_Equality(str2, "Reimbursement"))
  {
    if (!string.op_Equality(str2, "YeahChange"))
    {
      if (!string.op_Equality(str2, "ShengChange"))
      {
        if (!string.op_Equality(str2, "YeahChangeAll"))
        {
          if (!string.op_Equality(str2, "StandradForTravel"))
            return;
          this.getStandradForTravel(context);
        }
        else
          this.GetYeahChangeAll(context);
      }
      else
        this.GetSHI(context);
    }
    else
      this.GetPeriod(context);
  }
  else
    this.Reimbursement(context);
}
```

根据`action`的值进入不同的处理流程

代码安全审计

[![金和OA CostReimbursementHandler.ashx SQL注入漏洞](images/img-001-e902e3ba0456.webp)](https://image.mrxn.net/1a15bfae9a0848b8bb66568e3279b6c1.webp)

当 `action=YeahChange` 时，`yeah`被带入`Get_Budget_PeriodDivertInformation`方法

```
protected void GetPeriod(HttpContext context)
{
  string str1 = string.Empty;
  DataSet divertInformation = this.cm.Get_Budget_PeriodDivertInformation(context.Request["yeah"]);
```

跟进`Get_Budget_PeriodDivertInformation`方法

```
public DataSet Get_Budget_PeriodDivertInformation(string YearPeriod)
{
  return this.GetDS_BySQL($"{" Select Budget_PeriodManage.YearPeriod,Budget_PeriodManage.Period,Budget_PeriodDivert.Status " + " from Budget_PeriodManage " + " Left outer join Budget_PeriodDivert " + " on Budget_PeriodDivert.YearPeriod = Budget_PeriodManage.YearPeriod " + " and  Budget_PeriodDivert.Period = Budget_PeriodManage.Period "} where Budget_PeriodDivert.Status is null and Budget_PeriodManage.YearPeriod ='{YearPeriod}'" + " order by YearPeriod asc ,Period asc " + "   select Period from Budget_PeriodManage where getdate() between begindate and enddate ");
}
```

参数`yeah`被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

其他几个方法，也存在同样的sql注入

漏洞预警服务

**GetSHI**

[![金和OA CostReimbursementHandler.ashx SQL注入漏洞](images/img-002-db484d1b7e41.webp)](https://image.mrxn.net/fa9a4faea533477086b3f191a4ece0bf.webp)

[![金和OA CostReimbursementHandler.ashx SQL注入漏洞](images/img-003-ca9a68d3c22f.webp)](https://image.mrxn.net/c0bd51919eab4ecc8c6211aac4f08b76.webp)

**GetYeahChangeAll**

[![金和OA CostReimbursementHandler.ashx SQL注入漏洞](images/img-004-1ba83084f812.webp)](https://image.mrxn.net/81ee25582bd242f0a9df5405ee0e9284.webp)

[![金和OA CostReimbursementHandler.ashx SQL注入漏洞](images/img-005-59f75aa3c49d.webp)](https://image.mrxn.net/6425178a493d4ca5affdac3d89dc158a.webp)

**getStandradForTravel**

数据管理

[![金和OA CostReimbursementHandler.ashx SQL注入漏洞](images/img-006-2831f4095461.webp)](https://image.mrxn.net/3b0f1fa8338b4cd8bd1ed151b9a45b2e.webp)

[![金和OA CostReimbursementHandler.ashx SQL注入漏洞](images/img-007-926292cbcd00.webp)](https://image.mrxn.net/d4e69e52f6ec4a35b1dfb2069fe30116.webp)

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/CostManagement/Reimbursement/CostReimbursementHandler.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=YeahChange&yeah=SQLI_POC
```

[![金和OA CostReimbursementHandler.ashx SQL注入漏洞](images/img-008-608ee9ccba74.webp)](https://image.mrxn.net/0dd6e4ac67b54aa9ba15e2f2ab14f543.webp)

成功延时 4 秒

计算机服务器

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
