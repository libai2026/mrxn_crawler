---
title: "孚盟云CRM GetDropDownListContent.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-GetDropDownListContent-sqli.html
asset_dir: assets/孚盟云crm-getdropdownlistcontent.ashx-sql注入漏洞
---

# 孚盟云CRM GetDropDownListContent.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/17 08:31
- 746浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

客户关系管理

SaaS

服务器

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云`GetDropDownListContent.ashx`接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

深入探索

CRM

计算机安全

SQL注入防护

直接看 `GetDropDownListContent.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **GetDropDownListContent** 方法的实现如下

[![孚盟云CRM GetDropDownListContent.ashx SQL注入漏洞](images/img-001-b08869c8b0f3.webp)](https://image.mrxn.net/c8aeb63c54374710ad0bcd07ac624ef5.webp)

根据参数`action`的值进入不同的处理逻辑，可以看到众多的处理分支，其中当 **action=getType** 时，处理逻辑如下

深入探索

文件大小转换

安全认证考试

漏洞扫描服务

```
public void getType(HttpContext context)
{
  int num1 = 0;
  int num2 = 0;
  StringBuilder stringBuilder = new StringBuilder();
  DataTable dataSource = this.createPageManager.GetDataSource("select * from syProdPlusProp  sy inner join syProdPlusPropSort sp on sy.FUID=sp.PlusPropFUID WHERE SortFID=" + (context.Request["Typeid"] == null ? "" : context.Request["Typeid"].ToString()));
```

未经过滤或参数化绑定的参数 `Typeid` 被直接拼接进SQL语句中进行执行，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

当 `action=personalSetting`时

```
private void SavePseronalSettingContent(HttpContext context)
{
  string empId = context.Request["UserID"];
  string[] strArray1 = context.Request["SettingID"].Split(new char[1]
  {
    ','
  });
  string[] strArray2 = context.Request["SettingName"].Split(new char[1]
  {
    ','
  });
  string[] strArray3 = context.Request["SettingValue"].Split(new char[1]
  {
    ','
  });
  if (string.IsNullOrEmpty(empId) || strArray1.Length < 0 || strArray2.Length < 0)
    context.Response.Write("0");
  PersonalSettingManager personalSettingManager = new PersonalSettingManager();
  int num = 0;
  for (int index = 0; index < strArray1.Length; ++index)
  {
    personalSettingManager.SaveEmpPersonalSettingValue(empId, Convert.ToInt32(strArray1[index]), strArray2[index], strArray3[index]);
    ++num;
  }
```

跟进`SaveEmpPersonalSettingValue`方法

```
public void SaveEmpPersonalSettingValue(
  string empId,
  int settingId,
  string settingName,
  string settingValue)
{
  this.sqlStr = $"insert into PersonalSettingsValue (EmpID,SettingID,SettingName,SettingValue) values ('{empId}','{(object) settingId}','{settingName}','{settingValue}')";
  this.dbHelper.ExecuteSql(this.sqlStr);
}
```

`empId` 即参数 `UserID` 也是被直接拼接在SQL语句中执行，同样造成SQL注入漏洞。

以及 **action=getUnit**

[![孚盟云CRM GetDropDownListContent.ashx SQL注入漏洞](images/img-002-5b686add1bf5.webp)](https://image.mrxn.net/c84ca94f9ab140e8a997ed93d63e179e.webp)

[![孚盟云CRM GetDropDownListContent.ashx SQL注入漏洞](images/img-003-bf2a18b1926e.webp)](https://image.mrxn.net/ae2b99f4d55e431fb3d38708bfc3734f.webp)

参数`uid`也是同样被直接拼接进SQL语句执行，也存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞

当`action=lookUp` 时

[![孚盟云CRM GetDropDownListContent.ashx SQL注入漏洞](images/img-004-e8316af9f0f9.webp)](https://image.mrxn.net/89a7c6f2e6e34e6885a183e36e181f8a.webp)

# 漏洞复现

```
POST /Ajax/GetDropDownListContent.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=getType&Typeid='SQLI_POC--
```

[![孚盟云CRM GetDropDownListContent.ashx SQL注入漏洞](images/img-005-1e744cacf8ca.webp)](https://image.mrxn.net/0b18fa7b704f42149fcb3e4b026ad579.webp)

成功通过报错注入在响应爆出数据库版本信息

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
