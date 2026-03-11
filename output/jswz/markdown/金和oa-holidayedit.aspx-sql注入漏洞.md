---
title: "金和OA HolidayEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-HolidayEdit-sqli.html
asset_dir: assets/金和oa-holidayedit.aspx-sql注入漏洞
---

# 金和OA HolidayEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/13 13:31
- 237浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

云安全解决方案

物流软件安全

计算机安全

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `HolidayEdit.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `HolidayEdit.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.FlowStat.dll` 将其进行反编译后找到 **HolidayEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.type = this.Request["type"];
  if (((Control) this).Page.IsPostBack)
    return;
  ((WebControl) this.save).Attributes.Add("onclick", "return CheckInput()");
  DateTime dateTime = DateTime.Now;
  int year = dateTime.Year;
  if (string.op_Equality(this.type, "new"))
  {
    for (int index = year - 3; index < year + 3; ++index)
      ((ListControl) this.drop_Year).Items.Add(new ListItem(index.ToString(), index.ToString()));
    HtmlInputText txtStartTime = this.txt_StartTime;
    dateTime = DateTime.Now;
    string shortDateString1 = dateTime.ToShortDateString();
    ((HtmlInputControl) txtStartTime).Value = shortDateString1;
    HtmlInputText txtEndTime = this.txt_endTime;
    dateTime = DateTime.Now;
    string shortDateString2 = dateTime.ToShortDateString();
    ((HtmlInputControl) txtEndTime).Value = shortDateString2;
    ((ListControl) this.drop_Year).Items.FindByValue(year.ToString()).Selected = true;
  }
  else
  {
    DataTable dataTable = stat.HolidaySearch(this.Request["id"]);
    for (int index = year - 20; index < year + 5; ++index)
```

深入探索

传输层安全性协议

网络安全课程

JSON处理工具

当type不等于new时，参数id带入`HolidaySearch`方法

跟进`HolidaySearch`方法

```
public static DataTable HolidaySearch(string id)
{
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($" select * from HolidayData where hid='{id}' ");
}
```

参数`id`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.FlowStat/HolidayEdit.aspx/?id=SQLI_POC&type=1 HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA HolidayEdit.aspx SQL注入漏洞](images/img-001-2835498300fc.webp)](https://image.mrxn.net/aa77fa9bb73a4be18e3bd7c07c58a947.webp)

成功延时 4 秒

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
