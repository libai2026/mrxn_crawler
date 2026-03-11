---
title: "孚盟云CRM AjaxCustomizeReport.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-AjaxCustomizeReport-sqli.html
asset_dir: assets/孚盟云crm-ajaxcustomizereport.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxCustomizeReport.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/18 16:39
- 627浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

身份验证

CRM

SaaS

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxCustomizeReport.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 AjaxCustomizeReport.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 AjaxCustomizeReport 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["action"];
  if (!string.IsNullOrEmpty(UserCookie.GetCookieValue("empId")))
  {
    this.userId = UserCookie.GetCookieValue("empId");
    Helper.WriteLog("ShowCustomizeReportData userId:" + this.userId, "ddSaas");
    this.userId = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(this.userId);
    Helper.WriteLog("ShowCustomizeReportData DesDecrypt userId:" + this.userId, "ddSaas");
  }
  try
  {
    string str2 = "";
    string str3 = str1;
    if (!string.op_Equality(str3, "SetQueryConditionAndControlType"))
    {
      if (!string.op_Equality(str3, "GetMouldList"))
      {
        if (!string.op_Equality(str3, "GetCustomizeReportSelectItem"))
        {
          if (string.op_Equality(str3, "GetCustomizeReportDataPage"))
            str2 = this.GetCustomizeReportDataPage(context);
        }
        else
          str2 = this.GetCustomizeReportSelectItem(context);
      }
      else
        str2 = this.GetMouldList(context);
    }
    else
      str2 = this.SetQueryConditionAndControlType(context);
    context.Response.Write(str2);
  }
```

当 **method=GetMouldList** 时，进入**GetMouldList**方法

```
private string GetMouldList(HttpContext context)
{
  string mouldList = "";
  DataTable table = this.dbHelper.Query($"select * from syMouldFile where BMouldType=4 and MouldName like '%{context.Request["searchTxt"]}%'").Tables[0];
```

最终可以看到，未经过滤或参数化绑定的参数 **searchTxt** 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /m/Dingding/Ajax/AjaxCustomizeReport.ashx?method=GetMouldList&searchTxt=SQLI_POC HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM AjaxCustomizeReport.ashx SQL注入漏洞](images/img-001-4ddb92dc96c3.webp)](https://image.mrxn.net/838b059cd1cc491e9eea1f2bca8da9e9.webp)

成功延时 4 秒

SQL注入检测工具

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

漏洞预警服务
