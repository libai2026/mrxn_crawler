---
title: "孚盟云CRM AjaxProductFiled.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxProductFiled-sqli.html
asset_dir: assets/孚盟云crm-ajaxproductfiled.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxProductFiled.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/19 16:41
- 546浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

SQL

物流软件安全

软件

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxProductFiled.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 AjaxProductFiled.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 AjaxProductFiled 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  try
  {
    context.Response.ContentType = "text/plain";
    string str = context.Request["method"].ToString();
    context.Request["MouldID"].ToString();
    if (!string.op_Equality(str, "savePuductFiled"))
      return;
    this.savePuductFiled(context);
  }
```

当 **method=savePuductFiled** 时，进入**savePuductFiled**方法

```
public void savePuductFiled(HttpContext context)
{
  string MouldID = context.Request["MouldID"].ToString();
  DataTable dataTable = this.GetsyFieldGroup(MouldID);
```

继续跟进 **GetsyFieldGroup** 方法

```
public DataTable GetsyFieldGroup(string MouldID)
{
  return this.dbHelper.Query($"select FUID, MouldID, GroupName, OrderNo from dbo.syFieldGroup  WHERE MouldID= '{MouldID}' ORDER BY OrderNo").Tables[0];
}
```

深入探索

安全

Windows安全工具

安全运维咨询

最终可以看到，未经过滤或参数化绑定的参数 **MouldID** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxProductFiled.ashx?method=savePuductFiled&MouldID=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxProductFiled.ashx SQL注入漏洞](images/img-001-6d80a096d75c.webp)](https://image.mrxn.net/ec1df2062d4f4857b41687f79677d938.webp)

成功延时 5 秒

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
