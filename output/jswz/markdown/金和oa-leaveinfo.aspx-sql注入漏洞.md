---
title: "金和OA LeaveInfo.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-LeaveInfo-sqli.html
asset_dir: assets/金和oa-leaveinfo.aspx-sql注入漏洞
---

# 金和OA LeaveInfo.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/10 13:31
- 208浏览
- [0评论](#comment)
- 19分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `LeaveInfo.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `LeaveInfo.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.dossier.dll` 将其进行反编译后找到 **LeaveInfo** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.InitText();
  if (this.Request.QueryString["UserID"] != null)
    this.UserID = this.Request.QueryString["UserID"].ToString();
  if (this.IsPostBack)
    return;
  this.InitList();
}
```

跟进`InitList`方法

```
  private void InitList()
  {
    string empty = string.Empty;
    this.List1.RecordCount = 2;
    this.List1.Identify = 0;
    string str = $"<root>{empty}{this.GetListData()}</root>";
    this.List1.WidthStyle = UserWebControl.DataGrid.DataGrid.EnumWidthStyle.Fix;
    this.List1.DataSource = (object) str;
  }
```

跟进`GetListData`方法

```
  private string GetListData()
  {
    StringBuilder stringBuilder = new StringBuilder();
    DataTable leaveInfo = this.dossier.GetLeaveInfo(this.UserID);
```

继续跟进`GetLeaveInfo`方法

```
public DataTable GetLeaveInfo(string UserID)
{
  DataTable leaveInfo = this.dboperator.ExecSQLReDataTable($"select a.LeaveID,a.LeaveType,a.LeaveTime,a.[filename],b.[filename] as handOverFileName from LeaveWorker a left join LeaveHandOver b on a.HandOverID=b.HandOverID Where a.LeaveID in (select LeaveID from LeaveWorkerAttach Where LeaveCode = '{UserID}' and LeaveState = 1) and a.LeaveFlag =1 and a.DelFlag =0 ");
  if (this.dboperator.IsError)
    this.strErrMessage = this.dboperator.ErrorMessage;
  return leaveInfo;
}
```

参数`UserID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.dossier/LeaveInfo.aspx/?UserID=SQLI_POC&gettype=getstation HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA LeaveInfo.aspx SQL注入漏洞](images/img-001-ab14eda0f92c.webp)](https://image.mrxn.net/f7acb3a091864821a7ac66e51941af39.webp)

成功延时 4 秒

代码安全审计

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
