---
title: "金和OA OrderDelete.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-OrderDelete-sqli.html
asset_dir: assets/金和oa-orderdelete.aspx-sql注入漏洞
---

# 金和OA OrderDelete.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/5 13:31
* 282浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

木马

服务器

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `OrderDelete.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `OrderDelete.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CrmOrder.dll` 将其进行反编译后找到 **OrderDelete** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.KeyCtrl("JHICRM");
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.Bind();
  if (this.Request["DataID"] != null)
    this.strOrderID = this.Request["DataID"].ToString();
  this.PageInit();
  this.BindOrderData(this.strOrderID);
}
```

跟进`BindOrderData`方法

深入探索

JSON处理工具

安全研究报告

授权

```
private void BindOrderData(string OrderID)
{
  DataSet dataSet = this.CrmOrd.ReadOrderData(OrderID);
```

跟进`ReadOrderData`方法

[![金和OA OrderDelete.aspx SQL注入漏洞](images/img-001-0346ad749409.webp)](https://image.mrxn.net/0ff3c8ae7aa64362946c1f4606bc6ce1.webp)

参数`DataID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CrmOrder/OrderDelete.aspx/?DataID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA OrderDelete.aspx SQL注入漏洞](images/img-002-0a01440ba099.webp)](https://image.mrxn.net/40fe993df1a446daaf21d19faee3ce6b.webp)

[![金和OA OrderDelete.aspx SQL注入漏洞](images/img-003-428d435416e8.webp)](https://image.mrxn.net/e6fd0f88b4d64ebfbbbdecb8501aad27.webp)

成功延时 6 秒

代码安全审计

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[金和OA OrderDelete.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-OrderDelete-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-OrderDelete-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-OrderDelete-sqli.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-OrderDelete-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 