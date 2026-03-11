---
title: "红帆ioffice mrClearPwd.aspx SQL 注入漏洞"
source: https://mrxn.net/jswz/ioffice-ClearPwd-mrClearPwd-sqli.html
asset_dir: assets/红帆ioffice-mrclearpwd.aspx-sql-注入漏洞
---

# 红帆ioffice mrClearPwd.aspx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/24 16:36
- 853浏览
- [0评论](#comment)
- 41分钟阅读

深入探索

服务器安全服务

传输层安全性协议

文件大小转换

---

# 漏洞简介

红帆iOffice的/ioffice/prg/mr/ClearPwd/mrClearPwd.aspx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，未经身份验证地获取数据库敏感信息，影响范围包括红帆iOffice系统的数据访问权限。

SQL注入检测工具

# 影响版本

# fofa语法

> (title="iOffice.net" || body="/iOffice/js" || (body="iOffice.net" && header!="couchdb" && header!="drupal") || body="iOfficeOcxSetup.exe" || body="Hongfan. All Rights Reserved")

# 漏洞分析

先看下`mrClearPwd.aspx` 里引用的代码在哪里（Inherits）

```
<%@ Page Language="vb" AutoEventWireup="false" CodeBehind="mrClearPwd.aspx.vb"
    Inherits="mr.mrClearPwd" %>
    <form id="frm" runat="server" defaultfocus="txtpwd"
    defaultbutton="ok">
    <div style="position: absolute; bottom: 3px; left: 15px;
        font-size: 13">
        <a href="../../../help/ioset.exe" title="IE设置工具">IE设置工具</a>&nbsp;&nbsp;
        <a href="../../../help/iOfficeOcxSetup.exe" title="文档控件安装">
            文档控件安装</a>
    </div>
```

深入探索

漏洞预警服务

恶意软件分析工具

软件

去bin目录找到`mrClearPwd.dll`后编译打开，看`mrClearPwd`它的实现逻辑关键部分

```
public class mrClearPwd : WebPageBase
{
private void cmdValidate_Click(object sender, EventArgs e)
{
  if (((CheckBox) this.rad1).Checked)
  {
    int num = 0;
    string str = "";
    if (Operators.CompareString(this.txtloginid.Text.Trim(), "", false) != 0)
    {
      DataTable baseInfExtent = mr.mr.GetBaseInfExtent(0, this.txtloginid.Text);
      if (baseInfExtent.Rows.Count > 0)
      {
        num = 1;
        str = baseInfExtent.Rows[0]["Question"].ToString();
      }
      else
        num = 0;
    }
    if (num == 1)
    {
      ((WebControl) this.txtAnswer).Attributes["contenteditable"] = "true";
      ((WebControl) this.txtQuestion).Attributes["contenteditable"] = "false";
      this.txtQuestion.Text = str;
      this.txtAnswer.Text = "";
      ((Control) this.lblTip).Visible = false;
    }
    else
    {
      ((WebControl) this.txtAnswer).Attributes["contenteditable"] = "false";
      ((WebControl) this.txtQuestion).Attributes["contenteditable"] = "false";
      this.txtQuestion.Text = "";
      this.txtAnswer.Text = "";
      ((Control) this.lblTip).Visible = true;
    }
  }
  if (((CheckBox) this.rad2).Checked)
  {
    if (Operators.CompareString(Globals.get_Profile("PwdPolicy", "ClearPwdNeedMobile"), "1", false) == 0)
    {
      if (Operators.CompareString(this.txtmobileNO.Text, "", false) == 0)
      {
        Page pgeParent = (Page) this;
        pf.ShowMessage(ref pgeParent, "必须输入您的手机号码（必须在系统中有登记）");
        this.ClientScript.RegisterStartupScript(this.ClientScript.GetType(), "CtlssTree1", "<script>DisableButton()</script>");
      }
      else if (Conversions.ToInteger(SqlData.ExecuteScalar(Globals.ConnectString, (CommandType) 1, $"select count(*) from mrBaseInf where loginid='{this.txtloginid.Text}' and ( mobile='{this.txtmobileNO.Text}' or mobile1='{this.txtmobileNO.Text}' or mobile2='{this.txtmobileNO.Text}')")) <= 0)
      {
        Page pgeParent = (Page) this;
        pf.ShowMessage(ref pgeParent, "手机号码不正确！（该号码在系统中未登记或与登记的号码不符！）");
        this.ClientScript.RegisterStartupScript(this.ClientScript.GetType(), "CtlssTree1", "<script>DisableButton()</script>");
      }
      else
      {
        this.SendVerifyCode();
        this.ClientScript.RegisterStartupScript(this.ClientScript.GetType(), "send", "<script>startTimer()</script>");
      }
    }
    else
    {
      this.SendVerifyCode();
      this.ClientScript.RegisterStartupScript(this.ClientScript.GetType(), "send", "<script>startTimer()</script>");
    }
  }
}
```

在通过“短信验证”方式找回密码时，用户名字段（`txtloginid`）未经任何过滤或参数化处理，被直接拼接到 SQL 查询语句中，导致了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可借此执行任意 SQL 命令。

# 漏洞复现

> 漏洞复现需要打开漏洞文件页面获取一些其他必要参数如\_\_VIEWSTATE之类

[![红帆ioffice mrClearPwd.aspx SQL 注入漏洞](images/img-001-d057883e4ca6.webp)](https://image.mrxn.net/738cc76b57244dddbdcbd752fcba4c35.webp)

```
POST /ioffice/prg/mr/ClearPwd/mrClearPwd.aspx HTTP/1.1
Host: ioffice.mrxn.net
Content-Type: application/x-www-form-urlencoded

__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=YOUR__VIEWSTATE&__VIEWSTATEGENERATOR=YOUR___VIEWSTATEGENERATOR&txtloginid=SQLI_POC&grop1=rad2&txtmobileNO=1&txtmobile=13888888888&ok=%E7%A1%AE%E3%80%80%E8%AE%A4
```

[![红帆ioffice mrClearPwd.aspx SQL 注入漏洞](images/img-002-7b6b21836607.webp)](https://image.mrxn.net/94ef50e67dd044e58a569409241be4c3.webp)

成功利用[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显当前数据库用户信息

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
