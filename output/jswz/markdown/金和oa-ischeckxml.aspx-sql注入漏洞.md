---
title: "金和OA isCheckXml.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-isCheckXml-sqli.html
asset_dir: assets/金和oa-ischeckxml.aspx-sql注入漏洞
---

# 金和OA isCheckXml.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/18 13:31
- 230浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

漏洞修复方案

防火墙软件

授权

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `isCheckXml.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `isCheckXml.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Groups.dll` 将其进行反编译后找到 **isCheckXml** 的处理逻辑

深入探索

技术文章订阅

JSON处理工具

软件

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request["GroupName"] != null)
    this.reqGroupName = this.Request["GroupName"].ToString().Trim();
  if (this.Request.QueryString["GroupID"] != null)
    this.groupID = this.Request.QueryString["GroupID"].ToString();
  if (string.op_Inequality(this.reqGroupName, "") && string.op_Equality(this.groupID, ""))
  {
    if (!this.m_Group.IsCheckName(this.reqGroupName))
      this.Response.Write("ok");
    else
      this.Response.Write("");
  }
  if (string.op_Inequality(this.reqGroupName, "") && string.op_Inequality(this.groupID, ""))
  {
    if (!this.m_Group.IsCheckName(this.reqGroupName, this.groupID))
      this.Response.Write("ok");
    else
      this.Response.Write("");
  }
  this.Response.End();
}
```

跟进`IsCheckName`方法

```
public bool IsCheckName(string GroupName)
{
  if (string.op_Equality(GroupName.Trim(), ""))
    return false;
  string str = $"select GroupName From UserGroup Where GroupName='{GroupName.Trim()}'";
  DataSet dataSet1 = new DataSet();
  DataSet dataSet2 = this.svr.ExecSQLReDataSet(str);
```

参数`GroupName`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.groups/isCheckXml.aspx/?GroupName=SQLI_POC&GroupID=1 HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA isCheckXml.aspx SQL注入漏洞](images/img-001-cd536458afab.webp)](https://image.mrxn.net/749b991f015e4c5cafb176e644d0e776.webp)

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
