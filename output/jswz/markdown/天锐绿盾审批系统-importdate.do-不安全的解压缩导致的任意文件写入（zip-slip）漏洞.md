---
title: "天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞"
source: https://mrxn.net/jswz/trwfe-importDate-rce.html
asset_dir: assets/天锐绿盾审批系统-importdate.do-不安全的解压缩导致的任意文件写入（zip-slip）漏洞
---

# 天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/5 08:23
* 814浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

云安全解决方案

VPN服务

文本剥离工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。

安全研究工具

在其 `importDate.do` 接口中存在一个不安全的解压缩漏洞。攻击者可以利用“Zip Slip”技术，通过构造恶意的压缩文件，在系统解压缩时，利用文件路径遍历的缺陷，将文件写入到任意指定位置。

这可能导致敏感文件被覆盖、恶意文件被植入，进而引发[远程代码执行](https://mrxn.net/tag/rce)、系统功能破坏或数据泄露等严重安全风险。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 计算机科学

# 漏洞分析

先看`importDate.do`的实现

[![天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](images/img-001-a489f0df1548.webp)](https://image.mrxn.net/2e004cb0213647f1b710959bf085dd8e.webp)

跟进`configService.importDate` 看下实现逻辑

[![天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](images/img-002-a162a9c25601.webp)](https://image.mrxn.net/cfcf93acb1d24aceb135bc05bee96b42.webp)

接收一个文件上传的file参数内容

漏洞扫描服务

[![天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](images/img-003-b84af67d972c.webp)](https://image.mrxn.net/ba691f4c41bc4c4a975ce0f1ea21267f.webp)

处理用户上传的 zip 压缩包，该功能旨在实现数据库的导入恢复。它首先将上传的 `MultipartFile` 保存为临时 zip 文件，然后调用 `ZipUtil.getInstance().unZip()` 方法将该 zip 文件解压到服务器上的一个临时目录中。

深入探索

技术文章订阅

漏洞扫描器

Web安全课程

由于代码在解压 zip 文件之前，**完全没有对压缩包内的文件名进行合法性校验，特别是没有检查文件名中是否包含目录遍历序列（如** `../`**）**，造成了**致命的 Zip Slip 漏洞**。攻击者可以精心构造一个 zip 压缩包，其中包含一个文件名形如 `../../../../../../../../tmp/pwned.txt` 的文件。当 `ZipUtil.unZip()` 方法解压这个文件时，它会跳出预设的临时解压目录 `tempPath`，将 `pwned.txt` 文件写入到服务器的文件系统根目录下的 `/tmp` 目录中。通过这种方式，攻击者可以在服务器上任意位置写入任意内容的文件，例如上传一个 [WebShell](https://mrxn.net/tag/rce)、覆盖关键配置文件、或写入一个定时任务脚本。

安全研究工具

# 漏洞复现

> 创建一个带有目录穿越文件名的压缩包，只需要向上跳一级即可跳到根目录

[![天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](images/img-004-4777fdcf554c.webp)](https://image.mrxn.net/5ef93ad5dd4845ea87eef8560a1c7415.webp)

访问解压到根目录的测试文件test.jsp

[![天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](images/img-005-d6ea9cfa7fd1.webp)](https://image.mrxn.net/cfa21975357942e5b3f3b5bff27bba9d.webp)

成功[执行](https://mrxn.net/tag/rce)打印随机uuid后，删除自身，完成Zip Slip漏洞利用。

计算机科学

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#rce](https://mrxn.net/tag/rce)

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
文章标题：[天锐绿盾审批系统 importDate.do 不安全的解压缩导致的任意文件写入（Zip Slip）漏洞](https://mrxn.net/jswz/trwfe-importDate-rce.html)  
文章链接：<https://mrxn.net/jswz/trwfe-importDate-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-importDate-rce.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/trwfe-importDate-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 