---
title: "金和OA CostApplyListDetails.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CostApplyListDetails-sqli.html
asset_dir: assets/金和oa-costapplylistdetails.aspx-sql注入漏洞
---

# 金和OA CostApplyListDetails.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/12 13:22
- 302浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

木马

软件

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CostApplyListDetails.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `CostApplyListDetails.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **CostApplyListDetails** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.KeyCtrl("JHCostControl");
  this.dataBind();
}
```

在`dataBind`方法里根据不同的`strGetType`值处理进入不同的处理

代码安全审计

[![金和OA CostApplyListDetails.aspx SQL注入漏洞](images/img-001-43c6a199710e.webp)](https://image.mrxn.net/901952f3de0d49b9a4cfb9e62e1b55c2.webp)

以**strGetType=Travel**为例，其处理逻辑如下

```
if (string.op_Equality(str1, "Travel"))
{
  DataTable travelApplyDetails = costHelper.GetTravelApplyDetails(RecordNo);
```

跟进`GetTravelApplyDetails`方法

```
public DataTable GetTravelApplyDetails(string RecordNo)
{
  return this.db.ExecSQLReDataTable($"Select Distinct Budget_TravelCostApply.AppID, RecordNo, AppDeptID, AppUserID, SubTime, YearPeriod, Period, EntityID, EntityObjectID, Budget_TravelCostApply.Remark, PositionID, SumMoney, AppFlag, DelFlag  from Budget_TravelCostApply left outer join Budget_TravelCostApplySub on Budget_TravelCostApplySub.AppID = Budget_TravelCostApply.AppID where RecordNo = '{RecordNo}'");
}
```

至此，就非常明了了，参数`RecordNo`被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

深入探索

安全工具开发

Windows安全工具

JSON处理工具

其他几个处理逻辑差不多如下图所示

漏洞扫描服务

[![金和OA CostApplyListDetails.aspx SQL注入漏洞](images/img-002-b3c30117029a.webp)](https://image.mrxn.net/2455cc22a42248a8ba55f2fe89e89764.webp)

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/BudgetExecution/CostApplyListDetails.aspx/?RecordNo=SQLI_POC&strGetType=Travel HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA CostApplyListDetails.aspx SQL注入漏洞](images/img-003-939c32574a68.webp)](https://image.mrxn.net/7f353dfc5f4445198c9cb79284b7079b.webp)

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
