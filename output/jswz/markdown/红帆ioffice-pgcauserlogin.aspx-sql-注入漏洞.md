---
title: "红帆ioffice PgcaUserLogin.aspx SQL 注入漏洞"
source: https://mrxn.net/jswz/ioffice-Identity-PgcaUserLogin-sqli.html
asset_dir: assets/红帆ioffice-pgcauserlogin.aspx-sql-注入漏洞
---

# 红帆ioffice PgcaUserLogin.aspx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/26 16:30
- 787浏览
- [0评论](#comment)
- 1小时阅读

深入探索

软件

鉴权

认证

---

# 漏洞简介

红帆iOffice的/ioffice/Identity/PgcaUserLogin.aspx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，未经身份验证地获取数据库敏感信息，影响范围包括红帆iOffice系统的数据访问权限。

SQL注入防护

# 影响版本

# fofa语法

> (title="iOffice.net" || body="/iOffice/js" || (body="iOffice.net" && header!="couchdb" && header!="drupal") || body="iOfficeOcxSetup.exe" || body="Hongfan. All Rights Reserved")

# 漏洞分析

先看下`PgcaUserLogin.aspx` 里引用的代码在哪里（Inherits）

```
<%@ Page Language="vb" AutoEventWireup="false" CodeBehind="PgcaUserLogin.aspx.vb"
    Inherits="iden.PgcaUserLogin" %>
```

去bin目录找到`iden.dll`后编译打开，看`PgcaUserLogin`它的实现逻辑

代码安全审计

```
public class PgcaUserLogin : WebPageBase
{
  [AccessedThroughProperty("Head1")]
  private HtmlHead _Head1;
  [AccessedThroughProperty("form1")]
  private HtmlForm _form1;
  [AccessedThroughProperty("ioScriptManager1")]
  private ioScriptManager _ioScriptManager1;
  [AccessedThroughProperty("updatePanel1")]
  private ioUpdatePanel _updatePanel1;
  [AccessedThroughProperty("btVerify")]
  private Button _btVerify;
  [AccessedThroughProperty("txthidIsLogin")]
  private TextBox _txthidIsLogin;
  [AccessedThroughProperty("btSetVisitBefore")]
  private Button _btSetVisitBefore;
  [AccessedThroughProperty("lblSerialNum")]
  private TextBox _lblSerialNum;
  [AccessedThroughProperty("ReConnect")]
  private HtmlAnchor _ReConnect;

......
```

深入探索

企业安全咨询

Docker加速服务

计算机安全

最开始的一些变量定义，前端按钮**btVerify**

漏洞扫描服务

```
function doLogin() {
    //document.getElementById("txthidIsLogin").value = "1";
    try {
        var CertID = document.getElementById("CertID").value;
        if (CertID == "") {
            alert("没有读取到key信息，请检查key是否运行正常！");
            return false;
        }
        else {
            document.all.lblSerialNum.value = CertID;
            var obj = document.getElementById("btVerify");
            obj.click();
            return true;
        }

......
<form id="form1" runat="server">
<uc1:ioScriptManager ID="ioScriptManager1" runat="server" />
<ioctl:ioUpdatePanel ID="updatePanel1" UpdateMode="Conditional"
    runat="server">
    <ContentTemplate>
        <asp:Button ID="btVerify" runat="server" Style="display: none" />
        <asp:TextBox ID="txthidIsLogin" runat="server" Style="display: none"></asp:TextBox>
        <asp:Button ID="btSetVisitBefore" runat="server" Style="display: none" />
        <table id="Table1" cellspacing="0" cellpadding="0"
            width="100%" align="center" border="0">
            <tr>
                <td height="100px">
                </td>
            </tr>
            <tr>
                <td class="td" valign="top" align="center">
                    <table id="Table5" cellspacing="0" cellpadding="0"
                        border="0" style="width: 480px; height: 220px">
                        <tr>
                            <td align="right" style="font-size: 12px;">
                                请选择用户证书：
                            </td>
                            <td>
                                <select name="CertID"  id="CertID" style="width: 150px">

                                </select>
                        </tr>
                        <tr style="display: none">
                            <td align="right" style="font-size: 12px;">
                                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户PIN码：
                            </td>
                            <td>
                                <input type="password" size="10" name="UserPIN" style="width: 150px"
                                    onkeypress="if(event.keyCode==13) {doLogin();return false;}" />
                        </tr>
                        <tr>
                            <td align="center" colspan="2">
                            </td>
                            <asp:TextBox ID="lblSerialNum" runat="server" Width="0px" Style="display:none"></asp:TextBox>
                        </tr>
                        <tr>
```

对应后端的**btVerify**

编程

```
protected virtual Button btVerify
{
  [DebuggerNonUserCode] get => this._btVerify;
  [DebuggerNonUserCode, MethodImpl((MethodImplOptions) 32)] set
  {
    EventHandler eventHandler = new EventHandler(this.btVerify_Click);
    if (this._btVerify != null)
      this._btVerify.Click -= eventHandler;
    this._btVerify = value;
    if (this._btVerify == null)
      return;
    this._btVerify.Click += eventHandler;
  }
}
```

跟进**btVerify\_Click**看下

```
protected void btVerify_Click(object sender, EventArgs e)
{
  if (Operators.CompareString(this.lblSerialNum.Text.Trim(), "", false) == 0)
    return;
  iden.iden.PGCA pgca = new iden.iden.PGCA();
  pgca.EmpID = checked ((int) Math.Round(Conversion.Val(this.Emp.EmpID)));
  pgca.SubjectName = "PGCA";
  pgca.Serial = this.lblSerialNum.Text;
  switch (pgca.Verify())
  {
```

在判断`lblSerialNum`不为空后带入`iden.iden.PGCA()` 方法，跟进看下

网络安全

```
public class PGCA : iden.iden.Identity
{
  public string SubjectName;
  public string Issuer;

  public PGCA()
  {
    this.p_Hardware = nameof (PGCA);
    this.ConfigPage = "/ioffice/identity/PgcaConfig.aspx";
    this.LoginPage = "/ioffice/identity/PgcaUserLogin.aspx";
  }

  public override void Addup()
  {
    this.IdentityAddUp(this.EmpID, this.Serial, this.Hardware, this.SubjectName, sIssuer: this.Issuer);
  }

  public override int Verify()
  {
    if (Operators.CompareString(this.SubjectName, "", false) != 0)
      this.LookupEmpAndLogin(this.Serial);
    return Operators.ConditionalCompareObjectGreater(SqlData.ExecuteScalar(Globals.ConnectString, (CommandType) 1, $"{"select count(*) " + " from ssIdentity " + " where "}  Serial='{this.Serial}' and empid={Conversions.ToString(this.EmpID)}"), (object) 0, false) ? 1 : 0;
  }

  protected override int LookupEmp(string SearchKey)
  {
    object objectValue = RuntimeHelpers.GetObjectValue(SqlData.ExecuteScalar(Globals.ConnectString, (CommandType) 1, $"select b.empid from ssIdentity a join mrbaseinf b on a.SubjectName=b.loginid where a.Serial='{SearchKey}'"));
    return objectValue == DBNull.Value ? 0 : Conversions.ToInteger(objectValue);
  }
}
```

`Serial`即`lblSerialNum`又先被带入`LookupEmpAndLogin` 方法

```
protected void LookupEmpAndLogin(string SearchKey)
{
  if (Operators.ConditionalCompareObjectEqual(HttpContext.Current.Session["VisitBefore"], (object) "", false) && Operators.CompareString(ioSet.GetClientSet("硬件认证直接登录"), "", false) != 0)
  {
    int iEmpID = this.LookupEmp(SearchKey);
    if (iEmpID == 0)
      return;
    this.EmpID = this.LoginiOffice(iEmpID) != 0 ? 0 : iEmpID;
  }
}
```

继续跟进`LookupEmp` 方法

```
protected virtual int LookupEmp(string SearchKey)
{
  object objectValue = RuntimeHelpers.GetObjectValue(SqlData.ExecuteScalar(Globals.ConnectString, (CommandType) 1, $"select empid from ssIdentity where Serial='{SearchKey}'"));
  return objectValue == DBNull.Value ? 0 : Conversions.ToInteger(objectValue);
}
```

ok,到这里，漏洞成因就非常明了了，从前端`TextBox`获取的**lblSerialNum**最终经过一系列赋值传递后被直接拼接进`$"select empid from ssIdentity where Serial='{SearchKey}'"` sql语句里，全程无过滤或者校验，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 漏洞复现需要打开漏洞文件页面获取一些其他必要参数如\_\_VIEWSTATE之类
>
> 数据管理

```
POST /ioffice/Identity/PgcaUserLogin.aspx HTTP/1.1
Host: ioffice.mrxn.ent
Content-Type: application/x-www-form-urlencoded

__EVENTTARGET=btVerify&__EVENTARGUMENT=&__VIEWSTATE=YOUR___VIEWSTATE&__VIEWSTATEGENERATOR=YOUR___VIEWSTATEGENERATOR&btVerify=&CertID=SQLI_POC&lblSerialNum=SQLI_POC&txthidIsLogin=1&UserPIN=123456
```

[![红帆ioffice PgcaUserLogin.aspx SQL 注入漏洞](images/img-001-5a7702b8071a.webp)](https://image.mrxn.net/47f1a72398444b73867fbfc34ea1ffaf.webp)

成功利用[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显当前数据库用户信息

漏洞扫描服务

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
