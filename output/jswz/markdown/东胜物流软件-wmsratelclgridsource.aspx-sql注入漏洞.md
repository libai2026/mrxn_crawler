---
title: "东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-SeaiInfoLCL-WmsRateLCLGridSource-sqli.html
asset_dir: assets/东胜物流软件-wmsratelclgridsource.aspx-sql注入漏洞
---

# 东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/20 15:26
* 566浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

安全

身份验证

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 WmsRateLCLGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `WmsRateLCLGridSource.aspx` 的代码引用 `DSWeb.SeaiInfoLCL.WmsRateLCLGridSource`，在dll中找到它的逻辑实现

主要就是根据`read`参数的值来进行处理不同的分支逻辑

SQL注入防护

[![东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](images/img-001-4f6bd67c3345.webp)](https://image.mrxn.net/9680137af95d4d7db94289d5135a4390.webp)

用户通过 `Request.QueryString` 控制 `handle`, `tb`, `linkgid` 等参数，根据`handle`的不同值 进入不同的方法，

代码安全审计

深入探索

文件大小转换

漏洞扫描服务

Docker加速服务

当**handle=getiswmsin**时，进入**getiswmsin**方法

[![东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](images/img-002-d6f737296031.webp)](https://image.mrxn.net/d04c1982bc5b406784db43947917d56c.webp)

`str`的值被直接拼接在`strSQL`语句里，而`str`又来自**gids**请求参数

[![东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](images/img-003-a8a39743789c.webp)](https://image.mrxn.net/580bba09ae70476c9e1dd71ec8b9a8d4.webp)

然后用**GetStrSQL**进行执行，全程无过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

同时其他多个方法也是存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

[![东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](images/img-004-135401039f15.webp)](https://image.mrxn.net/c1f54443ef5b488a82c410a3e648b5c9.webp)

# 漏洞复现

```
GET /SeaiInfoLCL/WmsRateLCLGridSource.aspx?handle=getiswmsin&gids=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](images/img-005-e14c264949cf.webp)](https://image.mrxn.net/5347762623ee47f8927acf6d79e5ae8d.webp)

通过报错注入在响应里回显数据库版本信息。

漏洞修复方案

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](https://mrxn.net/jswz/dongsheng-SeaiInfoLCL-WmsRateLCLGridSource-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-SeaiInfoLCL-WmsRateLCLGridSource-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-SeaiInfoLCL-WmsRateLCLGridSource-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/dongsheng-SeaiInfoLCL-WmsRateLCLGridSource-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 