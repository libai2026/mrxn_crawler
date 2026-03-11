---
title: "红帆ioffice MobileBind.aspx SQL 注入漏洞"
source: https://mrxn.net/jswz/ioffice-MobileBind-sqli.html
asset_dir: assets/红帆ioffice-mobilebind.aspx-sql-注入漏洞
---

# 红帆ioffice MobileBind.aspx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/29 08:20
- 717浏览
- [0评论](#comment)
- 34分钟阅读

深入探索

鉴权

身份验证

SQL

---

# 漏洞简介

红帆iOffice的/ioffice/prg/Mobile/Base/MobileBind.aspx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，未经身份验证地获取数据库敏感信息，影响范围包括红帆iOffice系统的数据访问权限。

SQL注入防护

# 影响版本

# fofa语法

> (title="iOffice.net" || body="/iOffice/js" || (body="iOffice.net" && header!="couchdb" && header!="drupal") || body="iOfficeOcxSetup.exe" || body="Hongfan. All Rights Reserved")

# 漏洞分析

先看下`MobileBind.aspx` 里引用的代码在哪里（Inherits）

```
<%@ Page Language="vb" AutoEventWireup="false" CodeBehind="MobileBind.aspx.vb" Inherits="Mobile.MobileBind"
    MasterPageFile="~/prg/set/ioPage/ioPageEdit.master" %>
```

去bin目录找到`MobileBind.dll`后编译打开，看`MobileBind`它的实现逻辑

代码安全审计

```
public class MobileBind : WebPageBase
{
[field: AccessedThroughProperty("txtUDIDReqHisID")]
protected virtual TextBox txtUDIDReqHisID { get; [MethodImpl((MethodImplOptions) 32)] set; }

private bool SaveData()
{
  DataTable dataTable = Mobile.Mobile.GetclientUDIDReqHisByID(this.txtUDIDReqHisID.Text);
  if (dataTable.Rows.Count > 0)
  {
    switch (Mobile.Mobile.bindClientUDID((Array) new string[2]
    {
      Conversions.ToString(dataTable.Rows[0]["LoginID"]),
      Conversions.ToString(dataTable.Rows[0]["UDID"])
    }))
    {
      case -2:
        Page page1 = ((Control) this).Page;
        pf.ShowMessage(ref page1, "不允许绑定重复设备");
        ((Control) this).Page = page1;
        return false;
      case -1:
        Page page2 = ((Control) this).Page;
        pf.ShowMessage(ref page2, "当前登录号只允许绑定一个移动设备");
        ((Control) this).Page = page2;
        return false;
    }
  }
  return true;
}
```

最开始的一些变量定义，前端按钮`cmdUDIDReqHis`以及`cmdClearAll`

[![红帆ioffice MobileBind.aspx SQL 注入漏洞](images/img-001-9546457d019b.webp)](https://image.mrxn.net/f8dee53ed1274dc68c09aae5b84aba08.webp)

对应后端的两个逻辑

漏洞扫描服务

```
private void cmdUDIDReqHis_Click(object sender, EventArgs e)
{
  this.SaveData();
  this.BindDataGrid();
}

private void cmdClearAll_Click(object sender, EventArgs e)
{
  this.ClearSaveData();
  this.BindDataGrid();
}
```

跟进`SaveData`看下

```
private bool SaveData()
{
  DataTable dataTable = Mobile.Mobile.GetclientUDIDReqHisByID(this.txtUDIDReqHisID.Text);
  if (dataTable.Rows.Count > 0)
  {
    switch (Mobile.Mobile.bindClientUDID((Array) new string[2]
    {
      Conversions.ToString(dataTable.Rows[0]["LoginID"]),
      Conversions.ToString(dataTable.Rows[0]["UDID"])
    }))
    {
      case -2:
        Page page1 = ((Control) this).Page;
        pf.ShowMessage(ref page1, "不允许绑定重复设备");
        ((Control) this).Page = page1;
        return false;
      case -1:
        Page page2 = ((Control) this).Page;
        pf.ShowMessage(ref page2, "当前登录号只允许绑定一个移动设备");
        ((Control) this).Page = page2;
        return false;
    }
  }
  return true;
}
```

**txtUDIDReqHisID**被带入`Mobile.Mobile.GetclientUDIDReqHisByID` 方法，跟进看下

编程

```
public static DataTable GetclientUDIDReqHisByID(string ID)
{
  return SqlData.ExecuteDataset(Globals.ConnectString, (CommandType) 1, $"select * from clientUDIDReqHis where ID in ({ID})").Tables[0];
}
```

ok,到这里，漏洞成因就非常明了了，从前端TextBox获取的**txtUDIDReqHisID**最终经过一系列赋值传递后被直接拼接进`$"select * from clientUDIDReqHis where ID in ({ID})"` sql语句里，全程无过滤或者校验，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 漏洞复现需要打开漏洞文件页面获取一些其他必要参数如\_\_VIEWSTATE之类

```
POST /ioffice/prg/Mobile/Base/MobileBind.aspx HTTP/1.1
Host: ioffice.mrxn.net
Content-Type: application/x-www-form-urlencoded

__EVENTTARGET=ctl00%24cntForm%24cmdUDIDReqHis&__EVENTARGUMENT=&__VIEWSTATE=xxxx&__VIEWSTATEGENERATOR=xxxxx&btVerify=&ctl00%24cntForm%24txtUDIDReqHisID=SQLI_POC&ctl00%24cntForm%24cmdUDIDReqHis=Button
```

[![红帆ioffice MobileBind.aspx SQL 注入漏洞](images/img-002-0c02a6f46b34.webp)](https://image.mrxn.net/111c291fbc9b41e4bc7c78f2ccd8428d.webp)

成功利用报错[注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显当前数据库用户信息

网络安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
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
