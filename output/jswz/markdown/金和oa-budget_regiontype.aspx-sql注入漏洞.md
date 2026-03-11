---
title: "金和OA Budget_RegionType.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Budget_RegionType-sqli.html
asset_dir: assets/金和oa-budget_regiontype.aspx-sql注入漏洞
---

# 金和OA Budget\_RegionType.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/1 13:31
- 245浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

软件

数据库

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SubjectHandler.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

云安全解决方案

防火墙软件

SQL注入检测工具

根据 `SubjectHandler.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **SubjectHandler** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitPage();
  if (this.Request.QueryString["RegionID"] == null || string.op_Equality(this.Request.QueryString["RegionID"], ""))
  {
    this.title = "区域添加";
    this.btnOK.Text = "添 加";
  }
  else
  {
    this.title = "区域修改";
    this.btnOK.Text = "修 改";
    ((WebControl) this.txtRegionID).Enabled = false;
    if (((Control) this).Page.IsPostBack)
      return;
    this.getInfomation();
  }
}
```

跟进`getInfomation`方法看下其实现

代码安全审计

```
protected void getInfomation()
{
  DataSet typeInfomationById = this.costManager.Get_Budget_RegionTypeInfomationByID(this.Request.QueryString["RegionID"]);
```

`RegionID` 被带入`Get_Budget_RegionTypeInfomationByID`方法

```
public DataSet Get_Budget_RegionTypeInfomationByID(string RegionID)
{
  return this.GetDS_BySQL($" Select RegionName,remark from Budget_RegionType where RegionID = '{RegionID}' ");
}
```

参数`RegionID`被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/CostManagement/TravelBasicSetting/Budget_RegionType.aspx/?RegionID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA Budget_RegionType.aspx SQL注入漏洞](images/img-001-d7f3e6743557.webp)](https://image.mrxn.net/14820c48be0d42d58156e4e8845add71.webp)

成功延时 4 秒

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
