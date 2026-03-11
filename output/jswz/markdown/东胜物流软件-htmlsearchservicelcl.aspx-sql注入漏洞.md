---
title: "东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-PriceCarrier-HtmlSearchServiceLCL-sqli.html
asset_dir: assets/东胜物流软件-htmlsearchservicelcl.aspx-sql注入漏洞
---

# 东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/17 08:45
* 195浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

服务器

木马

身份验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 HtmlSearchServiceLCL.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `HtmlSearchServiceLCL.aspx` 的代码引用 `DSWeb.PriceCarrier.HtmlSearchServiceLCL`，在dll中找到它的逻辑实现

[![东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞](images/img-001-769087f56a45.webp)](https://image.mrxn.net/d47e42726bb441e9ac07f35052466179.webp)

[![东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞](images/img-002-c9855c0dbef5.webp)](https://image.mrxn.net/7a54ee092a18499c873b0485abb6ba5b.webp)

关键点如下

SQL注入检测工具

深入探索

云安全解决方案

服务器安全服务

网页浏览器

```
// 接收未经验证的排序参数
if (this.Request.QueryString["sidx"] != null)
  this.strSidx = this.Request.QueryString["sidx"].ToString();
if (this.Request.QueryString["sord"] != null)
  this.strSord = this.Request.QueryString["sord"].ToString();

// ... 在 GetSearchSeaPrice 方法中 ...

// 直接将用户输入拼接到 ORDER BY 子句
strSql = string.Format($" SELECT ... FROM eb_pricequery WHERE ... ORDER BY {this.strSidx} {this.strSord} ", ...);

// 执行恶意的 SQL 语句
DataTable table = ebPricequeryDa.GetExcuteSql(strSql).Tables[0];

//---------------------------------------------------------

// 接收未经验证的搜索参数
if (this.Request.QueryString["searchString"] != null)
{
  this.strSearchString = Regex.Unescape(this.Request.QueryString["searchString"].ToString());
}

// ... 在 GetSearchSeaPrice 方法中，对 searchString 进行解析 ...

// 直接将解析出的值拼接到 WHERE 子句
string[] strArray3 = strArray1[index].Split(':');
...
str1 += $" AND CARRIER = '{strArray3[1].Replace("\"", "").Replace("##", ",")}' ";
...

// 将包含注入的 WHERE 子句拼接到主查询
strSql = string.Format($" SELECT ... FROM eb_pricequery WHERE TYPE='LCL' {str1}{this.strSearchOper}  ORDER BY ... ", ...);

// 执行恶意的 SQL 语句
DataTable table = ebPricequeryDa.GetExcuteSql(strSql).Tables[0];
```

可以看到通过直接拼接用户控制的请求参数来构造SQL查询语句，导致查询功能中存在多处[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /PriceCarrier/HtmlSearchServiceLCL.aspx?page=1&rows=10&sidx=SQLI_POC&sord=asc&searchField=&searchString=&searchOper= HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞](images/img-003-ac6e2a69e262.webp)](https://image.mrxn.net/92bc0c9b70c8480c90ccc804603527e3.webp)

成功延时 5 秒

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
文章标题：[东胜物流软件 HtmlSearchServiceLCL.aspx SQL注入漏洞](https://mrxn.net/jswz/dongsheng-PriceCarrier-HtmlSearchServiceLCL-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-PriceCarrier-HtmlSearchServiceLCL-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-PriceCarrier-HtmlSearchServiceLCL-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/dongsheng-PriceCarrier-HtmlSearchServiceLCL-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 