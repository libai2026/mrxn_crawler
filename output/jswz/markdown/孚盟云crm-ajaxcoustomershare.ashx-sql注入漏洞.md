---
title: "孚盟云CRM AjaxCoustomerShare.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxCoustomerShare-sqli.html
asset_dir: assets/孚盟云crm-ajaxcoustomershare.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxCoustomerShare.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/17 17:02
- 570浏览
- [0评论](#comment)
- 24分钟阅读

深入探索

软件即服务

鉴权

客户关系管理

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxCoustomerShare.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 AjaxCoustomerShare.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 AjaxCoustomerShare 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  try
  {
    context.Response.ContentType = "text/plain";
    string str = context.Request["method"].ToString();
    if (!string.op_Equality(str, "DeleteEmpID"))
    {
      if (!string.op_Equality(str, "powerDetil"))
        return;
      this.powerDetil(context);
    }
    else
      this.DeleteEmpID(context);
  }
```

深入探索

传输层安全性协议

Web安全课程

网络安全会议

当 **method=DeleteEmpID** 时，进入**DeleteEmpID**方法

```
public void DeleteEmpID(HttpContext context)
{
  string str = context.Request["empid"].ToString();
  int num = this.dbHelper.ExecuteSql($" delete syMouldCustomShare where MouldID='BF001' AND BillFID='{context.Request["billfid"].ToString()}' AND EmpID='{str}'");
  context.Response.Write((object) num);
}
```

当 **type=powerDetil** 时进入 **powerDetil**

SQL注入防护

```
public string powerDetil(HttpContext context)
{
  string str1 = context.Request["empid"].ToString();
  string str2 = context.Request["billfid"].ToString();
  string str3 = context.Request["CNEmpName"].ToString();
  DataSet dataSet = this.dbHelper.Query($"{$"select bfEMP.EmpID, bfEMP.CNEmpName,syMouldFile.MouldName,syMouldCustomShare.BillFID,syMouldCustomShare.MouldID,\r\n   syMouldCustomShare.LinkMouldID,IsPowerAll\r\n   from syMouldCustomShare(nolock)\r\n   inner join bfEMP(nolock) on syMouldCustomShare.EmpID=bfEMP.EmpID\r\n   inner join syMouldFile(nolock) on  syMouldFile.MouldID=syMouldCustomShare.LinkMouldID\r\n    where syMouldCustomShare.MouldID='BF001' AND BillFID='{str2}'  and  bfEMP.EmpID='{str1}'   "}    select bfEMP.EmpID, bfEMP.CNEmpName,syMouldCustomShare.BillFID,\r\n   syMouldCustomShare.LinkMouldID,'附件' as MouldName,AttachPurCaption from  syMouldCustomShare(nolock)\r\n       inner join bfEMP(nolock) on syMouldCustomShare.EmpID=bfEMP.EmpID\r\n     where syMouldCustomShare.MouldID='BF001' AND BillFID='{str2}'  and  bfEMP.EmpID='{str1}'   ");
  DataTable table = dataSet.Tables[0];
```

最终可以看到，未经过滤或参数化绑定的参数 **billfid、 empid** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxCoustomerShare.ashx?method=DeleteEmpID&billfid=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxCoustomerShare.ashx SQL注入漏洞](images/img-001-58ded6ce1f26.webp)](https://image.mrxn.net/0641df71e5034bb9998c90a299043bf6.webp)

通过报错注入 成功在响应回显数据版本信息

代码安全审计

以及当 **method=powerDetil** 时，就不赘述了。

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
