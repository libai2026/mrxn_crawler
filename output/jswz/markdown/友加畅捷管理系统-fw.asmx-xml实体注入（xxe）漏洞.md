---
title: "友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞"
source: https://mrxn.net/jswz/youjiasoft-fw-xxe.html
asset_dir: assets/友加畅捷管理系统-fw.asmx-xml实体注入（xxe）漏洞
---

# 友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/6 08:35
* 365浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

网络服务

软件

Web服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理软件，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

代码安全审计

该系统fw.asmx下的`ZTList`、`login`、`OrderPost`、`OrderUpdate`、`QueryUnit`、`QueryUnit_Sup`、`QueryUnit_Cus`、`QueryStoreHouse`、`QueryEmp`、`QueryDept`、`QueryMoneyAccount`、`GetBillSN`、`QueryProd`、`QueryBarCode`、`QueryProdUnit`、`QueryProdBatch`、`GetPrice`、`QueryOutStorBillDraft`、`QuerySaleOrder`、`QueryProdPrice`、`QuerySaleOrderDetail`、`QuerySaleBillDrafeDetail`、`GetUserList`、`GetPriceNameList`等方法均存在 XML实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞，是由于其在处理XML输入时，未能有效禁用外部实体加载所导致。攻击者可以通过构造恶意的XML数据，并在其中引用外部实体，当系统解析这些未经严格过滤的XML数据时，便会触发漏洞。

成功利用此漏洞可能导致多种严重的安全风险，包括但不限于敏感信息泄露（如读取系统文件）、执行任意系统命令、对内网进行端口扫描、攻击内部[网络服务](#)，甚至发起拒绝服务（DoS）攻击等。

# 影响版本

18.8000.1095.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="
>
> 漏洞扫描服务

# 漏洞分析

直接查看 `fw.asmx` 文件的代码引用

深入探索

Docker加速服务

VPN服务

网页浏览器

```
<%@ WebService Language="C#" CodeBehind="fw.asmx.cs" Class="CnSub.Web.fw" %>
```

直接在 `bin` 目录下反编译 `CnSub.Web.dll` 获取 **fw** 的`ZTList`处理逻辑

[![友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞](images/img-001-b12d0a468195.webp)](https://image.mrxn.net/dbc00c7f3c8447eeb75143f48581ea18.webp)

可以看到`xmldata`被直接带入`setXmlData`方法，跟进`setXmlData`方法看下它的实现逻辑

物流软件安全

[![友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞](images/img-002-7297d1680d63.webp)](https://image.mrxn.net/2a363b50d4b5413c8100acc53f010c0d.webp)

可以看到`setXmlData`方法直接将`xmldata`使用XmlDocument的LoadXml进行XML反序列化操作，但是并没有对参数`xmldata` 传递的数据进行过滤或校验，造成[XML实体注入](https://mrxn.net/tag/XXE)（XXE）漏洞。

其他方法也是存在同样的[XXE](https://mrxn.net/tag/XXE)漏洞

[![友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞](images/img-003-c3ce419ad955.webp)](https://image.mrxn.net/a17ab000ac5c4eeeaca115b09f37f8db.webp)

# 漏洞复现

```
POST /fw.asmx HTTP/1.1
Host: youjiasoft.mrxn.net
SOAPAction: http://tempuri.org/ZTList
Content-Type: application/xml

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:ZTList>
         <!--type: string-->
         <tem:xmldata>XXE_POC</tem:xmldata>
      </tem:ZTList>
   </soapenv:Body>
</soapenv:Envelope>
```

[![友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞](images/img-004-135bcc35865e.webp)](https://image.mrxn.net/562a12e49fcb45db8f6fe8706d4b2a71.webp)

成功在DNSLOG平台获得HTTP响应。

代码安全审计

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
文章标题：[友加畅捷管理系统 fw.asmx XML实体注入（XXE）漏洞](https://mrxn.net/jswz/youjiasoft-fw-xxe.html)  
文章链接：<https://mrxn.net/jswz/youjiasoft-fw-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/youjiasoft-fw-xxe.html"),
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

安全运维咨询

  

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
text: encodeURI("https://mrxn.net/jswz/youjiasoft-fw-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 