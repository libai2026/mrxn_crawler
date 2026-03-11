---
title: "金和OA BookGetStoreType.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-BookGetStoreType-sqli.html
asset_dir: assets/金和oa-bookgetstoretype.aspx-sql注入漏洞
---

# 金和OA BookGetStoreType.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/1 13:30
* 332浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

防火墙软件

Web安全课程

Windows安全工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `BookGetStoreType.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

漏洞扫描器

漏洞扫描服务

计算机安全

根据 `BookGetStoreType.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Books.dll` 将其进行反编译后找到 **BookGetStoreType** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  string str = this.Request["StoreID"].ToString();
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($"select bookTypeID,bookTypeName,bookTypeNumber from booksType where booktypeDelFlag=0 and bookstoreID='{str}' order by booktypenumber");
```

至此，就非常明了了，参数**StoreID**是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Books/BookGetStoreType.aspx/?StoreID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA BookGetStoreType.aspx SQL注入漏洞](images/img-001-165874f57f1d.webp)](https://image.mrxn.net/10f31b20f2dd491d9e6ddaa458f00da8.webp)

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
文章标题：[金和OA BookGetStoreType.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-BookGetStoreType-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-BookGetStoreType-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-BookGetStoreType-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-BookGetStoreType-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 