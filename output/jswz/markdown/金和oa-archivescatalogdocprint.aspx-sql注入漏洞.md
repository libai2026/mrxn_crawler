---
title: "金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesCatalogDocPrint-sqli.html
asset_dir: assets/金和oa-archivescatalogdocprint.aspx-sql注入漏洞
---

# 金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/6 13:30
* 497浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

技术文章订阅

安全

编码转换工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesCatalogDocPrint.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

网络安全课程

VPN服务

安全工具开发

根据 `ArchivesCatalogDocPrint.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesCatalogDocPrint** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.language();
  string str = this.Request["DossID"].ToString();
  DataTable indexList = ArchivesCatalog.GetIndexList(str);
```

参数 `DossID` 被带入`GetAllAdvice`方法

```
public static DataTable GetIndexList(string DossID)
{
  string QueryString = $"SELECT DocNo,DocTitle,DocZH,docOwner,DocCreateDate,DocPage,DocMemo FROM ArchivesDoc where dossid='{DossID}' and DelFlag=0 order by DocNo";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

深入探索

服务器安全服务

计算机安全

身份验证

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesCatalogDocPrint.aspx/?fileid=1&filetype=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞](images/img-001-14098a41f17a.webp)](https://image.mrxn.net/573fef295f1f4558ada8e5ac24391945.webp)

成功延时 10 秒，执行两次

代码安全审计

深入探索

软件

云安全解决方案

SQL注入防护

[![金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞](images/img-002-2201906f3e8c.webp)](https://image.mrxn.net/6ca1bd319a884246915fe56af055cfe4.webp)

[![金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞](images/img-003-da799b2736cf.webp)](https://image.mrxn.net/948defc2e2114b20a30f98946e0cc085.webp)

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
文章标题：[金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-ArchivesCatalogDocPrint-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-ArchivesCatalogDocPrint-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞扫描服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesCatalogDocPrint-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-ArchivesCatalogDocPrint-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 