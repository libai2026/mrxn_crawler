---
title: "用友U8 CRM objectview.php SQL注入漏洞"
source: https://mrxn.net/jswz/yonyon-u8crm-pub-objectview-ID-sqli.html
asset_dir: assets/用友u8-crm-objectview.php-sql注入漏洞
---

# 用友U8 CRM objectview.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/6 08:26
* 1046浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

网络安全会议

编程语言教程

网页浏览器


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

用友U8 CRM客户关系管理系统是一款专业的企业级CRM软件，旨在帮助企业高效管理客户关系、提升销售业绩和提供优质的客户服务。用友 U8 CRM客户关系管理系统 objectview.php 文件存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者通过漏洞执行任意SQL语句，调用xp\_cmdshell写入后门文件，执行任意代码，从而获取到服务器权限

SQL注入防护

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V13

# fofa语法

> `title="用友U8CRM"`

# 漏洞分析

深入探索

防火墙软件

漏洞修复方案

安全研究报告

根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)通告

[![用友U8 CRM objectview.php SQL注入漏洞](images/img-001-4f6b7b32de12.webp)](https://image.mrxn.net/66502f10c66349b5922fb675fb5d1a52.webp)

可知漏洞原因为sql注入导致的命令注入攻击。

代码安全审计

那直接看 `U8SOFT/turbocrm70/code/www/pub/objectview.php` 修复前后的差异

[![用友U8 CRM objectview.php SQL注入漏洞](images/img-002-644285979cb3.webp)](https://image.mrxn.net/dcd2413929de4dedb5678cc1ba91c3f7.webp)

可以看到修复版本是对 `getRealID` 方法增加了更安全的参数化处理sql语句，那直接看有那里调用了 `getRealID` 方法，找到如下调用

```
function getRealID($ID){
    $realID = $ID;
    global $gblDB;
    $sql="select account_id from tc_account where cLtcCustomerCode='$ID' and account_id <> cLtcCustomerCode";
    $rs = $gblDB->query($sql);
    if ($rs && $rs->fetchRecord())
    {
        $realID=$rs->getFieldValueByName("account_id");
    }
    $rs->close();
    return TRegisterID($realID);
}
......

$ObjType = TGetRequest("ObjType");
$ID = TRegisterID(TGetRequest("ID"));
if($ObjType == 1){
    $ID = getRealID(TGetRegID($ID));
}
```

深入探索

恶意软件分析工具

安全

文本剥离工具

可以看到没有修复之前是当 `ObjType=1` 时， `getRealID` 方法是直接将 `$ID` 拼接进sql语句中，无任何过滤和校验，造成[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /pub/objectview.php?DontCheckLogin=1&ObjType=1&ID=1' HTTP/1.1
Host: u8crm.mrxn.net
```

# 参考

* `https://security.yonyou.com/#/patchInfo?identifier=dbed49af1ced41e89fcc67d35e5df6c9`

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

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
* [6.参考](#toc-6-)



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
文章标题：[用友U8 CRM objectview.php SQL注入漏洞](https://mrxn.net/jswz/yonyon-u8crm-pub-objectview-ID-sqli.html)  
文章链接：<https://mrxn.net/jswz/yonyon-u8crm-pub-objectview-ID-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞扫描服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/yonyon-u8crm-pub-objectview-ID-sqli.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/yonyon-u8crm-pub-objectview-ID-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 