---
title: "金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForGetBudgetTime-sqli.html
asset_dir: assets/金和oa-ajaxforgetbudgettime.ashx-sql注入漏洞
---

# 金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/15 13:29
- 300浏览
- [0评论](#comment)
- 22分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForGetBudgetTime.ashx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AjaxForGetBudgetTime.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForGetBudgetTime** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string strType = context.Request["strType"];
  string strPeriod = context.Request["strTime"];
  string str1 = context.Request["strYear"];
  string str2 = string.Empty;
  if (string.op_Equality(strType, "getTime"))
  {
    DataTable periodByYear = this.cc.GetPeriodByYear(str1);

else
{
  string strSubjectCode = context.Request["strSubjectCode"];
  string strValue = context.Request["strValue"];
  DataTable budgetImportData = this.deptCostSet.GetBudgetImportData(strType, strValue, str1, strPeriod, strSubjectCode);
```

根据**strType**的值进入不同的处理流程

代码安全审计

[![金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞](images/img-001-e077d17e9c25.webp)](https://image.mrxn.net/09f03d61453146b6a7546b3df23e5521.webp)

当 `strType=getTime` 时，`strYear`被带入`GetPeriodByYear`方法

```
context.Response.ContentType = "text/plain";
string strType = context.Request["strType"];
string strPeriod = context.Request["strTime"];
string str1 = context.Request["strYear"];
string str2 = string.Empty;
if (string.op_Equality(strType, "getTime"))
{
  DataTable periodByYear = this.cc.GetPeriodByYear(str1);
```

跟进 `GetPeriodByYear` 方法

```
public DataTable GetPeriodByYear(string Year)
{
  return this.db.ExecSQLReDataTable($"{" Select distinct Budget_PeriodManage.Period " + " from Budget_PeriodManage " + " Left outer join Budget_PeriodDivert " + " on Budget_PeriodDivert.YearPeriod = Budget_PeriodManage.YearPeriod " + " and  Budget_PeriodDivert.Period = Budget_PeriodManage.Period "} where Budget_PeriodDivert.Status is null and Budget_PeriodManage.YearPeriod ='{Year}'" + " order by Period asc ");
}
```

非常明显的直接将strYear参数拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

GetBudgetImportData

[![金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞](images/img-002-60a520ad8673.webp)](https://image.mrxn.net/e2c271f4795d4bcaa4b670081f3e015c.webp)

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/BudgetExecution/Handlers/AjaxForGetBudgetTime.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getTime&strTime=&strYear=SQLI_POC
```

[![金和OA AjaxForGetBudgetTime.ashx SQL注入漏洞](images/img-003-3e6f7cd9827a.webp)](https://image.mrxn.net/a4e5bf2b49b645e1b0ede8b930f8c196.webp)

成功延时 4 秒

漏洞预警服务

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
