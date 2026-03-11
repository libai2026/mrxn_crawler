---
title: "孚盟云CRM LicManage.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-LicManage-sqli.html
asset_dir: assets/孚盟云crm-licmanage.ashx-sql注入漏洞
---

# 孚盟云CRM LicManage.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/17 11:39
- 584浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

客户关系管理

application

数据库

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云`LicManage.ashx`接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `LicManage.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **LicManage** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str = context.Request["action"];
  if (!string.op_Equality(str, "GetLicDetail"))
  {
    if (string.op_Equality(str, "GetReNewList"))
      return;
    if (!string.op_Equality(str, "ExtensionPermit"))
    {
      if (!string.op_Equality(str, "ExtPermitByMoney"))
        return;
      this.ExtPermitByMoney(context);
    }
    else
      this.ExtensionPermit(context);
  }
  else
    this.GetLicDetail(context);
}
```

深入探索

安全工具开发

云安全解决方案

安全研究报告

根据参数`action`的值进入不同的处理逻辑，当`action=ExtensionPermit`时，看**ExtensionPermit**方法的实现

SQL注入防护

```
public void ExtensionPermit(HttpContext context)
{
  try
  {
    string empty = string.Empty;
    string AMouldID = context.Request["MouldID"] == null ? "" : context.Request["MouldID"].ToString();
    string ABillFID = context.Request["BillFID"] == null ? "" : context.Request["BillFID"].ToString();
    string str1 = context.Request["Auditer"] == null ? "" : context.Request["Auditer"].ToString();
    if (string.op_Inequality(AMouldID, "") && string.op_Inequality(ABillFID, ""))
    {
      int AAuditState = 0;
      DataTable dt = (DataTable) null;
      DataTable dt2 = (DataTable) null;
      if (!this.GetLicTable(AMouldID, ABillFID, ref AAuditState, ref dt, ref dt2))
      {
        context.Response.Write("false");
        return;
      }
```

当`MouldID`和`BillFID`**不为空**时，将二者带入**GetLicTable**方法

```
public bool GetLicTable(
  string AMouldID,
  string ABillFID,
  ref int AAuditState,
  ref DataTable dt,
  ref DataTable dt2)
{
  string empty = string.Empty;
  DataSet dataSet = this.dbHelper.Query($"SELECT TOP 1 B.TableName  FROM syMouldTables B WHERE B.MouldID='{AMouldID}' AND B.SQLNo=1 AND B.IsUpdate=1");
```

未经过滤或参数化绑定的参数 `AMouldID` 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

当 **action=ExtPermitByMoney**时，和上面看逻辑一样，就不赘述了，看下图即可明白

代码安全审计

[![孚盟云CRM LicManage.ashx SQL注入漏洞](images/img-001-3fe7bdfc00bd.webp)](https://image.mrxn.net/c48dcd07ecb64391955cee1f0f4d0d80.webp)

# 漏洞复现

```
POST /Ajax/LicManage.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=ExtensionPermit&MouldID='SQLI_POC--
```

[![孚盟云CRM LicManage.ashx SQL注入漏洞](images/img-002-05fbd0f7e274.webp)](https://image.mrxn.net/097fa989a137451db15b0b3c32637361.webp)

成功延时 5 秒

漏洞扫描服务

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
