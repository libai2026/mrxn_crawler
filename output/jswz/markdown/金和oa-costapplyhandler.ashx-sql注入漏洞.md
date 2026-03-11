---
title: "金和OA CostApplyHandler.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CostApplyHandler-sqli.html
asset_dir: assets/金和oa-costapplyhandler.ashx-sql注入漏洞
---

# 金和OA CostApplyHandler.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/16 13:29
- 329浏览
- [0评论](#comment)
- 36分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CostApplyHandler.ashx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `CostApplyHandler.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **CostApplyHandler** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str = context.Request["action"];
  if (string.IsNullOrEmpty(str))
    return;
  switch (str)
  {
    case "Amount":
      this.GetAmount(context);
      break;
    case "YeahChange":
      this.GetPeriod(context);
      break;
    case "GetAppID":
      this.GetAppID(context);
      break;
    case "ShengChange":
      this.GetSHI(context);
      break;
    case "CostApply_Export":
      this.ExportData(context);
      break;
    case "GetDeptName":
      this.GetDepAlltName(context);
      break;
    case "GetItemName":
      this.GetItemName(context);
      break;
    case "GetJE":
      this.GetTotalJE(context);
      break;
    case "GetBZAmount":
      this.GetBZAmount(context);
      break;
    case "CheckObj":
      this.CheckObj(context);
      break;
    case "IsParent":
      this.CheckIsParent(context);
      break;
    case "CheckForMoney":
      this.CheckForMoney(context);
      break;
    case "GetTravelAppID":
      this.GetTravelAppID(context);
      break;
    case "IsParentFeeItem":
      this.GetIsParent(context);
      break;
    case "GetAllDepartmentName":
      this.GetAllDepName(context);
      break;
    case "AppSumMoney":
      this.GetAppSumMoney(context);
      break;
    case "CheckForTravelExpend":
      this.GetCheckForTravel(context);
      break;
    case "CheckForCostExpend":
      this.GetCheckForCost(context);
      break;
    case "CostAppSumMoney":
      this.GetCostAppSumMoney(context);
      break;
    case "GetSubjectID":
      this.GetSubjectIDByItemCode(context);
      break;
    case "GetDeptByUserID":
      this.GetDeptByUserID(context);
      break;
    case "getUserCostBorrower":
      this.GetUserCostBorrower(context);
      break;
    case "DelTempImp":
      this.DelTempImp(context);
      break;
    case "SaveVouch":
      this.VouchSave(context);
      break;
    case "GetFlowDealUsers":
      this.GetFlowDealUsers(context);
      break;
    case "UseExpendMoney":
      this.IsUseExpendMoney(context);
      break;
  }
}
```

根据**action**的值进入不同的处理流程

代码安全审计

以 `action=YeahChange` 为例，`yeah`被带入GetPeriodByYear方法

```
protected void GetPeriod(HttpContext context)
{
  string str1 = string.Empty;
  DataTable periodByYear = this.cc.GetPeriodByYear(context.Request["yeah"]);
......
protected void GetPeriod(HttpContext context)
{
  string str1 = string.Empty;
  DataTable periodByYear = this.cc.GetPeriodByYear(context.Request["yeah"]);
```

跟进 `GetPeriodByYear` 方法

```
public DataTable GetPeriodByYear(string Year)
{
  return this.db.ExecSQLReDataTable($"{" Select distinct Budget_PeriodManage.Period " + " from Budget_PeriodManage " + " Left outer join Budget_PeriodDivert " + " on Budget_PeriodDivert.YearPeriod = Budget_PeriodManage.YearPeriod " + " and  Budget_PeriodDivert.Period = Budget_PeriodManage.Period "} where Budget_PeriodDivert.Status is null and Budget_PeriodManage.YearPeriod ='{Year}'" + " order by Period asc ");
}
```

非常明显的直接将`yeah`参数拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

其他处理类似，就不赘述了。

漏洞扫描服务

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/BudgetExecution/Handlers/CostApplyHandler.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=YeahChange&yeah=SQLI_POC
```

[![金和OA CostApplyHandler.ashx SQL注入漏洞](images/img-001-b03784b6f14e.webp)](https://image.mrxn.net/c9bef9726e7d44039eb6bda7515e3a4a.webp)

成功延时 4 秒

数据管理

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
