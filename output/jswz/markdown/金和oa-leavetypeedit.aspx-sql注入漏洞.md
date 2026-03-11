---
title: "金和OA LeaveTypeEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-LeaveTypeEdit-sqli.html
asset_dir: assets/金和oa-leavetypeedit.aspx-sql注入漏洞
---

# 金和OA LeaveTypeEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/11 13:31
- 237浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

漏洞预警服务

网络安全培训

漏洞扫描器

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `LeaveTypeEdit.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `LeaveTypeEdit.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.dossier.dll` 将其进行反编译后找到 **LeaveTypeEdit** 的处理逻辑

```
this.type = this.Request.QueryString["type"];
this.typeID = this.Request.QueryString["ID"];
this.type = this.type.ToUpper();
this.InitText();
if (this.IsPostBack)
  return;
if (!string.IsNullOrEmpty(this.type) && !string.IsNullOrEmpty(this.typeID))
{
  if (this.type.Equals("ADD"))
  {
    this.PageTitle = this.strPageTitle1;
  }
  else
  {
    if (!this.type.Equals("EDIT"))
      return;
    this.PageTitle = this.strPageTitle2;
    this.ShowTypeName(this.typeID);
  }
}
```

深入探索

技术文章订阅

计算机安全

Web安全书籍

当**type=EDIT**且**ID参数不为空或null**时进入`ShowTypeName`方法

跟进`ShowTypeName`方法

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
private void ShowTypeName(string typeID)
{
  this.txtTypeName.Text = this.leaveType.GetTypeNameByID(typeID);
}
```

继续跟进`GetTypeNameByID`方法

```
public string GetTypeNameByID(string typeID)
{
  object obj = this.db.ExecSQLReobject("select leaveTypeName from LeaveWorkerType where delflag=0 and leaveTypeid=" + typeID);
  return obj != DBNull.Value ? obj.ToString() : string.Empty;
}
```

参数`ID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.dossier/LeaveTypeEdit.aspx/?ID=SQLI_POC&type=EDIT HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA LeaveTypeEdit.aspx SQL注入漏洞](images/img-001-20ac0546226d.webp)](https://image.mrxn.net/60a51351c7c243859741870e2684e7e0.webp)

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
