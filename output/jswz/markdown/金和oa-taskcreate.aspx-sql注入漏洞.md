---
title: "金和OA TaskCreate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-TaskCreate-sqli.html
asset_dir: assets/金和oa-taskcreate.aspx-sql注入漏洞
---

# 金和OA TaskCreate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/6 12:15
- 596浏览
- [0评论](#comment)
- 17分钟阅读

深入探索

服务器

软件

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `TaskCreate.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

先看下 TaskCreate.aspx 的代码定义区域

```
<%@ Page Language="c#" CodeBehind="TaskCreate.aspx.cs" AutoEventWireup="True" Inherits="JHSoft.Web.DailyTaskManage.TaskCreate" %>

<%@ Register TagPrefix="cc1" Namespace="JHSoft.UserControl" Assembly="JHSoft.UserControl" %>
<%@ Register TagPrefix="cc2" Namespace="HBControls" Assembly="HBControls" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <title>TaskCreate</title>
.....
```

在 `bin` 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `TaskCreate` 的处理逻辑

代码安全审计

[![金和OA TaskCreate.aspx SQL注入漏洞](images/img-001-697e38376f9b.webp)](https://image.mrxn.net/7dfba764b42844649f190a54b6fd234c.webp)

跟进 `GetTaskSuperior` 方法

深入探索

网络安全会议

技术文章订阅

VPN服务

```
public void GetTaskSuperior()
{
  this.strSuperiorTaskID = this.Request["taskID"].ToString();
  string QueryString1 = $" select top 1 TaskID,TaskName,TaskNumber,TaskRootScale,TaskContent,OriginModule,OriginID from TaskManage where TaskID = '{this.strSuperiorTaskID}'";
  string QueryString2 = $" select FileID,FilePath from Files where ModuleID = 'ProjectTaskNew' and ModuleMessageID = '{this.strSuperiorTaskID}' ";
  DataTable dataTable = this.dbop.ExecSQLReDataTable(QueryString1);
  DataTable dt = this.dbop.ExecSQLReDataTable(QueryString2);
  if (((InternalDataCollectionBase) dataTable.Rows).Count > 0)
```

多个参数 **taskID** 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.dailytaskmanage/TaskCreate.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

taskID='SQLI_POC
```

[![金和OA TaskCreate.aspx SQL注入漏洞](images/img-002-08a6abf8e690.webp)](https://image.mrxn.net/5973e13d8bfb423db2ff40f317f57e6d.webp)

延时 8 秒（执行两次）

漏洞扫描服务

[![金和OA TaskCreate.aspx SQL注入漏洞](images/img-003-dd89d49d8ebd.webp)](https://image.mrxn.net/12cd813a59494b5282b4e63ed77b8486.webp)

以及延时 4 秒（执行两次）

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
